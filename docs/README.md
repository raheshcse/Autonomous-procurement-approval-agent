# Autonomous Procurement Approval Agent

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

## Overview

The Autonomous Procurement Approval Agent is a full-stack AI-powered procurement governance platform designed to simulate enterprise procurement approval workflows using multi-agent orchestration.

The system combines a React-based dashboard, FastAPI backend services, and LangGraph workflow orchestration to coordinate specialized AI agents responsible for vendor risk analysis, budget validation, approval decisions, escalation handling, and audit logging.

This project demonstrates how autonomous workflow agents can collaborate to automate procurement processes while maintaining governance, transparency, auditability, and operational oversight.

---

# Key Features

### Multi-Agent Workflow Orchestration

* Vendor Risk Analysis
* Budget Validation
* Approval Decision Making
* Escalation Handling
* Audit Logging
* Governance Monitoring

### Enterprise Governance Simulation

* Vendor risk scoring
* Budget utilization validation
* Procurement approval workflows
* Escalation routing
* Governance warning generation
* Audit trail creation

### Full-Stack Platform

* React Dashboard
* FastAPI REST APIs
* LangGraph Workflow Engine
* Interactive Workflow Runner
* Procurement Operations Dashboard
* API-driven Architecture

### Observability & Auditability

* Workflow trace generation
* Agent decision tracking
* Confidence scoring
* Governance warnings
* Audit log persistence

---

# System Architecture

## Full-Stack Architecture

```text
┌─────────────────────────────┐
│     React Dashboard UI      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│      REST API Layer         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    LangGraph Orchestrator   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Multi-Agent Procurement     │
│ Approval Workflow           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Dashboard Response      │
└─────────────────────────────┘
```

---

## Backend Agent Workflow Architecture

```text
                         ┌──────────────────────┐
                         │ Procurement Request  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────┐
                    │   VendorRiskAgent        │
                    │ - vendor risk scoring    │
                    │ - compliance validation  │
                    │ - supplier evaluation    │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ BudgetValidationAgent    │
                    │ - budget availability    │
                    │ - utilization analysis   │
                    │ - spending validation    │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ ApprovalDecisionAgent    │
                    │ - approval confidence    │
                    │ - decision generation    │
                    │ - workflow validation    │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ EscalationAgent          │
                    │ - escalation routing     │
                    │ - governance review      │
                    │ - exception handling     │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ AuditLoggerAgent         │
                    │ - audit events           │
                    │ - workflow trace         │
                    │ - warning generation     │
                    └──────────┬───────────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │ JSON API Output  │
                      └──────────────────┘
```

---

# Agent Responsibilities

## Vendor Risk Agent

Evaluates suppliers and vendors before procurement approval.

Responsibilities:

* Vendor risk scoring
* Compliance validation
* Supplier assessment
* Risk categorization

Outputs:

* Risk Score
* Risk Level
* Vendor Assessment

---

## Budget Validation Agent

Validates procurement requests against organizational budgets.

Responsibilities:

* Budget availability checks
* Spending analysis
* Utilization forecasting
* Cost center validation

Outputs:

* Budget Availability
* Projected Utilization
* Validation Status

---

## Approval Decision Agent

Makes procurement decisions using previous agent outputs.

Responsibilities:

* Decision evaluation
* Approval confidence calculation
* Workflow validation
* Procurement recommendation

Outputs:

* Approved
* Rejected
* Escalated
* Confidence Score

---

## Escalation Agent

Handles high-risk procurement scenarios.

Responsibilities:

* Governance review routing
* Escalation management
* Operational oversight
* Exception handling

Outputs:

* Escalation Status
* Assigned Review Team

---

## Audit Logger Agent

Maintains operational traceability.

Responsibilities:

* Audit event logging
* Workflow trace generation
* Governance warning creation
* Execution history recording

Outputs:

* Audit Logs
* Workflow History
* Governance Warnings

---

# Frontend Dashboard

The React dashboard provides an enterprise-style interface for interacting with procurement workflows.

Modules include:

### Dashboard

* Procurement overview
* Workflow metrics
* Governance indicators

### Workflow Runner

* Execute procurement workflows
* Submit procurement request IDs
* View workflow results

### Procurement Requests

* Request management
* Procurement visibility
* Request tracking

### Vendor Analysis

* Vendor risk monitoring
* Risk assessments
* Supplier insights

### Budget Review

* Budget utilization monitoring
* Cost center visibility
* Financial validation

### Audit Logs

* Governance warnings
* Workflow execution history
* Audit trail review

### System Health

* Backend connectivity
* Workflow availability
* Service monitoring

---

# Technology Stack

## Frontend

* React
* Vite
* JavaScript
* CSS
* Axios

## Backend

* Python
* FastAPI
* Uvicorn

## AI Workflow Layer

* LangGraph
* Multi-Agent Orchestration
* Workflow State Management

## Data Layer

* JSON Mock Datasets

## Documentation & Testing

* Swagger/OpenAPI
* Unit Testing

## DevOps & Version Control

* Git
* GitHub
* Virtual Environments

---

# Project Structure

```text
autonomous-procurement-approval-agent/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
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
├── tests/
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/raheshcse/Autonomous-procurement-approval-agent.git
cd Autonomous-procurement-approval-agent
```

---

## Backend Setup

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
cd ai-agents
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend
npm install
```

Run Frontend:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# API Endpoint

## Execute Procurement Workflow

### Request

```http
POST /run-procurement-workflow
```

### Example Request

```json
{
  "request_id": "PR-2026-002"
}
```

---

# Example Workflow Response

```json
{
  "workflow_id": "wf-12345",
  "request_id": "PR-2026-002",
  "vendor_risk": {
    "risk_score": 0.7,
    "risk_level": "high"
  },
  "budget_validation": {
    "budget_available": false,
    "projected_utilization": 1.137
  },
  "approval_decision": {
    "decision": "rejected",
    "approval_confidence": 0.3
  },
  "escalation_status": {
    "result": "escalated"
  }
}
```

---

# Audit Logging

Workflow execution traces are written to:

```text
logs/audit-log.jsonl
```

Recorded information includes:

* Workflow IDs
* Agent Decisions
* Governance Warnings
* Escalation Events
* Confidence Scores
* Execution Timestamps

---

# Testing

Run unit tests:

```bash
python -m unittest discover -s tests
```

---

# Learning Outcomes

Through this project, I gained practical experience with:

* FastAPI backend development
* LangGraph workflow orchestration
* Multi-agent system design
* Agent-to-Agent (A2A) communication
* Workflow state management
* Enterprise governance concepts
* Audit logging strategies
* API development and testing
* Full-stack application integration
* AI-assisted software development

---

# Future Enhancements

* Database integration
* Authentication & authorization
* Role-based access control
* Real-time workflow monitoring
* Workflow analytics dashboards
* Advanced risk models
* Cloud deployment
* Enterprise reporting

---

# Author

**Rahesh Saravanan**

Software Engineer | AI & Full-Stack Developer | Cyber Security Enthusiast

GitHub:
https://github.com/raheshcse

LinkedIn:
https://www.linkedin.com/in/raheshsaravanan/

---

⭐ If you found this project interesting, consider giving it a star.
