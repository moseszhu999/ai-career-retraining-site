# AI Agent Delivery Readiness OS

Formerly: AI Skill Growth Education Platform.

Current strategic positioning:

```text
AI Agent 交付能力证明系统
```

The project is evolving from a generic AI skill growth / coding training site into an operations system for training employees to safely supervise AI coding agents in real enterprise delivery tasks.

## Streamlit deploy settings

Use Streamlit Community Cloud with:

```text
Repository: moseszhu999/ai-career-retraining-site
Branch: main
Main file path: streamlit_app.py
Python: 3.12
```

## Current product line

The product is no longer positioned as a Java / HTML / coding course.

It is positioned as:

```text
AI Agent Delivery Readiness OS
```

Chinese product statement:

```text
帮助企业训练员工安全使用 Claude Code / Codex / Cursor 等 AI 编程 Agent 完成真实软件交付，并通过可审计 Proof Files 证明交付监督能力。
```

## Core market insight

AI coding agents will compress low-level coding work. The enterprise problem is shifting from:

```text
Can this person write code?
```

to:

```text
Can this person safely supervise AI-generated code in a real enterprise repository?
```

The system therefore focuses on proving:

```text
business understanding
agent task brief quality
repository context and constraints
diff review accuracy
test / verification completeness
security / permission / data risk detection
merge / reject / revise judgment
customer-safe explanation
```

## Current operating loop

```text
Client / Cohort / Learner
-> Agent Delivery Assignment
-> Agent Task Brief
-> AI Agent Output
-> Learner Diff Review
-> Verification Evidence
-> Agent Delivery Review
-> Proof-of-Agent-Work File
-> Customer Safe Delivery Pack
-> Leads / Expansion
-> Audit
```

## Latest implementation milestones

```text
v4.10.2 Customer Safe Delivery Pack
v4.11.0 Database Foundation / Supabase Migration Contract
v4.11.1 Repository Read Layer
v4.12.0 AI Agent Delivery Readiness Strategy
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

The Streamlit demo still defaults to session DataFrames. Supabase is introduced as the next backend target, not as a breaking runtime dependency.

## Primary customer

First beachhead:

```text
Enterprise software delivery teams with legacy Java / Web / SQL systems.
```

Especially suitable for:

```text
Japan-facing offshore delivery teams
Java / Spring / MyBatis / SQL maintenance projects
new-hire onboarding
AI coding tool adoption programs
quality and delivery managers who need evidence, not course completion
```

## What this business sells

Do not sell this as:

```text
Java course
HTML course
prompt course
AI tool demo
```

Sell this as:

```text
reduced AI-generated delivery risk
faster new-hire readiness
auditable proof of AI-supervised software work
customer-safe delivery reports
repeatable enterprise task library
```

## Product packaging

### 5-Day AI Agent Delivery Bootcamp

Goal:

```text
Show one complete AI-supervised delivery cycle and generate one Proof-of-Agent-Work File.
```

### 4-Week AI Agent Delivery Readiness Cohort

Goal:

```text
Train a small cohort to handle repeated AI-assisted maintenance tasks with increasing complexity.
```

### 12-Week Enterprise AI Delivery Operating System

Goal:

```text
Build an internal company workflow for safe AI coding agent adoption.
```

## Proof-of-Agent-Work File

A Proof File should prove supervision quality, not just output quality.

Required sections:

```text
1. Business request
2. Agent tool used
3. Agent task brief
4. Repository context and constraints
5. Diff summary
6. Verification evidence
7. Risk checklist result
8. Human corrections
9. Final merge / reject / revise decision
10. Customer-safe delivery explanation
11. Reviewer score and comments
```

## Core KPI

Old KPI:

```text
How many learners submitted coding homework?
```

New KPI:

```text
How many learners can safely supervise an AI coding agent through a real delivery task?
```

Core metrics:

```text
Agent Task Brief Quality
Context Constraint Quality
Diff Review Accuracy
Verification Completeness
Risk Detection Rate
Customer Explanation Quality
Proof-of-Agent-Work Ready Rate
```

## Product resource library

The repository includes a unified resource index:

```text
product_resource_library.md
```

Use it as the main navigation document for:

```text
sales
lead follow-up
two-hour trial lesson delivery
5-day skill growth camp
5-day freelance monetization camp
enterprise AI training
compliance boundaries
```

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
We do not teach employees to generate more code.
We train employees to safely turn AI-generated code into enterprise-acceptable delivery.
```
