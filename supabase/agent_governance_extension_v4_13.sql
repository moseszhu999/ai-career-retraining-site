-- AI Agent Governance & Readiness OS v4.13.0
-- Lightweight governance extension for agent task authorization, risk, approval, evidence, and accountability.
-- Keep enum-like values as text for portability in early pilots.

alter table assignments
    add column if not exists agent_task_eligibility text default 'agent_allowed_with_review',
    add column if not exists agent_risk_level text default 'medium',
    add column if not exists agent_approval_rule text default 'human_review_required',
    add column if not exists responsible_role text default 'Learner',
    add column if not exists approver_role text default 'Founder';

alter table submissions
    add column if not exists agent_output_risk_level text default 'medium',
    add column if not exists verification_status text default 'pending',
    add column if not exists accountability_note text;

alter table reviews
    add column if not exists approval_decision text,
    add column if not exists approved_at timestamptz,
    add column if not exists escalation_reason text;

alter table proof_files
    add column if not exists governance_summary jsonb not null default '{}'::jsonb;

create table if not exists agent_governance_policies (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid references clients(id) on delete cascade,
    policy_code text not null,
    policy_name text not null,
    task_category text not null,
    eligibility text not null default 'agent_allowed_with_review',
    default_risk_level text not null default 'medium',
    approval_rule text not null default 'human_review_required',
    evidence_required jsonb not null default '[]'::jsonb,
    restricted_inputs jsonb not null default '[]'::jsonb,
    customer_safe_fields jsonb not null default '[]'::jsonb,
    internal_note text,
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (tenant_id, policy_code)
);

create table if not exists agent_authority_levels (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    level_code text not null,
    level_name text not null,
    description text,
    allowed_risk_levels jsonb not null default '[]'::jsonb,
    allowed_task_categories jsonb not null default '[]'::jsonb,
    requires_review boolean not null default true,
    can_approve_customer_output boolean not null default false,
    created_at timestamptz not null default now(),
    unique (tenant_id, level_code)
);

create table if not exists agent_governance_events (
    id uuid primary key default gen_random_uuid(),
    tenant_id uuid not null references tenants(id) on delete cascade,
    client_id uuid references clients(id) on delete set null,
    assignment_id uuid references assignments(id) on delete set null,
    submission_id uuid references submissions(id) on delete set null,
    review_id uuid references reviews(id) on delete set null,
    event_type text not null,
    risk_level text,
    approval_rule text,
    approval_decision text,
    summary text not null,
    evidence jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

alter table agent_governance_policies enable row level security;
alter table agent_authority_levels enable row level security;
alter table agent_governance_events enable row level security;

create index if not exists idx_agent_governance_policies_tenant
    on agent_governance_policies (tenant_id, task_category, is_active);

create index if not exists idx_agent_authority_levels_tenant
    on agent_authority_levels (tenant_id, level_code);

create index if not exists idx_agent_governance_events_tenant_created
    on agent_governance_events (tenant_id, created_at desc);

comment on table agent_governance_policies is
    'Policy templates defining which AI Agent tasks are allowed, what risk level applies, what approval rule is required, and what evidence must be retained.';

comment on table agent_authority_levels is
    'Role authority levels for AI Agent work, including what risk categories can be handled and whether review is required.';

comment on table agent_governance_events is
    'Event log for AI Agent task authorization, verification, approval, escalation, rejection, and proof creation.';
