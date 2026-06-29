# v4.18.0 Application Architecture Refresh

This document refreshes the application architecture after v4.17.0 Business Process Architecture.

## 1. Architecture Position

The consulting architecture sequence is:

```text
BLM
-> Business Process / Business Architecture
-> Application Architecture
-> Data Architecture
-> Technical Architecture
```

v4.17.0 defined the business processes. v4.18.0 derives application domains and modules from those processes.

## 2. Input from Business Process Architecture

The business process layer requires applications that support:

```text
value-chain diagnosis
manual work step inventory
Agent automation opportunity mapping
automation level classification
policy and authority checks
Agent work request creation
evidence capture
risk classification
approval / revision / escalation
proof file generation
manager / customer reporting
KPI tracking
```

Therefore the application architecture must shift from generic training modules to process-driven governance applications.

## 3. Target Application Domain Map

```text
1. Value Chain Diagnosis Center
2. Automation Opportunity Map
3. Business Process Center
4. Governance Policy Center
5. Authority & Role Center
6. Agent Work Request Center
7. Evidence & Verification Center
8. Risk & Approval Workflow Center
9. Proof File Center
10. Readiness & Capability Center
11. Reporting & Export Center
12. Audit & Compliance Center
13. Client / Cohort / Department Center
14. Service & Commercialization Center
```

## 4. Application Domains

### 4.1 Value Chain Diagnosis Center

Purpose:

```text
Map the client's value chain and identify where manual work, cost, delay, and risk exist.
```

Functions:

```text
value-chain stage setup
manual work step inventory
pain / cost / cycle-time scoring
current owner / role mapping
candidate process selection
baseline KPI entry
consulting diagnosis report
```

Business process supported:

```text
Process Pattern A: Value Chain Automation Diagnosis
```

### 4.2 Automation Opportunity Map

Purpose:

```text
Classify which manual work steps can be automated by AI Agents and at what level.
```

Functions:

```text
R0-R4 automation level classification
Agent automation target definition
business value estimate
time saved estimate
risk / complexity score
pilot shortlist
replacement / automation roadmap
```

Business process supported:

```text
Value-chain opportunity identified -> Business process selected -> Manual work step decomposed -> Automation level assigned
```

### 4.3 Business Process Center

Purpose:

```text
Model end-to-end business processes selected from value-chain opportunities.
```

Functions:

```text
process catalog
process owner assignment
process step definition
manual / Agent / human approval split
process status model
process KPI model
process-to-application mapping
```

Examples:

```text
Lead-to-Proposal Automation
Requirement-to-Delivery Automation
Training-to-Readiness Automation
Support-to-Knowledge Automation
```

### 4.4 Governance Policy Center

Purpose:

```text
Define which Agent outputs may enter formal workflows and under what controls.
```

Functions:

```text
task eligibility policy
value-chain-stage policy
task category policy
restricted input policy
evidence requirement policy
approval rule policy
customer-safe field policy
policy versioning
```

### 4.5 Authority & Role Center

Purpose:

```text
Define who can request, verify, approve, or release Agent work.
```

Functions:

```text
authority level definitions
role-to-authority mapping
allowed automation levels
allowed risk levels
allowed process categories
review requirement
customer-output approval permission
```

### 4.6 Agent Work Request Center

Purpose:

```text
Convert a selected process step into a governed Agent work request.
```

Functions:

```text
business task capture
value-chain stage link
business process link
manual work step link
automation level link
Agent tool selection
Agent task brief
constraints
acceptance criteria
evidence checklist
```

Business process supported:

```text
Process Pattern B: Governed Agent Work Request
```

### 4.7 Evidence & Verification Center

Purpose:

```text
Capture proof that the Agent output was verified and controlled.
```

Functions:

```text
Agent output summary
artifact links
log / screenshot / file evidence
verification checklist
human correction notes
source reference
missing evidence detection
evidence completeness score
```

Business process supported:

```text
Process Pattern C: Agent Work Execution and Evidence Capture
```

### 4.8 Risk & Approval Workflow Center

Purpose:

```text
Prevent uncontrolled Agent output from entering formal workflows.
```

Functions:

```text
risk suggestion
risk classification
approval rule matching
review queue
revision request
rejection decision
escalation path
approval timestamp
decision reason
```

Business process supported:

```text
Process Pattern D: Risk, Approval, and Escalation
```

### 4.9 Proof File Center

Purpose:

```text
Turn approved Agent work into evidence of automation, readiness, and governance.
```

Functions:

```text
proof file generation
proof-ready status
governance summary
automation level summary
customer-safe summary
internal evidence link
reviewer comments
proof export
```

Business process supported:

```text
Process Pattern E: Proof File and Reporting
```

### 4.10 Readiness & Capability Center

Purpose:

```text
Measure whether people, roles, teams, and processes are ready for governed Agent automation.
```

Functions:

```text
learner / employee readiness score
role readiness matrix
cohort readiness dashboard
authority level recommendation
process readiness score
automation capability maturity
readiness trend
```

### 4.11 Reporting & Export Center

Purpose:

```text
Generate manager, customer-safe, internal, consulting, and audit reports.
```

Functions:

```text
value-chain diagnosis report
automation opportunity report
manager readiness report
customer-safe proof report
internal audit report
cohort report
Excel / Markdown / PDF export
field whitelist
report snapshot
export job history
```

### 4.12 Audit & Compliance Center

Purpose:

```text
Retain evidence of policy, authority, risk, approval, proof, and report events.
```

Functions:

```text
audit event list
event detail
actor / role / timestamp
object link
before / after status
reason / summary
evidence reference
export audit log
```

### 4.13 Client / Cohort / Department Center

Purpose:

```text
Manage the organizational boundary for pilots and enterprise rollout.
```

Functions:

```text
client profile
cohort / department setup
employee / learner list
manager / reviewer assignment
scope and package status
client-level reporting boundary
```

### 4.14 Service & Commercialization Center

Purpose:

```text
Convert diagnosis and pilot results into productized service packages and expansion opportunities.
```

Functions:

```text
service package catalog
lead tracking
proposal scope
pilot shortlist
expansion opportunity
renewal recommendation
commercial follow-up
```

## 5. Mapping Current Streamlit Pages to Target Domains

| Current Page | Current Meaning | Target Domain | Required Upgrade |
| --- | --- | --- | --- |
| Clients | client list | Client / Cohort / Department Center | add value-chain diagnosis scope and client process inventory |
| Cohorts | training groups | Client / Cohort / Department + Readiness Center | support department / process pilot groups |
| Learners | learners | Authority & Role + Readiness Center | add authority level, automation readiness, approver path |
| Tasks | task templates | Business Process + Agent Work Request Center | add value-chain stage, process, manual step, automation level |
| Assignments | assigned tasks | Agent Work Request + Evidence Center | add policy, authority, evidence, risk, process link |
| Review Queue | review tasks | Risk & Approval Workflow Center | add approval rule, risk, escalation, decision reason |
| Proof Files | proof output | Proof File Center | add automation level and governance summary |
| Reports | delivery report | Reporting & Export Center | add value-chain, process, automation, readiness report modes |
| Exports | files | Reporting & Export Center | add customer-safe / manager / audit templates |
| Audit | action log | Audit & Compliance Center | add governance event model |
| Leads | commercial leads | Service & Commercialization Center | add diagnosis-to-pilot-to-expansion path |

## 6. MVP Thin Slice

Do not build all domains fully at once. The next MVP should show one complete process slice:

```text
Value Chain Diagnosis
-> Automation Opportunity
-> Governed Agent Work Request
-> Evidence
-> Risk / Approval
-> Proof File
-> Report
-> Audit
```

Minimum fields to show in UI:

```text
value_chain_stage
business_process
manual_work_step
automation_level
Agent automation target
policy
human authority level
evidence required
risk level
approval decision
proof-ready status
business KPI
```

## 7. Suggested Navigation for Production Product

```text
Dashboard
Value Chain
Automation Map
Processes
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

## 8. Suggested Navigation for Streamlit Pilot

Keep the pilot lighter:

```text
Dashboard
Clients
Cohorts
Learners
Tasks
Assignments
Review Queue
Proof Files
Reports
Exports
Audit
```

But update labels and content so that:

```text
Tasks = Process / Agent Work Templates
Assignments = Governed Agent Work Requests
Review Queue = Risk & Approval Queue
Proof Files = Automation + Governance Proof
Reports = Value Chain / Readiness / Customer-safe Reports
```

## 9. Application-to-Data Requirements

Application architecture requires data fields for:

```text
value_chain_stage
business_process_name
manual_work_step
automation_level
Agent automation target
governance_policy_id
authority_level
risk_level
approval_rule
evidence_required
proof_file_id
audit_event_id
business_kpi_link
```

These fields should drive v4.19.0 Data Architecture Refresh.

## 10. Application-to-Technical Requirements

Application architecture requires technical support for:

```text
role-based access control
policy-driven workflow
Agent tool-agnostic integration
evidence artifact storage
append-only audit event logging
customer-safe export templates
report snapshot persistence
future search / retrieval over proof files
```

These requirements should drive v4.20.0 Technical Architecture Refresh.

## 11. One-Line Application Architecture Claim

```text
The application architecture turns value-chain automation opportunities into governed Agent work applications: diagnosis, opportunity mapping, process design, work execution, evidence, approval, proof, reporting, and audit.
```

Chinese:

```text
应用架构把价值链自动化机会转成可运行的 Agent 治理应用：诊断、机会图、流程、任务、证据、审批、证明、报告与审计。
```
