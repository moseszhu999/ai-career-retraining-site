from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from frontend.audit_log import add_audit, init_audit_log, reset_audit_log
from frontend.business_data import CONSULT_LEADS, PROOF_FILES, TASK_INSTANCES
from frontend.training_records import ASSIGNMENTS, REVIEWS, SUBMISSIONS


def init_operation_state() -> None:
    """Create mutable in-session copies of demo business tables.

    This is the bridge between static test data and a real database. Later,
    these getters/actions can be replaced by Supabase reads/writes without
    rewriting page UI.
    """
    init_audit_log()
    table_defaults = {
        "op_task_instances": TASK_INSTANCES.copy(),
        "op_assignments": ASSIGNMENTS.copy(),
        "op_submissions": SUBMISSIONS.copy(),
        "op_reviews": REVIEWS.copy(),
        "op_proof_files": PROOF_FILES.copy(),
        "op_consult_leads": CONSULT_LEADS.copy(),
    }
    for key, value in table_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def task_instances() -> pd.DataFrame:
    return st.session_state.op_task_instances


def assignments() -> pd.DataFrame:
    return st.session_state.op_assignments


def submissions() -> pd.DataFrame:
    return st.session_state.op_submissions


def reviews() -> pd.DataFrame:
    return st.session_state.op_reviews


def proof_files() -> pd.DataFrame:
    return st.session_state.op_proof_files


def consult_leads() -> pd.DataFrame:
    return st.session_state.op_consult_leads


def _submission_view() -> pd.DataFrame:
    df = submissions().copy()
    defaults = {
        "question_type": "",
        "selected_option": "",
        "correct_option": "",
        "is_correct": pd.NA,
        "auto_score": pd.NA,
        "answer_note": "",
    }
    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default
    return df


def joined_records() -> pd.DataFrame:
    submission_cols = [
        "assignment_id",
        "submission_id",
        "submitted_at",
        "answer_summary",
        "question_type",
        "selected_option",
        "correct_option",
        "is_correct",
        "auto_score",
        "answer_note",
        "status",
    ]
    merged = assignments().merge(
        _submission_view()[submission_cols].rename(columns={"status": "submission_status"}),
        on="assignment_id",
        how="left",
    )
    merged = merged.merge(
        reviews()[["submission_id", "reviewer", "score", "review_comment", "decision", "proof_ready"]],
        on="submission_id",
        how="left",
    )
    return merged


def operation_metrics() -> dict[str, int]:
    submission_df = _submission_view()
    correct_series = submission_df["is_correct"].fillna(False)
    total_mcq = int((submission_df["question_type"] == "单选题").sum())
    return {
        "assignments": int(len(assignments())),
        "submissions": int(len(submissions())),
        "reviews": int(len(reviews())),
        "proof_ready": int((reviews()["proof_ready"] == "是").sum()),
        "need_revision": int((reviews()["decision"].isin(["需修改", "需复习"])).sum()),
        "proof_files": int(len(proof_files())),
        "leads": int(len(consult_leads())),
        "lead_value": int(consult_leads()["potential_value"].sum()),
        "mcq_total": total_mcq,
        "mcq_correct": int(correct_series.sum()),
    }


def _next_id(prefix: str, df: pd.DataFrame, column: str) -> str:
    return f"{prefix}-{len(df) + 1:03d}"


def assign_exercise(*, exercise_id: str, learner_id: str, learner_name: str, cohort_id: str, note: str) -> str:
    df = assignments().copy()
    assignment_id = _next_id("asn", df, "assignment_id")
    today = datetime.now().strftime("%Y-%m-%d")
    new_row = {
        "assignment_id": assignment_id,
        "exercise_id": exercise_id,
        "learner_id": learner_id,
        "learner_name": learner_name,
        "cohort_id": cohort_id,
        "status": "已布置",
        "assigned_at": today,
        "due_date": today,
        "note": note,
    }
    st.session_state.op_assignments = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    add_audit(
        action="布置练习题",
        object_type="Assignment",
        object_id=assignment_id,
        before_status="无",
        after_status="已布置",
        summary=f"{learner_name} · {exercise_id} · {note}",
    )
    return assignment_id


def submit_assignment(
    *,
    assignment_id: str,
    exercise_id: str,
    learner_id: str,
    learner_name: str,
    answer_summary: str,
    question_type: str = "",
    selected_option: str = "",
    correct_option: str = "",
    is_correct: bool | None = None,
    auto_score: int | None = None,
    answer_note: str = "",
) -> str:
    sub_df = _submission_view()
    existing = sub_df[sub_df["assignment_id"] == assignment_id]
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    before_status = "未提交" if existing.empty else str(existing.iloc[0]["status"])
    submitted_values = {
        "status": "已提交",
        "submitted_at": submitted_at,
        "answer_summary": answer_summary or "已提交练习作答。",
        "question_type": question_type,
        "selected_option": selected_option,
        "correct_option": correct_option,
        "is_correct": is_correct,
        "auto_score": auto_score,
        "answer_note": answer_note,
    }
    if existing.empty:
        submission_id = _next_id("sub", sub_df, "submission_id")
        new_row = {
            "submission_id": submission_id,
            "assignment_id": assignment_id,
            "exercise_id": exercise_id,
            "learner_id": learner_id,
            "learner_name": learner_name,
            **submitted_values,
        }
        st.session_state.op_submissions = pd.concat([sub_df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        submission_id = str(existing.iloc[0]["submission_id"])
        idx = existing.index[0]
        for col, value in submitted_values.items():
            sub_df.loc[idx, col] = value
        st.session_state.op_submissions = sub_df
    _set_assignment_status(assignment_id, "已提交")
    add_audit(
        action="提交作答",
        object_type="Submission",
        object_id=submission_id,
        before_status=before_status,
        after_status="已提交",
        summary=f"{learner_name} · {exercise_id} · {answer_summary[:60] if answer_summary else '已提交练习作答'}",
    )
    return submission_id


def review_submission(*, submission_id: str, reviewer: str, score: int, review_comment: str, decision: str, proof_ready: str) -> str:
    rev_df = reviews().copy()
    existing = rev_df[rev_df["submission_id"] == submission_id]
    before_status = "未Review" if existing.empty else str(existing.iloc[0]["decision"])
    if existing.empty:
        review_id = _next_id("rev", rev_df, "review_id")
        new_row = {
            "review_id": review_id,
            "submission_id": submission_id,
            "reviewer": reviewer,
            "score": score,
            "review_comment": review_comment,
            "decision": decision,
            "proof_ready": proof_ready,
        }
        st.session_state.op_reviews = pd.concat([rev_df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        review_id = str(existing.iloc[0]["review_id"])
        idx = existing.index[0]
        rev_df.loc[idx, ["reviewer", "score", "review_comment", "decision", "proof_ready"]] = [reviewer, score, review_comment, decision, proof_ready]
        st.session_state.op_reviews = rev_df
    assignment_row = submissions()[submissions()["submission_id"] == submission_id]
    if not assignment_row.empty:
        _set_assignment_status(str(assignment_row.iloc[0]["assignment_id"]), "已确认" if proof_ready == "是" else decision)
    add_audit(
        action="生成/更新Review",
        object_type="Review",
        object_id=review_id,
        before_status=before_status,
        after_status=decision,
        summary=f"{reviewer} · {submission_id} · {score}分 · Proof Ready={proof_ready}",
    )
    return review_id


def mark_assignment_proof_ready(assignment_id: str) -> None:
    records = joined_records()
    row_df = records[records["assignment_id"] == assignment_id]
    if row_df.empty:
        return
    row = row_df.iloc[0]
    before_status = str(row.get("status", ""))
    submission_id = row.get("submission_id")
    if pd.notna(submission_id):
        review_submission(
            submission_id=str(submission_id),
            reviewer="Founder",
            score=int(row["score"]) if pd.notna(row.get("score")) else 85,
            review_comment="Founder确认进入 Proof Files。",
            decision="已确认",
            proof_ready="是",
        )
    _set_assignment_status(assignment_id, "已确认")
    proof_id = add_proof_file_from_record(assignment_id)
    add_audit(
        action="确认进入Proof Files",
        object_type="Assignment",
        object_id=assignment_id,
        before_status=before_status,
        after_status="已确认",
        summary=f"生成 Proof File：{proof_id or '已存在'}",
    )


def request_resubmission(assignment_id: str) -> None:
    records = joined_records()
    row_df = records[records["assignment_id"] == assignment_id]
    before_status = str(row_df.iloc[0].get("status", "")) if not row_df.empty else ""
    _set_assignment_status(assignment_id, "需修改")
    records = joined_records()
    row_df = records[records["assignment_id"] == assignment_id]
    if not row_df.empty and pd.notna(row_df.iloc[0].get("submission_id")):
        review_submission(
            submission_id=str(row_df.iloc[0]["submission_id"]),
            reviewer="Founder",
            score=int(row_df.iloc[0]["score"]) if pd.notna(row_df.iloc[0].get("score")) else 60,
            review_comment="Founder要求重新提交，补充缺失证据。",
            decision="需修改",
            proof_ready="否",
        )
    add_audit(
        action="要求重新提交",
        object_type="Assignment",
        object_id=assignment_id,
        before_status=before_status,
        after_status="需修改",
        summary="Founder要求补充证据后重新提交。",
    )


def add_proof_file_from_record(assignment_id: str) -> str | None:
    records = joined_records()
    row_df = records[records["assignment_id"] == assignment_id]
    if row_df.empty:
        return None
    row = row_df.iloc[0]
    proof_df = proof_files().copy()
    title = f"{row['exercise_id']} 训练证明"
    duplicate = proof_df[(proof_df["learner_name"] == row["learner_name"]) & (proof_df["title"] == title)]
    if not duplicate.empty:
        return str(duplicate.iloc[0]["proof_id"])
    proof_id = _next_id("proof", proof_df, "proof_id")
    new_row = {
        "proof_id": proof_id,
        "learner_name": row["learner_name"],
        "title": title,
        "status": "可展示",
        "score": int(row["score"]) if pd.notna(row.get("score")) else 85,
        "evidence": row["answer_summary"] if pd.notna(row.get("answer_summary")) else "练习提交 + Founder确认",
        "note": "由 Assignment / Submission / Review 状态机生成。",
    }
    st.session_state.op_proof_files = pd.concat([proof_df, pd.DataFrame([new_row])], ignore_index=True)
    add_audit(
        action="新增Proof File",
        object_type="ProofFile",
        object_id=proof_id,
        before_status="无",
        after_status="可展示",
        summary=f"{row['learner_name']} · {title}",
    )
    return proof_id


def add_lead(*, client_name: str, package: str, need: str, potential_value: int, note: str) -> str:
    df = consult_leads().copy()
    lead_id = _next_id("lead", df, "lead_id")
    new_row = {
        "lead_id": lead_id,
        "client_name": client_name,
        "package": package,
        "need": need,
        "status": "新线索",
        "potential_value": potential_value,
        "note": note,
    }
    st.session_state.op_consult_leads = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    add_audit(
        action="新增Lead",
        object_type="Lead",
        object_id=lead_id,
        before_status="无",
        after_status="新线索",
        summary=f"{client_name} · {need} · ¥{potential_value:,}",
    )
    return lead_id


def update_lead_status(lead_id: str, status: str) -> None:
    df = consult_leads().copy()
    target = df[df["lead_id"] == lead_id]
    before_status = str(target.iloc[0]["status"]) if not target.empty else ""
    df.loc[df["lead_id"] == lead_id, "status"] = status
    st.session_state.op_consult_leads = df
    add_audit(
        action="更新Lead状态",
        object_type="Lead",
        object_id=lead_id,
        before_status=before_status,
        after_status=status,
        summary=f"Lead状态从 {before_status} 改为 {status}",
    )


def reset_operation_state() -> None:
    for key in ["op_task_instances", "op_assignments", "op_submissions", "op_reviews", "op_proof_files", "op_consult_leads"]:
        st.session_state.pop(key, None)
    reset_audit_log()
    init_operation_state()
    add_audit(
        action="重置测试数据",
        object_type="SessionState",
        object_id="operation_state",
        before_status="已加载",
        after_status="已重置",
        summary="恢复默认业务测试数据。",
    )


def _set_assignment_status(assignment_id: str, status: str) -> None:
    df = assignments().copy()
    df.loc[df["assignment_id"] == assignment_id, "status"] = status
    st.session_state.op_assignments = df
