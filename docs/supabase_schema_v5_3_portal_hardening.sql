-- v5.3 portal hardening migration.

alter table proof_files add column if not exists client_id text;
alter table proof_files add column if not exists cohort_id text;
alter table proof_files add column if not exists learner_id text;

create index if not exists idx_proof_files_tenant_client on proof_files (tenant_code, client_id);
create index if not exists idx_proof_files_tenant_cohort on proof_files (tenant_code, cohort_id);
create index if not exists idx_proof_files_tenant_learner on proof_files (tenant_code, learner_id);
