import { useState } from "react";
import axios from "axios";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  CheckCircle,
  ClipboardList,
  Database,
  FileText,
  Gauge,
  GitBranch,
  LayoutDashboard,
  PlayCircle,
  Server,
  ShieldAlert,
  ShieldCheck,
  Wallet,
} from "lucide-react";
import "./App.css";

const procurementRequests = [
  {
    id: "PR-2026-001",
    vendor: "Northstar Cloud Services",
    department: "IT Operations",
    amount: "$84,500",
    risk: "Low",
    status: "Ready",
  },
  {
    id: "PR-2026-002",
    vendor: "Apex Industrial Components",
    department: "Manufacturing",
    amount: "$275,000",
    risk: "High",
    status: "Review Required",
  },
  {
    id: "PR-2026-003",
    vendor: "ClearLedger Advisory",
    department: "Finance Transformation",
    amount: "$42,000",
    risk: "Low",
    status: "Ready",
  },
  {
    id: "PR-2026-004",
    vendor: "Greyline Access Systems",
    department: "Security",
    amount: "$132,000",
    risk: "High",
    status: "Escalated",
  },
];

function Badge({ value }) {
  return (
    <span className={`badge badge-${String(value || "pending").toLowerCase().replaceAll(" ", "-")}`}>
      {value || "Pending"}
    </span>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState("Dashboard");
  const [requestId, setRequestId] = useState("PR-2026-002");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runWorkflow = async () => {
    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/run-procurement-workflow",
        { request_id: requestId }
      );

      setResult(response.data);
    } catch {
      setResult({
        error: "Failed to run procurement workflow. Please check backend server.",
      });
    } finally {
      setLoading(false);
    }
  };

  const navItems = [
    ["Dashboard", LayoutDashboard],
    ["Workflow Runner", PlayCircle],
    ["Procurement Requests", ClipboardList],
    ["Vendor Analysis", ShieldAlert],
    ["Budget Review", Wallet],
    ["Audit Logs", FileText],
    ["System Health", Server],
  ];

  const hasResult = result && !result.error;
  const decision = result?.approval_decision?.decision || "pending";
  const decisionLabel = decision.replace("_", " ");
  const approvalConfidence = result?.approval_decision?.approval_confidence;
  const riskScore = result?.vendor_risk?.risk_score || 0;
  const riskPercent = Math.round(riskScore * 100);
  const budgetUtilization = result?.budget_validation?.projected_utilization || 0;
  const budgetPercent = Math.round(budgetUtilization * 100);
  const warningCount = result?.governance_warnings?.length || 0;
  const escalation = result?.escalation_status || result?.escalation_result;
  const auditTrail = result?.audit_trail || [];

  const PageHeader = ({ label, title, text }) => (
    <section className="page-header">
      <div>
        <p className="eyebrow">{label}</p>
        <h2>{title}</h2>
        <p>{text}</p>
      </div>
      <div className="health-pill">
        <span />
        {hasResult ? "Workflow data available" : "Ready"}
      </div>
    </section>
  );

  const EmptyState = ({ title, text }) => (
    <section className="empty-state">
      <BarChart3 size={28} />
      <div>
        <h3>{title}</h3>
        <p>{text}</p>
      </div>
    </section>
  );

  const MetricCards = () => (
    <section className="metric-grid">
      <article className={`metric-card decision-${decision}`}>
        <div className="metric-top">
          <CheckCircle size={22} />
          <span>Decision</span>
        </div>
        <strong>{decisionLabel}</strong>
        <p>{approvalConfidence ? `${Math.round(approvalConfidence * 100)}% confidence` : "Awaiting workflow"}</p>
      </article>

      <article className="metric-card">
        <div className="metric-top">
          <ShieldAlert size={22} />
          <span>Vendor Risk</span>
        </div>
        <strong>{riskPercent}%</strong>
        <p>{result?.vendor_risk?.risk_level || "No risk data yet"}</p>
      </article>

      <article className="metric-card">
        <div className="metric-top">
          <Gauge size={22} />
          <span>Budget Utilization</span>
        </div>
        <strong>{budgetPercent}%</strong>
        <p>{hasResult ? "Projected utilization" : "Awaiting validation"}</p>
      </article>

      <article className="metric-card">
        <div className="metric-top">
          <AlertTriangle size={22} />
          <span>Governance Warnings</span>
        </div>
        <strong>{warningCount}</strong>
        <p>{warningCount ? "Review required" : "No warnings surfaced"}</p>
      </article>
    </section>
  );

  const WorkflowRunner = () => (
    <>
      <PageHeader
        label="Workflow Runner"
        title="Run Procurement Workflow"
        text="Enter a procurement request ID and execute the multi-agent approval workflow."
      />
      <section className="runner-toolbar panel">
        <div>
          <label htmlFor="request-id">Procurement Request ID</label>
          <input
            id="request-id"
            value={requestId}
            onChange={(event) => setRequestId(event.target.value)}
            placeholder="PR-2026-002"
          />
        </div>
        <button onClick={runWorkflow} disabled={loading}>
          <PlayCircle size={18} />
          {loading ? "Running" : "Run Procurement Workflow"}
        </button>
      </section>
      {result?.error && <div className="error-card">{result.error}</div>}
      {hasResult ? <WorkflowResults /> : <EmptyState title="No workflow result yet" text="Run a procurement workflow to display approval, risk, budget, escalation, warnings, timeline, and raw response." />}
    </>
  );

  const DecisionSummary = () => (
    <article className="panel decision-panel">
      <div className="section-title">
        <CheckCircle size={20} />
        <h3>Decision Summary</h3>
      </div>
      <Badge value={decisionLabel} />
      <p>{result.approval_decision?.reason}</p>
      <div className="detail-grid">
        <div>
          <span>Workflow ID</span>
          <strong>{result.workflow_id}</strong>
        </div>
        <div>
          <span>Request ID</span>
          <strong>{result.request_id}</strong>
        </div>
        <div>
          <span>Approval Confidence</span>
          <strong>{approvalConfidence}</strong>
        </div>
      </div>
    </article>
  );

  const VendorRiskAnalysis = () => (
    <article className="panel">
      <div className="section-title">
        <ShieldAlert size={20} />
        <h3>Vendor Risk Analysis</h3>
      </div>
      {hasResult ? (
        <>
          <div className="score-row">
            <div>
              <span>Risk Score</span>
              <strong>{riskPercent}%</strong>
            </div>
            <Badge value={result.vendor_risk?.risk_level} />
          </div>
          <div className="progress">
            <span style={{ width: `${riskPercent}%` }} />
          </div>
          <div className="detail-grid two">
            <div>
              <span>Vendor ID</span>
              <strong>{result.vendor_risk?.vendor_id}</strong>
            </div>
            <div>
              <span>Risk Level</span>
              <strong>{result.vendor_risk?.risk_level}</strong>
            </div>
          </div>
        </>
      ) : (
        <p>Run a workflow to populate vendor risk data.</p>
      )}
    </article>
  );

  const BudgetValidation = () => (
    <article className="panel">
      <div className="section-title">
        <Wallet size={20} />
        <h3>Budget Validation</h3>
      </div>
      {hasResult ? (
        <>
          <div className="score-row">
            <div>
              <span>Projected Utilization</span>
              <strong>{budgetPercent}%</strong>
            </div>
            <Badge value={result.budget_validation?.budget_available ? "Budget Available" : "Over Budget"} />
          </div>
          <div className="progress budget">
            <span style={{ width: `${Math.min(budgetPercent, 100)}%` }} />
          </div>
          <div className="detail-grid two">
            <div>
              <span>Cost Center</span>
              <strong>{result.budget_validation?.cost_center}</strong>
            </div>
            <div>
              <span>Projected Remaining</span>
              <strong>{result.budget_validation?.projected_remaining}</strong>
            </div>
          </div>
        </>
      ) : (
        <p>Run a workflow to populate budget validation data.</p>
      )}
    </article>
  );

  const EscalationStatus = () => (
    <article className="panel">
      <div className="section-title">
        <Activity size={20} />
        <h3>Escalation Status</h3>
      </div>
      {hasResult ? (
        <>
          <Badge value={escalation?.result || "Not Required"} />
          <p>{escalation?.reason || "No escalation reason returned."}</p>
          <div className="detail-grid two">
            <div>
              <span>Escalation Required</span>
              <strong>{String(escalation?.escalation_required)}</strong>
            </div>
            <div>
              <span>Assigned To</span>
              <strong>{escalation?.assigned_to || "None"}</strong>
            </div>
          </div>
        </>
      ) : (
        <p>Run a workflow to populate escalation status.</p>
      )}
    </article>
  );

  const GovernanceWarnings = () => (
    <article className="panel warnings-panel">
      <div className="section-title">
        <AlertTriangle size={20} />
        <h3>Governance Warnings</h3>
      </div>
      {result?.governance_warnings?.length ? (
        <div className="warning-list">
          {result.governance_warnings.map((warning, index) => (
            <div className="warning-item" key={`${warning}-${index}`}>
              <AlertTriangle size={16} />
              <span>{warning}</span>
            </div>
          ))}
        </div>
      ) : (
        <p>No governance warnings available.</p>
      )}
    </article>
  );

  const AgentTimeline = () => (
    <article className="panel">
      <div className="section-title">
        <GitBranch size={20} />
        <h3>Agent Workflow Timeline</h3>
      </div>
      {auditTrail.length ? (
        <div className="timeline">
          {auditTrail.map((event, index) => (
            <div className="timeline-item" key={`${event.agent}-${index}`}>
              <div className="timeline-dot">
                <CheckCircle size={14} />
              </div>
              <div>
                <h4>{event.agent}</h4>
                <p>{event.reason}</p>
                <span>{event.confidence} confidence</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>No workflow timeline available.</p>
      )}
    </article>
  );

  const RawApiResponse = () => (
    <article className="panel json-panel">
      <div className="section-title">
        <Database size={20} />
        <h3>Raw API Response</h3>
      </div>
      {hasResult ? <pre>{JSON.stringify(result, null, 2)}</pre> : <p>No API response available.</p>}
    </article>
  );

  const WorkflowResults = () => (
    <section className="result-stack">
      <MetricCards />
      <section className="content-grid">
        <DecisionSummary />
        <VendorRiskAnalysis />
        <BudgetValidation />
      </section>
      <section className="wide-grid">
        <EscalationStatus />
        <GovernanceWarnings />
      </section>
      <section className="wide-grid">
        <AgentTimeline />
        <RawApiResponse />
      </section>
    </section>
  );

  const Dashboard = () => (
    <>
      <PageHeader
        label="Dashboard"
        title="Autonomous Procurement Approval Agent"
        text="Enterprise AI procurement governance dashboard powered by FastAPI, LangGraph, and multi-agent workflow orchestration."
      />
      {hasResult ? <WorkflowResults /> : (
        <>
          <MetricCards />
          <EmptyState title="No workflow data yet" text="Run a procurement workflow to populate the dashboard with approval, vendor, budget, warning, and audit details." />
        </>
      )}
    </>
  );

  const ProcurementRequests = () => (
    <>
      <PageHeader
        label="Procurement Requests"
        title="Procurement Request Queue"
        text="Review mock procurement requests available for workflow evaluation."
      />
      <section className="panel table-panel">
        <table>
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Vendor</th>
              <th>Department</th>
              <th>Amount</th>
              <th>Risk</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {procurementRequests.map((request) => (
              <tr key={request.id}>
                <td>{request.id}</td>
                <td>{request.vendor}</td>
                <td>{request.department}</td>
                <td>{request.amount}</td>
                <td><Badge value={request.risk} /></td>
                <td><Badge value={request.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );

  const VendorAnalysis = () => (
    <>
      <PageHeader label="Vendor Analysis" title="Vendor Risk Analysis" text="Latest vendor risk data returned by the procurement workflow." />
      <VendorRiskAnalysis />
    </>
  );

  const BudgetReview = () => (
    <>
      <PageHeader label="Budget Review" title="Budget Review" text="Latest budget validation data returned by the procurement workflow." />
      <BudgetValidation />
    </>
  );

  const AuditLogs = () => (
    <>
      <PageHeader label="Audit Logs" title="Audit Logs" text="Governance warnings and raw API response from the latest workflow run." />
      <section className="wide-grid">
        <GovernanceWarnings />
        <RawApiResponse />
      </section>
    </>
  );

  const SystemHealth = () => (
    <>
      <PageHeader label="System Health" title="System Health" text="Frontend status, backend workflow availability, and configured API endpoint." />
      <section className="health-grid">
        <article className="panel">
          <span>Frontend</span>
          <strong>Active</strong>
        </article>
        <article className="panel">
          <span>Backend</span>
          <strong>{hasResult ? "Connected" : "Awaiting Workflow Run"}</strong>
        </article>
        <article className="panel">
          <span>API Endpoint</span>
          <strong>Configured</strong>
          <p>http://127.0.0.1:8000/run-procurement-workflow</p>
        </article>
      </section>
    </>
  );

  const renderTab = () => {
    if (activeTab === "Workflow Runner") return <WorkflowRunner />;
    if (activeTab === "Procurement Requests") return <ProcurementRequests />;
    if (activeTab === "Vendor Analysis") return <VendorAnalysis />;
    if (activeTab === "Budget Review") return <BudgetReview />;
    if (activeTab === "Audit Logs") return <AuditLogs />;
    if (activeTab === "System Health") return <SystemHealth />;
    return <Dashboard />;
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <ShieldCheck size={22} />
          </div>
          <div>
            <p>Enterprise AI</p>
            <h1>Procurement Agent</h1>
          </div>
        </div>

        <nav className="nav-list" aria-label="Dashboard navigation">
          {navItems.map(([label, Icon]) => (
            <button
              className={activeTab === label ? "active" : ""}
              key={label}
              onClick={() => setActiveTab(label)}
              type="button"
            >
              <Icon size={18} />
              <span>{label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-status">
          <Activity size={18} />
          <span>Workflow engine ready</span>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <p>Autonomous Procurement Approval Agent</p>
            <h2>Enterprise Procurement Governance</h2>
          </div>
          <div className="topbar-badge">
            <span />
            {hasResult ? "Latest workflow loaded" : "Ready"}
          </div>
        </header>

        <section className="page-content">
          {renderTab()}
        </section>
      </main>
    </div>
  );
}

export default App;
