from datetime import datetime, timezone
from uuid import uuid4

from app.checks import data_leakage, input_validation, output_policy, prompt_injection, robustness
from app.reporting import save_report

CHECKS = {
    "input_validation": input_validation.run,
    "robustness": robustness.run,
    "prompt_injection": prompt_injection.run,
    "data_leakage": data_leakage.run,
    "output_policy": output_policy.run,
}


def available_checks() -> list[dict[str, str]]:
    return [
        {"id": check_id, "name": check_id.replace("_", " ").title()}
        for check_id in CHECKS
    ]


def run_scan(target_name: str = "local-demo-model", requested_checks: list[str] | None = None) -> dict:
    names = requested_checks or list(CHECKS)
    unknown = sorted(set(names) - set(CHECKS))
    if unknown:
        raise ValueError(f"Unknown check(s): {', '.join(unknown)}")
    findings = [CHECKS[name]() for name in names]
    passed = sum(item["status"] == "PASS" for item in findings)
    failed = len(findings) - passed
    result = {
        "scan_id": uuid4().hex,
        "target_name": target_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if failed == 0 else "FAIL",
        "totals": {"checks": len(findings), "passed": passed, "failed": failed},
        "findings": findings,
    }
    save_report(result)
    return result
