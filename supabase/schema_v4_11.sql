-- AI Skill Growth OS v4.11.0
-- Supabase / PostgreSQL schema for multi-client training delivery operations.
-- This migration keeps the current Streamlit demo intact while defining the durable SaaS data model.

create extension if not exists pgcrypto;

-- -----------------------------------------------------------------------------
-- Shared enums
-- -----------------------------------------------------------------------------

do $$ begin
    create type app_role as enum ('Founder', 'ClientAdmin', 'Reviewer', 'Learner');
exception when duplicate_object then null;
end $$;

do $$ begin
    create type delivery_visibility as enum ('internal', 'customer');
exception when duplicate_object then null;
end $$;

-- -----------------------------------------------------------------------------
-- Tenant / user boundary
-- -----------------------------------------------------------------------------

create table if not exists tenants (
    id uuid primary key default gen_random_uuid(),
    tenant_code text not null unique,
    tenant_name text not null,
    status text not null default 'active',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists app_users (
    id uuid primary key default gen_random_uuid(),
    auth_user_id uuid unique references auth.users(id) on delete cascade,
    tenant_id uuid not null references tenants(id) on delete cascade,
    display_name text not null,
    email text,
    role app_role not null,
    client_id uuid,
    learner_id uuid,
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- -----------------------------------------------------------------------------
-- Client / cohort / learner
-- -----------------------------------------------------------------------------

create table if not exists clients (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_code text not null,
    client_name text not null,
    contact text,
    service_package text,
    contract_value numeric(12,2),
    currency text not null default 'CNY',
    status text not null default 'active',
    internal_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (tenant_id, client_code)
);

create table if not exists cohorts (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid not null references clients(id) on delete cascade,
    cohort_code text not null,
    cohort_name text not null,
    learner_count integer not null default 0,
    start_date date,
    end_date date,
    trainer text,
    status text not null default 'planned',
    internal_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (tenant_id, cohort_code)
);

create table if not exists learners (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid not null references clients(id) on delete cascade,
    cohort_id uuid not null references cohorts(id) on delete cascade,
    learner_code text not null,
    learner_name text not null,
    role text not null default '学员',
    group_name text,
    status text not null default '进行中',
    progress integer not null default 0 check (progress between 0 and 100),
    tasks_done integer not null default 0,
    proof_files integer not null default 0,
    internal_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (tenant_id, learner_code)
);

alter table app_users
    add constraint app_users_client_fk foreign key (client_id) references clients(id) on delete set null;

alter table app_users
    add constraint app_users_learner_fk foreign key (learner_id) references learners(id) on delete set null;

-- -----------------------------------------------------------------------------
-- Exercise / assignment / submission / review
-- -----------------------------------------------------------------------------

create table if not exists exercises (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid references tenants(id) on delete cascade,
    exercise_code text not null,
    category text not null,
    title text not null,
    scenario text,
    required_output text,
    rubric jsonb not null default '{}'::jsonb,
    status text not null default 'active',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (tenant_id, exercise_code)
);

create table if not exists assignments (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid not null references clients(id) on delete cascade,
    cohort_id uuid not null references cohorts(id) on delete cascade,
    learner_id uuid not null references learners(id) on delete cascade,
    exercise_id uuid references exercises(id) on delete set null,
    assignment_code text not null,
    status text not null default '已布置',
    assigned_at date not null default current_date,
    due_date date,
    note text,
    created_by uuid references app_users(id) on delete set null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (tenant_id, assignment_code)
);

create table if not exists submissions (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid not null references clients(id) on delete cascade,
    cohort_id uuid not null references cohorts(id) on delete cascade,
    assignment_id uuid not null references assignments(id) on delete cascade,
    learner_id uuid not null references learners(id) on delete cascade,
    submission_code text not null,
    status text not null default '已提交',
    submitted_at timestamptz not null default now(),
    answer_summary text,
    artifact_url text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (tenant_id, submission_code)
);

create table if not exists reviews (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid not null references clients(id) on delete cascade,
    cohort_id uuid not null references cohorts(id) on delete cascade,
    submission_id uuid not null references submissions(id) on delete cascade,
    reviewer_user_id uuid references app_users(id) on delete set null,
    reviewer_label text not null default 'Agent',
    score integer check (score between 0 and 100),
    rubric_scores jsonb not null default '{}'::jsonb,
    review_comment text,
    decision text not null default '待Founder确认',
    proof_ready text not null default '否',
    visibility delivery_visibility not null default 'internal',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- -----------------------------------------------------------------------------
-- Proof files / leads / audit / export jobs
-- -----------------------------------------------------------------------------

create table if not exists proof_files (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid not null references clients(id) on delete cascade,
    cohort_id uuid references cohorts(id) on delete set null,
    learner_id uuid not null references learners(id) on delete cascade,
    submission_id uuid references submissions(id) on delete set null,
    title text not null,
    status text not null default '待Review',
    score integer check (score between 0 and 100),
    evidence text,
    public_note text,
    internal_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists consult_leads (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid references clients(id) on delete set null,
    package text,
    need text not null,
    status text not null default '新线索',
    potential_value numeric(12,2),
    public_status_note text,
    internal_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists audit_logs (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid references clients(id) on delete set null,
    actor_user_id uuid references app_users(id) on delete set null,
    actor_label text,
    role app_role,
    action text not null,
    object_type text not null,
    object_id text,
    before_status text,
    after_status text,
    summary text,
    created_at timestamptz not null default now()
);

create table if not exists export_jobs (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid references clients(id) on delete set null,
    requested_by uuid references app_users(id) on delete set null,
    export_kind text not null,
    visibility delivery_visibility not null,
    file_name text,
    file_url text,
    status text not null default 'created',
    created_at timestamptz not null default now()
);

-- -----------------------------------------------------------------------------
-- Helpful indexes
-- -----------------------------------------------------------------------------

create index if not exists idx_clients_tenant on clients(tenant_id);
create index if not exists idx_cohorts_client on cohorts(client_id);
create index if not exists idx_learners_cohort on learners(cohort_id);
create index if not exists idx_assignments_learner on assignments(learner_id);
create index if not exists idx_submissions_assignment on submissions(assignment_id);
create index if not exists idx_reviews_submission on reviews(submission_id);
create index if not exists idx_proof_files_learner on proof_files(learner_id);
create index if not exists idx_audit_logs_client_created on audit_logs(client_id, created_at desc);

-- -----------------------------------------------------------------------------
-- Row-level security boundary
-- -----------------------------------------------------------------------------

alter table tenants enable row level security;
alter table app_users enable row level security;
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
alter table export_jobs enable row level security;

-- Helper view used by policies. Supabase exposes auth.uid() for logged-in users.
create or replace view current_app_user as
select * from app_users where auth_user_id = auth.uid() and is_active = true;

-- Founder can access all rows inside their tenant.
-- Learner and ClientAdmin policies are intentionally narrower and should be applied table-by-table
-- before production launch. Until then, keep production tables behind service-role writes only.

create policy if not exists founder_select_clients on clients
for select using (
    tenant_id in (select tenant_id from current_app_user where role = 'Founder')
);

create policy if not exists founder_select_cohorts on cohorts
for select using (
    tenant_id in (select tenant_id from current_app_user where role = 'Founder')
);

create policy if not exists founder_select_learners on learners
for select using (
    tenant_id in (select tenant_id from current_app_user where role = 'Founder')
);

create policy if not exists founder_select_assignments on assignments
for select using (
    tenant_id in (select tenant_id from current_app_user where role = 'Founder')
);

create policy if not exists learner_select_own_assignments on assignments
for select using (
    learner_id in (select learner_id from current_app_user where role = 'Learner')
);

create policy if not exists learner_select_own_submissions on submissions
for select using (
    learner_id in (select learner_id from current_app_user where role = 'Learner')
);

create policy if not exists learner_insert_own_submissions on submissions
for insert with check (
    learner_id in (select learner_id from current_app_user where role = 'Learner')
);

create policy if not exists client_admin_select_client_proofs on proof_files
for select using (
    client_id in (select client_id from current_app_user where role = 'ClientAdmin')
    and internal_note is null
);
