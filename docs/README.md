# Autonomous Procurement Approval Agent

Enterprise AI multi-agent procurement governance system built using:

* FastAPI
* LangGraph
* TypedDict
* JSON enterprise mock data
* Audit logging
* Workflow orchestration
* Governance monitoring

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
                    │ - spending analysis      │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ ApprovalDecisionAgent    │
                    │ - approval confidence    │
                    │ - dynamic decisions      │
                    │ - workflow validation    │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ EscalationAgent          │
                    │ - escalation routing     │
                    │ - governance review      │
                    │ - operational handling   │
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
* mutates workflow state
* contributes confidence scores
* generates governance observations
* passes decisions to downstream agents

The workflow simulates enterprise procurement approval coordination across multiple AI-assisted services.

---

# Governance Monitoring

The platform simulates enterprise procurement governance scenarios including:

* vendor approval conflicts
* high-risk supplier detection
* budget over-utilization
* approval confidence inconsistencies
* escalation routing
* operational anomaly detection
* audit trace generation

The workflow helps demonstrate how enterprise AI systems can maintain:

* operational transparency
* auditability
* approval accountability
* escalation control
* workflow observability

within autonomous procurement pipelines.

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
cd c:\Rahesh\autonomous-procurement-approval-agent
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
    "approval_confidence": 0.3
  },
  "escalation_status": {
    "result": "escalated",
    "assigned_to": "Vendor Risk Committee"
  },
  "governance_warnings": [
    "Risky vendor approval pressure detected.",
    "Budget utilization exceeded approval threshold.",
    "Operational review required.",
    "Escalation triggered for governance review."
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
cd c:\Rahesh\autonomous-procurement-approval-agent
.\venv\Scripts\python.exe -m unittest discover -s tests
```

---

# Purpose

This project was built to explore:

* enterprise AI workflow orchestration
* autonomous procurement decision systems
* LangGraph multi-agent coordination
* governance monitoring
* operational risk analysis
* audit logging and observability
* enterprise escalation workflows

The system combines:

* autonomous decision-making
* workflow validation
* governance oversight
* confidence scoring
* audit transparency

to simulate real-world enterprise procurement operations.