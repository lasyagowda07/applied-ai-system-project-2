# 🤖 AI Design — PawPal AI Planner

> *Local specialization: natural language → structured pet care data, no paid API required.*

---

## Overview

PawPal AI Planner uses a local AI pipeline to convert natural language pet care instructions into structured scheduling data. The system avoids GPT, Claude, or any external API by training a small, domain-specific classifier entirely offline.

---

## AI Feature: Local Specialization

| Component | Detail |
|---|---|
| Training data | Synthetic pet care phrases |
| Vectorizer | `TfidfVectorizer` |
| Classifier | `LogisticRegression` |
| Serialization | `joblib` |
| Extraction | Rule-based (time, names, recurrence) |

---

## Synthetic Dataset

Located at `backend/app/ai/synthetic_data.py`. Each example maps a short phrase to a label:

```
feed bruno at 8 am           → feeding
walk max at 7 am             → walking
give luna medicine at 9 pm   → medication
brush bella today            → grooming
vet appointment for coco     → appointment
play with bruno after lunch  → play
random unclear text          → unknown
```

Labels were chosen to match the core task types from the original PawPal+ project.

---

## Classification Labels

| Label | Triggered by |
|---|---|
| `feeding` | feed, food, kibble, breakfast, dinner |
| `walking` | walk, run, exercise, outside |
| `medication` | medicine, pill, tablet, antibiotics, medcine |
| `grooming` | brush, groom, bath, clean |
| `appointment` | vet, appointment, checkup |
| `play` | play, playtime, fetch |
| `unknown` | anything unrecognised |

---

## Classifier Design

```
Text input
    ↓
TfidfVectorizer   ← converts words to numeric features
    ↓
LogisticRegression ← classifies into a task label
    ↓
Predicted task type + confidence score
```

**Why TF-IDF?**
Weights word importance so the model learns that `feed`, `food`, and `kibble` all point to `feeding`, while `pill`, `tablet`, and `medicine` all point to `medication`.

**Why Logistic Regression?**
Simple, fast, interpretable, and well-suited to small text classification datasets. Easy to document and explain.

---

## Parser Design

The parser combines ML classification with rule-based extraction:

1. Receive natural language input
2. Split into smaller task phrases
3. Extract pet names → pattern: `"a dog named {Name}"`
4. Extract species → `dog` · `cat` · `bird` · `rabbit` · `hamster` · `fish`
5. Extract time → normalise to 24h format
6. Extract recurrence → `daily` · `weekly` · `none`
7. Classify each phrase with the trained model
8. Return structured JSON

---

## Rule-Based Extraction Details

### Time normalisation

| Input | Output |
|---|---|
| `8 AM` | `08:00` |
| `6 PM` | `18:00` |
| `8:30 am` | `08:30` |

### Recurrence values

`daily` · `weekly` · `none`

---

## Confidence Scoring

Score = average classifier confidence across all phrases, minus penalties:

| Penalty condition | Effect |
|---|---|
| Missing pet name | Score reduced |
| Missing time | Score reduced |
| Unknown species | Score reduced |
| Unknown task type | Score reduced |
| Empty input | Score reduced |
| No valid tasks | Score reduced |

**Example:**

```
Classifier confidence:  0.88
Active warnings:        2
Final confidence:       0.72
```

---

## Guardrails

Output is validated before being returned to the frontend:

- ⚠️ Empty input check
- ⚠️ Missing pet name check
- ⚠️ Missing task time check
- ⚠️ Unknown task type check
- ⚠️ Duplicate task / time check
- ⚠️ Low confidence warning

The system never silently pretends it understood something when it did not.

---

## Specialization Proof

| Generic rule-based parser | Specialized classifier |
|---|---|
| Only detects: `medicine` | Learns: `pill`, `tablet`, `antibiotics`, `medcine`, `medicine` |
| Exact keyword match only | Vocabulary generalisation from training |

The classifier makes the system better for the specific PawPal use case without needing a large language model.

---

## Example Input and Output

**Input:**

```
I have a dog named Bruno. Feed him at 8 AM and give medicine at 8 PM.
```

**Output:**

```json
{
  "pets": [
    { "name": "Bruno", "species": "dog", "age": null }
  ],
  "tasks": [
    { "pet_name": "Bruno", "task_type": "feeding",    "time": "08:00" },
    { "pet_name": "Bruno", "task_type": "medication", "time": "20:00" }
  ],
  "confidence": 0.82,
  "warnings": []
}
```

---

## Agentic Workflow

The pipeline exposes its reasoning as `agent_steps`:

| Step | Action |
|---|---|
| Step 1 | Received natural language pet care request |
| Step 2 | Split request into possible task phrases |
| Step 3 | Used local specialized intent classifier |
| Step 4 | Extracted pet names, species, times, recurrence |
| Step 5 | Created Owner, Pet, and Task objects |
| Step 6 | Generated sorted schedule using Scheduler |
| Step 7 | Detected conflicts and applied guardrails |
| Step 8 | Returned final structured schedule |

---

## Limitations

- Small synthetic training dataset
- Limited vocabulary
- Weak handling of long, complex sentences
- Limited multi-pet task assignment
- No true reasoning like a large language model
- May misclassify unusual phrasing

---

## Future Improvements

- More and diverse training examples
- Real user-generated data
- Better spelling correction
- Stronger offline NLP model
- Improved multi-pet extraction
- More detailed confidence scoring
- Persistent feedback loop

---

## Summary

The AI is fully integrated — not a standalone classifier:

```
FastAPI backend
    + PawPal scheduler
    + Guardrails
    + Evaluation script
    + Next.js frontend
    = Complete applied AI system
```

---

*PawPal AI Planner · AI Design · Local Specialization*
