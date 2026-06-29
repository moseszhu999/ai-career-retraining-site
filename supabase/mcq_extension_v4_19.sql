-- AI Agent Governance & Readiness OS v4.19.0
-- MCQ-first exercise extension.
-- This keeps quick learner operation and automatic first-pass scoring compatible with future Supabase persistence.

alter table exercises
    add column if not exists question_type text default '单选题',
    add column if not exists options jsonb not null default '[]'::jsonb,
    add column if not exists correct_option text,
    add column if not exists explanation text;

alter table submissions
    add column if not exists question_type text default '单选题',
    add column if not exists selected_option text,
    add column if not exists correct_option text,
    add column if not exists is_correct boolean,
    add column if not exists auto_score integer,
    add column if not exists answer_note text;

create index if not exists idx_submissions_mcq_correct
    on submissions (question_type, is_correct);

create index if not exists idx_submissions_auto_score
    on submissions (auto_score);

comment on column exercises.question_type is
    'Exercise type. Early MVP uses 单选题 / MCQ-first design for easier learner operation.';

comment on column exercises.options is
    'MCQ options as JSON array. Example: ["A. ...", "B. ...", "C. ...", "D. ..."].';

comment on column exercises.correct_option is
    'Correct MCQ option letter, such as A/B/C/D.';

comment on column exercises.explanation is
    'Explanation shown after submission or in review materials.';

comment on column submissions.selected_option is
    'Learner selected option letter for MCQ submissions.';

comment on column submissions.is_correct is
    'Whether the selected option matches the correct option.';

comment on column submissions.auto_score is
    'Automatic first-pass score based on MCQ correctness and difficulty.';
