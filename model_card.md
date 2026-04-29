# 📋 Model Card — PawPal AI Planner

> *Local Intent Classification + Rule-Based Parser*

---

## Model / System Name

**PawPal AI Planner** — Local Intent Classification + Rule-Based Parser

---

## Purpose

The system converts natural language pet care instructions into structured tasks, generates a daily schedule, detects conflicts, and explains its reasoning. Designed to work fully offline without external LLM APIs.

---

## Original Project

Based on **PawPal+**, a Python OOP system built around four core classes:

| Class | Role |
|---|---|
| `Owner` | Stores owner data |
| `Pet` | Stores pet data linked to owner |
| `Task` | Stores individual care tasks |
| `Scheduler` | Sorts, filters, and detects conflicts |

---

## AI Feature

A locally trained intent classification model replaces external LLM APIs.

| Component | Detail |
|---|---|
| Vectorizer | `TfidfVectorizer` |
| Classifier | `LogisticRegression` |
| Serialization | `joblib` |
| Framework | `scikit-learn` |

---

## Training Data

- Synthetic dataset of pet care phrases
- Covers common instructions: feeding, walking, medication, etc.
- Includes misspellings and vague inputs for robustness

---

## Labels / Classes

| Label | Description |
|---|---|
| `feeding` | Food-related tasks |
| `walking` | Exercise/walk tasks |
| `medication` | Medicine administration |
| `grooming` | Brushing, cleaning |
| `appointment` | Vet visits |
| `play` | Play sessions |
| `unknown` | Unrecognised input |

---

## Input / Output Format

**Input** — natural language text:

```
I have a dog named Bruno. Feed him at 8 AM and walk him at 6 PM.
```

**Output** — structured JSON:

```json
{
  "pets": [...],
  "tasks": [...],
  "confidence": 0.82,
  "warnings": [...],
  "agent_steps": [...]
}
```

---

## Specialization Behavior

The model is built specifically for pet care scheduling. It does **not** generalize beyond this domain.

- ✅ Pet care task classification
- ✅ Time-based scheduling contexts
- ✅ Simple natural language instructions
- ❌ General-purpose NLP

---

## Confidence Scoring

Score is computed as average classifier confidence across all tasks, then penalized for:

- Missing fields
- Ambiguous phrases
- Active warnings

**Range:** `0.0` (low) → `1.0` (high)

---

## Guardrails

The system validates output before returning it to the frontend:

- ⚠️ Missing pet name
- ⚠️ Missing time
- ⚠️ Unknown task types
- ⚠️ Invalid time formats
- ⚠️ Duplicate tasks
- ⚠️ Low confidence outputs
- ⚠️ Empty input

---

## Evaluation Results

| Metric | Value |
|---|---|
| Total test cases | 10 |
| Passed | 10 |
| Failed | 0 |
| Average confidence | ~0.80 |

**Tests covered:**
- Correct task classification
- Misspelling handling
- Conflict detection
- Guardrail effectiveness

---

## Limitations

- Small synthetic dataset
- Limited natural language understanding
- Weak handling of complex sentences
- Single-pet dominant extraction
- No contextual memory
- Rule-based parsing limitations

---

## Biases

- Biased toward common English phrasing
- Limited vocabulary coverage
- May misclassify rare or unconventional phrasing
- Risk of overfitting to synthetic patterns

---

## Misuse Risks

- Incorrect schedules for critical pet care tasks
- Over-reliance on automation without human verification
- Misinterpretation of vague instructions

---

## Future Improvements

- Larger and more diverse training dataset
- Transformer-based offline models
- Improved multi-pet task assignment
- Better time extraction
- Persistent storage
- Improved UI feedback loops

---

## Reflection

**What are the limitations or biases?**
The model relies on a small synthetic dataset, limiting generalisation to diverse real-world inputs. It is biased toward common phrases and may struggle with unusual wording or complex instructions.

**Could this AI be misused?**
Yes. Users might rely on it for critical pet care decisions without verifying outputs, which could lead to missed or incorrect tasks.

**How would you prevent misuse?**
- Show confidence scores clearly
- Display warnings prominently
- Encourage manual verification
- Improve guardrails for unsafe outputs

**What surprised you during reliability testing?**
The model handled simple inputs well but struggled with vague or incomplete instructions. Misspellings like `medcine` were handled better than expected due to their inclusion in training data.

**How did you collaborate with AI?**
AI tools assisted with system architecture design, code structure generation, debugging, and implementation clarity. All final logic and decisions were manually validated and refined.

**One helpful AI suggestion:**
Using a pipeline with `TfidfVectorizer` + `LogisticRegression` provided a simple yet effective way to implement local AI without external APIs.

**One flawed AI suggestion:**
Some generated parsing logic was overly complex or unrealistic for the dataset, requiring simplification and manual correction.

---

*PawPal AI Planner · Model Card · Local Intent Classification + Rule-Based Parser*
