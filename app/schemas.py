from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ScanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_name: str = Field(default="local-demo-model", min_length=1, max_length=80)
    checks: list[str] | None = Field(default=None, max_length=10)


class Finding(BaseModel):
    check_id: str
    name: str
    category: str
    status: Literal["PASS", "FAIL"]
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    summary: str
    evidence: str
    recommendation: str


class ScanResult(BaseModel):
    scan_id: str
    target_name: str
    created_at: datetime
    status: Literal["PASS", "FAIL"]
    totals: dict[str, int]
    findings: list[Finding]
