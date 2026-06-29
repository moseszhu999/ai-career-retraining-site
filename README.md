# AI Agent Governance & Readiness OS

Formerly:

```text
AI Skill Growth Education Platform
AI Agent Delivery Readiness OS
```

Current strategic positioning:

```text
企业 AI Agent 治理与能力证明系统
```

The project is evolving from coding training and AI Agent supervision into an enterprise operating system for making AI Agent work governable, auditable, and accountable.

## Streamlit deploy settings

Use Streamlit Community Cloud with:

```text
Repository: moseszhu999/ai-career-retraining-site
Branch: main
Main file path: streamlit_app.py
Python: 3.12
```

## Current product line

The product is no longer positioned as a Java / HTML / coding course, and it should not remain limited to AI Agent supervision.

It is positioned as:

```text
AI Agent Governance & Readiness OS
```

Chinese product statement:

```text
帮助企业定义、授权、验证、审批和审计 AI Agent 如何进入真实工作流，并通过 Proof Files 证明员工与岗位的 AI Agent 协同能力。
```

## Core market insight

Low-level coding and routine Agent supervision will both be compressed by more capable agents. The long-term enterprise problem is shifting from:

```text
Can this person supervise AI output?
```

to:

```text
Can this enterprise safely let AI Agent work enter formal business workflows?
```

The system therefore focuses on proving and governing:

```text
task eligibility
human authority level
Agent work request
verification evidence
risk classification
approval rule
approval decision
responsibility chain
audit record
readiness score
manager / customer report
```

## Current operating loop

```text
Business task
-> Agent eligibility rule
-> Human authority level
-> Agent work request
-> Agent output
-> Verification evidence
-> Risk classification
-> Approval / reject / revise / escalate
-> Audit record
-> Proof File
-> Manager / Customer Report
```

## Latest implementation milestones

```text
v4.10.2 Customer Safe Delivery Pack
v4.11.0 Database Foundation / Supabase Migration Contract
v4.11.1 Repository Read Layer
v4.12.0 AI Agent Delivery Readiness Strategy
v4.13.0 AI Agent Governance & Readiness Strategy
```

v4.10.2 separates internal delivery packs from customer-safe delivery packs. Customer-facing exports use a field whitelist and hide internal notes, raw audit logs, Founder/Agent operation details, contract value, and potential lead value.

v4.11.0 adds the durable SaaS migration foundation:

```text
supabase/schema_v4_11.sql
frontend/data_repository.py
docs/v4_11_database_migration_plan.md
```

v4.11.1 migrates Reports and Exports to the repository read layer:

```text
docs/v4_11_1_repository_read_layer.md
```

v4.12.0 adds the AI Agent Delivery Readiness pivot:

```text
docs/v4_12_agent_delivery_readiness_strategy.md
docs/agent_delivery_task_spec_v4_12.md
supabase/agent_delivery_extension_v4_12.sql
```

v4.13.0 adds the governance layer:

```text
docs/v4_13_agent_governance_readiness_strategy.md
supabase/agent_governance_extension_v4_13.sql
```

The Streamlit demo still defaults to session DataFrames. Supabase is introduced as the next backend target, not as a breaking runtime dependency.

## Primary customer

First beachhead remains narrow, but the architecture is wider.

Initial wedge:

```text
Enterprise software delivery teams with legacy Java / Web / SQL systems.
```

Expanded governance market:

```text
software / IT delivery
business analysis / PMO
sales / service operations
HR / training readiness
customer support / knowledge work
supply chain / operations workflows
```

## What this business sells

Do not sell this as:

```text
Java course
HTML course
prompt course
AI tool demo
Claude Code tutorial
Codex training camp
generic productivity bootcamp
```

Sell this as:

```text
Agent governance policy templates
role-based authority model
risk and approval workflow
audit evidence store
manager readiness dashboard
customer-safe governance reports
Proof Files for AI-supervised enterprise tasks
```

## Governance concepts

### Agent Eligibility

```text
Agent Allowed
Agent Allowed With Human Review
Senior Approval Required
Manual Only
Restricted / Regulated
```

### Human Authority Level

```text
L0 Observer
L1 Assisted Operator
L2 Supervised Operator
L3 Trusted Operator
L4 Approver
L5 Release Owner
```

### Risk Level

```text
Low
Medium
High
Critical
```

### Approval Rule

```text
auto-log only
human review required
senior approval required
security review required
customer approval required
manual-only / no Agent use
```

## Starter verticals

### 1. Software / IT Delivery Governance

Focus:

```text
diff review
test evidence
security / permission / data risk
merge decision
release responsibility
```

### 2. Business / PM Governance

Focus:

```text
fact accuracy
missing stakeholder checks
deadline / owner correctness
customer-safe wording
escalation judgment
```

### 3. Sales / Service Governance

Focus:

```text
claim compliance
price / scope boundary
customer need fit
next-action clarity
no guarantee wording
```

### 4. HR / Training Governance

Focus:

```text
evidence-based evaluation
no fake certification
fairness / privacy
manager decision support
```

## Proof File

A Proof File should prove not only output quality or supervision quality, but also governance quality.

Required sections:

```text
1. Business task
2. Agent eligibility rule
3. Human authority level
4. Agent work request
5. Agent output summary
6. Verification evidence
7. Risk classification
8. Human correction notes
9. Approval / reject / revise / escalate decision
10. Responsible person / role
11. Customer-safe or manager-safe explanation
12. Reviewer score and comments
```

## Core KPI

Old KPI:

```text
How many learners can supervise an AI coding agent?
```

New KPI:

```text
How many employees can safely move Agent work through enterprise policy, evidence, approval, and accountability?
```

Core metrics:

```text
Agent Task Eligibility Accuracy
Authority Level Fit
Verification Completeness
Risk Classification Accuracy
Approval Decision Quality
Audit Evidence Completeness
Customer / Manager Explanation Quality
Governance-Ready Proof File Rate
```

## Product resource library

The repository includes a unified resource index:

```text
product_resource_library.md
```

Use it as the main navigation document for sales, lead follow-up, trial delivery, enterprise AI training, and compliance boundaries.

## Optional Streamlit Secrets

Feishu / Lark robot:

```toml
LEAD_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
WEBHOOK_PROVIDER = "feishu"
OWNER_EMAIL = "your-email@example.com"
```

WeCom / Enterprise WeChat robot:

```toml
LEAD_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"
WEBHOOK_PROVIDER = "wecom"
OWNER_EMAIL = "your-email@example.com"
```

Generic backend API, Tencent Cloud Function, Alibaba Cloud Function, Supabase, etc.:

```toml
LEAD_WEBHOOK_URL = "https://your-api-endpoint"
WEBHOOK_PROVIDER = "generic"
OWNER_EMAIL = "your-email@example.com"
```

If `LEAD_WEBHOOK_URL` is not configured, the site still works, but leads must be downloaded as TXT/CSV or sent manually.

## Compliance boundary

Do not sell this as:

```text
K12 tutoring
official certificate
guaranteed employment
salary guarantee
guaranteed freelance income
regulated professional qualification training
```

## Strategic claim

```text
We do not merely train employees to supervise AI.
We help enterprises make AI Agent work governable, auditable, and accountable.
```
