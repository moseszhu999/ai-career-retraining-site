# v5.1 / v5.2 Acceptance Path

This is the fastest manual acceptance path for the usable website direction.

## 1. Founder enters Admin

Login as Founder, then open:

```text
Admin/Health
```

Expected:

```text
Health Check visible
Backend mode visible
Tenant visible
Client / Cohort / Learner / Exercise tabs visible
```

## 2. Create real master data

Create in this order:

```text
Client
Cohort
Learner
MCQ Exercise
```

Expected:

```text
Rows appear after save
Rows remain after Streamlit rerun in session mode
Rows write to Supabase when DATA_BACKEND is supabase
```

## 3. Assign exercise

Open Admin/Health -> Assignment tab.

Expected:

```text
Select cohort
Select learner
Select exercise
Create assignment
Assignment appears in Assignment table
```

## 4. Founder task console

Open:

```text
练习题
```

Expected:

```text
Production Task Console opens
Uses Admin-created cohort / learner / exercise
Can assign
Can submit answer
Can generate Agent Review
Learner records table updates
```

## 5. Review Queue

Open:

```text
Review Queue
```

Expected:

```text
Submitted MCQ appears
Review route is visible
Founder can confirm Proof or request resubmission
```

## 6. Proof Files

Open:

```text
Proof Files
```

Expected:

```text
Confirmed records generate Proof File
Proof can be used for report/export
```

## 7. Executable Flow

Open:

```text
Executable Flow
```

Expected:

```text
Create flow for client/cohort
Advance status chain:
draft -> configured -> assigned -> submitted -> agent_reviewed -> human_reviewing -> approved -> proof_ready -> exported
Status board updates
```

## Current boundary

v5.1 production master data is the main persistent layer.
v5.2 flow runtime is executable and session-backed first; Supabase table schema is prepared in `docs/supabase_schema_v5_2_flow.sql`.

## Next hardening

```text
1. Persist flow runtime loading from Supabase
2. Make learner portal use only assigned exercises
3. Add real login and role isolation
4. Add customer portal report view
5. Deploy with production secrets
```
