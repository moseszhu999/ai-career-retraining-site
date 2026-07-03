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

## 0.1 Pre-prototype implementation freeze

Before the prototype design phase is approved, this branch only produces analysis and architecture documents.

Allowed now:

```text
战略分析
痛点把握
TOGAF 分层功能架构
数据架构
原型需求说明
页面清单
技术架构规划
验收标准
```

Not allowed yet:

```text
Streamlit 页面实现
路由接入
前端组件实现
后端服务实现
数据访问实现
数据库迁移
运行配置改动
```

Implementation starts only after the prototype design gate is explicitly passed.

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

## 3. TOGAF layered functional architecture and layered data architecture

### 3.0 Layering principle

To make the product scalable, functions and data must be designed as parallel hierarchies.

```text
一级功能 -> 一级数据域
二级功能 -> 二级主题数据
三级功能 -> 三级实体 / 字段 / 证据项
```

This prevents the system from becoming a collection of pages. It also makes later expansion possible across industries, departments, scenarios, roles, reports, and customer portals.

### 3.1 Three-level functional architecture

#### 3.1.1 Level-1 functions

Level-1 functions are product capability domains. They should remain stable even when the implementation changes.

| 一级功能 | Business meaning | Main owner |
| --- | --- | --- |
| F1 Strategy and Commercialization | Define customer, value proposition, sales boundary, pilot package | Founder |
| F2 Pain and Scenario Discovery | Capture customer pain, value-chain stage, process and risk | Consultant / Founder |
| F3 Business Architecture and Capability Map | Convert pain into business capability and process design | Architect / Founder |
| F4 Agent Work Governance | Define which work steps can be automated and how humans approve them | Process Owner / Reviewer |
| F5 Evidence and Proof Management | Capture task evidence, review evidence, proof candidates and proof files | Reviewer / Founder |
| F6 Readiness and Reporting | Generate internal and customer-safe readiness reports | Founder / Manager |
| F7 Platform Operations | Manage customer, cohort, learner, task, assignment, health and audit | Operator / Admin |

#### 3.1.2 Level-2 functions

Level-2 functions are sub-capabilities under each Level-1 domain.

| 一级功能 | 二级功能 | Description |
| --- | --- | --- |
| F1 Strategy and Commercialization | F1.1 Customer Segmentation | Identify customer type, industry, department and buyer |
| F1 Strategy and Commercialization | F1.2 Value Proposition | Define what the customer pays for |
| F1 Strategy and Commercialization | F1.3 Product Package | Define diagnosis, pilot, delivery pack and renewal path |
| F1 Strategy and Commercialization | F1.4 Commercial Boundary | Define what cannot be promised or sold |
| F2 Pain and Scenario Discovery | F2.1 Pain Intake | Record pain from interview, workshop or sales conversation |
| F2 Pain and Scenario Discovery | F2.2 Value-chain Mapping | Map pain to value-chain stage and process |
| F2 Pain and Scenario Discovery | F2.3 Scenario Priority | Rank scenario by value, risk, evidence and feasibility |
| F2 Pain and Scenario Discovery | F2.4 Pilot Scope | Select scenarios for prototype or pilot delivery |
| F3 Business Architecture and Capability Map | F3.1 Capability Decomposition | Break business into capability domains |
| F3 Business Architecture and Capability Map | F3.2 Process Architecture | Define role, step, input, output and exception path |
| F3 Business Architecture and Capability Map | F3.3 Application Mapping | Map capability to future application module |
| F3 Business Architecture and Capability Map | F3.4 KPI Mapping | Map capability to measurable result |
| F4 Agent Work Governance | F4.1 Work-step Eligibility | Judge whether a step can be done by AI Agent |
| F4 Agent Work Governance | F4.2 Automation Level | R0 to R4 automation level definition |
| F4 Agent Work Governance | F4.3 Human Authority | Define who approves, rejects, revises or escalates |
| F4 Agent Work Governance | F4.4 Risk Policy | Define policy, evidence and exception rules |
| F5 Evidence and Proof Management | F5.1 Evidence Capture | Capture answer, file, score, comment, decision and version |
| F5 Evidence and Proof Management | F5.2 Review Decision | Human review result and reason |
| F5 Evidence and Proof Management | F5.3 Proof Candidate | Candidate proof item after task and review |
| F5 Evidence and Proof Management | F5.4 Proof File | Approved proof that can be shown to customer or manager |
| F6 Readiness and Reporting | F6.1 Readiness Metric | Score, accuracy, completion, exception and proof rate |
| F6 Readiness and Reporting | F6.2 Internal Report | Founder and operator view |
| F6 Readiness and Reporting | F6.3 Customer-safe Report | Customer view with sensitive fields removed |
| F6 Readiness and Reporting | F6.4 Export Package | Excel / PDF / report snapshot requirement |
| F7 Platform Operations | F7.1 Client Management | Customer, department, cohort, contract context |
| F7 Platform Operations | F7.2 Learner / Employee Management | User, role, class, assignment and learning path |
| F7 Platform Operations | F7.3 Task Bank Management | Question, task, rubric and template |
| F7 Platform Operations | F7.4 Audit and Health | System health, event log and permission check |

#### 3.1.3 Level-3 functions

Level-3 functions are concrete operations that will later become screens, forms, buttons, reports or workflow steps. They are not implemented before the prototype gate.

| 二级功能 | 三级功能 examples |
| --- | --- |
| F1.1 Customer Segmentation | create customer profile; tag industry; tag buyer role; define target department |
| F1.2 Value Proposition | record customer value hypothesis; estimate time saved; define proof value |
| F1.3 Product Package | define diagnosis pack; define pilot pack; define delivery pack; define renewal input |
| F1.4 Commercial Boundary | mark prohibited promise; mark customer-visible claim; mark internal-only note |
| F2.1 Pain Intake | create pain point; classify pain type; record frequency; record severity |
| F2.2 Value-chain Mapping | select value-chain stage; map process; map role; map source document |
| F2.3 Scenario Priority | score business value; score feasibility; score risk; rank scenario |
| F2.4 Pilot Scope | choose pilot scenario; define success metric; define delivery artifact |
| F3.1 Capability Decomposition | create capability; map capability to pain; set maturity level |
| F3.2 Process Architecture | define step; define input; define output; define exception path |
| F3.3 Application Mapping | map capability to module; define module boundary; define future screen |
| F3.4 KPI Mapping | define KPI; define numerator and denominator; define report owner |
| F4.1 Work-step Eligibility | assess automation suitability; mark blocked reason; define human checkpoint |
| F4.2 Automation Level | assign R0/R1/R2/R3/R4; record rationale; set upgrade condition |
| F4.3 Human Authority | set approver; set reviewer; set escalation owner; set final authority |
| F4.4 Risk Policy | classify risk; define evidence required; define approval rule |
| F5.1 Evidence Capture | store submission; store score; store comment; store attachment metadata |
| F5.2 Review Decision | approve; revise; reject; escalate; record decision reason |
| F5.3 Proof Candidate | mark candidate; link evidence; link review decision; set readiness status |
| F5.4 Proof File | approve proof; define customer summary; define visibility field list |
| F6.1 Readiness Metric | calculate completion; calculate accuracy; calculate proof-ready rate |
| F6.2 Internal Report | generate founder report; show exceptions; show weak modules |
| F6.3 Customer-safe Report | mask private data; include approved proof; include next-step advice |
| F6.4 Export Package | define export dataset; define report snapshot; define delivery date |
| F7.1 Client Management | create client; create cohort; set service package; set tenant context |
| F7.2 Learner / Employee Management | create learner; assign role; assign cohort; assign task |
| F7.3 Task Bank Management | create task; create MCQ; create rubric; create template |
| F7.4 Audit and Health | record audit event; view health status; check permission boundary |

### 3.2 Three-level data architecture

The data architecture must mirror the functional hierarchy. Data should not be designed only as database tables. It should start from enterprise data domains, then become subject data groups, then become entities, fields, evidence and report measures.

#### 3.2.1 Level-1 data domains

| 一级数据域 | Corresponding Level-1 function | Meaning |
| --- | --- | --- |
| D1 Strategy Data | F1 Strategy and Commercialization | customer segmentation, commercial package and boundary data |
| D2 Pain and Scenario Data | F2 Pain and Scenario Discovery | pain, value-chain stage, process and scenario priority data |
| D3 Capability and Architecture Data | F3 Business Architecture and Capability Map | business capability, process, app mapping and KPI data |
| D4 Governance and Work Data | F4 Agent Work Governance | work-step, automation level, authority and policy data |
| D5 Evidence and Proof Data | F5 Evidence and Proof Management | evidence, review, decision, proof candidate and proof file data |
| D6 Reporting and Metric Data | F6 Readiness and Reporting | readiness metric, internal report, customer report and export data |
| D7 Operation and Audit Data | F7 Platform Operations | client, cohort, user, task bank, assignment, health and audit data |

#### 3.2.2 Level-2 data subjects

| 一级数据域 | 二级数据主题 | Main data contents |
| --- | --- | --- |
| D1 Strategy Data | D1.1 Customer Segment Data | customer type, industry, department, buyer, target role |
| D1 Strategy Data | D1.2 Commercial Package Data | diagnosis pack, pilot pack, delivery pack, price assumption |
| D1 Strategy Data | D1.3 Boundary Data | prohibited claim, allowed claim, internal note, customer-safe note |
| D2 Pain and Scenario Data | D2.1 Pain Point Data | pain type, severity, frequency, cost, risk, owner |
| D2 Pain and Scenario Data | D2.2 Value-chain Data | value-chain stage, process, role, input, output |
| D2 Pain and Scenario Data | D2.3 Scenario Priority Data | value score, feasibility score, risk score, priority rank |
| D3 Capability and Architecture Data | D3.1 Capability Data | capability domain, capability name, maturity, related pain |
| D3 Capability and Architecture Data | D3.2 Process Data | process, step, role, input, output, exception path |
| D3 Capability and Architecture Data | D3.3 Application Mapping Data | module, screen candidate, function boundary, owner |
| D3 Capability and Architecture Data | D3.4 KPI Data | metric name, formula, owner, reporting period |
| D4 Governance and Work Data | D4.1 Agent Work-step Data | work-step, input, output, eligibility, blocked reason |
| D4 Governance and Work Data | D4.2 Automation Level Data | R0-R4 level, rationale, upgrade condition |
| D4 Governance and Work Data | D4.3 Authority Data | reviewer, approver, escalation owner, final authority |
| D4 Governance and Work Data | D4.4 Risk Policy Data | risk class, evidence requirement, approval rule |
| D5 Evidence and Proof Data | D5.1 Evidence Record Data | submission, answer, score, attachment, version, source |
| D5 Evidence and Proof Data | D5.2 Review Decision Data | decision, reason, reviewer, timestamp, next action |
| D5 Evidence and Proof Data | D5.3 Proof Candidate Data | candidate status, linked evidence, readiness reason |
| D5 Evidence and Proof Data | D5.4 Proof File Data | approved proof, public summary, visibility rule |
| D6 Reporting and Metric Data | D6.1 Readiness Metric Data | completion, accuracy, exception, proof-ready rate |
| D6 Reporting and Metric Data | D6.2 Internal Report Data | founder view, weak point, exception, operational decision |
| D6 Reporting and Metric Data | D6.3 Customer-safe Report Data | customer-visible proof, masked fields, delivery summary |
| D6 Reporting and Metric Data | D6.4 Export Snapshot Data | export dataset, generated file, generated time, delivery target |
| D7 Operation and Audit Data | D7.1 Tenant / Client Data | tenant, client, cohort, department, service package |
| D7 Operation and Audit Data | D7.2 User and Role Data | user, role, learner, reviewer, founder, permission scope |
| D7 Operation and Audit Data | D7.3 Task Bank Data | task, question, answer, rubric, template, assignment |
| D7 Operation and Audit Data | D7.4 Audit Event Data | actor, action, object, timestamp, before/after state |

#### 3.2.3 Level-3 data entities and fields

| 二级数据主题 | 三级数据实体 | Representative fields |
| --- | --- | --- |
| D1.1 Customer Segment Data | CustomerSegment | segment_id, segment_name, industry, company_size, buyer_role |
| D1.2 Commercial Package Data | ProductPackage | package_id, package_type, scope, deliverable, price_note |
| D1.3 Boundary Data | CommercialBoundary | boundary_id, claim_type, allowed_flag, customer_visible_flag |
| D2.1 Pain Point Data | PainPoint | pain_id, client_id, pain_type, severity, frequency, business_impact |
| D2.2 Value-chain Data | ValueChainStage | stage_id, stage_name, process_name, role_name, input_output |
| D2.3 Scenario Priority Data | BusinessScenario | scenario_id, client_id, value_score, feasibility_score, risk_score, priority_rank |
| D3.1 Capability Data | Capability | capability_id, level1_function, level2_function, maturity, owner |
| D3.2 Process Data | ProcessStep | step_id, process_id, role, input_data, output_data, exception_path |
| D3.3 Application Mapping Data | ApplicationModuleCandidate | module_id, capability_id, screen_candidate, boundary, owner |
| D3.4 KPI Data | KpiDefinition | kpi_id, name, formula_text, owner, report_period |
| D4.1 Agent Work-step Data | AgentWorkStep | work_step_id, scenario_id, eligibility, input, output, blocked_reason |
| D4.2 Automation Level Data | AutomationLevelAssessment | assessment_id, work_step_id, automation_level, rationale, upgrade_condition |
| D4.3 Authority Data | AuthorityRule | rule_id, role, permission_scope, approval_action, escalation_owner |
| D4.4 Risk Policy Data | GovernancePolicy | policy_id, risk_class, required_evidence, approval_rule, visibility_rule |
| D5.1 Evidence Record Data | EvidenceRecord | evidence_id, assignment_id, submission, score, source, version |
| D5.2 Review Decision Data | ReviewDecision | decision_id, evidence_id, reviewer, decision, reason, next_action |
| D5.3 Proof Candidate Data | ProofCandidate | candidate_id, evidence_id, readiness_status, reason, created_at |
| D5.4 Proof File Data | ProofFile | proof_id, candidate_id, approved_by, public_summary, visibility_fields |
| D6.1 Readiness Metric Data | ReadinessMetric | metric_id, cohort_id, metric_name, numerator, denominator, value |
| D6.2 Internal Report Data | InternalReport | report_id, client_id, weak_points, exceptions, founder_recommendation |
| D6.3 Customer-safe Report Data | CustomerSafeReport | report_id, client_id, approved_proofs, masked_fields, delivery_summary |
| D6.4 Export Snapshot Data | ExportSnapshot | export_id, report_id, dataset_name, generated_at, delivery_target |
| D7.1 Tenant / Client Data | EnterpriseClient | client_id, tenant_id, name, department, service_package, status |
| D7.2 User and Role Data | UserRoleProfile | user_id, role, cohort_id, permission_scope, status |
| D7.3 Task Bank Data | TaskTemplate | task_id, module, prompt, rubric, answer_key, difficulty |
| D7.4 Audit Event Data | AuditEvent | event_id, actor_id, action, object_type, object_id, timestamp |

### 3.3 Function-data traceability matrix

Every future screen and implementation task must pass this traceability test.

| Trace level | Required mapping |
| --- | --- |
| Level 1 | 一级功能 maps to one 一级数据域 |
| Level 2 | 二级功能 maps to one or more 二级数据主题 |
| Level 3 | 三级功能 maps to concrete 三级数据实体 and fields |
| Evidence | any report field must trace back to EvidenceRecord, ReviewDecision or approved ProofFile |
| Customer-safe output | any customer-visible field must have a visibility rule |
| Audit | any approval, export or proof action must produce an AuditEvent |

### 3.4 TOGAF architecture layer summary

| TOGAF layer | What it contains in this project |
| --- | --- |
| Business architecture | 三层功能架构、业务能力、流程、角色、责任、KPI |
| Application architecture | future modules and screens derived from Level-2 and Level-3 functions |
| Data architecture | 三层数据架构、实体、字段、证据链、报表口径 |
| Technology architecture | runtime, persistence, permission, export, deployment and observability plan |

### 3.5 Technology architecture

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

### 4.1 Prototype design gate

Prototype design is a documentation phase, not implementation.

It must define:

```text
user roles
navigation model
screen inventory
screen purpose
input/output per screen
primary user action
approval point
visible data fields
customer-safe fields
nonfunctional constraints
```

Prototype design must also show which Level-1 / Level-2 / Level-3 function and data level each screen belongs to.

### 4.2 Prototype navigation requirement

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

### 4.3 Proposed future screen

```text
Waterfall Architecture
```

Purpose:

```text
Show the complete waterfall method inside the live product.
Make the founder demo explain strategy, pain, TOGAF, data, prototype, and technical architecture from one page.
```

No implementation file is added in this phase.

### 4.4 Demo routes

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

Use Streamlit as an executable prototype only after the prototype design gate is approved.

### 5.2 MVP implementation order after the prototype gate

1. Convert Level-1 / Level-2 / Level-3 function architecture into prototype navigation and screen inventory.
2. Convert Level-1 / Level-2 / Level-3 data architecture into data dictionary and persistence plan.
3. Add Waterfall architecture page.
4. Add Founder navigation entry.
5. Convert pain points into editable persistent records.
6. Convert capabilities into configurable architecture records.
7. Fix Proof File and Report data lineage.
8. Later: migrate from Streamlit prototype to formal web architecture.

### 5.3 Next development tasks after the prototype gate

| Priority | Task | Result |
| --- | --- | --- |
| P0 | Three-level function dictionary | every feature has L1/L2/L3 code and owner |
| P0 | Three-level data dictionary | every data object has domain, subject and entity level |
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
功能分层清楚：一级功能、二级功能、三级功能 can guide future modules and screens.
数据分层清楚：一级数据域、二级数据主题、三级数据实体 can guide future schema and reports.
TOGAF 清楚：business, application, data, technology layers are traceable.
数据链路清楚：Proof File and report can trace back to evidence and review decisions.
原型清楚：screen purpose, input, output, action, approval and data visibility are defined.
技术清楚：Streamlit MVP and future production architecture are separated.
实现门禁清楚：prototype design approval before implementation changes.
```
