# v5.3 Deployment Checklist

## App entries

Main app:

```text
streamlit_app.py
```

Portal pages:

```text
pages/Customer_Portal.py
pages/Learner_Portal.py
```

## Database setup

Run these SQL files in order:

```text
docs/supabase_schema_v5_1.sql
docs/supabase_schema_v5_2_flow.sql
```

## Founder acceptance path

```text
Login as Founder
Open Admin/Health
Create Client
Create Cohort
Create Learner
Create MCQ Exercise
Assign Exercise
Open Tasks
Submit and generate Agent Review
Open Review Queue
Confirm Proof
Open Proof Files
Open Reports / Exports
Open Executable Flow
Move a flow through the status chain
```

## Learner acceptance path

```text
Founder creates learner and assigns exercise
Open pages/Learner_Portal.py
Enter the learner name exactly as stored in Admin data
View assigned tasks
Submit answer and request Agent Review
Check learner records
```

## Customer acceptance path

```text
Founder creates client, cohort, learner, proof files
Open pages/Customer_Portal.py
Enter Customer Demo
View client report and customer-visible Proof Files
```

## Current boundary

```text
Founder CRUD is production-ready with the configured backend
Assignment / submission / review / proof use the existing write-through helpers
Executable Flow is session-first; schema is ready for persistence
Learner Portal is assigned-task preview
Customer Portal is read-only preview
```

## Next hardening

```text
Replace demo login with real auth
Add RLS policies for Founder / customer / learner
Persist flow runtime fully
Bind customer portal to login identity
Remove demo shortcuts before paid pilot
```
