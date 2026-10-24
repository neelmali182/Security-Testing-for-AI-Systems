import json
from pathlib import Path

REPORTS_DIR = Path("reports")


def save_report(result: dict) -> None:
    """Persist a synthetic scan report; filenames are generated scan IDs."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / f"{result['scan_id']}.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
