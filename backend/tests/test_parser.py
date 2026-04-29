from app.ai.parser import parse_pet_care_text


def test_parser_extracts_feeding_task():
    result = parse_pet_care_text("I have a dog named Bruno. Feed him at 8 AM.")

    assert result["pets"][0]["name"] == "Bruno"
    assert result["tasks"][0]["task_type"] == "feeding"
    assert result["tasks"][0]["time"] == "08:00"
    assert result["confidence"] > 0


def test_parser_extracts_medication_task():
    result = parse_pet_care_text("I have a cat named Luna. Give her medicine at 9 PM.")

    task_types = [task["task_type"] for task in result["tasks"]]

    assert "medication" in task_types


def test_parser_handles_misspelling():
    result = parse_pet_care_text("I have a dog named Max. Give him medcine at 8 PM.")

    task_types = [task["task_type"] for task in result["tasks"]]

    assert "medication" in task_types


def test_parser_returns_low_confidence_for_unclear_input():
    result = parse_pet_care_text("My pet needs care tomorrow.")

    assert result["confidence"] < 0.6
    assert len(result["warnings"]) > 0