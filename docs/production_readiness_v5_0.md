# v5.0.0 Production Readiness

This version turns the project from a Streamlit prototype into a production-ready persistence path.

## What changed

v4.x used Streamlit session DataFrames as the default data layer. That was useful for demonstration, but it was not a real product because data disappeared after session reset.

v5.0.0 adds:

- Real Supabase repository adapter.
- Tenant-scoped production schema.
- Demo seed data for a real Supabase project.
- Write-through persistence for core operations.
- Streamlit secrets example.
- Clear error messages when Supabase is misconfigured.

## Production setup

### 1. Create a Supabase project

Create a Supabase project and copy:

- Project URL
- Service role key

The current Streamlit app uses server-side service-role access. Do not expose the service role key in client-side code.

### 2. Run schema

In Supabase SQL Editor, run:

```sql
-- supabase/production_schema_v5.sql
```

This creates:

- clients
- cohorts
- learners
- task_instances
- exercises
- assignments
- submissions
- reviews
- proof_files
- consult_leads
- audit_logs

All tables include `tenant_code`.

### 3. Seed demo tenant

For first test, run:

```sql
-- supabase/seed_demo_v5.sql
```

This seeds tenant:

```text
demo
```

### 4. Configure Streamlit secrets

Copy:

```text
.streamlit/secrets.example.toml
```

To:

```text
.streamlit/secrets.toml
```

Then set:

```toml
DATA_BACKEND = "supabase"
TENANT_CODE = "demo"
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "YOUR_SERVICE_ROLE_KEY"
```

### 5. Run app

```bash
streamlit run streamlit_app.py
```

## What is now persistent

The following operations write through to Supabase when `DATA_BACKEND="supabase"`:

- Create Assignment
- Submit MCQ answer
- Generate / update Review
- Mark Proof ready
- Add Proof File
- Add Lead
- Update Lead status
- Add Audit Log
- Update Assignment status

## What remains session/demo-backed

The following are still partially static or seed-driven and should be made fully editable in future versions:

- Client creation / editing
- Cohort creation / editing
- Learner creation / editing
- Exercise authoring UI
- Task instance editing
- Real user authentication / invite flow
- Row-level policies for end-user Supabase Auth

## Production rule

Do not call it production if:

- `DATA_BACKEND` is still `session`.
- Supabase schema has not been run.
- The service role key is not configured in server-side secrets.
- Customers or learners cannot return later and see saved state.

## Next step

v5.1.0 should add:

- Real login identity mapping.
- Founder-only admin creation forms for clients, cohorts, learners, exercises.
- Environment banner showing Session / Supabase mode.
- Health check page for Supabase connection and table counts.
