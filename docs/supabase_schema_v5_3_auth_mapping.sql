create table if not exists app_users (
  tenant_code text not null,
  user_id text not null,
  email text,
  display_name text,
  app_role text not null,
  client_id text,
  learner_id text,
  is_active boolean default true,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  primary key (tenant_code, user_id)
);

create index if not exists idx_app_users_tenant_email on app_users (tenant_code, email);
create index if not exists idx_app_users_tenant_role on app_users (tenant_code, app_role);
create index if not exists idx_app_users_tenant_client on app_users (tenant_code, client_id);
create index if not exists idx_app_users_tenant_learner on app_users (tenant_code, learner_id);
