"""FastAPI entrypoint for the Autonomous Procurement Approval Agent.

Run from this directory with:
    uvicorn main:app --reload
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from json import JSONDecodeError
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from config import (
    APPROVAL_HISTORY_FILE,
    BUDGET_FILE,
    PROCUREMENT_REQUESTS_FILE,
    VENDORS_FILE,
)
from state import ProcurementState
from workflow import procurement_workflow


class WorkflowRunRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"request_id": "PR-2026-002"}]})

    request_id: str = Field(
        ...,
        min_length=1,
        description="Procurement request ID from mock-data/procurement-requests.json.",
    )


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Autonomous Procurement Approval Agent",
    description="AI-powered procurement workflow orchestration API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_json(path) -> Any:
    """Load JSON with API-friendly errors instead of raw tracebacks."""
    if not path.exists():
        raise HTTPException(status_code=500, detail=f"Required data file is missing: {path.name}")
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {path.name}: {exc}") from exc


def _require_list(data: Any, file_name: str) -> list[dict[str, Any]]:
    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail=f"{file_name} must contain a JSON array.")
    return data


def _find_by_id(records: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    return next((item for item in records if item.get(key) == value), None)


def _build_initial_state(request_id: str) -> ProcurementState:
    requests = _require_list(_load_json(PROCUREMENT_REQUESTS_FILE), PROCUREMENT_REQUESTS_FILE.name)
    vendors = _require_list(_load_json(VENDORS_FILE), VENDORS_FILE.name)
    budgets = _require_list(_load_json(BUDGET_FILE), BUDGET_FILE.name)
    approval_history = _require_list(_load_json(APPROVAL_HISTORY_FILE), APPROVAL_HISTORY_FILE.name)

    request = _find_by_id(requests, "request_id", request_id)
    if not request:
        raise HTTPException(status_code=404, detail=f"Procurement request {request_id} was not found.")
    required_fields = {"request_id", "vendor_id", "cost_center", "amount", "urgency"}
    missing_fields = sorted(required_fields - set(request))
    if missing_fields:
        raise HTTPException(
            status_code=500,
            detail=f"Procurement request {request_id} is missing fields: {', '.join(missing_fields)}",
        )

    vendor = _find_by_id(vendors, "vendor_id", request["vendor_id"]) or {}
    budget = _find_by_id(budgets, "cost_center", request["cost_center"]) or {}
    history = [item for item in approval_history if item.get("vendor_id") == request["vendor_id"]]

    return {
        "workflow_id": f"wf-{uuid4()}",
        "request_id": request_id,
        "request": request,
        "vendor": vendor,
        "budget": budget,
        "approval_history": history,
        "governance_warnings": [],
        "confidence_scores": {},
        "audit_trail": [],
        "errors": [],
    }


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "service": "Autonomous Procurement Approval Agent",
        "status": "ready",
        "docs": "/docs",
        "health": "/health",
        "workflow_endpoint": "/run-procurement-workflow",
        "sample_request_id": "PR-2026-002",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "autonomous-procurement-approval-agent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/run-procurement-workflow")
def run_procurement_workflow(payload: WorkflowRunRequest) -> dict[str, Any]:
    """Run the full governance workflow for a request in mock JSON data."""
    try:
        initial_state = _build_initial_state(payload.request_id)
        result = procurement_workflow.invoke(initial_state)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {exc}") from exc

    return {
        "workflow_id": result["workflow_id"],
        "request_id": result["request_id"],
        "vendor_risk": result.get("vendor_risk"),
        "budget_validation": result.get("budget_status"),
        "approval_decision": result.get("approval_decision"),
        "escalation_status": result.get("escalation_result"),
        "governance_warnings": result.get("governance_warnings", []),
        "confidence_scores": result.get("confidence_scores", {}),
        "audit_trail": result.get("audit_trail", []),
    }
