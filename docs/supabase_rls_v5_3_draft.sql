-- v5.3 RLS draft.
-- This is a hardening template for the real-auth phase.
-- The current Streamlit service-role backend can bypass RLS, so apply this only after auth claims are wired.

-- Expected JWT claims later:
-- app_role: founder | customer | learner
-- tenant_code: demo or real tenant
-- client_id: customer client id
-- learner_id: learner id

alter table clients enable row level security;
alter table cohorts enable row level security;
alter table learners enable row level security;
alter table exercises enable row level security;
alter table assignments enable row level security;
alter table submissions enable row level security;
alter table reviews enable row level security;
alter table proof_files enable row level security;
alter table consult_leads enable row level security;
alter table audit_logs enable row level security;
alter table flow_runs enable row level security;

-- Founder: tenant-wide access.
create policy if not exists founder_all_clients on clients
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_cohorts on cohorts
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_learners on learners
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_exercises on exercises
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_assignments on assignments
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_submissions on submissions
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_reviews on reviews
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_proof_files on proof_files
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_leads on consult_leads
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_audit on audit_logs
for select using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

create policy if not exists founder_all_flow on flow_runs
for all using (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code')
with check (auth.jwt() ->> 'app_role' = 'founder' and tenant_code = auth.jwt() ->> 'tenant_code');

-- Learner: own assignments and submissions.
create policy if not exists learner_own_assignments on assignments
for select using (
  auth.jwt() ->> 'app_role' = 'learner'
  and tenant_code = auth.jwt() ->> 'tenant_code'
  and learner_id = auth.jwt() ->> 'learner_id'
);

create policy if not exists learner_own_submissions on submissions
for all using (
  auth.jwt() ->> 'app_role' = 'learner'
  and tenant_code = auth.jwt() ->> 'tenant_code'
  and learner_id = auth.jwt() ->> 'learner_id'
)
with check (
  auth.jwt() ->> 'app_role' = 'learner'
  and tenant_code = auth.jwt() ->> 'tenant_code'
  and learner_id = auth.jwt() ->> 'learner_id'
);

create policy if not exists learner_own_profile on learners
for select using (
  auth.jwt() ->> 'app_role' = 'learner'
  and tenant_code = auth.jwt() ->> 'tenant_code'
  and learner_id = auth.jwt() ->> 'learner_id'
);

-- Customer: read data scoped by client_id.
create policy if not exists customer_own_client on clients
for select using (
  auth.jwt() ->> 'app_role' = 'customer'
  and tenant_code = auth.jwt() ->> 'tenant_code'
  and client_id = auth.jwt() ->> 'client_id'
);

create policy if not exists customer_own_cohorts on cohorts
for select using (
  auth.jwt() ->> 'app_role' = 'customer'
  and tenant_code = auth.jwt() ->> 'tenant_code'
  and client_id = auth.jwt() ->> 'client_id'
);

-- Proof files currently scope by learner_name; later add client_id/cohort_id to proof_files for stricter customer RLS.
