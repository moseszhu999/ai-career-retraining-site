-- v5.1 Production Admin Console schema
-- Run this in Supabase SQL Editor before using DATA_BACKEND = "supabase".
-- v5.3 will harden RLS / customer / learner isolation. v5.1 uses service-role writes from Streamlit secrets.

create table if not exists clients (
  tenant_code text not null,
  client_id text not null,
  client_name text not null,
  contact text,
  service_package text,
  contract_value integer default 0,
  currency text default 'CNY',
  status text default '待跟进',
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, client_id)
);

create table if not exists cohorts (
  tenant_code text not null,
  cohort_id text not null,
  client_id text not null,
  cohort_name text not null,
  learner_count integer default 0,
  start_date text,
  end_date text,
  trainer text,
  status text default '准备中',
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, cohort_id)
);

create table if not exists learners (
  tenant_code text not null,
  learner_id text not null,
  learner_name text not null,
  cohort_id text not null,
  role text default '学员',
  "group" text default '默认组',
  status text default '未开始',
  progress integer default 0,
  tasks_done integer default 0,
  proof_files integer default 0,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, learner_id)
);

create table if not exists exercises (
  tenant_code text not null,
  exercise_id text not null,
  module text,
  difficulty text,
  cohort_id text,
  related_task text,
  scenario text,
  question_type text default '单选题',
  question text,
  options jsonb default '[]'::jsonb,
  correct_option text,
  explanation text,
  required_output text,
  hint text,
  golden_solution text,
  rubric text,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, exercise_id)
);

create table if not exists task_instances (
  tenant_code text not null,
  task_id text not null,
  learner_id text,
  learner_name text,
  cohort_id text,
  day text,
  proof_task text,
  business_context text,
  required_output text,
  status text,
  progress integer default 0,
  draft text,
  agent_review text,
  founder_decision text,
  proof_score integer default 0,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, task_id)
);

create table if not exists assignments (
  tenant_code text not null,
  assignment_id text not null,
  exercise_id text not null,
  learner_id text not null,
  learner_name text,
  cohort_id text,
  status text default '已布置',
  assigned_at text,
  due_date text,
  note text,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, assignment_id)
);

create table if not exists submissions (
  tenant_code text not null,
  submission_id text not null,
  assignment_id text not null,
  exercise_id text,
  learner_id text,
  learner_name text,
  status text,
  submitted_at text,
  answer_summary text,
  question_type text,
  selected_option text,
  correct_option text,
  is_correct boolean,
  auto_score integer,
  answer_note text,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, submission_id)
);

create table if not exists reviews (
  tenant_code text not null,
  review_id text not null,
  submission_id text not null,
  reviewer text,
  score integer,
  review_comment text,
  decision text,
  proof_ready text,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, review_id)
);

create table if not exists proof_files (
  tenant_code text not null,
  proof_id text not null,
  learner_name text,
  title text,
  status text,
  score integer,
  evidence text,
  note text,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, proof_id)
);

create table if not exists consult_leads (
  tenant_code text not null,
  lead_id text not null,
  client_name text,
  package text,
  need text,
  status text,
  potential_value integer default 0,
  note text,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, lead_id)
);

create table if not exists audit_logs (
  tenant_code text not null,
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
  created_at timestamptz default now(),
  primary key (tenant_code, audit_id)
);

create index if not exists idx_clients_tenant on clients (tenant_code);
create index if not exists idx_cohorts_tenant_client on cohorts (tenant_code, client_id);
create index if not exists idx_learners_tenant_cohort on learners (tenant_code, cohort_id);
create index if not exists idx_exercises_tenant_cohort on exercises (tenant_code, cohort_id);
create index if not exists idx_assignments_tenant_learner on assignments (tenant_code, learner_id);
create index if not exists idx_submissions_tenant_assignment on submissions (tenant_code, assignment_id);
create index if not exists idx_reviews_tenant_submission on reviews (tenant_code, submission_id);
create index if not exists idx_audit_tenant_time on audit_logs (tenant_code, time desc);
