-- AI Agent Governance & Readiness OS v5.0.0
-- Production Supabase schema for real tenant-scoped persistence.
-- Run this before setting DATA_BACKEND='supabase'.

create extension if not exists pgcrypto;

create table if not exists clients (
    tenant_code text not null default 'demo',
    client_id text not null,
    client_name text not null,
    contact text,
    service_package text,
    contract_value integer default 0,
    currency text default 'CNY',
    status text default '进行中',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, client_id)
);

create table if not exists cohorts (
    tenant_code text not null default 'demo',
    cohort_id text not null,
    client_id text not null,
    cohort_name text not null,
    learner_count integer default 0,
    start_date date,
    end_date date,
    trainer text,
    status text default '进行中',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, cohort_id),
    foreign key (tenant_code, client_id) references clients(tenant_code, client_id) on delete cascade
);

create table if not exists learners (
    tenant_code text not null default 'demo',
    learner_id text not null,
    learner_name text not null,
    cohort_id text not null,
    role text default '学员',
    "group" text,
    status text default '进行中',
    progress integer default 0,
    tasks_done integer default 0,
    proof_files integer default 0,
    login_email text,
    login_alias text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, learner_id),
    foreign key (tenant_code, cohort_id) references cohorts(tenant_code, cohort_id) on delete cascade
);

create table if not exists task_instances (
    tenant_code text not null default 'demo',
    task_id text not null,
    learner_id text not null,
    learner_name text,
    cohort_id text not null,
    day text,
    proof_task text,
    business_context text,
    required_output text,
    status text default '进行中',
    progress integer default 0,
    draft text,
    agent_review text,
    founder_decision text,
    proof_score integer default 0,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, task_id),
    foreign key (tenant_code, learner_id) references learners(tenant_code, learner_id) on delete cascade,
    foreign key (tenant_code, cohort_id) references cohorts(tenant_code, cohort_id) on delete cascade
);

create table if not exists exercises (
    tenant_code text not null default 'demo',
    exercise_id text not null,
    module text,
    difficulty text,
    cohort_id text,
    related_task text,
    scenario text,
    question_type text default '单选题',
    question text,
    options jsonb not null default '[]'::jsonb,
    correct_option text,
    explanation text,
    required_output text,
    hint text,
    golden_solution text,
    rubric text,
    capability text,
    business_process text,
    value_chain_stage text,
    proof_skill text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, exercise_id)
);

create table if not exists assignments (
    tenant_code text not null default 'demo',
    assignment_id text not null,
    exercise_id text not null,
    learner_id text not null,
    learner_name text,
    cohort_id text not null,
    status text default '已布置',
    assigned_at text,
    due_date text,
    note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, assignment_id),
    foreign key (tenant_code, exercise_id) references exercises(tenant_code, exercise_id) on delete restrict,
    foreign key (tenant_code, learner_id) references learners(tenant_code, learner_id) on delete cascade,
    foreign key (tenant_code, cohort_id) references cohorts(tenant_code, cohort_id) on delete cascade
);

create table if not exists submissions (
    tenant_code text not null default 'demo',
    submission_id text not null,
    assignment_id text not null,
    exercise_id text not null,
    learner_id text not null,
    learner_name text,
    status text default '已提交',
    submitted_at text,
    answer_summary text,
    question_type text default '单选题',
    selected_option text,
    correct_option text,
    is_correct boolean,
    auto_score integer,
    answer_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, submission_id),
    unique (tenant_code, assignment_id),
    foreign key (tenant_code, assignment_id) references assignments(tenant_code, assignment_id) on delete cascade,
    foreign key (tenant_code, exercise_id) references exercises(tenant_code, exercise_id) on delete restrict,
    foreign key (tenant_code, learner_id) references learners(tenant_code, learner_id) on delete cascade
);

create table if not exists reviews (
    tenant_code text not null default 'demo',
    review_id text not null,
    submission_id text not null,
    reviewer text,
    score integer,
    review_comment text,
    decision text,
    proof_ready text default '否',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, review_id),
    unique (tenant_code, submission_id),
    foreign key (tenant_code, submission_id) references submissions(tenant_code, submission_id) on delete cascade
);

create table if not exists proof_files (
    tenant_code text not null default 'demo',
    proof_id text not null,
    learner_name text,
    title text,
    status text default '待Review',
    score integer,
    evidence text,
    note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, proof_id)
);

create table if not exists consult_leads (
    tenant_code text not null default 'demo',
    lead_id text not null,
    client_name text,
    package text,
    need text,
    status text default '新线索',
    potential_value integer default 0,
    note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_code, lead_id)
);

create table if not exists audit_logs (
    tenant_code text not null default 'demo',
    audit_id text not null,
    time text,
    actor text,
    role text,
    action text,
    object_type text,
    object_id text,
    before_status text,
    after_status text,
    summary text,
    created_at timestamptz not null default now(),
    primary key (tenant_code, audit_id)
);

create index if not exists idx_cohorts_client on cohorts (tenant_code, client_id);
create index if not exists idx_learners_cohort on learners (tenant_code, cohort_id);
create index if not exists idx_task_instances_learner on task_instances (tenant_code, learner_id);
create index if not exists idx_assignments_learner on assignments (tenant_code, learner_id);
create index if not exists idx_submissions_assignment on submissions (tenant_code, assignment_id);
create index if not exists idx_submissions_mcq_correct on submissions (tenant_code, question_type, is_correct);
create index if not exists idx_submissions_auto_score on submissions (tenant_code, auto_score);
create index if not exists idx_reviews_submission on reviews (tenant_code, submission_id);
create index if not exists idx_audit_object on audit_logs (tenant_code, object_type, object_id);

-- Minimal RLS stance: service-role backend access for now.
-- For end-user Supabase Auth, add policies by tenant_code and user role later.
alter table clients enable row level security;
alter table cohorts enable row level security;
alter table learners enable row level security;
alter table task_instances enable row level security;
alter table exercises enable row level security;
alter table assignments enable row level security;
alter table submissions enable row level security;
alter table reviews enable row level security;
alter table proof_files enable row level security;
alter table consult_leads enable row level security;
alter table audit_logs enable row level security;

create policy if not exists service_role_all_clients on clients for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_cohorts on cohorts for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_learners on learners for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_task_instances on task_instances for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_exercises on exercises for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_assignments on assignments for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_submissions on submissions for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_reviews on reviews for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_proof_files on proof_files for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_consult_leads on consult_leads for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
create policy if not exists service_role_all_audit_logs on audit_logs for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
