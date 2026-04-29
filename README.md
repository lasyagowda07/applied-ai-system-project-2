# 🐾 PawPal AI Planner

> *Natural language → structured pet care schedules, powered by local ML — no external APIs required.*

---

## Summary

PawPal AI Planner is a local AI-powered pet care scheduling system that converts natural language into structured pet care tasks, generates a daily schedule, detects conflicts, and explains its reasoning. The system works entirely offline using a locally trained machine learning model.

---

## Original Project: PawPal+

The original PawPal+ project was a Python-based object-oriented system for manually managing pet care schedules.

| Feature | Status |
|---|---|
| Add owner, pet, and tasks | ✅ |
| Sort tasks by time | ✅ |
| Handle recurring tasks | ✅ |
| Detect scheduling conflicts | ✅ |
| CLI-based interaction | ✅ |

---

## Capstone Extension

This project extends PawPal+ into a full AI-powered system:

- Natural language input → structured task extraction
- Local intent classification using scikit-learn
- FastAPI backend for API-based interaction
- Next.js frontend UI
- Guardrails and confidence scoring
- Agentic workflow explanation
- Evaluation pipeline for reliability testing

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js (React), TypeScript, CSS |
| **Backend** | FastAPI, Python |
| **AI / ML** | scikit-learn, TfidfVectorizer, LogisticRegression, joblib |
| **Testing** | pytest |

---

## How the AI Works

1. **Natural language input** — user provides free-form text
2. **Phrase splitting** — input is split into individual task phrases
3. **ML classification** — each phrase classified by the local model
4. **Rule-based extraction** — pet names, species, time, recurrence identified
5. **Task creation** — structured task objects are built
6. **Confidence scoring** — a reliability score is calculated
7. **Warning generation** — warnings raised if data is missing or unclear

---

## Agentic Workflow

```
Understand → Plan → Act → Check → Explain
```

| Step | Action |
|---|---|
| Understand | Parse and interpret user input |
| Plan | Extract structured tasks |
| Act | Create objects and build schedule |
| Check | Detect conflicts and validate |
| Explain | Return steps and confidence score |

---

## Guardrails

The system checks for and reports:

- ⚠️ Missing pet name
- ⚠️ Missing time
- ⚠️ Unknown task classification
- ⚠️ Duplicate task detection
- ⚠️ Invalid time handling
- ⚠️ Low confidence warnings
- ⚠️ Empty input validation

---

## Setup

### 1 · Clone the repository

```bash
git clone <your-repo-url>
cd pawpal-ai-planner
```

### 2 · Run the backend

```bash
cd backend
pip install -r requirements.txt

# Train the model
python -m app.ai.train_model

# Start the server
uvicorn app.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`

### 3 · Run the frontend

```bash
cd frontend
npm install
npm run dev
```

### 4 · Run tests

```bash
cd backend
python -m pytest
```

### 5 · Run evaluation

```bash
cd backend
python -m app.evaluation.evaluate
```

---

## Sample Interaction

**Input**

```
I have a dog named Bruno. Feed him at 8 AM and give medicine at 8 PM.
```

**Output**

```
Schedule:
  08:00  Feeding    Bruno
  20:00  Medication Bruno

Confidence: 0.82
Warnings:   []
```

---

## Demo Video

▶ [Watch Demo]([https://your-video-link.com](https://www.loom.com/share/0a1110bfa216400da29fabc96ed3599d))

---

## Limitations & Future Improvements

| Limitations | Future Improvements |
|---|---|
| Limited training data (synthetic) | Expand training dataset |
| Basic NLP parsing (rule-based) | Use transformer-based models (offline) |
| Single-pet dominant extraction | Add multi-pet support |
| No real-time updates | Add calendar integration |
| No database persistence | Add persistent storage |
| — | Improve UI/UX design |
| — | Deploy to cloud |

---

*PawPal AI Planner · Capstone Extension · Local ML Pet Care Scheduling*
