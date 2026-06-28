# AI Skill Growth OS - Product First Architecture

Version: v4.4 draft

## 0. Current strategic focus

Current priority is product clarity, not backend complexity.

The system should first become a clear, usable product:

- Student sees only: Home / My Tasks / Portfolio / Consult.
- Agent handles high-frequency feedback and review.
- Founder sees only exceptions, quality issues, portfolio candidates, and daily operations.
- Database tables, SQL, RLS, SOP, and admin language must not appear in the normal student flow.

Product sentence:

> One entry, four actions: task, feedback, portfolio, consult.

Operating sentence:

> Student completes tasks; Agent gives feedback; portfolio records proof; Founder manages exceptions.

---

## 1. Product scenarios

### Scenario A: Individual student growth

Target users:

- New graduates
- Working employees
- People preparing for promotion
- People preparing to switch jobs
- People who need a demonstrable skill portfolio

Core user story:

> I do not want to browse a course backend. I want to know what I should do today, submit a draft, get feedback, revise it, and finally have something I can show.

Core flow:

1. User lands on Home.
2. User enters My Tasks.
3. User sees today's task card.
4. User writes or uploads a draft.
5. User asks AI/Agent for feedback.
6. User revises.
7. Agent/Founder approves portfolio entry.
8. Portfolio becomes proof of learning.

### Scenario B: Freelancer / one-person company skill monetization

Target users:

- Freelancers
- Side-project workers
- Small business owners
- People who want to package a skill into a service

Core user story:

> I need to turn a skill into a sellable service package and produce examples that customers can understand.

Core flow:

1. Choose service direction.
2. Complete service package task.
3. Generate sample case.
4. Get Agent feedback.
5. Turn the result into portfolio/service proof.
6. Use consult page for sales conversion.

### Scenario C: Founder operating as a one-person AI education company

Target user:

- Founder / owner

Core user story:

> I do not want to manually review every student every day. I only want to see what needs my decision.

Core flow:

1. Agent reviews pending submissions.
2. Agent quality-checks its own reviews.
3. System marks low-score, short-draft, abnormal, or portfolio-candidate tasks.
4. Founder Console shows only exceptions and daily summary.
5. Founder handles product, sales, quality, and high-value cases.

---

## 2. Application architecture

### 2.1 Application zones

The product should be split into three application zones.

```text
AI Skill Growth OS
├── Student Frontstage
│   ├── Home
│   ├── My Tasks
│   ├── Portfolio
│   └── Consult
├── Agent Middle Office
│   ├── Feedback Agent
│   ├── Review Agent
│   ├── Quality Agent
│   └── Portfolio Agent
└── Founder Backstage
    ├── Founder Console
    ├── Daily Summary
    ├── Exception Queue
    └── Quality / Portfolio Decisions
```

### 2.2 Student Frontstage

Goal: make the product feel simple.

Screens:

1. Home
   - Product explanation
   - Current progress
   - Main CTA: continue today's task

2. My Tasks
   - Task timeline
   - Today's task card
   - Draft area
   - Request feedback
   - Submit to Agent

3. Portfolio
   - Approved works
   - Score / status
   - Proof material
   - Export/share later

4. Consult
   - User identity
   - User goal
   - Need summary
   - Lead capture / download / webhook later

Rules:

- Do not expose table names.
- Do not expose SQL or RLS.
- Do not show admin/ops concepts.
- Every screen must answer: what should the user do next?

### 2.3 Agent Middle Office

Goal: make Agent do the high-frequency work.

Agent modules:

1. Feedback Agent
   - Reads draft
   - Gives immediate suggestions
   - Does not need final scoring

2. Review Agent
   - Reads task standard + draft
   - Produces score, conclusion, review text
   - Writes review record
   - Updates task status

3. Quality Agent
   - Checks if review is too short, too generic, or inconsistent
   - Flags risky cases
   - Sends exceptions to Founder Console

4. Portfolio Agent
   - Decides whether a task is portfolio-ready
   - Suggests proof title and proof summary
   - Founder can approve or override

### 2.4 Founder Backstage

Goal: keep the founder out of repetitive work.

Founder screens:

1. Founder Console
   - Pending Agent review
   - Pending quality check
   - Portfolio candidates
   - Risk queue

2. Daily Summary
   - New submissions
   - Agent-reviewed tasks
   - Low-score tasks
   - Portfolio-ready works
   - Suggested founder actions

3. Exception Queue
   - Low score
   - Short draft
   - Short feedback
   - Repeated failure
   - High-value user

Rules:

- Founder Console must remain owner-gated.
- Founder Console should not appear in normal user navigation.
- Founder only handles exceptions and product decisions.

---

## 3. Data architecture

### 3.1 Core data domains

```text
User / Enrollment Domain
├── students
├── enrollments
└── access / passcode later

Learning Domain
├── courses
├── task_templates
└── task_instances

Agent Review Domain
├── feedbacks
├── reviews
├── quality_checks
└── agent_runs

Portfolio Domain
├── portfolio_items
└── portfolio_evidence

Founder Ops Domain
├── daily_summaries
├── risk_flags
└── founder_actions

Lead / Sales Domain
├── consult_leads
└── lead_notes
```

### 3.2 Current minimum tables

Current Supabase tables already used or planned:

1. `courses`
   - Defines product/course package.

2. `task_templates`
   - Defines reusable training tasks.

3. `enrollments`
   - Connects student with a course.

4. `task_instances`
   - Actual student task records.

5. `reviews`
   - Agent or human review records.

These are enough for the current product-first stage.

### 3.3 Next necessary tables

For product maturity, add later:

1. `portfolio_items`

Purpose: separate approved portfolio proof from raw tasks.

Suggested fields:

- portfolio_id
- student
- task_instance_id
- title
- summary
- score
- proof_type
- status
- approved_by
- created_at

2. `agent_runs`

Purpose: record every Agent action.

Suggested fields:

- run_id
- agent_type
- input_ref
- output_ref
- status
- model
- token_cost
- created_at

3. `quality_checks`

Purpose: inspect Agent output quality.

Suggested fields:

- check_id
- review_id
- score
- issues
- risk_level
- action_required
- created_at

4. `consult_leads`

Purpose: persist consult form submissions.

Suggested fields:

- lead_id
- name
- contact
- identity
- goal
- note
- source
- status
- created_at

### 3.4 Product-facing data rule

Internal data names and product labels must be separated.

Examples:

```text
task_instances  -> 我的任务
reviews         -> Agent反馈
portfolio_items -> 作品集
consult_leads   -> 咨询记录
quality_checks  -> 质检结果
agent_runs      -> Agent运行记录
```

The UI should always show product labels, not database names.

---

## 4. Technical architecture

### 4.1 Current practical architecture

The current stack should stay simple:

```text
Browser
  ↓
Streamlit Frontend
  ↓
Supabase Client
  ↓
Supabase Postgres
```

Current good choice:

- Streamlit is fast for product iteration.
- Supabase is enough for data persistence.
- GitHub is enough for version control.
- Founder can manually redeploy through Streamlit Cloud.

Do not over-engineer yet.

### 4.2 Target modular architecture

```text
Frontend Layer
├── Student UI
├── Portfolio UI
├── Consult UI
└── Founder Console UI

Application Service Layer
├── Task Service
├── Feedback Service
├── Review Service
├── Portfolio Service
├── Lead Service
└── Founder Ops Service

Agent Layer
├── Feedback Agent
├── Review Agent
├── Quality Agent
└── Founder Daily Agent

Data Layer
├── Supabase Postgres
├── Storage later
└── Analytics later

External Integration Layer
├── Email / webhook
├── Payment later
├── LLM API later
└── Export/share later
```

### 4.3 Technical evolution path

Stage 1: Product-first Streamlit

- Keep one clean default product frontend.
- Keep Founder Console separate.
- Use mock data where needed.
- Avoid complex login.

Stage 2: Real data connection

- Connect My Tasks to `task_instances`.
- Connect Portfolio to `portfolio_items` or portfolio=true tasks.
- Connect Consult to `consult_leads` or webhook.

Stage 3: Owner-only security

- Add owner passcode for Founder Console.
- Add minimal student access code.
- Avoid full auth until product flow is stable.

Stage 4: Agent automation

- Add real LLM feedback.
- Add agent run logs.
- Add quality check agent.
- Add daily founder summary.

Stage 5: SaaS hardening

- Multi-user / multi-tenant model.
- Payment.
- Email notification.
- Export portfolio.
- Analytics dashboard.

---

## 5. Product-first roadmap

### v4.4 - Product unification

Goal:

- One default product homepage.
- One student task flow.
- One portfolio flow.
- One consult flow.
- One Founder Console.

Tasks:

1. Keep default app clean.
2. Remove duplicate experiment pages.
3. Standardize product language.
4. Keep backend hidden from users.
5. Write architecture blueprint.

### v4.5 - Real task data

Goal:

- Replace mock tasks with real Supabase `task_instances`.

Tasks:

1. Add student selector or access code.
2. Load tasks by student.
3. Save draft.
4. Request AI feedback.
5. Submit to Agent review.

### v4.6 - Real portfolio

Goal:

- Portfolio should come from approved task results.

Tasks:

1. Create `portfolio_items` table.
2. Convert approved tasks into portfolio items.
3. Show portfolio in product UI.
4. Add export/share structure.

### v4.7 - Founder OS

Goal:

- Founder only sees exceptions and daily decisions.

Tasks:

1. Improve Founder Console.
2. Add quality checks.
3. Add risk queue.
4. Add daily summary.

---

## 6. Design principle

Do not build from database outward.

Build from scenario inward:

```text
Scenario → User action → Product screen → Application service → Data table → Agent automation
```

Every new feature must answer:

1. Which scenario does it serve?
2. Which user sees it?
3. What action does the user take?
4. What data does it create or update?
5. Does Agent or Founder handle the next step?

If a feature cannot answer these five questions, do not build it yet.
