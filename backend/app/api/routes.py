from fastapi import APIRouter

from app.models import TextRequest
from app.ai.parser import parse_pet_care_text
from app.guardrails.validator import validate_parsed_output
from app.core.pawpal_system import Owner, Pet, Task, Scheduler


router = APIRouter(prefix="/api")


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "PawPal AI Planner backend is running",
    }


@router.post("/parse")
def parse_text(request: TextRequest):
    return parse_pet_care_text(request.text)


@router.post("/validate")
def validate_text(request: TextRequest):
    parsed = parse_pet_care_text(request.text)
    return validate_parsed_output(parsed)


@router.post("/schedule")
def generate_schedule(request: TextRequest):
    parsed = parse_pet_care_text(request.text)

    owner = Owner()
    pet_objects = {}

    for pet_data in parsed["pets"]:
        pet = Pet(
            name=pet_data["name"],
            species=pet_data.get("species", "unknown"),
            age=pet_data.get("age"),
        )
        owner.add_pet(pet)
        pet_objects[pet.name] = pet

    for task_data in parsed["tasks"]:
        pet_name = task_data["pet_name"]

        if pet_name not in pet_objects:
            pet = Pet(name=pet_name, species=task_data.get("species", "unknown"))
            owner.add_pet(pet)
            pet_objects[pet_name] = pet

        task = Task(
            description=task_data["description"],
            task_type=task_data["task_type"],
            time=task_data["time"],
            pet_name=task_data["pet_name"],
            recurrence=task_data.get("recurrence"),
            priority=task_data.get("priority", 1),
            duration=task_data.get("duration", 15),
        )

        pet_objects[pet_name].add_task(task)

    scheduler = Scheduler(owner)

    validation = validate_parsed_output(parsed)
    conflicts = scheduler.detect_conflicts()

    agent_steps = parsed["agent_steps"] + [
        "Step 5: Created PawPal Owner, Pet, and Task objects.",
        "Step 6: Generated sorted schedule using Scheduler.",
        "Step 7: Ran guardrails for missing fields, low confidence, and conflicts.",
        "Step 8: Returned final schedule with warnings, confidence, and agent steps.",
    ]

    all_warnings = list(parsed["warnings"]) + list(validation["warnings"])

    for conflict in conflicts:
        all_warnings.append(conflict["message"])

    return {
        "owner": owner.name,
        "pets": [pet.to_dict() for pet in owner.pets],
        "schedule": scheduler.generate_daily_schedule(),
        "conflicts": conflicts,
        "confidence": parsed["confidence"],
        "warnings": sorted(list(set(all_warnings))),
        "agent_steps": agent_steps,
    }


@router.get("/evaluation-summary")
def evaluation_summary():
    from app.evaluation.evaluate import run_evaluation

    return run_evaluation(return_dict=True)