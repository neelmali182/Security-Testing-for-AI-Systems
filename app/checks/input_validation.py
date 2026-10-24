from app.model_adapter import classify


def run() -> dict:
    """Verify the model adapter rejects invalid input without raising."""
    invalid_samples = [None, "", "   ", "x" * 5000, 42, ["hello"]]
    rejected = 0
    for sample in invalid_samples:
        try:
            classify(sample)
        except (TypeError, ValueError):
            rejected += 1

    passed = rejected == len(invalid_samples)
    return {
        "check_id": "INPUT-001",
        "name": "Input validation",
        "category": "input_validation",
        "status": "PASS" if passed else "FAIL",
        "severity": "LOW" if passed else "HIGH",
        "summary": "Invalid and oversized inputs are rejected safely" if passed else "One or more invalid inputs were accepted",
        "evidence": f"Rejected {rejected} of {len(invalid_samples)} invalid synthetic inputs",
        "recommendation": "Keep strict type, blank-input, and length validation enabled",
    }
