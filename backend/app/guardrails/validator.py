def validate_parsed_output(parsed_output):
    warnings = list(parsed_output.get("warnings", []))
    missing_fields = []

    tasks = parsed_output.get("tasks", [])
    confidence = parsed_output.get("confidence", 0.0)

    if not tasks:
        warnings.append("No tasks available for scheduling.")
        missing_fields.append("tasks")

    for task in tasks:
        if not task.get("pet_name") or task.get("pet_name") == "Unknown Pet":
            missing_fields.append("pet_name")

        if not task.get("time"):
            missing_fields.append("time")

        if not task.get("task_type") or task.get("task_type") == "unknown":
            missing_fields.append("task_type")

    if confidence < 0.6:
        warnings.append("Low confidence output. Please review the extracted schedule.")

    seen = set()
    for task in tasks:
        key = (task.get("pet_name"), task.get("time"))

        if task.get("time") and key in seen:
            warnings.append(
                f"Possible conflict: multiple tasks for {task.get('pet_name')} at {task.get('time')}."
            )

        seen.add(key)

    missing_fields = sorted(list(set(missing_fields)))

    return {
        "is_valid": len(missing_fields) == 0 and confidence >= 0.6,
        "warnings": sorted(list(set(warnings))),
        "missing_fields": missing_fields,
        "confidence": confidence,
    }