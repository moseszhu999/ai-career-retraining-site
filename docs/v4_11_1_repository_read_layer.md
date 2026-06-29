# v4.11.1 Repository Read Layer

v4.11.1 migrates the two highest-value read-heavy delivery pages to the repository boundary introduced in v4.11.0.

## Goal

Keep the existing Streamlit demo behavior unchanged while making the following pages backend-switchable:

```text
Reports
Exports
```

These pages now read through:

```python
get_repository()
```

instead of importing raw demo tables or calling `operation_state` directly.

## Why Reports and Exports first

Reports and Exports are the safest first migration targets because they are mostly read-only and already represent the customer delivery value:

```text
training progress
submissions
reviews
proof files
leads
audit summary
customer-safe delivery packs
```

If these pages can read from `SessionDataRepository` today and from `SupabaseRepository` later, the product can move toward a real database without rewriting the customer delivery layer.

## Files changed

```text
frontend/report_pages.py
frontend/export_pages.py
streamlit_app.py
```

## Report page changes

`frontend/report_pages.py` now:

- imports `TrainingRepository` and `get_repository()`
- computes operation metrics from repository data
- computes audit metrics from repository data
- generates `_report_text(repo)` from repository data
- keeps the same visible Founder report UI

The previous direct dependencies on these were removed from the report page:

```text
operation_state
business_data.CLIENTS
business_data.COHORTS
business_data.LEARNERS
audit_metrics
```

## Export page changes

`frontend/export_pages.py` now:

- reads all export tables through `get_repository()`
- scopes client exports through repository-provided clients/cohorts/learners
- preserves v4.10.2 customer-safe field whitelist logic
- preserves internal/customer export mode separation
- calls `_report_text(repo)` for the internal full Markdown report

The customer version still hides:

```text
contract_value
potential_value
raw audit_logs
internal notes
Founder / Agent operation details
other customers' data
```

## Current backend behavior

Default behavior remains:

```text
DATA_BACKEND = session
```

So the existing public Streamlit demo is not broken.

Future behavior:

```text
DATA_BACKEND = supabase
```

will be enabled only after `SupabaseRepository` is implemented.

## Next version suggestion

v4.11.2 should add a Supabase seed script that loads the current demo data into the SQL schema while preserving current demo IDs as stable codes:

```text
client_id -> client_code
cohort_id -> cohort_code
learner_id -> learner_code
assignment_id -> assignment_code
submission_id -> submission_code
```
