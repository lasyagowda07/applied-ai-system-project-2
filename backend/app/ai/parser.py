import os
import re
import joblib

from app.ai.train_model import train_and_save_model


MODEL_PATH = os.path.join(os.path.dirname(__file__), "intent_model.joblib")


SPECIES = ["dog", "cat", "bird", "rabbit", "hamster", "fish"]


def load_model():
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()
    return joblib.load(MODEL_PATH)


def normalize_time(raw_time):
    raw_time = raw_time.strip().lower().replace(".", "")

    match = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", raw_time)
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    period = match.group(3)

    if period == "pm" and hour != 12:
        hour += 12
    elif period == "am" and hour == 12:
        hour = 0

    if hour > 23 or minute > 59:
        return None

    return f"{hour:02d}:{minute:02d}"


def extract_times(text):
    pattern = r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?\b"
    matches = re.findall(pattern, text)
    return [normalize_time(match) for match in matches if normalize_time(match)]


def extract_species(text):
    lowered = text.lower()
    for species in SPECIES:
        if species in lowered:
            return species
    return "unknown"


def extract_pet_names(text):
    patterns = [
        r"named\s+([A-Z][a-zA-Z]+)",
        r"pet\s+([A-Z][a-zA-Z]+)",
        r"dog\s+named\s+([A-Z][a-zA-Z]+)",
        r"cat\s+named\s+([A-Z][a-zA-Z]+)",
    ]

    names = []
    for pattern in patterns:
        names.extend(re.findall(pattern, text))

    return list(dict.fromkeys(names))


def extract_recurrence(text):
    lowered = text.lower()

    if "daily" in lowered or "every day" in lowered:
        return "daily"

    if "weekly" in lowered or "every week" in lowered:
        return "weekly"

    return None


def split_task_phrases(text):
    separators = r"\band\b|,|\.|\n"
    phrases = re.split(separators, text)
    return [phrase.strip() for phrase in phrases if len(phrase.strip()) > 2]


def classify_task_type(model, phrase):
    prediction = model.predict([phrase])[0]

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([phrase])[0]
        confidence = max(probabilities)
    else:
        confidence = 0.75

    return prediction, round(float(confidence), 2)


def calculate_overall_confidence(tasks, warnings):
    if not tasks:
        return 0.2

    confidence = sum(task["classifier_confidence"] for task in tasks) / len(tasks)

    confidence -= len(warnings) * 0.08
    confidence = max(0.0, min(1.0, confidence))

    return round(confidence, 2)


def parse_pet_care_text(text):
    model = load_model()

    agent_steps = [
        "Step 1: Received natural language pet care request.",
        "Step 2: Split request into possible task phrases.",
        "Step 3: Used local specialized intent classifier to detect task types.",
        "Step 4: Extracted pet names, species, times, and recurrence rules.",
    ]

    warnings = []

    if not text or not text.strip():
        return {
            "pets": [],
            "tasks": [],
            "confidence": 0.0,
            "warnings": ["Input is empty."],
            "agent_steps": agent_steps,
        }

    pet_names = extract_pet_names(text)
    species = extract_species(text)
    times = extract_times(text)
    recurrence = extract_recurrence(text)
    phrases = split_task_phrases(text)

    if not pet_names:
        pet_names = ["Unknown Pet"]
        warnings.append("No clear pet name found. Defaulted to Unknown Pet.")

    if species == "unknown":
        warnings.append("No clear species found. Defaulted to unknown.")

    tasks = []
    time_index = 0

    for phrase in phrases:
        task_type, classifier_confidence = classify_task_type(model, phrase)

        if task_type == "unknown":
            continue

        task_time = times[time_index] if time_index < len(times) else None

        if task_time:
            time_index += 1
        else:
            warnings.append(f"No clear time found for task phrase: '{phrase}'.")

        task = {
            "pet_name": pet_names[0],
            "species": species,
            "description": phrase,
            "task_type": task_type,
            "time": task_time,
            "recurrence": recurrence,
            "priority": 1,
            "duration": 15,
            "completed": False,
            "classifier_confidence": classifier_confidence,
        }
        tasks.append(task)

    if not tasks:
        warnings.append("No valid pet care tasks were detected.")

    confidence = calculate_overall_confidence(tasks, warnings)

    return {
        "pets": [{"name": name, "species": species, "age": None} for name in pet_names],
        "tasks": tasks,
        "confidence": confidence,
        "warnings": warnings,
        "agent_steps": agent_steps,
    }