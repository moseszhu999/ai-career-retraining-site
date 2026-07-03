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

Correct waterfall sequence:

```text
战略分析
-> 痛点把握
-> 领域诊断桥：IS / TO-BE / Gap
-> TOGAF 分层功能架构
-> 三层数据架构
-> 原型设计
-> 技术架构
```

Important correction:

```text
痛点不是功能。
痛点只是输入信号。
功能必须来自这个领域的 TO-BE 目标能力。
数据必须来自 TO-BE 能力、流程、证据、指标和治理要求。
```

## 0.1 Pre-prototype implementation freeze

Before the prototype design phase is approved, this branch only produces analysis and architecture documents.

Allowed now:

```text
战略分析
痛点把握
领域 IS / TO-BE 分析
TOGAF 分层功能架构
三层数据架构
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

---

## 2. Pain-point grasp

Pain-point grasp is not a function list. It is the discovery input used to understand why the domain must change.

### 2.1 Pain matrix

| User | Pain signal | What it indicates |
| --- | --- | --- |
| Founder / business owner | Cannot tell which AI ideas are commercially valuable | The domain lacks value-chain automation diagnosis |
| Manager | Cannot measure AI readiness or delivery risk | The domain lacks readiness metrics and governance evidence |
| Operator / instructor | Cannot turn training into proof | The domain lacks task-to-evidence-to-proof conversion |
| Learner / employee | Cannot show credible AI work ability | The domain lacks approved proof files and work records |
| Customer / compliance | Cannot trust AI output without evidence | The domain lacks approval, visibility rules and audit trail |

### 2.2 Pain-to-architecture rule

Pain must be converted through a bridge before it becomes architecture.

```text
Pain signal
-> root cause
-> current-state IS
-> target-state TO-BE
-> capability gap
-> target function
-> target data
-> prototype requirement
```

---

## 3. Domain diagnosis bridge: IS / TO-BE / Gap

This is the missing bridge between pain and architecture.

### 3.1 Bridge model

| Step | Question | Output |
| --- | --- | --- |
| Pain signal | What hurts? | pain statement |
| Root cause | Why does it hurt? | domain weakness |
| IS | How does the domain work today? | current business/process/data/system state |
| TO-BE | How should the domain work after redesign? | target operating model |
| Gap | What is missing between IS and TO-BE? | capability, data, governance and system gaps |
| Architecture | What must be built or configured? | function architecture and data architecture |

### 3.2 Domain IS / TO-BE overview

| Domain aspect | IS current state | TO-BE target state | Gap to close |
| --- | --- | --- | --- |
| Business model | Selling training, demo or manual service is easy to understand but hard to scale | Selling AI Agent governance diagnosis, pilot and proof-based delivery package | productized service model and reusable delivery method |
| Customer entry | Customer pain is captured through conversation and founder judgment | Customer pain is converted into value-chain stage, scenario, expected outcome and pilot scope | structured intake and scenario classification |
| Work process | AI use is scattered across tools, people and tasks | AI work is organized as governed work steps with input, output, automation level and human checkpoint | work-step model and governance rules |
| Role and authority | Responsibility between AI, operator, reviewer and founder is implicit | Agent, operator, reviewer, founder and customer viewer have clear authority boundary | role and approval model |
| Evidence | Training output and task output are not consistently linked to evidence | Every important output can trace to evidence, review decision, proof candidate and approved proof file | evidence chain and version control |
| Data | Data exists as scattered customer, learner, task, score and report records | Data is layered by domain, subject and entity, and supports traceability from strategy to report | three-level data architecture |
| Reporting | Reports depend on manual selection and founder explanation | Internal and customer-safe reports are generated from approved evidence and visibility rules | metric model and report dataset |
| Compliance and trust | AI output may be useful but hard to explain and defend | Customer-visible output is controlled by approval, audit and visibility policy | audit and customer-safe field rules |

### 3.3 Scenario-level IS / TO-BE examples

| Scenario | IS | TO-BE | Required target capability |
| --- | --- | --- | --- |
| Lead-to-Proposal | Sales material and proposal drafting rely on founder experience | AI drafts customer profile, need summary and proposal outline; human approves commercial boundary | value-chain diagnosis, proposal evidence, claim boundary |
| Requirement-to-Delivery | Requirements, task output and acceptance evidence are fragmented | Requirements map to tasks, evidence, review and customer-safe delivery summary | scenario-to-task mapping and evidence trail |
| Training-to-Readiness | Training completion does not prove job readiness | Tasks, scores, review decisions and proof files produce readiness evidence | readiness evaluation and proof management |
| Support-to-Knowledge | Support answers are repeated and not converted into reusable knowledge | Issues become verified knowledge drafts with approval and audit | knowledge evidence and approval workflow |

---

## 4. TOGAF layered target functional architecture

The functional architecture below is not a pain list. It is the target capability structure required by the TO-BE domain.

### 4.1 Three-level target function architecture

#### 4.1.1 Level-1 target functions

| 一级功能 | TO-BE purpose | Derived from gap |
| --- | --- | --- |
| F1 Domain Diagnosis and Transformation Planning | Convert customer context into value-chain AI transformation plan | structured diagnosis gap |
| F2 Scenario and Process Architecture | Define target business scenario, process, role, input, output and exception path | process architecture gap |
| F3 Agent Work Design and Governance | Define AI Agent work step, automation level, authority and risk policy | AI work governance gap |
| F4 Task Execution and Evidence Capture | Convert work execution into structured task records and evidence | evidence capture gap |
| F5 Human Review, Approval and Escalation | Make human decision explicit and auditable | authority and accountability gap |
| F6 Proof, Readiness and Reporting | Convert evidence and review into proof files, readiness metrics and reports | proof and reporting gap |
| F7 Platform Operation and Audit | Manage clients, users, tasks, assignments, health and audit | scalable operation gap |

#### 4.1.2 Level-2 target functions

| 一级功能 | 二级功能 | TO-BE description |
| --- | --- | --- |
| F1 Domain Diagnosis and Transformation Planning | F1.1 Customer Context Modeling | define customer, industry, department, buyer and service context |
| F1 Domain Diagnosis and Transformation Planning | F1.2 Value-chain Opportunity Analysis | identify where AI Agent can create business value |
| F1 Domain Diagnosis and Transformation Planning | F1.3 Transformation Roadmap | define diagnosis, pilot, delivery and renewal path |
| F1 Domain Diagnosis and Transformation Planning | F1.4 Commercial Boundary Control | define claims, non-claims and customer-safe promise boundary |
| F2 Scenario and Process Architecture | F2.1 Scenario Definition | define target business scenario and expected outcome |
| F2 Scenario and Process Architecture | F2.2 Process Decomposition | decompose process into steps, roles, inputs and outputs |
| F2 Scenario and Process Architecture | F2.3 Exception Path Design | define abnormal cases, risk events and escalation path |
| F2 Scenario and Process Architecture | F2.4 KPI Design | define measurable business and readiness metrics |
| F3 Agent Work Design and Governance | F3.1 Agent Work-step Design | define AI Agent work unit and required context |
| F3 Agent Work Design and Governance | F3.2 Automation Level Assessment | assign R0 to R4 level and rationale |
| F3 Agent Work Design and Governance | F3.3 Authority Model | define reviewer, approver and final responsible role |
| F3 Agent Work Design and Governance | F3.4 Governance Policy | define risk class, evidence requirement and visibility rule |
| F4 Task Execution and Evidence Capture | F4.1 Task Template Design | define task, question, rubric and expected output |
| F4 Task Execution and Evidence Capture | F4.2 Assignment Execution | assign task to learner, employee or operator |
| F4 Task Execution and Evidence Capture | F4.3 Evidence Capture | capture answer, file, score, comment and source |
| F4 Task Execution and Evidence Capture | F4.4 Evidence Versioning | preserve version, timestamp and source record |
| F5 Human Review, Approval and Escalation | F5.1 Review Queue | route evidence to reviewer or founder |
| F5 Human Review, Approval and Escalation | F5.2 Review Decision | approve, revise, reject or escalate |
| F5 Human Review, Approval and Escalation | F5.3 Exception Management | identify weak point, high risk or missing evidence |
| F5 Human Review, Approval and Escalation | F5.4 Approval Audit | record reviewer, reason, timestamp and action |
| F6 Proof, Readiness and Reporting | F6.1 Proof Candidate Generation | identify evidence that may become proof |
| F6 Proof, Readiness and Reporting | F6.2 Proof File Approval | approve and package customer-visible proof |
| F6 Proof, Readiness and Reporting | F6.3 Readiness Metric Calculation | calculate completion, accuracy, exception and proof-ready rate |
| F6 Proof, Readiness and Reporting | F6.4 Report and Export | generate internal report, customer-safe report and export snapshot |
| F7 Platform Operation and Audit | F7.1 Client and Tenant Management | manage client, tenant, department, cohort and package |
| F7 Platform Operation and Audit | F7.2 User and Role Management | manage founder, operator, reviewer, learner and customer viewer |
| F7 Platform Operation and Audit | F7.3 Task Bank Management | manage task, MCQ, rubric and template library |
| F7 Platform Operation and Audit | F7.4 System Health and Audit | monitor health, permission and audit events |

#### 4.1.3 Level-3 target functions

Level-3 functions are future operation candidates. They are defined for prototype design, not implemented now.

| 二级功能 | 三级功能 examples |
| --- | --- |
| F1.1 Customer Context Modeling | create customer profile; tag industry; tag buyer role; define target department |
| F1.2 Value-chain Opportunity Analysis | select value-chain stage; record opportunity; estimate business value |
| F1.3 Transformation Roadmap | define diagnosis pack; define pilot pack; define delivery pack |
| F1.4 Commercial Boundary Control | mark allowed claim; mark prohibited claim; mark customer-safe statement |
| F2.1 Scenario Definition | create scenario; define outcome; define owner; define scope |
| F2.2 Process Decomposition | define step; define role; define input; define output |
| F2.3 Exception Path Design | define risk event; define exception path; define escalation trigger |
| F2.4 KPI Design | define metric; define formula; define owner; define report period |
| F3.1 Agent Work-step Design | create work step; define context; define expected AI output |
| F3.2 Automation Level Assessment | assign R0/R1/R2/R3/R4; record rationale; set upgrade condition |
| F3.3 Authority Model | set reviewer; set approver; set final authority; set customer visibility owner |
| F3.4 Governance Policy | classify risk; require evidence; define approval rule; define visibility rule |
| F4.1 Task Template Design | create task; create MCQ; create rubric; create answer key |
| F4.2 Assignment Execution | assign task; start task; submit task; mark completion |
| F4.3 Evidence Capture | store answer; store file metadata; store score; store comment |
| F4.4 Evidence Versioning | create evidence version; link source; lock approved version |
| F5.1 Review Queue | route to reviewer; filter pending; show missing evidence |
| F5.2 Review Decision | approve; revise; reject; escalate; record reason |
| F5.3 Exception Management | flag weak module; flag risk; request resubmission |
| F5.4 Approval Audit | record decision event; record before/after state; record actor |
| F6.1 Proof Candidate Generation | mark proof candidate; link evidence; set readiness reason |
| F6.2 Proof File Approval | approve proof; define public summary; define visible fields |
| F6.3 Readiness Metric Calculation | calculate completion rate; calculate accuracy; calculate proof-ready rate |
| F6.4 Report and Export | generate report snapshot; export dataset; mask customer-hidden fields |
| F7.1 Client and Tenant Management | create client; create cohort; set service package; set tenant scope |
| F7.2 User and Role Management | create user; assign role; assign permission scope; deactivate user |
| F7.3 Task Bank Management | create task template; edit rubric; classify difficulty; publish task |
| F7.4 System Health and Audit | view health; view audit log; check permission boundary |

### 4.2 Three-level target data architecture

The data architecture is not simply a list of tables. It is the TO-BE data foundation required to support target functions, evidence traceability, reporting and customer-safe delivery.

#### 4.2.1 Level-1 data domains

| 一级数据域 | Supports target function | Meaning |
| --- | --- | --- |
| D1 Customer and Commercial Context Data | F1 | customer, industry, buyer, package, commercial boundary |
| D2 Scenario and Process Data | F2 | scenario, process, step, role, input, output, exception |
| D3 Governance and Authority Data | F3 | work-step, automation level, authority, risk and policy |
| D4 Task and Execution Data | F4 | task template, assignment, answer, score and version |
| D5 Evidence and Review Data | F5 | evidence, review decision, exception and approval audit |
| D6 Proof, Readiness and Report Data | F6 | proof file, metric, report, export and customer-safe snapshot |
| D7 Platform Operation and Audit Data | F7 | tenant, client, user, role, task bank, health and audit event |

#### 4.2.2 Level-2 data subjects

| 一级数据域 | 二级数据主题 | Main contents |
| --- | --- | --- |
| D1 Customer and Commercial Context Data | D1.1 Customer Profile Data | customer, industry, department, buyer, target role |
| D1 Customer and Commercial Context Data | D1.2 Commercial Package Data | diagnosis pack, pilot pack, delivery pack, renewal input |
| D1 Customer and Commercial Context Data | D1.3 Boundary Data | allowed claim, prohibited claim, customer-safe statement |
| D2 Scenario and Process Data | D2.1 Business Scenario Data | scenario, objective, owner, value-chain stage |
| D2 Scenario and Process Data | D2.2 Process Step Data | step, role, input, output, dependency |
| D2 Scenario and Process Data | D2.3 Exception Path Data | risk event, escalation trigger, exception owner |
| D2 Scenario and Process Data | D2.4 KPI Definition Data | metric, formula, owner, period |
| D3 Governance and Authority Data | D3.1 Agent Work-step Data | AI work unit, context, expected output |
| D3 Governance and Authority Data | D3.2 Automation Level Data | R0-R4 level, rationale, upgrade condition |
| D3 Governance and Authority Data | D3.3 Authority Rule Data | reviewer, approver, final owner, permission scope |
| D3 Governance and Authority Data | D3.4 Governance Policy Data | risk class, evidence requirement, approval rule, visibility rule |
| D4 Task and Execution Data | D4.1 Task Template Data | task, question, rubric, answer key, difficulty |
| D4 Task and Execution Data | D4.2 Assignment Data | assignee, due date, status, completion |
| D4 Task and Execution Data | D4.3 Submission Data | answer, file metadata, score, comment |
| D4 Task and Execution Data | D4.4 Version Data | source, version, locked state, timestamp |
| D5 Evidence and Review Data | D5.1 Evidence Record Data | evidence, source, linked task, linked submission |
| D5 Evidence and Review Data | D5.2 Review Decision Data | decision, reason, reviewer, next action |
| D5 Evidence and Review Data | D5.3 Exception Data | missing evidence, weak module, high risk, resubmission |
| D5 Evidence and Review Data | D5.4 Approval Audit Data | actor, action, before/after state, timestamp |
| D6 Proof, Readiness and Report Data | D6.1 Proof Candidate Data | candidate, linked evidence, readiness reason |
| D6 Proof, Readiness and Report Data | D6.2 Proof File Data | approved proof, public summary, visible fields |
| D6 Proof, Readiness and Report Data | D6.3 Readiness Metric Data | completion, accuracy, exception rate, proof-ready rate |
| D6 Proof, Readiness and Report Data | D6.4 Report Snapshot Data | internal report, customer-safe report, export snapshot |
| D7 Platform Operation and Audit Data | D7.1 Tenant and Client Data | tenant, client, cohort, service package |
| D7 Platform Operation and Audit Data | D7.2 User and Role Data | founder, operator, reviewer, learner, customer viewer |
| D7 Platform Operation and Audit Data | D7.3 Task Bank Data | template library, module, difficulty, publication state |
| D7 Platform Operation and Audit Data | D7.4 System Audit Data | health check, permission event, audit event |

#### 4.2.3 Level-3 data entities and fields

| 二级数据主题 | 三级数据实体 | Representative fields |
| --- | --- | --- |
| D1.1 Customer Profile Data | EnterpriseClient | client_id, tenant_id, name, industry, department, buyer_role |
| D1.2 Commercial Package Data | ServicePackage | package_id, package_type, scope, deliverable, renewal_path |
| D1.3 Boundary Data | CommercialBoundary | boundary_id, claim_type, allowed_flag, customer_visible_flag |
| D2.1 Business Scenario Data | BusinessScenario | scenario_id, client_id, objective, value_chain_stage, owner |
| D2.2 Process Step Data | ProcessStep | step_id, scenario_id, role, input_data, output_data, dependency |
| D2.3 Exception Path Data | ExceptionPath | exception_id, trigger, risk_event, escalation_owner |
| D2.4 KPI Definition Data | KpiDefinition | kpi_id, name, formula_text, owner, report_period |
| D3.1 Agent Work-step Data | AgentWorkStep | work_step_id, scenario_id, context, expected_output |
| D3.2 Automation Level Data | AutomationAssessment | assessment_id, work_step_id, automation_level, rationale |
| D3.3 Authority Rule Data | AuthorityRule | rule_id, role, permission_scope, approval_action |
| D3.4 Governance Policy Data | GovernancePolicy | policy_id, risk_class, required_evidence, visibility_rule |
| D4.1 Task Template Data | TaskTemplate | task_id, module, prompt, rubric, answer_key, difficulty |
| D4.2 Assignment Data | Assignment | assignment_id, task_id, assignee_id, due_date, status |
| D4.3 Submission Data | Submission | submission_id, assignment_id, answer, score, comment |
| D4.4 Version Data | EvidenceVersion | version_id, source_id, version_no, locked_flag, timestamp |
| D5.1 Evidence Record Data | EvidenceRecord | evidence_id, submission_id, source, version_id, evidence_type |
| D5.2 Review Decision Data | ReviewDecision | decision_id, evidence_id, reviewer_id, decision, reason |
| D5.3 Exception Data | ReviewException | exception_id, evidence_id, exception_type, next_action |
| D5.4 Approval Audit Data | ApprovalAudit | audit_id, actor_id, action, before_state, after_state |
| D6.1 Proof Candidate Data | ProofCandidate | candidate_id, evidence_id, readiness_status, reason |
| D6.2 Proof File Data | ProofFile | proof_id, candidate_id, approved_by, public_summary, visible_fields |
| D6.3 Readiness Metric Data | ReadinessMetric | metric_id, cohort_id, metric_name, numerator, denominator, value |
| D6.4 Report Snapshot Data | ReportSnapshot | report_id, client_id, report_type, generated_at, masked_fields |
| D7.1 Tenant and Client Data | TenantContext | tenant_id, client_id, cohort_id, service_package, status |
| D7.2 User and Role Data | UserRoleProfile | user_id, role, cohort_id, permission_scope, status |
| D7.3 Task Bank Data | TaskBankItem | item_id, task_id, category, difficulty, publication_state |
| D7.4 System Audit Data | AuditEvent | event_id, actor_id, action, object_type, object_id, timestamp |

### 4.3 Function-data traceability matrix

Every future screen and implementation task must pass this traceability test.

| Trace level | Required mapping |
| --- | --- |
| Pain | pain only maps to root cause and IS / TO-BE analysis; it does not directly become a feature |
| IS / TO-BE | every target function must be justified by an IS weakness and a TO-BE target state |
| Level 1 | 一级功能 maps to one 一级数据域 |
| Level 2 | 二级功能 maps to one or more 二级数据主题 |
| Level 3 | 三级功能 maps to concrete 三级数据实体 and fields |
| Evidence | any report field must trace back to EvidenceRecord, ReviewDecision or approved ProofFile |
| Customer-safe output | any customer-visible field must have a visibility rule |
| Audit | any approval, export or proof action must produce an AuditEvent |

### 4.4 TOGAF architecture layer summary

| TOGAF layer | What it contains in this project |
| --- | --- |
| Business architecture | IS / TO-BE model, target operating model, three-level target functions |
| Application architecture | future modules and screens derived from TO-BE functions, not from raw pain points |
| Data architecture | three-level target data domains, subjects, entities, evidence chain and report measures |
| Technology architecture | runtime, persistence, permission, export, deployment and observability plan |

---

## 5. Prototype design

### 5.1 Prototype design gate

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

Prototype design must also show which IS / TO-BE gap, Level-1 / Level-2 / Level-3 function and data level each screen belongs to.

### 5.2 Prototype navigation requirement

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

### 5.3 Proposed future screen

```text
Waterfall Architecture
```

Purpose:

```text
Show the complete waterfall method inside the live product.
Make the founder demo explain strategy, pain, IS, TO-BE, gap, TOGAF, data, prototype, and technical architecture from one page.
```

No implementation file is added in this phase.

---

## 6. Technical architecture and implementation plan

### 6.1 Current implementation decision

Use Streamlit as an executable prototype only after the prototype design gate is approved.

### 6.2 MVP implementation order after the prototype gate

1. Convert IS / TO-BE / Gap analysis into prototype navigation and screen inventory.
2. Convert Level-1 / Level-2 / Level-3 target function architecture into feature dictionary.
3. Convert Level-1 / Level-2 / Level-3 target data architecture into data dictionary and persistence plan.
4. Add Waterfall architecture page.
5. Add Founder navigation entry.
6. Convert scenario, governance, evidence and report objects into editable persistent records.
7. Fix Proof File and Report data lineage.
8. Later: migrate from Streamlit prototype to formal web architecture.

### 6.3 Next development tasks after the prototype gate

| Priority | Task | Result |
| --- | --- | --- |
| P0 | IS / TO-BE dictionary | every future feature is justified by current-state weakness and target-state need |
| P0 | Three-level target function dictionary | every feature has L1/L2/L3 code and owner |
| P0 | Three-level target data dictionary | every data object has domain, subject and entity level |
| P1 | Scenario-to-task mapping | every task traces to a business scenario |
| P1 | Governance and authority schema | automation level, risk, approval and visibility become configurable |
| P1 | Evidence and approval schema | proof/report source becomes auditable |
| P2 | Customer report portal | customer-safe output separated from internal data |
| P2 | Formal API and frontend | move beyond Streamlit demo |

---

## 7. Acceptance checklist

The rebuild is acceptable when:

```text
战略口径清楚：not course, not AI tool demo, but Agent governance and proof OS.
痛点边界清楚：pain is input, not function.
桥接层清楚：pain -> root cause -> IS -> TO-BE -> gap -> architecture.
IS / TO-BE 清楚：current state and target state are listed by domain aspect.
功能分层清楚：一级功能、二级功能、三级功能 are target capabilities derived from TO-BE.
数据分层清楚：一级数据域、二级数据主题、三级数据实体 support target capabilities and reports.
TOGAF 清楚：business, application, data, technology layers are traceable.
数据链路清楚：Proof File and report can trace back to evidence and review decisions.
原型清楚：screen purpose, input, output, action, approval and data visibility are defined.
技术清楚：Streamlit MVP and future production architecture are separated.
实现门禁清楚：prototype design approval before implementation changes.
```
