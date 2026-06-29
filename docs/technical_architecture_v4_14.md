# v4.14.0 Technical Architecture

This document defines the MVP and target technical architecture for AI Agent Governance & Readiness OS.

## 1. Architecture Principles

### 1.1 Tool-Agnostic Agent Layer

The system must not bind itself to one Agent tool.

Use generic abstractions:

```text
Agent Provider
Agent Tool
Agent Run Reference
Agent Output Summary
Agent Evidence
```

Supported future tools may include:

```text
Claude Code
Codex
Cursor
Copilot-style agents
custom enterprise agents
workflow agents
```

### 1.2 Policy-Driven Workflow

Workflow behavior should come from policy records:

```text
task eligibility
risk level
approval rule
evidence requirement
customer-safe fields
```

Not from hardcoded UI logic.

### 1.3 Evidence First

Every readiness score and proof file must be grounded in evidence:

```text
task brief
Agent output summary
verification result
risk checklist
approval decision
audit event
```

### 1.4 Customer-Safe Reporting

Reports must support field whitelisting:

```text
internal report
manager report
customer-safe report
audit report
```

## 2. Current MVP Architecture

Current prototype:

```text
Streamlit UI
-> Session DataFrames
-> operation_state
-> Repository Read Layer
-> Reports / Exports
-> Supabase schema contracts
```

Strengths:

```text
fast demo
low deployment friction
business workflow visible
customer-safe export already started
repository read boundary introduced
Supabase schema path defined
```

Limitations:

```text
no real auth / SSO
session data only
no production persistence
limited concurrency
limited workflow automation
no object storage
no production audit immutability
no live Agent integration
```

## 3. Target Architecture

```text
Web Frontend
-> API Backend
-> Workflow / Policy Engine
-> Agent Integration Layer
-> PostgreSQL / Supabase
-> Object Storage
-> Search / Vector Index
-> Audit Event Store
-> Reporting / Export Service
-> Observability
```

## 4. Layered Architecture

### 4.1 Presentation Layer

Options:

```text
Streamlit pilot
Next.js / React production frontend
Enterprise portal / client portal
```

Main UI areas:

```text
Dashboard
Policies
Authority
Agent Work
Evidence
Approvals
Proof Files
Readiness
Reports
Audit
Clients
Leads
```

### 4.2 API Layer

Options:

```text
FastAPI
NestJS
Spring Boot
Supabase Edge Functions
```

Responsibilities:

```text
user session
role checks
repository APIs
workflow actions
report generation requests
Agent run metadata ingestion
```

### 4.3 Workflow / Policy Engine

MVP:

```text
Python state machine
PostgreSQL policy lookup
manual approval actions
```

Production options:

```text
Temporal
Inngest
Camunda / BPMN
custom lightweight workflow engine
```

Core functions:

```text
check task eligibility
check authority level
select evidence requirement
assign risk rule
route approval
record governance event
```

### 4.4 Agent Integration Layer

Purpose:

```text
Record Agent tool usage and outputs without making one Agent vendor the core product dependency.
```

Integration modes:

```text
manual evidence upload
copy/paste Agent transcript summary
GitHub PR / commit link
CLI run metadata
API-based Agent run
enterprise Agent connector
```

Suggested abstraction:

```text
agent_provider
agent_tool
agent_run_id
agent_run_url
input_summary
output_summary
artifact_links
```

### 4.5 Data Layer

MVP:

```text
pandas DataFrames
session state
```

Pilot:

```text
Supabase PostgreSQL
RLS
repository adapter
```

Production:

```text
PostgreSQL
object storage
append-only audit events
report snapshots
search index
```

### 4.6 Object Storage

Used for:

```text
screenshots
logs
PDF reports
Excel exports
Agent transcript files
code diff summaries
proof artifacts
```

Options:

```text
Supabase Storage
S3
MinIO
Cloudflare R2
```

### 4.7 Search / Vector Layer

Used for:

```text
finding similar Agent tasks
risk pattern search
proof file retrieval
policy matching
knowledge base lookup
```

Options:

```text
pgvector
Qdrant
OpenSearch
Postgres full-text search
```

### 4.8 Reporting / Export Service

Output formats:

```text
Markdown
Excel
PDF
customer-safe pack
internal audit pack
manager report
```

Requirements:

```text
field whitelist
sensitive field removal
report snapshot
export job history
versioned templates
```

### 4.9 Audit / Compliance Layer

Audit must capture:

```text
actor
role
object type
object id
action
before status
after status
evidence reference
timestamp
reason / summary
```

Long-term audit should be append-only.

## 5. Deployment Options

### Option A: Demo / Sales Pilot

```text
Streamlit Community Cloud
session data
manual export
```

Best for:

```text
sales demonstration
consulting workshop
small cohort pilot
```

### Option B: Supabase Pilot

```text
Streamlit or React frontend
Supabase Auth
Supabase PostgreSQL
Supabase Storage
repository adapter
```

Best for:

```text
first real client pilot
small multi-user usage
proof file persistence
customer-safe report history
```

### Option C: Production SaaS

```text
React / Next.js frontend
API backend
PostgreSQL
object storage
workflow engine
Agent connectors
observability
audit storage
```

Best for:

```text
multi-client SaaS
enterprise governance
department-level adoption
long-term proof archive
```

## 6. Security Architecture

### 6.1 Access Control

Role model:

```text
Founder
ClientAdmin
Reviewer
Learner / Employee
Auditor
```

Permission examples:

```text
Founder: full tenant access
ClientAdmin: own client reports and customer-safe proof files
Reviewer: assigned evidence and approvals
Learner: own assignments and proof files
Auditor: read-only governance and audit records
```

### 6.2 Data Segmentation

Security boundaries:

```text
tenant_id
client_id
cohort_id / department_id
learner_id
report visibility
```

### 6.3 Sensitive Data Controls

Sensitive fields:

```text
raw Agent transcript
internal repo paths
security-sensitive logs
tokens / keys / credentials
contract value
lead potential value
internal reviewer notes
raw audit object IDs
```

Controls:

```text
field whitelist
report visibility mode
customer-safe export templates
object storage permissions
audit trail
```

## 7. Integration Architecture

Potential integrations:

| Integration | Purpose |
| --- | --- |
| GitHub / GitLab | PR, commit, issue, diff and CI evidence. |
| Jira / Backlog / Redmine | business task and defect source. |
| Slack / Teams / Feishu / WeCom | notifications and approvals. |
| Claude Code / Codex / Cursor | Agent work metadata and output. |
| SSO / OAuth | enterprise identity. |
| Supabase / PostgreSQL | data persistence. |
| S3 / R2 / MinIO | proof artifacts. |

## 8. Technical Roadmap

### v4.14.x Consulting Architecture Pack

```text
BLM
scenario process
application architecture
data architecture
technical architecture
```

### v4.15.x Governance Demo Data

```text
3-4 governed Agent task examples
policy examples
authority level examples
risk / approval examples
proof file examples
```

### v4.16.x Governance UI Slice

```text
Governance Overview
Policy summary
Authority level view
Agent work request fields
risk / approval display
```

### v4.17.x Supabase Pilot

```text
seed governance demo data
read adapter
write adapter for governed assignments
proof file persistence
```

### v4.18.x Reporting Pack

```text
manager governance report
customer-safe governance report
audit export
readiness score report
```

## 9. Technical Risks

| Risk | Mitigation |
| --- | --- |
| Agent vendor lock-in | Keep Agent layer provider-agnostic. |
| Data leakage in reports | Customer-safe whitelist and export templates. |
| Weak audit integrity | Append-only audit event design. |
| Over-complex workflow | Start with lightweight status model. |
| Too much schema normalization early | Use JSONB for early pilot fields. |
| Product becomes generic training | Keep governance, evidence, approval and accountability as core. |

## 10. Target Architecture Summary

```text
The product should become a system of record for AI Agent task policy, authorization, evidence, approval, readiness, proof, and audit.
```

This remains valuable even when Agent tools become more autonomous, because enterprises will still need governance and accountability.
