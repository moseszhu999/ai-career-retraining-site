# Agent Delivery Task Spec v4.12

This document defines the task, submission, review, and proof-file structure for the AI Agent Delivery Readiness OS.

## 1. Agent Delivery Assignment

An assignment is no longer only a manual coding task. It is an enterprise delivery task where the learner supervises an AI coding agent.

Recommended fields:

| Field | Purpose |
| --- | --- |
| `agent_tool` | Tool used: Claude Code, Codex, Cursor, Copilot Agent, etc. |
| `business_request` | Original business need or defect report. |
| `repo_context` | Repository/module/files involved. |
| `agent_task_brief` | The task instruction given to the AI agent. |
| `constraints` | Must-follow rules, coding standards, security limits, no-touch files. |
| `acceptance_criteria` | Conditions that must be true for completion. |
| `test_command` | Command or manual verification process. |
| `risk_checklist` | Security, permission, data, regression, and customer-impact checks. |
| `customer_output_required` | Whether the learner must produce a customer-safe explanation. |

## 2. Agent Delivery Submission

A submission proves that the learner did not merely ask AI to code. It proves that the learner supervised the delivery.

Recommended fields:

| Field | Purpose |
| --- | --- |
| `agent_prompt_used` | Final prompt or task brief used with the agent. |
| `agent_transcript_summary` | Key agent actions and decisions. |
| `diff_summary` | What changed, at file/module level. |
| `test_result` | Test output, screenshots, logs, or manual verification. |
| `risk_review_notes` | Learner's risk findings. |
| `human_corrections` | What the learner changed or rejected from AI output. |
| `merge_decision` | Accept, reject, revise, or escalate. |
| `customer_explanation` | Customer-safe explanation of the change. |
| `proof_artifacts` | Links or notes for screenshots, commits, docs, and evidence. |

## 3. Agent Delivery Review Rubric

Recommended score dimensions:

| Dimension | Weight | Description |
| --- | ---: | --- |
| Business Understanding | 15 | Did the learner understand the real business request? |
| Agent Task Brief Quality | 15 | Did the learner give the agent a clear, bounded, executable task? |
| Context & Constraint Setup | 15 | Did the learner provide repo context, no-touch rules, and acceptance criteria? |
| Diff Review Accuracy | 15 | Did the learner understand and verify the generated changes? |
| Verification Completeness | 15 | Did the learner run or document adequate tests / checks? |
| Risk Detection | 15 | Did the learner catch security, permission, data, regression, or customer-impact risks? |
| Customer Explanation | 10 | Can the learner explain the result clearly to a customer or manager? |

Total: 100

## 4. Review Decisions

Suggested review decision values:

```text
Proof Ready
Needs Revision
Unsafe To Merge
Escalate To Senior
Agent Misused
Insufficient Evidence
```

## 5. Proof-of-Agent-Work File

A Proof File should prove supervision quality, not just output quality.

Required sections:

```text
1. Business request
2. Agent tool used
3. Agent task brief
4. Repository context and constraints
5. Diff summary
6. Verification evidence
7. Risk checklist result
8. Human corrections
9. Final merge / reject / revise decision
10. Customer-safe delivery explanation
11. Reviewer score and comments
```

## 6. Customer-Safe Export Rules

Customer-facing reports may include:

```text
business request
learner name
agent tool category
high-level change summary
verification result
risk status
customer-safe explanation
readiness score
proof-ready status
```

Customer-facing reports must not include:

```text
raw agent transcript with secrets
internal repo paths that expose confidential structure
internal reviewer notes
security-sensitive logs
private tokens / keys / credentials
contract value
potential lead value
raw audit log object IDs
```

## 7. Future Database Extension

The existing schema can be extended with columns or JSONB fields:

```sql
alter table assignments add column if not exists agent_delivery jsonb not null default '{}'::jsonb;
alter table submissions add column if not exists agent_evidence jsonb not null default '{}'::jsonb;
alter table reviews add column if not exists agent_rubric_scores jsonb not null default '{}'::jsonb;
alter table proof_files add column if not exists agent_proof jsonb not null default '{}'::jsonb;
```

The first implementation can keep these fields as JSONB before normalizing them into separate tables.
