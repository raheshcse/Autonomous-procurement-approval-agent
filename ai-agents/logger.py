"""Audit logging helpers.

Logs are written as JSON Lines so they are easy to inspect locally and easy to
ship into enterprise observability tools later.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from config import AUDIT_LOG_FILE, LOG_DIR
from state import AuditEvent


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_audit_event(
    *,
    agent: str,
    action: str,
    decision: str,
    reason: str,
    confidence: float,
    governance_warnings: list[str] | None = None,
) -> AuditEvent:
    return {
        "timestamp": utc_now(),
        "agent": agent,
        "action": action,
        "decision": decision,
        "reason": reason,
        "confidence": round(confidence, 3),
        "governance_warnings": governance_warnings or [],
    }


def append_audit_log(record: dict[str, Any]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(record, sort_keys=True) + "\n")
