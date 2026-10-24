from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.model_adapter import answer_prompt, classify
from app.scanner import available_checks, run_scan
from app.schemas import DemoPromptRequest, ScanRequest

app = FastAPI(
    title="AIShield",
    description="A local educational demonstration of repeatable AI security checks.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aishield"}


@app.get("/api/checks")
def checks() -> dict:
    return {"checks": available_checks()}


@app.post("/api/scans")
def create_scan(request: ScanRequest) -> dict:
    try:
        return run_scan(request.target_name, request.checks)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/scans/{scan_id}")
def get_scan(scan_id: str) -> dict:
    if len(scan_id) != 32 or any(char not in "0123456789abcdef" for char in scan_id):
        raise HTTPException(status_code=404, detail="Scan not found")
    from pathlib import Path
    import json

    path = Path("reports") / f"{scan_id}.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Scan not found")
    return json.loads(path.read_text(encoding="utf-8"))


@app.post("/api/demo/classify")
def demo_classify(payload: dict) -> dict:
    try:
        return classify(payload.get("text"))
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/demo/assistant")
def demo_assistant(payload: DemoPromptRequest) -> dict:
    try:
        return answer_prompt(payload.prompt)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
