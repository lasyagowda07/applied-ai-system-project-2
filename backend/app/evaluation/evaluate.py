from app.ai.parser import parse_pet_care_text


EVALUATION_CASES = [
    {
        "input": "I have a dog named Bruno. Feed him at 8 AM.",
        "expected_task": "feeding",
    },
    {
        "input": "I have a cat named Luna. Give her medicine at 9 PM.",
        "expected_task": "medication",
    },
    {
        "input": "I have a dog named Max. Walk him at 7 AM daily.",
        "expected_task": "walking",
    },
    {
        "input": "I have a cat named Bella. Brush her at 5 PM.",
        "expected_task": "grooming",
    },
    {
        "input": "I have a dog named Coco. Vet appointment at 3 PM.",
        "expected_task": "appointment",
    },
    {
        "input": "I have a dog named Bruno. Give him medcine at 8 PM.",
        "expected_task": "medication",
    },
    {
        "input": "My pet needs care tomorrow.",
        "expected_task": "unknown",
    },
]


def run_evaluation(return_dict=False):
    results = []
    passed = 0
    total_confidence = 0

    for case in EVALUATION_CASES:
        parsed = parse_pet_care_text(case["input"])
        tasks = parsed.get("tasks", [])

        detected_types = [task["task_type"] for task in tasks]

        if case["expected_task"] == "unknown":
            success = len(detected_types) == 0
        else:
            success = case["expected_task"] in detected_types

        if success:
            passed += 1

        total_confidence += parsed["confidence"]

        results.append(
            {
                "input": case["input"],
                "expected": case["expected_task"],
                "detected": detected_types,
                "confidence": parsed["confidence"],
                "passed": success,
                "warnings": parsed["warnings"],
            }
        )

    total = len(EVALUATION_CASES)
    average_confidence = round(total_confidence / total, 2)

    summary = {
        "total_cases": total,
        "passed": passed,
        "failed": total - passed,
        "average_confidence": average_confidence,
        "results": results,
    }

    if return_dict:
        return summary

    print("PawPal AI Evaluation Summary")
    print("----------------------------")
    print(f"Total cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Average confidence: {average_confidence}")
    print()

    for i, result in enumerate(results, start=1):
        status = "PASS" if result["passed"] else "FAIL"
        print(f"Case {i}: {status}")
        print(f"Input: {result['input']}")
        print(f"Expected: {result['expected']}")
        print(f"Detected: {result['detected']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Warnings: {result['warnings']}")
        print()


if __name__ == "__main__":
    run_evaluation()