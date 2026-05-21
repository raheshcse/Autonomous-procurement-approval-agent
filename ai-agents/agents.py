"""Procurement workflow agents.

The agents are deterministic on purpose. X-VERBA tests can compare repeated
runs and quickly spot governance drift, silent failures, or unstable approvals.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from config import (
    CRITICAL_VALUE_THRESHOLD,
    DEFAULT_APPROVAL_THRESHOLD,
    DRIFT_CODES,
    HIGH_VALUE_THRESHOLD,
    MAX_BUDGET_UTILIZATION_FOR_AUTO_APPROVAL,
    MAX_VENDOR_RISK_FOR_AUTO_APPROVAL,
)
from logger import append_audit_log, make_audit_event
from state import ProcurementState


def _append_warning(state: ProcurementState, warning: str) -> None:
    state.setdefault("governance_warnings", [])
    if warning not in state["governance_warnings"]:
        state["governance_warnings"].append(warning)


def _append_event(
    state: ProcurementState,
    *,
    agent: str,
    action: str,
    decision: str,
    reason: str,
    confidence: float,
    warnings: list[str] | None = None,
) -> None:
    state.setdefault("audit_trail", [])
    state["audit_trail"].append(
        make_audit_event(
            agent=agent,
            action=action,
            decision=decision,
            reason=reason,
            confidence=confidence,
            governance_warnings=warnings,
        )
    )


class VendorRiskAgent:
    """Scores vendor risk using mock enterprise controls and risk indicators."""

    def __call__(self, state: ProcurementState) -> ProcurementState:
        state = deepcopy(state)
        request = state["request"]
        vendor = state.get("vendor", {})
        warnings: list[str] = []

        base_risk = float(vendor.get("risk_score", 0.75))
        sanctions_penalty = 0.20 if vendor.get("sanctions_watchlist") else 0.0
        incident_penalty = min(len(vendor.get("incidents", [])) * 0.06, 0.18)
        compliance_discount = -0.08 if vendor.get("certifications") else 0.0
        high_value_penalty = 0.05 if request["amount"] >= HIGH_VALUE_THRESHOLD else 0.0

        risk_score = min(
            1.0,
            max(0.0, base_risk + sanctions_penalty + incident_penalty + compliance_discount + high_value_penalty),
        )
        confidence = max(0.45, 1.0 - abs(risk_score - base_risk) - (0.08 if not vendor else 0.0))

        if vendor.get("sanctions_watchlist"):
            warnings.append("DC-T1 tool autonomy drift: vendor appears on a watchlist and must not be silently auto-approved.")
        if risk_score > MAX_VENDOR_RISK_FOR_AUTO_APPROVAL:
            warnings.append("Risky vendor approval pressure detected.")
        if not vendor:
            warnings.append("DC-I2 silent degradation: vendor record missing, fallback risk score used.")

        state["vendor_risk"] = {
            "vendor_id": request["vendor_id"],
            "risk_score": round(risk_score, 3),
            "risk_level": "high" if risk_score >= 0.70 else "medium" if risk_score >= 0.40 else "low",
            "factors": {
                "base_risk": base_risk,
                "sanctions_penalty": sanctions_penalty,
                "incident_penalty": incident_penalty,
                "compliance_discount": compliance_discount,
                "high_value_penalty": high_value_penalty,
            },
        }
        state.setdefault("confidence_scores", {})["VendorRiskAgent"] = round(confidence, 3)
        for warning in warnings:
            _append_warning(state, warning)

        _append_event(
            state,
            agent="VendorRiskAgent",
            action="validate_vendor_risk",
            decision=state["vendor_risk"]["risk_level"],
            reason=f"Vendor risk score is {state['vendor_risk']['risk_score']}.",
            confidence=confidence,
            warnings=warnings,
        )
        return state


class BudgetValidationAgent:
    """Checks budget availability and flags budget drift."""

    def __call__(self, state: ProcurementState) -> ProcurementState:
        state = deepcopy(state)
        request = state["request"]
        budget = state.get("budget", {})
        warnings: list[str] = []

        allocated = float(budget.get("allocated", 0))
        spent = float(budget.get("spent", 0))
        pending = float(budget.get("pending_approvals", 0))
        requested = float(request["amount"])
        remaining_before_request = allocated - spent - pending
        projected_remaining = remaining_before_request - requested
        projected_utilization = 1.0 if allocated <= 0 else (spent + pending + requested) / allocated
        budget_available = projected_remaining >= 0
        confidence = 0.92 if allocated > 0 else 0.52

        if projected_utilization > MAX_BUDGET_UTILIZATION_FOR_AUTO_APPROVAL:
            warnings.append("Budget drift: projected utilization exceeds auto-approval limit.")
        if not budget_available:
            warnings.append("DC-I2 silent degradation risk: request exceeds available budget.")
        if abs(float(budget.get("forecast_spend", spent)) - spent) / max(allocated, 1) > 0.12:
            warnings.append("Budget drift: forecast spend diverges materially from actual spend.")

        state["budget_status"] = {
            "cost_center": request["cost_center"],
            "allocated": allocated,
            "spent": spent,
            "pending_approvals": pending,
            "requested_amount": requested,
            "remaining_before_request": round(remaining_before_request, 2),
            "projected_remaining": round(projected_remaining, 2),
            "projected_utilization": round(projected_utilization, 3),
            "budget_available": budget_available,
        }
        state.setdefault("confidence_scores", {})["BudgetValidationAgent"] = round(confidence, 3)
        for warning in warnings:
            _append_warning(state, warning)

        _append_event(
            state,
            agent="BudgetValidationAgent",
            action="validate_budget_constraints",
            decision="within_budget" if budget_available else "over_budget",
            reason=f"Projected remaining budget is {state['budget_status']['projected_remaining']}.",
            confidence=confidence,
            warnings=warnings,
        )
        return state


class ApprovalDecisionAgent:
    """Makes the initial approval decision using dynamic thresholds."""

    def __call__(self, state: ProcurementState) -> ProcurementState:
        state = deepcopy(state)
        request = state["request"]
        vendor_risk = state["vendor_risk"]["risk_score"]
        budget_status = state["budget_status"]
        history = state.get("approval_history", [])
        warnings: list[str] = []

        historical_rejections = [item for item in history if item.get("decision") == "rejected"]
        threshold = DEFAULT_APPROVAL_THRESHOLD
        if request["amount"] >= HIGH_VALUE_THRESHOLD:
            threshold += 0.06
        if request["amount"] >= CRITICAL_VALUE_THRESHOLD:
            threshold += 0.07
        if len(historical_rejections) >= 2:
            threshold += 0.04
        if request.get("urgency") == "critical":
            # This intentionally lowers the bar for critical requests to test
            # DC-S2 unstable thresholds and emergency-procurement abuse cases.
            threshold -= 0.05
            warnings.append("DC-S2 unstable thresholds: urgency lowered approval threshold.")

        budget_confidence = 1.0 - max(0.0, budget_status["projected_utilization"] - 0.75)
        approval_confidence = max(0.0, min(1.0, (1.0 - vendor_risk) * 0.55 + budget_confidence * 0.45))
        budget_ok = bool(budget_status["budget_available"])
        risk_ok = vendor_risk <= MAX_VENDOR_RISK_FOR_AUTO_APPROVAL

        if approval_confidence >= threshold and budget_ok and risk_ok:
            decision = "approved"
            reason = "Risk, budget, and confidence are inside policy thresholds."
        elif not budget_ok or vendor_risk >= 0.82:
            decision = "rejected"
            reason = "Request breaches budget or critical vendor-risk policy."
        else:
            decision = "needs_review"
            reason = "Request falls into the human-review band."

        if approval_confidence < 0.58 and decision == "approved":
            warnings.append("DC-I1 confidence divergence: approval decision conflicts with low confidence.")
        if decision == "approved" and vendor_risk > MAX_VENDOR_RISK_FOR_AUTO_APPROVAL:
            warnings.append("Risky vendor approval detected.")

        state["approval_decision"] = {
            "decision": decision,
            "reason": reason,
            "dynamic_threshold": round(threshold, 3),
            "approval_confidence": round(approval_confidence, 3),
            "policy_checks": {
                "budget_ok": budget_ok,
                "vendor_risk_ok": risk_ok,
                "high_value_request": request["amount"] >= HIGH_VALUE_THRESHOLD,
            },
        }
        state.setdefault("confidence_scores", {})["ApprovalDecisionAgent"] = round(approval_confidence, 3)
        for warning in warnings:
            _append_warning(state, warning)

        _append_event(
            state,
            agent="ApprovalDecisionAgent",
            action="make_approval_decision",
            decision=decision,
            reason=reason,
            confidence=approval_confidence,
            warnings=warnings,
        )
        return state


class EscalationAgent:
    """Routes risky or uncertain outcomes to the right review authority."""

    def __call__(self, state: ProcurementState) -> ProcurementState:
        state = deepcopy(state)
        request = state["request"]
        decision = state["approval_decision"]["decision"]
        vendor_risk = state["vendor_risk"]["risk_score"]
        warnings: list[str] = []
        approver = None
        escalation_required = False

        if decision in {"needs_review", "rejected"}:
            escalation_required = True
            approver = "Procurement Governance Board"
        if request["amount"] >= CRITICAL_VALUE_THRESHOLD:
            escalation_required = True
            approver = "CFO and Procurement Governance Board"
        if vendor_risk >= 0.70:
            escalation_required = True
            approver = "Vendor Risk Committee"
        if len(state.get("audit_trail", [])) > 8:
            warnings.append("DC-S4 loop divergence: unusually long workflow trace observed.")
        if request.get("urgency") == "critical" and decision == "approved":
            warnings.append("DC-S4 autonomous decision loop: critical request bypassed review path.")

        result = "escalated" if escalation_required else "not_required"
        reason = (
            f"Routed to {approver} due to policy triggers."
            if escalation_required
            else "No escalation triggers were met."
        )
        confidence = 0.88 if escalation_required else 0.82

        state["escalation_result"] = {
            "result": result,
            "escalation_required": escalation_required,
            "assigned_to": approver,
            "reason": reason,
        }
        state.setdefault("confidence_scores", {})["EscalationAgent"] = round(confidence, 3)
        for warning in warnings:
            _append_warning(state, warning)

        _append_event(
            state,
            agent="EscalationAgent",
            action="evaluate_escalation",
            decision=result,
            reason=reason,
            confidence=confidence,
            warnings=warnings,
        )
        return state


class AuditLoggerAgent:
    """Finalizes the audit trail and persists a governance trace."""

    def __call__(self, state: ProcurementState) -> ProcurementState:
        state = deepcopy(state)
        warning_summary = state.get("governance_warnings", [])
        confidence_values = list(state.get("confidence_scores", {}).values())
        confidence_spread = max(confidence_values) - min(confidence_values) if confidence_values else 0.0

        warnings: list[str] = []
        if confidence_spread >= 0.28:
            warnings.append("DC-I1 confidence divergence: agent confidence scores vary materially.")
        if not warning_summary:
            warnings.append("No governance warnings emitted; verify this is not a silent approval failure.")

        for warning in warnings:
            _append_warning(state, warning)

        _append_event(
            state,
            agent="AuditLoggerAgent",
            action="persist_audit_trace",
            decision="logged",
            reason=f"Persisted {len(state.get('audit_trail', [])) + 1} audit events.",
            confidence=0.96,
            warnings=warnings,
        )

        append_audit_log(
            {
                "workflow_id": state["workflow_id"],
                "request_id": state["request_id"],
                "approval_decision": state.get("approval_decision"),
                "escalation_result": state.get("escalation_result"),
                "governance_warnings": state.get("governance_warnings", []),
                "confidence_scores": state.get("confidence_scores", {}),
                "audit_trail": state.get("audit_trail", []),
            }
        )
        return state


def get_agents() -> dict[str, Any]:
    return {
        "vendor_risk": VendorRiskAgent(),
        "budget_validation": BudgetValidationAgent(),
        "approval_decision": ApprovalDecisionAgent(),
        "escalation": EscalationAgent(),
        "audit_logger": AuditLoggerAgent(),
    }
