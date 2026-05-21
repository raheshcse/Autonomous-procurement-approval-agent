# Autonomous Procurement Approval Agent

Enterprise AI multi-agent governance testing system built using:

* FastAPI
* LangGraph
* TypedDict
* JSON enterprise mock data
* Audit logging
* Governance drift simulation
* X-VERBA-style observability patterns

This project simulates an autonomous procurement approval workflow where multiple AI agents collaborate to evaluate vendor risk, validate budgets, make approval decisions, escalate governance concerns, and generate audit traces.

---

# Architecture

```text
                         ┌──────────────────────┐
                         │ Procurement Request  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────┐
                    │   VendorRiskAgent        │
                    │ - vendor risk scoring    │
                    │ - sanctions validation   │
                    │ - compliance checks      │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ BudgetValidationAgent    │
                    │ - budget availability    │
                    │ - forecast utilization   │
                    │ - budget drift analysis  │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ ApprovalDecisionAgent    │
                    │ - dynamic thresholds     │
                    │ - approval confidence    │
                    │ - autonomous decisions   │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ EscalationAgent          │
                    │ - governance escalation  │
                    │ - committee routing      │
                    │ - drift detection        │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ AuditLoggerAgent         │
                    │ - audit events           │
                    │ - governance warnings    │
                    │ - workflow trace         │
                    └──────────┬───────────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │ JSON API Output  │
                      └──────────────────┘
```

---

# A2A Workflow Design

This project demonstrates sequential Agent-to-Agent (A2A) orchestration using LangGraph.

Each agent:

* receives shared workflow state
* mutates state
* contributes confidence scores
* generates governance observations
* passes decisions to downstream agents

The workflow intentionally introduces governance instability patterns for X-VERBA testing.

---

# Governance Drift Simulation

The implementation intentionally includes governance-risk behaviors to simulate real enterprise AI governance failures.

## Simulated Drift Classes

| Drift Class | Description                                        |
| ----------- | -------------------------------------------------- |
| DC-I1       | Confidence divergence between agents               |
| DC-I2       | Silent degradation from incomplete/risky decisions |
| DC-S2       | Unstable approval thresholds under urgency         |
| DC-S4       | Escalation and workflow divergence                 |
| DC-T1       | Autonomous tool-style approval drift               |

---

# Project Structure

```text
autonomous-procurement-approval-agent/
│
├── ai-agents/
│   ├── main.py
│   ├── workflow.py
│   ├── agents.py
│   ├── state.py
│   ├── logger.py
│   └── config.py
│
├── mock-data/
│   ├── procurement-requests.json
│   ├── vendors.json
│   ├── budget-data.json
│   └── approval-history.json
│
├── logs/
├── docs/
└── tests/
```

---

# Install

```powershell
cd c:\Rahesh\X-VERBA\autonomous-procurement-approval-agent
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

# Run

```powershell
cd ai-agents
uvicorn main:app --reload
```

---

# Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

| Method | Endpoint                    |
| ------ | --------------------------- |
| GET    | `/`                         |
| GET    | `/health`                   |
| POST   | `/run-procurement-workflow` |

---

# Example Request

```json
{
  "request_id": "PR-2026-002"
}
```

---

# Example Response

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
    "DC-I2 silent degradation risk detected.",
    "DC-S2 unstable threshold behavior detected."
  ]
}
```

---

# Audit Logging

Audit traces are written to:

```text
logs/audit-log.jsonl
```

Each workflow execution records:

* timestamps
* agent decisions
* governance warnings
* escalation traces
* confidence scores
* workflow transitions

---

# Testing

```powershell
cd c:\Rahesh\X-VERBA\autonomous-procurement-approval-agent
.\venv\Scripts\python.exe -m unittest discover -s tests
```

---

# Purpose

This project was built to explore:

* AI governance testing
* enterprise multi-agent orchestration
* LangGraph workflow design
* governance drift simulation
* observability and auditability
* X-VERBA-style risk analysis patterns

The system intentionally balances:

* autonomous decision-making
* governance instability
* audit transparency
* escalation controls

to simulate real-world enterprise AI risks.
