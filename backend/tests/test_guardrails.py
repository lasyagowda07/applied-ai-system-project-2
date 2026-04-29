from app.ai.parser import parse_pet_care_text
from app.guardrails.validator import validate_parsed_output


def test_guardrail_catches_missing_time():
    parsed = parse_pet_care_text("I have a dog named Bruno. Feed him.")

    validation = validate_parsed_output(parsed)

    assert "time" in validation["missing_fields"]
    assert validation["is_valid"] is False


def test_guardrail_catches_empty_input():
    parsed = parse_pet_care_text("")

    validation = validate_parsed_output(parsed)

    assert "tasks" in validation["missing_fields"]
    assert validation["is_valid"] is False
    assert len(validation["warnings"]) > 0