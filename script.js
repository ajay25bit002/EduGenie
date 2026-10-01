const API_BASE = window.location.origin;


// ---------------------------------------------------------
// SECTION NAVIGATION
// ---------------------------------------------------------

function showSection(sectionId) {

  document.querySelectorAll(".feature-section")
    .forEach(section => {
      section.classList.remove("active-section");
    });

  document.querySelectorAll(".tab")
    .forEach(tab => {
      tab.classList.remove("active");
    });

  document.getElementById(sectionId)
    .classList.add("active-section");

  const sections = [
    "askSection",
    "explainSection",
    "quizSection",
    "summarySection",
    "pathSection"
  ];

  const index = sections.indexOf(sectionId);

  if (index >= 0) {
    document.querySelectorAll(".tab")[index]
      .classList.add("active");
  }
}


// ---------------------------------------------------------
// RESULT HELPERS
// ---------------------------------------------------------

function showResult(elementId, content) {

  const element = document.getElementById(elementId);

  element.innerHTML = content;
  element.classList.add("show");
}


function showLoading(elementId) {

  showResult(
    elementId,
    "⏳ EduGenie is thinking..."
  );
}


function escapeHtml(text) {

  const div = document.createElement("div");

  div.textContent = text;

  return div.innerHTML;
}


// ---------------------------------------------------------
// GENERIC API REQUEST
// ---------------------------------------------------------

async function apiRequest(endpoint, data) {

  const response = await fetch(
    `${API_BASE}/api/${endpoint}`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(data)
    }
  );

  const result = await response.json();

  if (!response.ok) {
    throw new Error(
      result.detail || "Something went wrong."
    );
  }

  return result;
}


// ---------------------------------------------------------
// ASK AI
// ---------------------------------------------------------

async function askAI() {

  const question =
    document.getElementById("question").value.trim();

  if (!question) {
    alert("Please enter a question.");
    return;
  }

  showLoading("askResult");

  try {

    const data = await apiRequest(
      "ask",
      {
        question: question
      }
    );

    showResult(
      "askResult",
      `<strong>EduGenie:</strong><br><br>${escapeHtml(data.answer)}`
    );

  } catch (error) {

    showResult(
      "askResult",
      `❌ ${escapeHtml(error.message)}`
    );
  }
}


// ---------------------------------------------------------
// EXPLAIN
// ---------------------------------------------------------

async function explainTopic() {

  const topic =
    document.getElementById("explainTopic").value.trim();

  const level =
    document.getElementById("explainLevel").value;

  if (!topic) {
    alert("Please enter a topic.");
    return;
  }

  showLoading("explainResult");

  try {

    const data = await apiRequest(
      "explain",
      {
        topic: topic,
        level: level
      }
    );

    showResult(
      "explainResult",
      escapeHtml(data.answer)
    );

  } catch (error) {

    showResult(
      "explainResult",
      `❌ ${escapeHtml(error.message)}`
    );
  }
}


// ---------------------------------------------------------
// QUIZ
// ---------------------------------------------------------

async function generateQuiz() {

  const topic =
    document.getElementById("quizTopic").value.trim();

  const difficulty =
    document.getElementById("quizDifficulty").value;

  const number =
    Number(
      document.getElementById("quizCount").value
    );

  if (!topic) {
    alert("Please enter a quiz topic.");
    return;
  }

  showLoading("quizResult");

  try {

    const data = await apiRequest(
      "quiz",
      {
        topic: topic,
        number_of_questions: number,
        difficulty: difficulty
      }
    );

    displayQuiz(data.quiz);

  } catch (error) {

    showResult(
      "quizResult",
      `❌ ${escapeHtml(error.message)}`
    );
  }
}


function displayQuiz(quiz) {

  const container =
    document.getElementById("quizResult");

  let questions = [];

  if (quiz && Array.isArray(quiz.questions)) {
    questions = quiz.questions;
  }

  if (questions.length === 0) {

    showResult(
      "quizResult",
      "❌ No quiz questions were returned."
    );

    return;
  }

  let html = "";

  questions.forEach((item, index) => {

    html += `
            <div class="quiz-question">

                <h3>
                    ${index + 1}. ${escapeHtml(item.question || "")}
                </h3>
        `;

    if (Array.isArray(item.options)) {

      item.options.forEach(option => {

        html += `
                    <button
                        class="quiz-option"
                        onclick="showAnswer(
                            this,
                            '${escapeHtml(item.answer || "")}',
                            '${escapeHtml(item.explanation || "")}'
                        )">

                        ${escapeHtml(option)}

                    </button>
                `;
      });
    }

    html += `
            </div>
        `;
  });

  container.innerHTML = html;
  container.classList.add("show");
}


// ---------------------------------------------------------
// QUIZ ANSWER
// ---------------------------------------------------------

function showAnswer(button, answer, explanation) {

  const buttons =
    button.parentElement.querySelectorAll(".quiz-option");

  buttons.forEach(btn => {
    btn.disabled = true;
  });

  const selected =
    button.textContent.trim();

  if (selected === answer.trim()) {

    button.innerHTML += " ✅ Correct!";

  } else {

    button.innerHTML += " ❌ Incorrect!";
  }

  const explanationElement =
    document.createElement("p");

  explanationElement.style.marginTop = "12px";

  explanationElement.innerHTML =
    `<strong>Answer:</strong> ${escapeHtml(answer)}
         <br>
         <strong>Explanation:</strong> ${escapeHtml(explanation)}`;

  button.parentElement.appendChild(
    explanationElement
  );
}


// ---------------------------------------------------------
// SUMMARIZE
// ---------------------------------------------------------

async function summarizeText() {

  const text =
    document.getElementById("summaryText").value.trim();

  if (!text) {
    alert("Please paste some text.");
    return;
  }

  showLoading("summaryResult");

  try {

    const data = await apiRequest(
      "summarize",
      {
        text: text
      }
    );

    showResult(
      "summaryResult",
      escapeHtml(data.summary)
    );

  } catch (error) {

    showResult(
      "summaryResult",
      `❌ ${escapeHtml(error.message)}`
    );
  }
}


// ---------------------------------------------------------
// LEARNING PATH
// ---------------------------------------------------------

async function generateLearningPath() {

  const subject =
    document.getElementById("pathSubject").value.trim();

  const level =
    document.getElementById("pathLevel").value;

  const goal =
    document.getElementById("pathGoal").value.trim();

  if (!subject) {
    alert("Please enter a subject.");
    return;
  }

  showLoading("pathResult");

  try {

    const data = await apiRequest(
      "learning-path",
      {
        subject: subject,
        level: level,
        goal: goal || "Learn the basics"
      }
    );

    showResult(
      "pathResult",
      escapeHtml(data.learning_path)
    );

  } catch (error) {

    showResult(
      "pathResult",
      `❌ ${escapeHtml(error.message)}`
    );
  }
}


// ---------------------------------------------------------
// HEALTH CHECK
// ---------------------------------------------------------

async function checkBackend() {

  try {

    const response =
      await fetch(`${API_BASE}/api/health`);

    const data =
      await response.json();

    console.log(
      "EduGenie Backend:",
      data
    );

  } catch (error) {

    console.error(
      "Backend connection failed:",
      error
    );
  }
}


// ---------------------------------------------------------
// START
// ---------------------------------------------------------

document.addEventListener(
  "DOMContentLoaded",
  () => {

    showSection("askSection");

    checkBackend();

  }
);