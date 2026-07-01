-- v5.2 executable flow persistence table.
-- Optional for the current lightweight runtime; required when you want flow state persisted in Supabase.

create table if not exists flow_runs (
  tenant_code text not null,
  flow_id text not null,
  client_id text,
  cohort_id text,
  title text,
  status text default 'draft',
  owner text default 'Founder',
  next_step text default 'configured',
  updated_at text,
  created_at timestamptz default now(),
  primary key (tenant_code, flow_id)
);

create index if not exists idx_flow_runs_tenant_status on flow_runs (tenant_code, status);
create index if not exists idx_flow_runs_tenant_client on flow_runs (tenant_code, client_id);
