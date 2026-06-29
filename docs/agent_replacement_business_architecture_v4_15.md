# v4.15.0 Agent Replacement Business Architecture

This document corrects the consulting architecture sequence and adds the missing breakthrough layer: AI Agent replacement of manual work.

## 1. Correct Consulting Architecture Sequence

The correct consulting-company architecture sequence is:

```text
BLM
-> Business Architecture
-> Application Architecture
-> Data Architecture
-> Technical Architecture
```

Scenario processes are not a separate architecture layer between BLM and application architecture. They belong inside Business Architecture as process architecture / scenario flow.

Correct mapping:

| Layer | Purpose |
| --- | --- |
| BLM | Why the business exists, what market problem it solves, what strategic intent it follows. |
| Business Architecture | Business capabilities, operating model, scenario processes, roles, KPIs, and Agent replacement model. |
| Application Architecture | Application domains and system functions that support the business architecture. |
| Data Architecture | Business objects, data domains, entity relationships, evidence, proof, audit, and data classification. |
| Technical Architecture | Runtime architecture, infrastructure, integration, security, Agent connectors, and deployment roadmap. |

## 2. Why Agent Replacement Must Be Explicit

A governance product cannot break out if it only says:

```text
humans supervise AI Agents
```

That is not enough. It sounds defensive and short-term.

The product must show where AI Agents replace manual labor and where humans / organizations retain responsibility.

Breakthrough positioning:

```text
AI Agents replace repeatable work steps.
The OS governs which Agent work may enter formal enterprise workflows.
```

Chinese:

```text
AI Agent 替代重复性人工环节；本系统治理哪些 Agent 工作结果可以进入企业正式流程。
```

## 3. Replacement vs Accountability Boundary

The key design principle:

```text
Agent replaces labor.
Human / organization retains authority, responsibility, and accountability.
```

| Work Layer | Agent Can Replace | Human / Organization Must Keep |
| --- | --- | --- |
| Information gathering | draft research, summarize inputs, extract facts | source selection, final factual responsibility |
| Drafting | emails, reports, WBS, test cases, proposals, code patches | business intent, tone, customer promise, final approval |
| Generation | code, SQL, test cases, documents, scripts, workflows | scope boundaries, security, compliance, acceptance |
| Checking | first-pass review, static checks, consistency checks | final risk judgment and exception handling |
| Reporting | draft reports, summarize evidence, format exports | what is safe to share and who receives it |
| Follow-up | suggested next actions, reminders, reply drafts | relationship judgment and commercial responsibility |

## 4. Agent Replacement Levels

Define five levels of replacement.

### R0: No Replacement

Manual-only work.

Examples:

```text
regulated legal judgment
final HR termination decision
critical security approval
contractual commitment
customer compensation decision
```

### R1: Draft Replacement

Agent drafts; human edits.

Examples:

```text
meeting minutes draft
customer email draft
proposal outline
bug report draft
training feedback draft
```

### R2: Task Execution Replacement

Agent performs a bounded task; human verifies.

Examples:

```text
code patch
test case generation
WBS creation
risk register draft
lead follow-up plan
knowledge-base article
```

### R3: Workflow Step Replacement

Agent performs a repeatable workflow step with evidence and policy guardrails.

Examples:

```text
triage support tickets
generate weekly project report
prepare customer follow-up package
create test coverage package
summarize learner readiness evidence
```

### R4: Conditional Autonomous Operation

Agent runs a low-risk workflow with automatic logging and exception escalation.

Examples:

```text
internal reminder generation
low-risk report formatting
non-customer-facing summary
internal data cleanup proposal
routine QA checklist draft
```

R4 is only acceptable when:

```text
risk is low
policy allows automation
evidence is automatically logged
exceptions are escalated
customer-facing output is blocked unless approved
```

## 5. Business Capability Map with Replacement Targets

| Capability | Current Human Work | Agent Replacement Target | Human Retained Role |
| --- | --- | --- | --- |
| Task Intake | read request, classify task | suggest task category and policy | confirm category and scope |
| Policy Matching | manually decide if Agent allowed | match task to eligibility policy | approve exception / override |
| Task Brief Creation | write detailed instruction | draft Agent task brief | validate constraints and intent |
| Evidence Checklist | remember required proof | generate required evidence list | confirm sufficiency |
| Work Execution | write code/doc/report manually | generate code/doc/report/workflow output | verify and correct output |
| Verification | manually check everything | run first-pass checklist / consistency checks | final verification and sign-off |
| Risk Classification | subjective judgment | suggest risk level and reasons | final risk classification |
| Approval Routing | manually ask senior | route based on policy | approve / reject / escalate |
| Proof File Creation | manually assemble evidence | auto-generate proof package | certify customer-safe summary |
| Reporting | manually prepare report | draft manager/customer report | decide what can be shared |
| Audit | manually record actions | auto-log events | audit exception handling |

## 6. Business Architecture After Replacement

The business architecture must include both governance and replacement.

```text
Business Task
-> Agent Replacement Eligibility
-> Policy / Risk / Authority Check
-> Agent Executes Replaceable Step
-> Evidence Auto-Captured
-> Agent / System Pre-Checks Output
-> Human Handles Exceptions / Approval
-> Proof File Generated
-> Report Produced
-> Audit Retained
```

This is stronger than a training workflow because it proves productivity gain and control.

## 7. Scenario Replacement Maps

### 7.1 Software / IT Delivery

| Manual Step | Agent Replacement | Human Retained |
| --- | --- | --- |
| read bug report | summarize issue and likely module | confirm business meaning |
| inspect code | locate candidate files | confirm touched scope |
| write patch | generate code diff | review diff and security risk |
| write tests | generate test cases | choose required regression set |
| prepare report | draft technical summary | approve customer-safe wording |

Agent replacement claim:

```text
Reduce manual code/test/report drafting, while keeping human responsibility for merge and customer delivery.
```

### 7.2 Business Analysis / PM

| Manual Step | Agent Replacement | Human Retained |
| --- | --- | --- |
| summarize meeting | draft minutes | verify facts and decisions |
| build WBS | draft WBS and owners | confirm ownership and dates |
| create risk list | draft risk register | prioritize and escalate |
| write weekly report | draft report | approve customer-safe version |

Agent replacement claim:

```text
Reduce PM documentation and reporting workload, while retaining accountability for facts, owners, and customer commitments.
```

### 7.3 Sales / Service Operations

| Manual Step | Agent Replacement | Human Retained |
| --- | --- | --- |
| qualify lead | draft customer profile | confirm real buying intent |
| write follow-up | draft message | adjust tone and relationship strategy |
| prepare proposal | draft scope and package | approve price and promise boundary |
| handle objection | suggest responses | choose commercial position |

Agent replacement claim:

```text
Reduce follow-up and proposal drafting work, while preventing overpromising and scope leakage.
```

### 7.4 HR / Training Readiness

| Manual Step | Agent Replacement | Human Retained |
| --- | --- | --- |
| design tasks | draft task templates | align with role requirements |
| score submissions | first-pass rubric scoring | final readiness decision |
| write learner report | draft growth report | approve fairness and privacy |
| recommend next step | suggest training path | manager decision |

Agent replacement claim:

```text
Reduce training review and reporting workload, while keeping evidence-based readiness decisions.
```

### 7.5 Customer Support / Knowledge Work

| Manual Step | Agent Replacement | Human Retained |
| --- | --- | --- |
| read support ticket | summarize issue | confirm customer context |
| draft response | generate reply | approve customer wording |
| update KB | draft article | verify source and policy |
| escalate issue | suggest escalation | final escalation decision |

Agent replacement claim:

```text
Reduce support response and knowledge-base drafting, while retaining customer-impact responsibility.
```

## 8. Product Differentiation

A normal AI training product says:

```text
Use AI to work faster.
```

This product says:

```text
Replace repeatable manual work with AI Agents, while preserving enterprise governance, evidence, approval, and accountability.
```

A normal governance product says:

```text
Control AI risk.
```

This product says:

```text
Control AI risk while proving which work steps can actually be replaced.
```

## 9. Consulting Deliverables

For a client, deliver:

```text
1. Agent Replacement Opportunity Map
2. Task Eligibility Matrix
3. Authority Level Matrix
4. Risk and Approval Workflow
5. Evidence Requirement Checklist
6. Agent Replacement Pilot Scenarios
7. Readiness Scorecard
8. Manager / Customer Report Template
9. Governance Roadmap
```

## 10. Revised Architecture Sequence for Repository

v4.14.0 introduced separate documents for BLM, scenario process, application, data, and technical architecture.

v4.15.0 corrects the hierarchy:

```text
BLM
-> Business Architecture
   -> capability map
   -> operating model
   -> scenario process
   -> Agent replacement map
   -> KPI model
-> Application Architecture
-> Data Architecture
-> Technical Architecture
```

Future documentation should treat `scenario_process_architecture_v4_14.md` as a Business Architecture sub-document, not as a separate peer layer.

## 11. One-Line Strategic Upgrade

```text
From AI Agent governance only, to AI Agent labor replacement with governance.
```

Chinese:

```text
不是只治理 AI Agent，而是让 AI Agent 替代可替代的人工环节，同时保留企业责任链。
```
