# v4.17.0 Business Process Architecture

This document converts BLM value-chain analysis into executable business process architecture for AI Agent Governance & Readiness OS.

## 1. Architecture Position

The consulting architecture sequence remains:

```text
BLM
-> Business Process / Business Architecture
-> Application Architecture
-> Data Architecture
-> Technical Architecture
```

Value chain analysis is inside BLM. This document starts after BLM and answers:

```text
Which business processes should be transformed based on the value-chain opportunities identified in BLM?
```

## 2. Input from BLM

BLM provides:

```text
market insight
strategic intent
value-chain stages
manual work step inventory
AI Agent automation opportunities
value-chain KPI direction
business design
```

Business process architecture converts those into:

```text
end-to-end process flows
roles and responsibilities
Agent automation points
governance controls
evidence requirements
approval paths
process KPIs
application requirements
```

## 3. Business Process Design Principle

The process architecture must show two things at the same time:

```text
1. Which repeatable human work steps are automated by AI Agents.
2. Which authority, evidence, risk, and approval steps remain controlled by humans or the organization.
```

Core rule:

```text
AI Agent performs automatable work.
The enterprise controls eligibility, authority, evidence, risk, approval, and accountability.
```

## 4. End-to-End Reference Process

```text
Value-chain opportunity identified
-> Business process selected
-> Manual work step decomposed
-> Automation level assigned
-> Agent eligibility checked
-> Human authority checked
-> Agent work request created
-> Agent performs automatable step
-> Evidence captured
-> System / Agent pre-check performed
-> Human verifies exceptions and risk
-> Approval / revision / escalation decision made
-> Proof File generated
-> Audit event retained
-> Manager / customer report produced
-> KPI updated
```

## 5. Process Roles

| Role | Responsibility |
| --- | --- |
| Business Owner | Defines value-chain pain point and accepts business outcome. |
| Process Owner | Owns the target process and approves process changes. |
| Agent Operator | Creates Agent work request and submits evidence. |
| Reviewer | Checks evidence, risk, and output quality. |
| Approver | Approves customer-facing, high-risk, or workflow-impacting results. |
| Auditor | Reviews policy, evidence, and decision history. |
| Agent Tool | Performs automatable work but does not own accountability. |

## 6. Process Pattern A: Value Chain Automation Diagnosis

### Purpose

Identify where AI Agent automation creates measurable business value.

### Flow

```text
Client value-chain interview
-> value-chain stage list
-> manual work step inventory
-> pain / cost / cycle-time assessment
-> automation opportunity scoring
-> R0-R4 automation level classification
-> governance requirement mapping
-> pilot candidate selection
-> KPI baseline
-> roadmap report
```

### Agent Automation Points

```text
interview note summary
manual work step extraction
initial opportunity clustering
KPI draft
roadmap draft
```

### Human Retained Responsibility

```text
client context judgment
priority decision
risk appetite
pilot selection
commercial scope
```

### Outputs

```text
value-chain map
manual work inventory
automation opportunity map
R0-R4 classification
pilot shortlist
KPI baseline
consulting report
```

## 7. Process Pattern B: Governed Agent Work Request

### Purpose

Convert a business task into a controlled Agent work request.

### Flow

```text
business task created
-> task category selected
-> value-chain stage linked
-> automation level assigned
-> policy matched
-> authority level checked
-> task brief drafted
-> constraints and acceptance criteria added
-> evidence requirement generated
-> Agent work request approved for execution
```

### Agent Automation Points

```text
task category suggestion
task brief draft
constraint suggestion
evidence checklist draft
acceptance criteria draft
```

### Human Retained Responsibility

```text
business intent
scope boundary
policy exception
final task brief approval
```

### Outputs

```text
Agent work request
policy match
authority check result
evidence checklist
approval rule
```

## 8. Process Pattern C: Agent Work Execution and Evidence Capture

### Purpose

Execute the automatable step while capturing proof.

### Flow

```text
Agent work request opened
-> Agent tool selected
-> Agent performs work step
-> output summary captured
-> artifacts linked
-> verification checklist completed
-> human correction notes added
-> evidence completeness checked
-> submission created
```

### Agent Automation Points

```text
draft output
artifact summary
first-pass checklist
report draft
```

### Human Retained Responsibility

```text
source quality
output relevance
correction decision
missing evidence judgment
```

### Outputs

```text
Agent output summary
verification evidence
human correction notes
artifact links
submission record
```

## 9. Process Pattern D: Risk, Approval, and Escalation

### Purpose

Prevent uncontrolled Agent outputs from entering formal workflows.

### Flow

```text
submission received
-> risk level suggested
-> reviewer checks evidence
-> policy approval rule applied
-> decision made: approve / revise / reject / escalate
-> escalation path triggered if needed
-> audit event written
```

### Agent Automation Points

```text
risk level suggestion
missing evidence detection
approval route suggestion
review comment draft
```

### Human Retained Responsibility

```text
final risk classification
approval decision
customer-facing release
security / compliance escalation
```

### Outputs

```text
risk classification
approval decision
revision request
escalation record
audit event
```

## 10. Process Pattern E: Proof File and Reporting

### Purpose

Turn accepted Agent work into evidence of value-chain automation and readiness.

### Flow

```text
approved Agent work item
-> proof file generated
-> governance summary added
-> customer-safe fields selected
-> manager report drafted
-> customer-safe report drafted if allowed
-> export job recorded
-> KPI updated
```

### Agent Automation Points

```text
proof file draft
manager report draft
customer-safe summary draft
KPI summary draft
```

### Human Retained Responsibility

```text
customer-safe field decision
final report approval
commercial interpretation
manager recommendation
```

### Outputs

```text
Proof File
manager report
customer-safe report
export record
KPI update
```

## 11. End-to-End Process 1: Lead-to-Proposal Automation

### Value Chain Stage

```text
Market / Lead -> Customer Need -> Solution / Proposal
```

### Flow

```text
lead captured
-> Agent summarizes customer profile
-> human verifies buying context
-> Agent drafts need summary
-> human confirms pain points
-> Agent drafts proposal outline
-> policy checks claim and price boundary
-> approver validates scope
-> customer-safe proposal summary generated
-> follow-up action recorded
```

### Business Value

```text
faster pre-sales response
better lead qualification
less proposal drafting time
lower overpromise risk
```

## 12. End-to-End Process 2: Requirement-to-Delivery Automation

### Value Chain Stage

```text
Customer Need -> Delivery / Execution -> Quality / Acceptance
```

### Flow

```text
requirement or bug report received
-> Agent summarizes requirement
-> human confirms business meaning
-> Agent identifies candidate files / tasks
-> human checks touched scope
-> Agent drafts code / test / report
-> verification evidence captured
-> risk classified
-> reviewer approves or requests revision
-> Proof File generated
-> customer-safe delivery report produced
```

### Business Value

```text
less manual coding / testing / reporting labor
faster acceptance cycle
clearer delivery evidence
controlled customer-facing output
```

## 13. End-to-End Process 3: Training-to-Readiness Automation

### Value Chain Stage

```text
HR / Training -> Readiness Decision -> Manager Report
```

### Flow

```text
role requirement defined
-> Agent drafts training task
-> instructor validates task
-> learner completes governed Agent work
-> Agent performs first-pass rubric scoring
-> reviewer verifies evidence and fairness
-> readiness level assigned
-> Proof File generated
-> manager report produced
-> next training path recommended
```

### Business Value

```text
scalable review process
evidence-based readiness
lower instructor reporting workload
clearer manager decision
```

## 14. End-to-End Process 4: Support-to-Knowledge Automation

### Value Chain Stage

```text
Customer Success / Support -> Knowledge Management
```

### Flow

```text
customer question received
-> Agent summarizes issue
-> Agent drafts response and KB update
-> human verifies facts and customer context
-> risk classified
-> customer-safe response approved
-> support proof record generated
-> KB draft submitted for review
```

### Business Value

```text
faster support response
lower repeated support cost
better knowledge capture
controlled customer communication
```

## 15. Process KPI Model

| KPI | Process Use |
| --- | --- |
| Process Automation Coverage | How many process steps have Agent automation target. |
| Time Saved Estimate | Estimated manual hours saved per process. |
| Evidence Completeness Rate | Whether automated work has enough proof. |
| Approval Cycle Time | Time from Agent output to approval / revision. |
| Exception Rate | Percentage needing human escalation. |
| Customer-Safe Output Rate | Percentage safely shareable externally. |
| Proof File Ready Rate | Percentage converted into accepted proof. |
| Readiness Conversion Rate | Employee movement across authority levels. |
| Value Chain Impact | Which value-chain stage receives measurable improvement. |

## 16. Application Architecture Requirements Derived from Process

Business process architecture requires these application modules:

```text
Value Chain Diagnosis Center
Automation Opportunity Map
Governance Policy Center
Authority & Role Center
Agent Work Request Center
Evidence & Verification Center
Risk Classification Center
Approval Workflow Center
Proof File Center
Readiness Score Center
Reporting & Export Center
Audit & Compliance Center
```

## 17. Data Architecture Requirements Derived from Process

The process requires data fields for:

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

## 18. One-Line Business Process Claim

```text
The system converts BLM value-chain opportunities into governed AI Agent business processes with evidence, approval, proof, audit, and KPI tracking.
```

Chinese:

```text
系统把 BLM 中识别出的价值链自动化机会，转化为带证据、审批、证明、审计和 KPI 的 AI Agent 业务流程。
```
