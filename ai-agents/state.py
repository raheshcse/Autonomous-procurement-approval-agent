"""Shared LangGraph state definitions.

TypedDict keeps this beginner-friendly while still documenting the exact shape
that each agent reads from and writes to during the workflow.
"""

from typing import Any, Literal, TypedDict


DecisionStatus = Literal["approved", "rejected", "escalated", "needs_review"]


class AuditEvent(TypedDict):
    timestamp: str
    agent: str
    action: str
    decision: str
    reason: str
    confidence: float
    governance_warnings: list[str]


class ProcurementState(TypedDict, total=False):
    workflow_id: str
    request_id: str
    request: dict[str, Any]
    vendor: dict[str, Any]
    budget: dict[str, Any]
    approval_history: list[dict[str, Any]]
    vendor_risk: dict[str, Any]
    budget_status: dict[str, Any]
    approval_decision: dict[str, Any]
    escalation_result: dict[str, Any]
    governance_warnings: list[str]
    confidence_scores: dict[str, float]
    audit_trail: list[AuditEvent]
    errors: list[str]
