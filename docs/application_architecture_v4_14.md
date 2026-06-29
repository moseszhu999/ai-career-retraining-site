# v4.14.0 Application Architecture

This document defines the application architecture for AI Agent Governance & Readiness OS.

## 1. Application Architecture Goal

The system should not be treated as a training app only. It should be treated as a governance operations platform.

Core application objective:

```text
Provide configurable applications for policy, authority, Agent work requests, evidence, risk, approval, proof files, reports, and audit.
```

## 2. Application Domains

```text
1. Governance Policy Center
2. Authority & Role Center
3. Agent Work Request Center
4. Evidence & Verification Center
5. Risk Classification Center
6. Approval Workflow Center
7. Proof File Center
8. Readiness Score Center
9. Reporting & Export Center
10. Audit & Compliance Center
11. Client / Cohort / Department Center
12. Service / Commercialization Center
```

## 3. Application Domain Details

### 3.1 Governance Policy Center

Purpose:

```text
Configure which tasks may use AI Agent, what evidence is required, and which approval rules apply.
```

Main functions:

```text
policy list
policy detail
create / edit policy
task category mapping
restricted inputs
customer-safe fields
evidence requirements
approval rule templates
```

### 3.2 Authority & Role Center

Purpose:

```text
Manage employee authority levels for AI Agent work.
```

Main functions:

```text
authority level definitions
role-to-authority mapping
learner / employee readiness level
allowed risk levels
allowed task categories
approval capability
review requirement
```

### 3.3 Agent Work Request Center

Purpose:

```text
Turn real business tasks into governed Agent work requests.
```

Main functions:

```text
create Agent work request
select task category
select Agent tool
write task brief
add business context
set constraints
link policy
link assignee
track request status
```

### 3.4 Evidence & Verification Center

Purpose:

```text
Capture and review proof that Agent work was verified.
```

Main functions:

```text
Agent output summary
file / screenshot / log evidence
verification checklist
human correction notes
test result
source reference
completeness check
```

### 3.5 Risk Classification Center

Purpose:

```text
Classify risk before Agent output enters internal or customer-facing workflows.
```

Main functions:

```text
risk level assignment
risk checklist
policy-based risk hints
security / privacy / compliance flags
customer impact flags
revision recommendations
```

### 3.6 Approval Workflow Center

Purpose:

```text
Approve, reject, revise, escalate, or block Agent outputs.
```

Main functions:

```text
review queue
approval decision
revision request
escalation path
approver assignment
decision reason
approval timestamp
```

### 3.7 Proof File Center

Purpose:

```text
Package accepted Agent work into readiness and governance proof.
```

Main functions:

```text
proof file generation
proof status
proof-ready scoring
governance summary
customer-safe summary
internal evidence link
export options
```

### 3.8 Readiness Score Center

Purpose:

```text
Measure whether employees, cohorts, departments, or roles are ready for governed Agent work.
```

Main functions:

```text
readiness scorecard
authority level recommendation
risk classification accuracy
evidence completeness rate
approval quality
proof-ready rate
manager recommendation
```

### 3.9 Reporting & Export Center

Purpose:

```text
Produce internal, manager, customer-safe, and audit-oriented reports.
```

Main functions:

```text
customer-safe delivery pack
manager readiness report
internal audit report
cohort report
Proof File export
Excel / Markdown / PDF export
field whitelist
sensitive data removal
```

### 3.10 Audit & Compliance Center

Purpose:

```text
Record an append-only history of policy, task, evidence, risk, approval, and proof events.
```

Main functions:

```text
audit event list
audit event detail
before / after status
actor / role
timestamp
object link
evidence hash / reference
export audit log
```

### 3.11 Client / Cohort / Department Center

Purpose:

```text
Manage client organizations, cohorts, departments, employees, and training groups.
```

Main functions:

```text
client profile
cohort / department setup
employee / learner list
trainer / manager assignment
contract / package status
client scope filtering
```

### 3.12 Service / Commercialization Center

Purpose:

```text
Convert governance pilots into productized service packages and follow-up leads.
```

Main functions:

```text
service package catalog
lead tracking
follow-up status
proposal package
scope and price boundary
renewal / expansion opportunity
```

## 4. Mapping Current Streamlit Pages to Target Application Domains

| Current Page | Target Application Domain | Gap |
| --- | --- | --- |
| Clients | Client / Cohort / Department Center | Needs governance scope and department-level setup. |
| Cohorts | Client / Cohort / Department Center + Readiness Score Center | Needs readiness progression and authority levels. |
| Learners | Authority & Role Center + Readiness Score Center | Needs Agent authority level and role-readiness view. |
| Tasks | Agent Work Request Center + Governance Policy Center | Needs policy, task category, evidence requirements. |
| Assignments | Agent Work Request Center + Evidence Center | Needs eligibility, authority, risk, approval fields. |
| Review Queue | Approval Workflow Center | Needs approval rules, escalation, and reason codes. |
| Proof Files | Proof File Center | Needs governance summary and customer-safe proof pack. |
| Reports | Reporting & Export Center | Needs manager / governance / customer-safe report modes. |
| Exports | Reporting & Export Center | Needs stronger field whitelist and report templates. |
| Audit | Audit & Compliance Center | Needs append-only governance event view. |
| Leads | Service / Commercialization Center | Needs governance package and expansion path. |

## 5. MVP Application Scope

For the next MVP, do not build all modules fully. Build a thin vertical slice:

```text
Policy summary
Authority level display
Agent Work Assignment demo
Evidence checklist
Risk level
Approval decision
Proof File
governance report
```

Minimum screens:

```text
1. Governance Overview
2. Agent Work Requests
3. Review / Approval Queue
4. Proof Files
5. Governance Report / Export
6. Audit Log
```

## 6. Target Application Flow

```text
Policy Center defines rules
-> Authority Center defines who can do what
-> Agent Work Request Center creates governed tasks
-> Evidence Center captures proof
-> Risk Center classifies risk
-> Approval Center decides
-> Proof File Center packages outcome
-> Reporting Center exports summary
-> Audit Center records everything
```

## 7. Permission Model

| Role | Application Access |
| --- | --- |
| Founder | Full policy, authority, review, proof, report, audit. |
| ClientAdmin | Own client reports, department readiness, customer-safe proof files. |
| Reviewer | Review queue, evidence check, readiness scoring. |
| Learner / Employee | Assigned work requests, own evidence, own proof files. |
| Auditor | Read-only audit, policy, approval and report history. |

## 8. Application Design Principles

### 8.1 Tool-Agnostic Agent Layer

Do not bind the application to Claude Code, Codex, Cursor, or any single tool.

Use generic fields:

```text
agent_provider
agent_tool
agent_run_reference
agent_output_summary
```

### 8.2 Policy-Driven Workflow

Approval and evidence requirements must come from policy configuration, not hardcoded UI logic.

### 8.3 Customer-Safe by Default

Every report/export should explicitly choose:

```text
internal
manager
customer-safe
audit
```

### 8.4 Evidence Before Score

Readiness scores should not be free-text opinions. They should be calculated from evidence, decisions, and proof-ready outcomes.

## 9. Future Product UI Navigation

Suggested navigation:

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

For the current Streamlit prototype, this can be simplified to:

```text
Governance
Tasks
Assignments
Review Queue
Proof Files
Reports
Exports
Audit
```
