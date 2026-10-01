import json
import os
import re
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------

load_dotenv(BASE_DIR / ".env")
load_dotenv(PROJECT_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

# ---------------------------------------------------------
# FASTAPI
# ---------------------------------------------------------

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# GEMINI
# ---------------------------------------------------------

try:
    from google import genai
    from google.genai import types

    GEMINI_AVAILABLE = True
except ImportError:
    genai = None
    types = None
    GEMINI_AVAILABLE = False


def get_gemini_client():
    if not GEMINI_AVAILABLE:
        raise RuntimeError(
            "google-genai is not installed. Run: "
            "python -m pip install google-genai"
        )

    if not GEMINI_API_KEY or GEMINI_API_KEY.startswith("AIzaSyYour"):
        raise RuntimeError(
            "GEMINI_API_KEY is missing or still a placeholder in backend/.env"
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def call_gemini(
    prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 2048,
) -> str:

    client = get_gemini_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text.strip()


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def extract_json(text: str) -> Optional[Any]:
    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON object
    object_match = re.search(r"\{.*\}", text, re.DOTALL)

    if object_match:
        try:
            return json.loads(object_match.group(0))
        except json.JSONDecodeError:
            pass

    # Try extracting JSON array
    array_match = re.search(r"\[.*\]", text, re.DOTALL)

    if array_match:
        try:
            return json.loads(array_match.group(0))
        except json.JSONDecodeError:
            pass

    return None


# ---------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------

class AskRequest(BaseModel):
    question: str


class ExplainRequest(BaseModel):
    topic: str
    level: str = "beginner"


class QuizRequest(BaseModel):
    topic: str
    number_of_questions: int = 5
    difficulty: str = "medium"


class SummarizeRequest(BaseModel):
    text: str


class LearningPathRequest(BaseModel):
    subject: str
    level: str = "beginner"
    goal: str = "learn the basics"


# ---------------------------------------------------------
# HEALTH
# ---------------------------------------------------------

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "EduGenie",
        "gemini_configured": bool(
            GEMINI_API_KEY and not GEMINI_API_KEY.startswith("AIzaSyYour")
        ),
        "gemini_model": GEMINI_MODEL,
    }


# ---------------------------------------------------------
# ASK AI
# ---------------------------------------------------------

@app.post("/api/ask")
def ask_ai(request: AskRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    prompt = f"""
You are EduGenie, a helpful educational AI assistant.

Answer the student's question clearly and accurately.

Student question:
{request.question}

Rules:
- Use simple language.
- Explain step by step when useful.
- Give examples when helpful.
- Keep the answer educational.
"""

    try:
        answer = call_gemini(prompt)

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------------
# EXPLAIN
# ---------------------------------------------------------

@app.post("/api/explain")
def explain_topic(request: ExplainRequest):

    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic."
        )

    prompt = f"""
You are an expert teacher helping a student.

Explain this topic:

Topic: {request.topic}
Student level: {request.level}

Provide:
1. Simple definition
2. Main concept
3. Step-by-step explanation
4. Simple example
5. Important points
6. Short real-world example

Use easy language.
"""

    try:
        answer = call_gemini(prompt)

        return {
            "success": True,
            "topic": request.topic,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------------
# QUIZ
# ---------------------------------------------------------

@app.post("/api/quiz")
def generate_quiz(request: QuizRequest):

    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic."
        )

    count = max(1, min(request.number_of_questions, 10))

    prompt = f"""
Create a multiple-choice educational quiz.

Topic: {request.topic}
Difficulty: {request.difficulty}
Number of questions: {count}

Return ONLY valid JSON.

Format:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Option A",
      "explanation": "Short explanation"
    }}
  ]
}}
"""

    try:
        result = call_gemini(
            prompt,
            temperature=0.5,
            max_output_tokens=3000
        )

        quiz = extract_json(result)

        if not isinstance(quiz, dict):
            raise RuntimeError("Gemini did not return valid quiz JSON.")

        return {
            "success": True,
            "quiz": quiz
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------------
# SUMMARIZE
# ---------------------------------------------------------

@app.post("/api/summarize")
def summarize_text(request: SummarizeRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter text to summarize."
        )

    prompt = f"""
Summarize the following educational text.

Text:
{request.text}

Provide:
- A short summary
- Main points
- Important terms

Use simple language.
"""

    try:
        answer = call_gemini(prompt)

        return {
            "success": True,
            "summary": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------------
# LEARNING PATH
# ---------------------------------------------------------

@app.post("/api/learning-path")
def learning_path(request: LearningPathRequest):

    if not request.subject.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a subject."
        )

    prompt = f"""
Create a personalized learning path.

Subject: {request.subject}
Student level: {request.level}
Goal: {request.goal}

Create a practical learning roadmap containing:
1. Prerequisites
2. Week 1
3. Week 2
4. Week 3
5. Week 4
6. Practice activities
7. Mini projects
8. Final revision

Keep it suitable for a student.
"""

    try:
        answer = call_gemini(prompt)

        return {
            "success": True,
            "learning_path": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------------
# FRONTEND
# ---------------------------------------------------------

if FRONTEND_DIR.exists():

    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND_DIR)),
        name="static"
    )


@app.get("/")
def serve_frontend():

    index_file = FRONTEND_DIR / "index.html"

    if not index_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Frontend index.html not found."
        )

    return FileResponse(index_file)


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )