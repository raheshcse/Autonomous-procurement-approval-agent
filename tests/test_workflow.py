import sys
import unittest
from pathlib import Path


AI_AGENTS_DIR = Path(__file__).resolve().parents[1] / "ai-agents"
sys.path.insert(0, str(AI_AGENTS_DIR))

from fastapi.testclient import TestClient  # noqa: E402

from main import _build_initial_state, app  # noqa: E402
from workflow import procurement_workflow  # noqa: E402


class WorkflowSmokeTest(unittest.TestCase):
    def test_workflow_returns_required_sections(self):
        result = procurement_workflow.invoke(_build_initial_state("PR-2026-002"))

        self.assertIn(result["vendor_risk"]["risk_level"], {"low", "medium", "high"})
        self.assertIn("budget_available", result["budget_status"])
        self.assertIn(result["approval_decision"]["decision"], {"approved", "rejected", "needs_review"})
        self.assertIn("escalation_required", result["escalation_result"])
        self.assertTrue(result["governance_warnings"])
        self.assertTrue(result["confidence_scores"])
        self.assertEqual(len(result["audit_trail"]), 5)

    def test_fastapi_endpoints_return_expected_contract(self):
        client = TestClient(app)

        self.assertEqual(client.get("/").status_code, 200)
        self.assertEqual(client.get("/health").json()["status"], "healthy")

        response = client.post("/run-procurement-workflow", json={"request_id": "PR-2026-002"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertTrue(payload["workflow_id"].startswith("wf-"))
        self.assertIn("vendor_risk", payload)
        self.assertIn("budget_validation", payload)
        self.assertIn("approval_decision", payload)
        self.assertIn("escalation_status", payload)
        self.assertTrue(payload["governance_warnings"])
        self.assertEqual(len(payload["audit_trail"]), 5)


if __name__ == "__main__":
    unittest.main()
