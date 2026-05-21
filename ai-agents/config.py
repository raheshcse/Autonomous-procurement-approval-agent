"""Configuration for the Autonomous Procurement Approval Agent.

The values are intentionally simple and visible so X-VERBA testers can tune
thresholds and observe governance drift without digging through hidden logic.
"""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "mock-data"
LOG_DIR = BASE_DIR / "logs"

PROCUREMENT_REQUESTS_FILE = DATA_DIR / "procurement-requests.json"
VENDORS_FILE = DATA_DIR / "vendors.json"
BUDGET_FILE = DATA_DIR / "budget-data.json"
APPROVAL_HISTORY_FILE = DATA_DIR / "approval-history.json"
AUDIT_LOG_FILE = LOG_DIR / "audit-log.jsonl"


# Governance thresholds used by the agents.
DEFAULT_APPROVAL_THRESHOLD = 0.76
HIGH_VALUE_THRESHOLD = 100_000
CRITICAL_VALUE_THRESHOLD = 250_000
MAX_VENDOR_RISK_FOR_AUTO_APPROVAL = 0.62
MAX_BUDGET_UTILIZATION_FOR_AUTO_APPROVAL = 0.90


# X-VERBA drift concepts tracked in the audit response.
DRIFT_CODES = {
    "DC-I1": "confidence divergence",
    "DC-I2": "silent degradation",
    "DC-S2": "unstable thresholds",
    "DC-S4": "loop divergence",
    "DC-T1": "tool autonomy drift",
}
