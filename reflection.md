# 💭 Reflection — PawPal AI Planner

> *Design decisions, technical trade-offs, and lessons learned.*

---

## Why I Chose PawPal+

PawPal+ already had a strong object-oriented design with clear classes — `Owner`, `Pet`, `Task`, and `Scheduler`. It was a solid foundation to extend into an AI-based system rather than building from scratch.

---

## What the Original System Did

The original PawPal+ system allowed users to manually manage schedules through a CLI. It worked well as a structured backend but had no support for natural language input.

| Feature | Supported |
|---|---|
| Add pets and tasks | ✅ |
| Sort tasks by time | ✅ |
| Handle recurring tasks | ✅ |
| Detect conflicts | ✅ |
| Natural language input | ❌ |

---

## Why I Added a Local AI Parser

Rather than requiring users to create tasks manually, a local parser with a trained classifier extracts and understands instructions automatically:

- Extract tasks automatically from free text
- Classify task types without manual tagging
- Keep everything offline and fully controlled

---

## Why I Avoided External APIs

| Avoiding external APIs | Using a local model |
|---|---|
| API usage costs money | Fully self-contained |
| Introduces external dependency | Faster for simple tasks |
| Unreliable for offline use | Easier to test and debug |

---

## How FastAPI and Next.js Improved the System

**FastAPI** turned the system into a proper backend:

- Clear API endpoints with structured JSON responses
- Easy integration testing
- Auto-generated `/docs` interface

**Next.js** improved user experience:

- Clean interface for natural language input
- Visual display of schedules, warnings, and confidence scores

---

## How the Agentic Workflow Works

The system follows a clear agent-style pipeline:

1. Understand the user's natural language input
2. Extract individual task phrases
3. Classify each task type using the trained model
4. Create structured task objects
5. Generate the daily schedule
6. Detect conflicts and validate
7. Return explanation with confidence and warnings

This makes each stage explicit and easier to reason about.

---

## How Guardrails Improved Reliability

Instead of failing silently, the system returns explicit warnings — making failure visible and actionable:

- ⚠️ Missing time
- ⚠️ Missing pet name
- ⚠️ Unknown task type
- ⚠️ Empty input
- ⚠️ Duplicate tasks

---

## What Tests Passed

| Test | Result |
|---|---|
| Feeding task extraction | ✅ Passed |
| Medication task extraction | ✅ Passed |
| Misspelling handling (`medcine`) | ✅ Passed |
| Sorting tasks by time | ✅ Passed |
| Same-time conflict detection | ✅ Passed |
| API returning correct JSON | ✅ Passed |

---

## What Failed or Was Difficult

These edge cases reduced confidence or produced warnings:

- Very vague inputs like `"take care of my pet"`
- Assigning multiple tasks in complex sentences
- Extracting multiple pet names reliably

---

## AI Collaboration

**One helpful suggestion:**
A scikit-learn pipeline with `TfidfVectorizer` + `LogisticRegression` was simple to implement and effective enough for this specific domain.

**One flawed suggestion:**
Some suggested parsing approaches were overly complex. They had to be simplified into rule-based extraction combined with classification to actually work.

---

## Limitations

- Small synthetic training dataset
- Limited sentence complexity handling
- Mostly single-pet scenarios
- No long-term memory or persistence

---

## Future Improvements

- Expand training data
- Better multi-pet support
- Improve time extraction edge cases
- Add database storage
- Use stronger offline NLP models

---

## What I Learned as an AI Engineer

| Lesson |
|---|
| Simple models can work well for specific, well-scoped problems |
| AI systems need guardrails to be reliable in production |
| End-to-end systems matter more than any single model |
| Testing and evaluation are critical for building trust |

> This project helped me understand how to build a **complete AI system** — not just a model.

---

*PawPal AI Planner · Engineering Reflection · Capstone Project*
