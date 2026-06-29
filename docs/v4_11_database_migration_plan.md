# v4.11.0 Database Migration Plan

AI Skill Growth OS is moving from a session-based Streamlit demo toward a durable multi-client SaaS backend. v4.11.0 does **not** replace the current demo data yet. It adds the database contract and repository boundary needed for a safe migration.

## Why this step matters

The current product loop is already clear:

```text
Client / Cohort / Learner
-> Exercise
-> Assignment
-> Submission
-> Review
-> Proof Files
-> Leads
-> Audit
-> Reports
-> Exports
```

The next bottleneck is persistence and tenant safety. A real client pilot needs durable tables, auth-linked users, row-level security, and a clean way to replace session DataFrames without rewriting every page.

## Files added

```text
supabase/schema_v4_11.sql
frontend/data_repository.py
```

## Database scope

The schema defines these durable tables:

| Area | Tables |
| --- | --- |
| Tenant boundary | `tenants`, `app_users` |
| Customer delivery | `clients`, `cohorts`, `learners` |
| Training loop | `exercises`, `assignments`, `submissions`, `reviews` |
| Commercial proof | `proof_files`, `consult_leads` |
| Governance | `audit_logs`, `export_jobs` |

## Security model

v4.11.0 introduces a row-level security direction:

| Role | Intended access |
| --- | --- |
| Founder | Full tenant-level operations |
| ClientAdmin | Own client delivery records and customer-safe reports |
| Learner | Own assignments, submissions, reviews, and proof files |
| Reviewer | Review queue within assigned tenant/client scope |

The schema starts with a conservative RLS boundary. Production rollout should continue policy hardening table by table before client login is enabled.

## Repository boundary

`frontend/data_repository.py` adds a `TrainingRepository` protocol and two adapters:

| Adapter | Status | Purpose |
| --- | --- | --- |
| `SessionDataRepository` | Active default | Preserves all current v4.10 behavior |
| `SupabaseRepository` | Placeholder | Explicit target for persistent backend wiring |

The rule for future development:

```text
Pages should read through get_repository() instead of importing raw demo DataFrames directly.
```

This allows a gradual migration:

```text
static demo tables
-> session repository
-> Supabase read adapter
-> Supabase write adapter
-> RLS-enforced production SaaS
```

## Recommended migration order

### Step 1: Read-only repository refactor

Replace page-level imports of static DataFrames with `get_repository()` reads.

Start with low-risk pages:

1. Reports
2. Exports
3. Founder dashboard
4. Student views

### Step 2: Seed demo data into Supabase

Create a seed script that maps current IDs to database codes:

| Current demo field | Database mapping |
| --- | --- |
| `client_id` | `client_code` |
| `cohort_id` | `cohort_code` |
| `learner_id` | `learner_code` |
| `assignment_id` | `assignment_code` |
| `submission_id` | `submission_code` |

### Step 3: Supabase read adapter

Implement read methods for:

```text
clients()
cohorts()
learners()
assignments()
submissions()
reviews()
proof_files()
consult_leads()
audit_logs()
joined_records()
```

Keep writes in session until read parity is verified.

### Step 4: Supabase write adapter

Move state-changing actions behind repository methods:

```text
assign_exercise
submit_assignment
review_submission
mark_assignment_proof_ready
request_resubmission
add_proof_file_from_record
add_lead
update_lead_status
add_audit
```

### Step 5: Role-based login

Map authenticated users to `app_users`:

```text
auth.users.id -> app_users.auth_user_id
```

Then enforce:

```text
Founder sees tenant scope.
ClientAdmin sees client scope.
Learner sees own records.
```

### Step 6: Customer-safe exports from database

Keep v4.10.2 customer-safe export logic. The difference is only data source:

```text
SessionDataRepository -> SupabaseRepository
```

Do not allow raw `audit_logs`, `contract_value`, or `potential_value` in customer-facing export jobs.

## Done definition for v4.11.x

v4.11 can be considered complete when:

- SQL schema runs in a new Supabase project.
- Current demo data can be seeded into database tables.
- Reports and Exports can read from repository instead of direct demo tables.
- Existing Streamlit demo still works with `DATA_BACKEND = session`.
- `DATA_BACKEND = supabase` can be enabled for read-only pilot testing.

## Next version suggestion

v4.11.1 should migrate the Reports and Exports pages to `get_repository()` first, because they are read-heavy and already represent the customer delivery value.
