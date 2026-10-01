# 🎓 EduGenie: Google Gemini Powered Learning Assistant

> **Skill Wallet Project** — An intelligent, full-stack educational assistant powered by the official **Google GenAI Python SDK** and **FastAPI**, with a responsive, modern glassmorphism frontend built in **HTML, CSS, and Vanilla JavaScript**.

---

## 🌟 Overview & Features

**EduGenie** is designed to transform the way students learn, revise, and master complex subjects through 5 core AI-powered learning tools:

1. 💬 **Ask AI Tutor (Interactive Q&A)**:
   - Ask any educational question across science, coding, mathematics, history, or literature.
   - Choose explanation depth: *Quick Summary*, *Balanced*, or *In-Depth Guide*.
   - Features rich markdown rendering, instant copy to clipboard, and integrated **Text-to-Speech** narration.

2. 💡 **Concept Simplifier (Explain Difficult Topics)**:
   - Breaks down intimidating concepts into intuitive, easy-to-understand explanations.
   - Choose explanation level:
     - 🧒 **Explain Like I'm 5 (ELI5)** — Everyday words, playful storytelling, zero jargon.
     - 🎒 **High School Level** — Relatable examples & foundational principles.
     - 🎓 **College / In-Depth** — Technical precision, core mechanics, and rigor.
     - ⚡ **Analogy Master** — Memorable real-world metaphors that make concepts click instantly.
   - Provides: *1-Sentence Summary*, *Analogy Card*, *Detailed Breakdown*, and *Key Takeaways*.

3. 🎯 **QuizGenie (Interactive Quiz Generator)**:
   - Automatically generates multiple-choice quizzes on any topic.
   - Customizable difficulty (*Beginner*, *Intermediate*, *Advanced*) and question count (3, 5, or 8 questions).
   - Interactive quiz runner with immediate visual feedback (green/red highlights), live score tracking, full answer explanations, and celebration confetti upon completion.

4. 📑 **EduSummarizer (Educational Text Summarizer)**:
   - Paste study notes, textbook excerpts, or research articles.
   - Formats:
     - 📌 *Key Bullet Points* — High-yield highlights.
     - 📝 *Executive TL;DR* — 2 to 3 sentence core summary.
     - 🃏 *Interactive 3D Flashcards* — Flip cards with terms and definitions for quick revision.
     - ✅ *Revision Checklist* — Actionable step-by-step review list.
   - Live word reduction statistics (e.g., *72% condensed*).

5. 🗺️ **PathFinder (Personalized Learning Roadmap)**:
   - Generates a customized, step-by-step syllabus and milestone tracker tailored to your goals, current skill level, and weekly study schedule.
   - Interactive milestone checklist with live completion progress bar.
   - Recommended resources, practical activities, and a final Capstone Project idea.

---

## 📁 Project Structure

```
EduGenie/
├── backend/
│   ├── main.py              # FastAPI server with Google GenAI SDK & API routes
│   ├── requirements.txt     # Python backend dependencies
│   ├── .env.example         # Template for environment variables
│   ├── .env                 # Local environment secrets (Contains GEMINI_API_KEY)
│   └── .gitignore           # Ignores virtual environments & secret keys
├── frontend/
│   ├── index.html           # Semantic HTML5 single-page application
│   ├── style.css            # Modern glassmorphism UI, themes & micro-animations
│   └── script.js            # Client logic, API integration, and interactive components
└── README.md                # Comprehensive documentation and setup guide
```

---

## 🛠️ Technology Stack

- **Backend**:
  - Python 3.10+
  - **FastAPI** — High-performance asynchronous web framework
  - **Uvicorn** — ASGI production server
  - **Pydantic** — Data validation and schema enforcement
  - **Google GenAI Python SDK** (`google-genai` / `google-generativeai`) — Official Google Gemini API client
  - **python-dotenv** — Secure environment variable management

- **Frontend**:
  - **HTML5** & **Vanilla CSS3** (Custom design tokens, glassmorphism, responsive grid, light/dark themes)
  - **Vanilla JavaScript (ES6+)** — No React or heavy frameworks, fast & beginner-friendly
  - **Marked.js** — Markdown parsing for formatted AI responses
  - **FontAwesome 6** — Clean UI icons
  - **Canvas-Confetti** — Celebration animations for quiz achievements
  - **Web Speech API** — Integrated Text-to-Speech audio reader

---

## 🚀 Step-by-Step Setup Guide

### 1. Prerequisites
- Python 3.10 or higher installed on your computer.
- A free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Get your Gemini API Key
1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).
2. Sign in with your Google account.
3. Click **"Create API key"** and copy the generated key.

### 3. Setup the Backend Environment

Open your terminal in the `EduGenie/backend` directory:

```bash
# Navigate to the backend folder
cd EduGenie/backend

# Optional but recommended: Create a virtual environment
python -m venv venv

# Activate the virtual environment:
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 4. Configure Your API Key
Create or edit the `.env` file in the `backend/` directory:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

> 🔒 **Security Best Practice:** Never commit your `.env` file to GitHub or share your API key. The `.gitignore` file is preconfigured to prevent secret leaks. The frontend never accesses the API key directly; all requests are securely proxied through the FastAPI backend.

### 5. Run the Application

Start the FastAPI server from the `backend/` directory:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Once running, open your web browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

The FastAPI backend automatically serves the frontend interface, connects to the Google Gemini API, and provides interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## 📡 Backend API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Checks server status and verifies if `GEMINI_API_KEY` is configured. |
| `POST` | `/api/ask` | AI Tutor endpoint for answering questions with configurable depth. |
| `POST` | `/api/explain` | Concept simplifier endpoint (ELI5, High School, College, Analogy). |
| `POST` | `/api/quiz` | Generates structured multiple-choice quiz questions with answer keys & explanations. |
| `POST` | `/api/summarize` | Summarizes text into bullet points, TL;DR, or flashcards with word stats. |
| `POST` | `/api/learning-path` | Generates a custom weekly roadmap with milestones and capstone project. |

---

## 💡 Beginner Troubleshooting

- **Error: "Gemini API Key is not configured"**:
  - Open `backend/.env` and ensure `GEMINI_API_KEY=AIzaSy...` has no quotes or extra spaces.
  - Restart the FastAPI server (`Ctrl+C` then re-run `uvicorn main:app --reload`).

- **Frontend shows "Backend Offline"**:
  - Ensure the terminal running `uvicorn` is active without errors.
  - Visit `http://127.0.0.1:8000/api/health` in your browser to check backend status.

---

## 📜 License & Acknowledgments
Built for the **Skill Wallet** project. Powered by **Google Gemini AI**.
