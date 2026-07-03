# v6.0 Waterfall Delivery Plan

Repository:

```text
moseszhu999/ai-career-retraining-site
```

Branch:

```text
waterfall-togaf-rebuild
```

## 0. Rebuild intent

The project is rebuilt from a page-driven prototype into a consulting-company waterfall delivery system.

Target sequence:

```text
战略分析 -> 痛点把握 -> TOGAF 分层功能架构 / 数据架构 -> 原型设计 -> 技术架构
```

The goal is to make every screen, data object, and technical component traceable to a business pain and a customer-safe delivery artifact.

---

## 1. Strategic analysis

### 1.1 Strategic positioning

```text
企业 AI Agent 治理与能力证明系统
```

The customer does not buy a course. The customer buys a governed way to introduce AI Agents into repeatable value-chain work while keeping evidence, approval, accountability, and reporting.

### 1.2 Target customers

| Segment | Need | Entry product |
| --- | --- | --- |
| Small and mid-sized enterprises | Need AI adoption but cannot govern AI output | Value Chain AI Automation Diagnosis |
| Training / delivery teams | Need proof that employees can use AI responsibly | Task + Evidence + Proof File delivery |
| Consulting / implementation teams | Need repeatable method and reports | Waterfall architecture package |
| Department managers | Need visibility into readiness and risk | Manager readiness dashboard |

### 1.3 Commercial boundary

Do not promise official certification, guaranteed employment, guaranteed salary, or regulated professional qualification outcomes.

Sell diagnosis, implementation design, governance workflow, evidence records, and customer-safe reporting.

### 1.4 Strategic gate

A scenario can enter design only when it has:

```text
clear business owner
repeatable work step
visible cost / risk / quality pain
data or evidence source
human approval boundary
customer-safe output
```

---

## 2. Pain-point grasp

### 2.1 Pain matrix

| User | Pain | Product response |
| --- | --- | --- |
| Founder / business owner | Cannot tell which AI ideas are commercially valuable | Strategy and value-chain diagnosis |
| Manager | Cannot measure AI readiness or delivery risk | Readiness metrics and review queue |
| Operator / instructor | Cannot turn training into proof | Task design, scoring, evidence records |
| Learner / employee | Cannot show credible AI work ability | Proof Files and portfolio records |
| Customer / compliance | Cannot trust AI output without evidence | Governance policy, approval, audit, customer-safe report |

### 2.2 Prioritized scenarios

1. Lead-to-Proposal automation.
2. Requirement-to-Delivery automation.
3. Training-to-Readiness automation.
4. Support-to-Knowledge automation.

### 2.3 Pain-to-capability rule

Every pain must map to at least one of:

```text
Strategy capability
Scenario capability
Governance capability
Evidence capability
Review capability
Reporting capability
Operation capability
```

---

## 3. TOGAF layered functional architecture

## 3.1 Business architecture

Business capabilities:

| Capability domain | Capability |
| --- | --- |
| Strategic analysis | customer positioning, value proposition, boundary definition |
| Pain and scenario | pain intake, severity, value-chain mapping, scenario priority |
| Process design | role, responsibility, process, exception path |
| Agent governance | automation level, task eligibility, human approval, risk policy |
| Evidence and proof | submission, scoring, evidence record, proof candidate, portfolio |
| Reporting | manager report, customer-safe report, Excel export |
| Platform operations | customer, cohort, learner, task, assignment, health check, audit |

## 3.2 Application architecture

Application domains:

| Domain | Modules |
| --- | --- |
| Strategy | Strategic Analysis Center, Waterfall Architecture |
| Pain | Pain Point Board, Scenario Intake |
| Business architecture | Capability Map, Workflow Blueprint |
| Agent work | Task Bank, Assignment Center, Learner Workbench |
| Governance | Governance Policy, Authority Model, Review Queue |
| Evidence | Evidence Store, Proof File Center, Portfolio |
| Reporting | Delivery Report, Export Center |
| Operations | Production Admin, Supabase Health, Audit Log |

## 3.3 Data architecture

Core entities:

| Entity | Meaning | Notes |
| --- | --- | --- |
| EnterpriseClient | customer / department / cohort | entry point for commercialization |
| BusinessScenario | target business scenario | belongs to value-chain stage |
| PainPoint | customer pain | has severity and frequency |
| Capability | business capability | maps pain to app module |
| AgentWorkStep | automatable work unit | has automation level |
| GovernancePolicy | rule and boundary | controls approval and visibility |
| EvidenceRecord | task evidence | source of proof and report |
| ReviewDecision | human decision | approve, revise, reject, escalate |
| ProofFile | customer-visible proof | must be approved |
| ReadinessReport | manager/customer report | generated from evidence and review |
| AuditEvent | audit trail | records critical actions |

Relationships:

```text
EnterpriseClient 1..n BusinessScenario
BusinessScenario 1..n PainPoint
PainPoint n..n Capability
Capability 1..n ApplicationModule
BusinessScenario 1..n AgentWorkStep
AgentWorkStep 1..n EvidenceRecord
EvidenceRecord 0..n ReviewDecision
ReviewDecision 0..1 ProofFile
ProofFile n..1 ReadinessReport
All critical actions -> AuditEvent
```

## 3.4 Technology architecture

| Layer | Current | Target |
| --- | --- | --- |
| UI | Streamlit | formal web admin console |
| Runtime | Python modules | API service layer |
| State | session + repository layer | Supabase/Postgres persistence |
| Auth | demo role switch | multi-tenant RBAC |
| Evidence | in-app records | evidence and audit tables |
| Export | openpyxl | report/export service |
| Deployment | Streamlit Cloud | containerized app + managed database |
| Observability | health check and audit log | metrics, logs, alerting |

---

## 4. Prototype design

### 4.1 Prototype navigation

Founder navigation should prioritize method and delivery:

```text
Dashboard
Waterfall
Admin/Health
Executable Flow
客户
班级
学员
练习题
Assignments
Review Queue
Proof Files
Leads
Reports
Exports
Audit
```

### 4.2 New screen added in v6.0

```text
frontend/waterfall_pages.py
```

Purpose:

```text
Show the complete waterfall method inside the live product.
Make the founder demo explain strategy, pain, TOGAF, data, prototype, and technical architecture from one page.
```

### 4.3 Demo routes

3-minute sales route:

```text
Public Strategy Landing -> Waterfall -> Proof / Report summary
```

8-minute founder route:

```text
Dashboard -> Waterfall -> Executable Flow -> Review Queue -> Reports
```

15-minute delivery route:

```text
Waterfall -> Clients -> Tasks -> Assignments -> Review Queue -> Proof Files -> Export -> Audit
```

---

## 5. Technical architecture and implementation plan

### 5.1 Current implementation decision

Use Streamlit as an executable prototype because it is fast, demo-friendly, and already integrated with the current state, admin, task, report, and export pages.

### 5.2 MVP implementation order

1. Add Waterfall architecture page.
2. Add Founder navigation entry.
3. Update README to make v6.0 method explicit.
4. Create architecture delivery document.
5. Later: convert pain points, capabilities, entities, and prototype routes into editable persistent records.

### 5.3 Next development tasks

| Priority | Task | Result |
| --- | --- | --- |
| P0 | Pain Point Board persistence | customer pains become data |
| P0 | Capability Map persistence | TOGAF capability layer becomes configurable |
| P1 | Scenario-to-task mapping | every task traces to a business scenario |
| P1 | Evidence and approval schema | proof/report source becomes auditable |
| P2 | Customer report portal | customer-safe output separated from internal data |
| P2 | Formal API and frontend | move beyond Streamlit demo |

---

## 6. Acceptance checklist

The rebuild is acceptable when:

```text
战略口径清楚：not course, not AI tool demo, but Agent governance and proof OS.
痛点清楚：buyer, manager, operator, learner, customer/compliance pains are separated.
TOGAF 清楚：business, application, data, technology layers are traceable.
数据清楚：Proof File and report can trace back to evidence and review decisions.
原型清楚：Founder can demo the method from the Waterfall page.
技术清楚：Streamlit MVP and future production architecture are separated.
```
