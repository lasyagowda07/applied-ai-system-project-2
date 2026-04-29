# 🏗️ System Architecture — PawPal AI Planner

> *Modular, layered design: frontend UI → API layer → AI pipeline → core scheduling system.*

---

## Overview

PawPal AI Planner transforms natural language pet care instructions into structured, validated schedules. Every layer has a single responsibility and can be tested independently.

---

## High-Level Components

### Layer Map

```
┌─────────────────────────────────────┐
│           Frontend (Next.js)        │  ← User interface
└──────────────┬──────────────────────┘
               │ HTTP POST /api/schedule
┌──────────────▼──────────────────────┐
│        Backend API (FastAPI)        │  ← Central coordinator
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌──────────────────┐
│  AI Parser  │  │ Intent Classifier │  ← ML layer
└──────┬──────┘  └────────┬─────────┘
       └────────┬──────────┘
                ▼
┌───────────────────────────────────┐
│       Core OOP System (PawPal+)   │  ← Owner / Pet / Task / Scheduler
└───────────────┬───────────────────┘
                ▼
┌───────────────────────────────────┐
│     Guardrails + Confidence       │  ← Validation layer
└───────────────┬───────────────────┘
                ▼
┌───────────────────────────────────┐
│         Response Layer            │  ← JSON output to frontend
└───────────────────────────────────┘
```

---

## Component Details

### 1 · Frontend — Next.js

**Responsibilities:**

- Capture natural language input from the user
- Send requests to `/api/schedule`
- Display schedule, warnings, confidence score, and agent steps

---

### 2 · Backend API — FastAPI

**Key endpoints:**

| Endpoint | Purpose |
|---|---|
| `POST /api/parse` | Parse natural language |
| `POST /api/schedule` | Full pipeline — parse + schedule |
| `POST /api/validate` | Validate a given schedule |
| `GET /api/evaluation-summary` | Return evaluation results |

**Responsibilities:**

- Receive and route frontend requests
- Orchestrate AI parser, classifier, and scheduler
- Apply guardrails and return structured JSON

---

### 3 · AI Parser Layer

**Responsibilities:**

- Split input into individual task phrases
- Extract pet names and species (rule-based)
- Extract time expressions and normalise to 24h format
- Extract recurrence (daily / weekly / none)
- Prepare phrases for classification

---

### 4 · Intent Classifier

A local scikit-learn model. No external API required.

```
Text input
    ↓
TfidfVectorizer
    ↓
LogisticRegression
    ↓
Predicted task type
```

**Output labels:** `feeding` · `walking` · `medication` · `grooming` · `appointment` · `play` · `unknown`

---

### 5 · Core OOP System (PawPal+)

Inherited from the original project.

| Class | Role |
|---|---|
| `Owner` | Stores owner data |
| `Pet` | Linked to owner; stores species and name |
| `Task` | Stores type, time, and recurrence |
| `Scheduler` | Sorts, filters, and detects conflicts |

---

### 6 · Scheduler

**Responsibilities:**

- Sort tasks by time
- Detect same-time conflicts
- Handle recurring tasks
- Generate the final ordered schedule

---

### 7 · Guardrails + Confidence Scoring

**Guardrail checks:**

- ⚠️ Missing time
- ⚠️ Missing pet name
- ⚠️ Unknown task type
- ⚠️ Duplicate task / same-time conflict
- ⚠️ Empty input

**Confidence scoring:**

- Based on average classifier confidence per phrase
- Penalised for each active warning or missing field
- Range: `0.0` → `1.0`

---

### 8 · Response Layer

Final JSON returned to the frontend includes:

- Structured schedule
- Conflict warnings
- Confidence score
- Agent workflow steps

---

## Data Flow

```
1.  User types natural language input
2.  Frontend sends POST → /api/schedule
3.  FastAPI receives the request
4.  AI parser:
      → splits text into phrases
      → extracts pet name, species, time, recurrence
5.  Classifier predicts task type per phrase
6.  Backend creates Owner, Pet, and Task objects
7.  Scheduler sorts tasks and detects conflicts
8.  Guardrails validate output and compute confidence
9.  Structured JSON response returned to backend
10. Frontend renders schedule, warnings, confidence, agent steps
```

---

## Why This Architecture

| Principle | Rationale |
|---|---|
| **Modularity** | Each layer has one job — easier to debug and test |
| **Separation of concerns** | UI, logic, and AI can change independently |
| **Offline capability** | Local model removes all external API dependency |
| **Explainability** | Agent steps and confidence make reasoning visible |

---

## Tradeoffs

| Decision | Advantage | Cost |
|---|---|---|
| LogisticRegression | Fast, interpretable | Less accurate than LLMs |
| Rule-based parsing | Reliable for structured input | Struggles with complex sentences |
| Synthetic training data | Easy to create and control | Lacks real-world diversity |
| In-memory processing | Simple, no setup | No history or persistence |

---

## Future Improvements

- Add database for schedule persistence
- Replace classifier with stronger offline model
- Improve multi-pet task assignment
- Enhance time parsing edge cases
- Add real-time updates
- Deploy for public access

---

## Summary

The architecture balances **simplicity**, **modularity**, **reliability**, and **explainability** — delivering a complete end-to-end AI system from natural language input to structured, validated output.

---

*PawPal AI Planner · System Architecture · Capstone Documentation*
