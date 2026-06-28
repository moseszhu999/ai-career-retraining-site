# AI Skill Growth OS - Scenario Interaction Flows

Version: v4.6 planning draft

## 0. Why this document exists

The current frontend already explains the product, but it still feels like a slide deck because the user has not yet experienced a real interaction loop.

The next product step is not more copywriting. The next step is to define what happens after a customer logs in:

```text
login -> see my state -> do today's task -> save draft -> get feedback -> submit -> wait for review -> receive next action -> portfolio proof
```

The product must move from presentation pages to an interactive workflow.

---

## 1. Core product loop

```text
Customer login
  -> Home dashboard
  -> Today's task
  -> Draft / upload work
  -> AI feedback
  -> Revise
  -> Submit to Agent
  -> Agent review
  -> Status update
  -> Portfolio candidate
  -> Consult / next training plan
```

This is the product's real value loop.

A page is not complete unless it answers:

1. Who is logged in?
2. What state is this user currently in?
3. What is the next action?
4. What data changes after the action?
5. Who handles the next step: user, Agent, or Founder?

---

## 2. Login and role scenes

### 2.1 Visitor scene

Before login, a visitor should see:

- What the product is
- Who it is for
- What result they can get
- CTA: start demo / request consult / login

Visitor can:

- View public product explanation
- Generate a consult summary
- Submit consult lead later
- Enter demo mode

Visitor cannot:

- Save drafts
- See private tasks
- See portfolio details tied to a real user
- Access Founder Console

### 2.2 Student scene

After student login, the student should see:

- Welcome message
- Current training package
- Today's task
- Progress
- Latest Agent feedback
- Portfolio status
- Next action

Student can:

- View own tasks
- Save draft
- Request AI feedback
- Submit to Agent
- View Agent review
- View own portfolio
- Submit consult / upgrade request

Student cannot:

- See backend table names
- See other students
- See Founder operations
- Change scores manually

### 2.3 Founder scene

After Founder login, Founder should see:

- Pending reviews
- Quality exceptions
- Portfolio candidates
- New consult leads
- Daily summary

Founder can:

- Review exceptions
- Approve portfolio items
- Override Agent decision
- Mark consult lead status
- Trigger daily summary

Founder should not:

- Manually review every normal task
- Browse all raw records unless needed
- Mix with student frontstage navigation

---

## 3. Main customer login flow

### Flow A: First login

```text
1. Customer opens product URL.
2. Customer selects login / demo access.
3. System asks for name or access code.
4. System identifies role: visitor / student / founder.
5. Student lands on Home dashboard.
6. Dashboard shows current state:
   - current training path
   - current day
   - today's task
   - last feedback
   - portfolio count
7. Main CTA: Continue today's task.
```

Required page behavior:

- If no user selected: show visitor landing.
- If student selected: show student dashboard.
- If founder selected: expose Founder Console entry.

Current Streamlit implementation can use `st.session_state` first before real auth.

---

## 4. Student task interaction flow

### Flow B: Do today's task

```text
1. Student enters My Tasks.
2. System highlights today's active task.
3. Student reads task goal, output, and standard.
4. Student writes draft.
5. Student clicks Save Draft.
6. System confirms saved state.
7. Status becomes In Progress.
```

Data change later:

```text
task_instances.draft = draft_text
task_instances.status = 进行中
task_instances.updated_at = now()
```

UI change now:

- Show saved confirmation.
- Show draft word count.
- Enable Request AI Feedback.

### Flow C: Request AI feedback

```text
1. Student clicks Request AI Feedback.
2. System reads task standard + draft.
3. Feedback Agent returns improvement suggestions.
4. UI shows feedback in right-side panel.
5. Student revises draft.
```

Data change later:

```text
agent_runs insert
feedbacks insert or task_instances.ai_feedback update
task_instances.status = AI已反馈
```

UI change now:

- Simulate feedback using demo logic.
- Show status chip: AI已反馈.
- Show next action: revise and submit.

### Flow D: Submit to Agent

```text
1. Student clicks Submit to Agent.
2. System locks current draft version.
3. Status becomes 待Agent点评.
4. Founder/Agent queue receives item.
5. Student sees waiting state.
```

Data change later:

```text
task_instances.status = 待Agent点评
task_instances.submitted_at = now()
```

UI change now:

- Show confirmation.
- Disable repeated submit or show submitted state.
- Tell student what happens next.

---

## 5. Agent review flow

### Flow E: Agent review

```text
1. Agent reads task template.
2. Agent reads submitted draft.
3. Agent generates review:
   - score
   - conclusion
   - strengths
   - issues
   - next action
   - portfolio recommendation
4. System writes review.
5. Task status becomes Agent已点评 or 需修改.
```

Data change later:

```text
reviews insert
task_instances.score update
task_instances.teacher_review update
task_instances.status update
agent_runs insert
```

UI change for student:

- Show review result.
- Show score.
- Show next action.
- If portfolio-ready, show portfolio candidate.

UI change for Founder:

- Only exceptions appear.
- Low quality review appears in quality queue.
- Portfolio candidate appears in portfolio queue.

---

## 6. Portfolio interaction flow

### Flow F: Portfolio candidate

```text
1. Task receives good score or Founder approval.
2. System marks it as portfolio candidate.
3. Student sees it in Portfolio page.
4. Student opens detail page.
5. System shows:
   - background
   - method
   - result
   - evidence
   - Agent review summary
6. Student can export/share later.
```

Data change later:

```text
portfolio_items insert or task_instances.portfolio = true
```

UI change now:

- Show portfolio item state.
- Let user select a portfolio item.
- Show proof structure.
- Show export/share placeholders.

---

## 7. Consult interaction flow

### Flow G: Consult after product experience

```text
1. Visitor or student enters Consult.
2. User selects identity and goal.
3. System recommends package:
   - Personal Growth
   - Freelancer
   - Enterprise Training
4. User fills name/contact/note.
5. System generates consult summary.
6. Later: save lead and notify Founder.
```

Data change later:

```text
consult_leads insert
founder_actions insert or notification trigger
```

UI change now:

- Recommendation updates immediately based on user choices.
- Summary generated on submit.
- Placeholder: save lead / book call / notify Founder.

---

## 8. Founder interaction flow

### Flow H: Founder daily operation

```text
1. Founder opens Founder Console.
2. System shows four queues:
   - Pending Agent review
   - Quality exceptions
   - Portfolio candidates
   - Consult leads
3. Founder handles only decisions:
   - approve portfolio
   - request revision
   - mark lead contacted
   - override Agent review
4. Founder reads daily summary.
```

Founder Console should not be a full database admin page.

It should be a decision cockpit:

```text
What needs my decision today?
```

---

## 9. Immediate implementation plan

### v4.6.0: Session-based demo interaction

Goal:

Make the frontend feel interactive before real database integration.

Implementation:

- Add `st.session_state` user mode:
  - visitor
  - student
  - founder
- Add login/demo panel.
- Store draft in session.
- Store task status in session.
- Simulate AI feedback.
- Simulate submit-to-Agent state.
- Simulate portfolio candidate.

No Supabase yet.

### v4.6.1: Real draft persistence

- Connect Save Draft to Supabase.
- Update task_instances.draft.
- Update status.

### v4.6.2: Real AI feedback

- Add Feedback Agent.
- Save feedback.
- Write agent_runs.

### v4.6.3: Real Founder queue

- Founder Console reads waiting tasks.
- Founder sees consult leads.
- Founder sees portfolio candidates.

---

## 10. Key design rule

Do not add more explanation-only pages.

Every new page must include at least one real or simulated interaction:

```text
select -> edit -> save -> feedback -> submit -> status change
```

For the next coding step, implement the session-based demo interaction first.

This gives the product a real feeling without waiting for backend readiness.
