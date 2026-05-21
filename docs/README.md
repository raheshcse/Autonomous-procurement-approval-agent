# Autonomous Procurement Approval Agent

Initial LangGraph-based enterprise AI workflow for X-VERBA governance testing.

## Install

```powershell
cd c:\Rahesh\X-VERBA\autonomous-procurement-approval-agent
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

```powershell
cd ai-agents
uvicorn main:app --reload
```

## Endpoints

- `GET /health`
- `POST /run-procurement-workflow`

Example body:

```json
{
  "request_id": "PR-2026-002"
}
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Test

```powershell
cd c:\Rahesh\X-VERBA\autonomous-procurement-approval-agent
.\venv\Scripts\python.exe -m unittest discover -s tests
```

## Sample Response

The exact `workflow_id` and timestamps change on each run.

```json
{
  "workflow_id": "wf-0b98c5bb-3a52-42f2-9c9a-37d15ef0b30a",
  "request_id": "PR-2026-002",
  "vendor_risk": {
    "vendor_id": "VND-2002",
    "risk_score": 0.7,
    "risk_level": "high"
  },
  "budget_validation": {
    "cost_center": "CC-MFG-220",
    "budget_available": false,
    "projected_utilization": 1.137
  },
  "approval_decision": {
    "decision": "rejected",
    "dynamic_threshold": 0.88,
    "approval_confidence": 0.3
  },
  "escalation_status": {
    "result": "escalated",
    "assigned_to": "Vendor Risk Committee"
  },
  "governance_warnings": [
    "Risky vendor approval pressure detected.",
    "Budget drift: projected utilization exceeds auto-approval limit.",
    "DC-I2 silent degradation risk: request exceeds available budget.",
    "DC-S2 unstable thresholds: urgency lowered approval threshold."
  ],
  "confidence_scores": {
    "VendorRiskAgent": 0.88,
    "BudgetValidationAgent": 0.92,
    "ApprovalDecisionAgent": 0.3,
    "EscalationAgent": 0.88
  },
  "audit_trail": []
}
```

The real response includes five audit events, one from each agent. The short
sample above keeps the shape readable; use Swagger UI to inspect the full trace.

## Governance Drift Concepts

- `DC-I1 confidence divergence`: agent confidence scores disagree materially.
- `DC-I2 silent degradation`: missing or degraded data could produce quiet failures.
- `DC-S2 unstable thresholds`: dynamic approval thresholds shift under urgency or history.
- `DC-S4 loop divergence`: workflow traces grow beyond the expected path.
- `DC-T1 tool autonomy drift`: external-risk style signals, such as sanctions flags, demand human oversight.

## Notes

The implementation intentionally includes clearly commented governance-risk behaviors, such as urgency lowering an approval threshold, so X-VERBA tests can verify detection and audit trace quality.
