# v5.3 Trial Use Manual

## What is usable now

```text
Founder internal console
Production master data entry
Assignment workflow
MCQ submission and Agent Review
Founder Review Queue
Proof Files
Customer read-only portal preview
Learner assigned-task portal preview
Executable Flow state machine
Supabase health check
```

## Recommended first pilot scope

Do not pilot this as a full SaaS yet.

Pilot it as:

```text
Founder internal use
Learner assigned-task submission
Customer read-only report preview
```

## Roles

```text
Founder: full operations
Learner: assigned tasks only in Learner Portal
Customer: read-only report and proof view in Customer Portal
```

## Pilot data setup

```text
1 client
1 cohort
3 learners
5 MCQ exercises
5 to 10 assignments
1 review cycle
1 customer report
```

## Founder operating loop

```text
Create data in Admin/Health
Assign tasks
Check learner submissions
Generate Agent Review
Confirm or reject Proof
Open customer portal preview
Export report
```

## Learner loop

```text
Open Learner Portal
Enter learner name
See assigned tasks only
Submit answer
See records
```

## Customer loop

```text
Open Customer Portal
View delivery summary
View proof files
Copy report text
```

## Things not ready for paid production

```text
Real auth
Password login
Email invite
Strict RLS enforcement
Customer identity binding
Learner identity binding beyond name matching
Payment / billing
Notification emails
```

## Definition of ready for real customer trial

```text
Data survives refresh
Founder can create real data
Learner can submit assigned task
Founder can review and approve
Customer can view report
Flow can advance through status chain
Supabase Health Check passes
```
