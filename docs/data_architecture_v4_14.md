# v4.14.0 Data Architecture

This document defines the target data architecture for AI Agent Governance & Readiness OS.

## 1. Data Architecture Goal

The data architecture must support:

```text
multi-client governance
task policy
authority level
Agent work request
Agent output evidence
verification
risk classification
approval decision
Proof File
audit and reports
```

The long-term data asset is not the Agent output itself. The long-term asset is the evidence and responsibility chain around Agent work.

## 2. Data Domains

| Domain | Core Objects |
| --- | --- |
| Tenant / Client Domain | tenant, client, department, cohort |
| People / Role Domain | app user, learner / employee, role, authority level |
| Policy Domain | governance policy, task category, eligibility, approval rule |
| Work Domain | assignment, Agent work request, task brief, constraints |
| Evidence Domain | Agent output, verification evidence, files, logs, screenshots, corrections |
| Decision Domain | risk classification, review, approval decision, escalation |
| Proof Domain | proof file, readiness score, customer-safe summary |
| Audit / Report Domain | governance event, audit log, export job, report snapshot |

## 3. Conceptual Data Model

```text
Tenant
 ├── Client
 │    ├── Department / Cohort
 │    │    ├── Learner / Employee
 │    │    │    ├── Assignment / Agent Work Request
 │    │    │    │    ├── Agent Output / Submission
 │    │    │    │    ├── Verification Evidence
 │    │    │    │    ├── Risk Classification
 │    │    │    │    ├── Review / Approval Decision
 │    │    │    │    ├── Proof File
 │    │    │    │    └── Governance Event / Audit Log
 │    │    │    └── Readiness Score
 │    │    └── Cohort Report
 │    └── Client-Safe Report
 └── Governance Policy
      ├── Task Category
      ├── Eligibility Rule
      ├── Evidence Requirement
      └── Approval Rule
```

## 4. Existing Tables and Target Meaning

| Existing Table | Target Meaning |
| --- | --- |
| tenants | Organization boundary. |
| clients | Customer / business unit boundary. |
| cohorts | Training cohort, project pilot, or department group. |
| learners | Employee / learner records. |
| exercises | Task templates. |
| assignments | Agent work request instance / governed task. |
| submissions | Agent output and human evidence submission. |
| reviews | review, approval, scoring and readiness decision. |
| proof_files | accepted proof of governed Agent work. |
| consult_leads | commercial follow-up and expansion opportunity. |
| audit_logs | general audit trail. |
| export_jobs | report and export history. |

## 5. New Governance Tables

### 5.1 agent_governance_policies

Purpose:

```text
Define which task categories may use Agent, what risk level applies, what evidence is required, and which approval rule is needed.
```

Key fields:

```text
policy_code
policy_name
task_category
eligibility
default_risk_level
approval_rule
evidence_required
restricted_inputs
customer_safe_fields
is_active
```

### 5.2 agent_authority_levels

Purpose:

```text
Define what employees are allowed to do with AI Agents.
```

Key fields:

```text
level_code
level_name
allowed_risk_levels
allowed_task_categories
requires_review
can_approve_customer_output
```

### 5.3 agent_governance_events

Purpose:

```text
Record Agent task authorization, verification, approval, escalation, rejection, proof creation, and reporting events.
```

Key fields:

```text
event_type
risk_level
approval_rule
approval_decision
summary
evidence
created_at
```

## 6. Core Entity Field Design

### 6.1 Assignment / Agent Work Request

Recommended fields:

```text
assignment_id
exercise_id
learner_id
cohort_id
status
agent_task_eligibility
agent_risk_level
agent_approval_rule
responsible_role
approver_role
agent_delivery jsonb
```

JSON structure for `agent_delivery`:

```json
{
  "agent_tool": "Claude Code / Codex / Cursor / Other",
  "business_request": "...",
  "task_category": "software_change / business_analysis / sales_service / hr_training",
  "task_brief": "...",
  "context": "...",
  "constraints": ["..."],
  "acceptance_criteria": ["..."],
  "evidence_required": ["..."],
  "customer_output_required": true
}
```

### 6.2 Submission / Agent Output Evidence

Recommended fields:

```text
submission_id
assignment_id
status
submitted_at
answer_summary
agent_output_risk_level
verification_status
accountability_note
agent_evidence jsonb
```

JSON structure for `agent_evidence`:

```json
{
  "agent_prompt_used": "...",
  "agent_output_summary": "...",
  "transcript_summary": "...",
  "changed_artifacts": ["..."],
  "test_result": "...",
  "screenshots": ["..."],
  "logs": ["..."],
  "human_corrections": ["..."],
  "risk_notes": ["..."],
  "customer_explanation": "..."
}
```

### 6.3 Review / Governance Decision

Recommended fields:

```text
review_id
submission_id
reviewer
score
review_comment
decision
proof_ready
approval_decision
approved_at
escalation_reason
agent_rubric_scores jsonb
```

JSON structure for `agent_rubric_scores`:

```json
{
  "eligibility_accuracy": 15,
  "authority_fit": 10,
  "task_brief_quality": 15,
  "verification_completeness": 20,
  "risk_classification_accuracy": 15,
  "approval_decision_quality": 15,
  "manager_customer_explanation": 10
}
```

### 6.4 Proof File

Recommended fields:

```text
proof_id
learner_name
title
status
score
evidence
note
agent_proof jsonb
governance_summary jsonb
```

JSON structure for `governance_summary`:

```json
{
  "business_task": "...",
  "agent_eligibility": "agent_allowed_with_review",
  "authority_level": "L2 Supervised Operator",
  "risk_level": "medium",
  "approval_rule": "human_review_required",
  "approval_decision": "approved",
  "responsible_role": "Learner",
  "approver_role": "Founder",
  "customer_safe_summary": "..."
}
```

## 7. Data Classification

| Data Type | Internal | Manager | Customer-Safe | Notes |
| --- | --- | --- | --- | --- |
| Raw Agent prompt | Yes | Limited | No | May expose internal logic. |
| Agent transcript | Yes | Limited | No | May include sensitive details. |
| Diff / logs / screenshots | Yes | Limited | Summary only | Must filter secrets. |
| Verification result | Yes | Yes | Summary | Good customer-safe evidence. |
| Risk level | Yes | Yes | Summary | Avoid exposing sensitive reasons. |
| Approval decision | Yes | Yes | Summary | Suitable for reports. |
| Proof File summary | Yes | Yes | Yes | Main customer-facing asset. |
| Contract value / lead value | Yes | No | No | Commercial internal only. |
| Raw audit object IDs | Yes | Limited | No | Internal traceability only. |
| Readiness score | Yes | Yes | Optional | Customer-safe if agreed. |

## 8. Data Quality Rules

Required data quality checks:

```text
assignment must link to learner and cohort
Agent work request must have task category
Agent work request must have eligibility and approval rule
submission must link to assignment
evidence must include verification status
high / critical risk must not auto-approve
customer-safe report must use field whitelist
proof file must have review decision
approval decision must be audited
```

## 9. Reporting Data Marts

Suggested reporting views:

```text
view_readiness_by_learner
view_readiness_by_cohort
view_agent_work_by_risk_level
view_evidence_completeness
view_approval_decision_quality
view_customer_safe_proof_files
view_governance_audit_events
```

## 10. Data Architecture Roadmap

### Phase 1: Session Demo

```text
pandas DataFrames
session state
manual proof file generation
customer-safe export
```

### Phase 2: Supabase Read Pilot

```text
schema_v4_11
agent_delivery_extension_v4_12
agent_governance_extension_v4_13
read-only repository adapter
```

### Phase 3: Governance Write Pilot

```text
create policies
create authority levels
create governed assignments
submit evidence
record approvals
create governance events
```

### Phase 4: Production Data Platform

```text
RLS policies
object storage
append-only audit log
report snapshots
search / vector index
data retention policy
customer-safe export controls
```
