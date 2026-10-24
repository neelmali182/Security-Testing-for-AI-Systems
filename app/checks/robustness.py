from app.model_adapter import classify


def run() -> dict:
    """Compare a fixed sample with meaning-preserving whitespace changes."""
    samples = [
        ("This is a good and helpful result", "  This is a good and helpful result  "),
        ("This is a bad and harmful result", "  This is a bad and harmful result  "),
        ("An ordinary neutral example", "  An ordinary neutral example  "),
    ]
    stable = sum(classify(original) == classify(variant) for original, variant in samples)
    score = stable / len(samples)
    passed = score == 1.0
    return {
        "check_id": "ROBUST-001",
        "name": "Whitespace robustness",
        "category": "robustness",
        "status": "PASS" if passed else "FAIL",
        "severity": "LOW" if passed else "MEDIUM",
        "summary": "Predictions stayed stable under harmless whitespace changes" if passed else "Predictions changed under harmless whitespace changes",
        "evidence": f"Stability score: {stable}/{len(samples)} ({score:.0%})",
        "recommendation": "Expand the fixed perturbation set when adding a real model adapter",
    }
