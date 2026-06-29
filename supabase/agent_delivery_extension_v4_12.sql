-- AI Skill Growth OS v4.12.0
-- Agent Delivery Readiness extension.
-- This migration adds JSONB extension fields without breaking the v4.11 schema.

alter table assignments
    add column if not exists agent_delivery jsonb not null default '{}'::jsonb;

alter table submissions
    add column if not exists agent_evidence jsonb not null default '{}'::jsonb;

alter table reviews
    add column if not exists agent_rubric_scores jsonb not null default '{}'::jsonb;

alter table proof_files
    add column if not exists agent_proof jsonb not null default '{}'::jsonb;

create index if not exists idx_assignments_agent_delivery_gin
    on assignments using gin (agent_delivery);

create index if not exists idx_submissions_agent_evidence_gin
    on submissions using gin (agent_evidence);

create index if not exists idx_reviews_agent_rubric_scores_gin
    on reviews using gin (agent_rubric_scores);

create index if not exists idx_proof_files_agent_proof_gin
    on proof_files using gin (agent_proof);

comment on column assignments.agent_delivery is
    'Agent delivery assignment brief: tool, repo context, constraints, acceptance criteria, test command, and risk checklist.';

comment on column submissions.agent_evidence is
    'Agent delivery submission evidence: prompt, transcript summary, diff summary, test results, risk notes, human corrections, and merge decision.';

comment on column reviews.agent_rubric_scores is
    'Structured review rubric for AI agent delivery supervision quality.';

comment on column proof_files.agent_proof is
    'Customer-safe proof-of-agent-work evidence package.';
