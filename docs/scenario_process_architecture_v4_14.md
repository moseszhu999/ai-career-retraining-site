# v4.14.0 Scenario Process Architecture

This document translates the BLM strategy into concrete business scenarios and process flows.

## 1. Universal Governance Process

All verticals share the same core process:

```text
Business Task Created
-> Agent Eligibility Check
-> Human Authority Check
-> Agent Work Request Created
-> Agent Output Produced
-> Verification Evidence Captured
-> Risk Classified
-> Approval Decision Made
-> Proof File Generated
-> Audit Event Recorded
-> Manager / Customer Report Produced
```

## 2. Process Objects

| Process Step | Main Object | Output |
| --- | --- | --- |
| Business Task Created | task / assignment | business task and owner |
| Agent Eligibility Check | governance policy | allowed / review / senior approval / manual only |
| Human Authority Check | authority level | user may proceed / needs reviewer / blocked |
| Agent Work Request Created | work request | task brief, context, constraints |
| Agent Output Produced | submission / output | output summary, transcript summary, changed artifacts |
| Verification Evidence Captured | evidence | test result, screenshot, log, checklist, correction notes |
| Risk Classified | risk record | low / medium / high / critical |
| Approval Decision Made | review / decision | approved / rejected / revise / escalated |
| Proof File Generated | proof file | readiness evidence package |
| Audit Event Recorded | audit event | append-only record |
| Report Produced | report / export | internal, manager, or customer-safe report |

## 3. Scenario 1: Software / IT Delivery Governance

### 3.1 Business Context

A legacy enterprise system has a bug, small feature request, screen mismatch, SQL issue, or test coverage gap. An employee wants to use Claude Code, Codex, Cursor, or another coding Agent.

### 3.2 Flow

```text
Bug / Change Request
-> classify task category: software_change
-> check policy: Agent allowed with human review
-> check authority: L2 or above required
-> create Agent task brief
-> provide repository context and no-touch rules
-> run Agent tool
-> inspect diff / generated files
-> run tests / manual verification
-> classify risk: low / medium / high / critical
-> approve / reject / revise / escalate
-> create Proof-of-Agent-Work File
-> generate customer-safe technical summary
```

### 3.3 Required Evidence

```text
original requirement or bug report
Agent task brief
repo context / touched files summary
diff summary
test result / screenshot / logs
security / permission / data checklist
human corrections
approval decision
customer-safe explanation
```

### 3.4 Success Criteria

```text
Agent use was allowed by policy
employee had sufficient authority
output was verified
risk was correctly classified
approval decision was justified
customer-safe report does not expose internal secrets
```

## 4. Scenario 2: Business Analysis / PM Governance

### 4.1 Business Context

A project member uses an Agent to generate meeting minutes, WBS, risk register, requirement summary, customer Q&A, or weekly report.

### 4.2 Flow

```text
Meeting / Requirement / Project Issue
-> classify task category: business_analysis
-> check policy: Agent allowed with human review
-> check authority: L1/L2 allowed for internal draft; L4 required for customer-facing output
-> create Agent work request
-> Agent generates summary / WBS / risks
-> human verifies facts, owners, dates, and missing stakeholders
-> classify risk based on customer impact
-> approve for internal use or customer sharing
-> create Proof File
-> produce manager-safe or customer-safe report
```

### 4.3 Required Evidence

```text
source meeting notes or requirement input
Agent output summary
fact-check notes
owner / deadline verification
missing issue list
customer-safe wording check
approval decision
manager / customer report
```

### 4.4 Success Criteria

```text
facts are correct
owners and deadlines are traceable
scope boundaries are explicit
risks are not hidden
customer wording is safe
```

## 5. Scenario 3: Sales / Service Governance

### 5.1 Business Context

A sales or service operator uses Agent to prepare customer profile, follow-up message, proposal draft, pricing explanation, objection handling, or service package recommendation.

### 5.2 Flow

```text
Lead / Customer Need
-> classify task category: sales_service
-> check policy: Agent allowed with compliance review for customer-facing content
-> check authority: L2 can draft; L4/L5 approves external claims
-> Agent generates profile / follow-up / proposal
-> human checks need fit, scope, price, promise, and compliance boundary
-> classify risk
-> approve / revise / block
-> record follow-up evidence
-> generate customer-safe next-action summary
```

### 5.3 Required Evidence

```text
lead source
customer need summary
Agent-generated proposal / script summary
scope and price boundary check
prohibited claim check
next action
approval decision
follow-up record
```

### 5.4 Success Criteria

```text
no exaggerated claims
no guaranteed employment / income / result wording
price and scope are bounded
next action is clear
customer need is matched to the right package
```

## 6. Scenario 4: HR / Training Readiness Governance

### 6.1 Business Context

A training manager or instructor uses Agent to generate training plans, assignments, readiness scorecards, learner reports, or role-fit recommendations.

### 6.2 Flow

```text
Training Goal / Role Requirement
-> classify task category: hr_training_readiness
-> check policy: Agent allowed with privacy and fairness review
-> create assessment task
-> learner completes governed Agent work
-> reviewer scores evidence
-> readiness level is calculated
-> manager receives readiness report
-> decision: more training / supervised work / trusted operator / approver candidate
```

### 6.3 Required Evidence

```text
role requirement
training task
learner evidence
review rubric scores
privacy check
fairness / no-fake-certification check
readiness recommendation
manager report
```

### 6.4 Success Criteria

```text
readiness is evidence-based
no fake certification claim
personal data is protected
manager can make a reasonable next-step decision
```

## 7. Scenario 5: Customer Support / Knowledge Work Governance

### 7.1 Business Context

A support or knowledge worker uses Agent to draft customer responses, FAQ updates, troubleshooting steps, or knowledge-base articles.

### 7.2 Flow

```text
Customer Question / Support Ticket
-> classify task category: support_knowledge
-> check policy: Agent allowed with customer-safe review
-> Agent drafts response or article
-> human verifies facts, product scope, and tone
-> classify customer risk
-> approve response or escalate
-> retain evidence
-> generate support proof record
```

### 7.3 Required Evidence

```text
customer question
Agent response summary
fact verification
source references / internal KB link
risk classification
approval decision
customer-safe final response
```

## 8. Cross-Scenario Status Model

Suggested status values:

```text
Draft
Eligibility Checked
Agent Requested
Output Submitted
Evidence Pending
Verification Complete
Risk Classified
Review Required
Approved
Rejected
Revision Required
Escalated
Proof Ready
Reported
```

## 9. Cross-Scenario Decision Model

Suggested decisions:

```text
Approve Internal Use
Approve Customer Use
Reject Agent Output
Request Revision
Escalate To Senior
Escalate To Security / Compliance
Manual Only
No Agent Use Allowed
```

## 10. Consulting Deliverables

For each client pilot, produce:

```text
scenario inventory
task category map
policy matrix
authority level assignment
evidence checklist
approval workflow
proof file examples
manager report
customer-safe report
roadmap for systemization
```
