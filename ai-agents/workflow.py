"""LangGraph workflow orchestration.

The graph is intentionally linear for the first version:
START -> VendorRiskAgent -> BudgetValidationAgent -> ApprovalDecisionAgent
-> EscalationAgent -> AuditLoggerAgent -> END.
"""

from langgraph.graph import END, START, StateGraph

from agents import get_agents
from state import ProcurementState


def build_procurement_graph():
    agents = get_agents()
    graph = StateGraph(ProcurementState)

    # Each node mutates the shared state with its decision, confidence, and
    # audit event. LangGraph provides the orchestration boundary between agents.
    graph.add_node("VendorRiskAgent", agents["vendor_risk"])
    graph.add_node("BudgetValidationAgent", agents["budget_validation"])
    graph.add_node("ApprovalDecisionAgent", agents["approval_decision"])
    graph.add_node("EscalationAgent", agents["escalation"])
    graph.add_node("AuditLoggerAgent", agents["audit_logger"])

    graph.add_edge(START, "VendorRiskAgent")
    graph.add_edge("VendorRiskAgent", "BudgetValidationAgent")
    graph.add_edge("BudgetValidationAgent", "ApprovalDecisionAgent")
    graph.add_edge("ApprovalDecisionAgent", "EscalationAgent")
    graph.add_edge("EscalationAgent", "AuditLoggerAgent")
    graph.add_edge("AuditLoggerAgent", END)

    return graph.compile()


procurement_workflow = build_procurement_graph()
