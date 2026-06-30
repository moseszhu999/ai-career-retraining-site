from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from frontend.audit_log import add_audit, init_audit_log, reset_audit_log
from frontend.business_data import CONSULT_LEADS, PROOF_FILES, TASK_INSTANCES
from frontend.exercise_bank import EXERCISES
from frontend.persistence import is_supabase_enabled, supabase_client, tenant_code, update_row, upsert_row
from frontend.training_records import ASSIGNMENTS, REVIEWS, SUBMISSIONS


def _load_table_or_seed(table: str, seed_df: pd.DataFrame) -> pd.DataFrame:
    """Load tenant-scoped production rows when Supabase is enabled.

    Empty production tables stay empty instead of silently using demo seed rows.
    In session mode, seed rows remain available for local demos.
    """
    if not is_supabase_enabled():
        return seed_df.copy()
    try:
        response = supabase_client().table(table).select("*").eq("tenant_code", tenant_code()).execute()
        df = pd.DataFrame(response.data or [])
        if df.empty:
            return seed_df.copy().iloc[0:0]
        if "tenant_code" in df.columns:
            df = df.drop(columns=["tenant_code"])
        return df
    except Exception as exc:
        st.error(f"Supabase load failed for {table}: {exc}")
        return seed_df.copy().iloc[0:0]


def init_operation_state() -> None:
    """Create mutable in-session copies of business tables.

    v5.0 supports two modes:
    - session: local demo rows for quick exploration.
    - supabase: tenant-scoped production rows loaded from Supabase.
    """
    init_audit_log()
    table_defaults = {
        "op_task_instances": _load_table_or_seed("task_instances", TASK_INSTANCES),
        "op_assignments": _load_table_or_seed("assignments", ASSIGNMENTS),
        "op_submissions": _load_table_or_seed("submissions", SUBMISSIONS),
        "op_reviews": _load_table_or_seed("reviews", REVIEWS),
        "op_proof_files": _load_table_or_seed("proof_files", PROOF_FILES),
        "op_consult_leads": _load_table_or_seed("consult_leads", CONSULT_LEADS),
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
    assignment_df = assignments().copy()
    if assignment_df.empty:
        return assignment_df
    merged = assignment_df.merge(
        _submission_view()[submission_cols].rename(columns={"status": "submission_status"}),
        on="assignment_id",
        how="left",
    )
    review_df = reviews().copy()
    review_cols = ["submission_id", "reviewer", "score", "review_comment", "decision", "proof_ready"]
    for col in review_cols:
        if col not in review_df.columns:
            review_df[col] = pd.NA
    merged = merged.merge(review_df[review_cols], on="submission_id", how="left")
    return merged


def _exercise_view() -> pd.DataFrame:
    cols = ["exercise_id", "module", "difficulty", "related_task", "question", "correct_option", "explanation", "hint"]
    return EXERCISES[[c for c in cols if c in EXERCISES.columns]].copy()


def mcq_records() -> pd.DataFrame:
    records = joined_records().copy()
    if records.empty:
        return records
    meta = _exercise_view().rename(columns={"correct_option": "exercise_correct_option"})
    enriched = records.merge(meta, on="exercise_id", how="left")
    if "is_correct" in enriched.columns:
        enriched["is_correct"] = enriched["is_correct"].fillna(False).astype(bool)
    return enriched


def mcq_module_stats() -> pd.DataFrame:
    records = mcq_records()
    if records.empty or "module" not in records.columns:
        return pd.DataFrame(columns=["module", "attempts", "correct", "wrong", "accuracy"])
    mcq = records[records["question_type"] == "单选题"].copy()
    if mcq.empty:
        return pd.DataFrame(columns=["module", "attempts", "correct", "wrong", "accuracy"])
    grouped = mcq.groupby("module", dropna=False).agg(
        attempts=("submission_id", "count"),
        correct=("is_correct", "sum"),
    ).reset_index()
    grouped["correct"] = grouped["correct"].astype(int)
    grouped["wrong"] = grouped["attempts"] - grouped["correct"]
    grouped["accuracy"] = (grouped["correct"] / grouped["attempts"] * 100).round(1)
    return grouped.sort_values(["accuracy", "attempts"], ascending=[True, False])


def wrong_answer_records(learner_id: str | None = None) -> pd.DataFrame:
    records = mcq_records()
    if records.empty:
        return records
    wrong = records[(records["question_type"] == "单选题") & (~records["is_correct"].fillna(False).astype(bool))].copy()
    if learner_id:
        wrong = wrong[wrong["learner_id"] == learner_id]
    return wrong


def review_route_for_record(row: pd.Series) -> str:
    if pd.isna(row.get("submission_id")):
        return "等待提交"
    if str(row.get("question_type", "")) == "单选题" and not bool(row.get("is_correct", False)):
        return "需复习"
    score = row.get("score")
    auto_score = row.get("auto_score")
    effective_score = score if pd.notna(score) else auto_score
    if pd.notna(effective_score) and int(effective_score) >= 80:
        return "Proof候选"
    return "Founder复核"


def review_queue_view() -> pd.DataFrame:
    records = mcq_records()
    if records.empty:
        return records
    records["review_route"] = records.apply(review_route_for_record, axis=1)
    return records


def operation_metrics() -> dict[str, int]:
    submission_df = _submission_view()
    correct_series = submission_df["is_correct"].fillna(False) if "is_correct" in submission_df.columns else pd.Series(dtype=bool)
    total_mcq = int((submission_df["question_type"] == "单选题").sum()) if "question_type" in submission_df.columns else 0
    review_df = reviews()
    lead_df = consult_leads()
    return {
        "assignments": int(len(assignments())),
        "submissions": int(len(submission_df)),
        "reviews": int(len(review_df)),
        "proof_ready": int((review_df["proof_ready"] == "是").sum()) if "proof_ready" in review_df.columns else 0,
        "need_revision": int((review_df["decision"].isin(["需修改", "需复习"])).sum()) if "decision" in review_df.columns else 0,
        "proof_files": int(len(proof_files())),
        "leads": int(len(lead_df)),
        "lead_value": int(lead_df["potential_value"].sum()) if "potential_value" in lead_df.columns and not lead_df.empty else 0,
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
    upsert_row("assignments", new_row, "tenant_code,assignment_id")
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
        new_row = {
            "submission_id": submission_id,
            "assignment_id": assignment_id,
            "exercise_id": exercise_id,
            "learner_id": learner_id,
            "learner_name": learner_name,
            **submitted_values,
        }
    upsert_row("submissions", new_row, "tenant_code,submission_id")
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
    review_values = {
        "submission_id": submission_id,
        "reviewer": reviewer,
        "score": score,
        "review_comment": review_comment,
        "decision": decision,
        "proof_ready": proof_ready,
    }
    if existing.empty:
        review_id = _next_id("rev", rev_df, "review_id")
        new_row = {"review_id": review_id, **review_values}
        st.session_state.op_reviews = pd.concat([rev_df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        review_id = str(existing.iloc[0]["review_id"])
        idx = existing.index[0]
        rev_df.loc[idx, ["reviewer", "score", "review_comment", "decision", "proof_ready"]] = [reviewer, score, review_comment, decision, proof_ready]
        st.session_state.op_reviews = rev_df
        new_row = {"review_id": review_id, **review_values}
    upsert_row("reviews", new_row, "tenant_code,review_id")
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
    upsert_row("proof_files", new_row, "tenant_code,proof_id")
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
    upsert_row("consult_leads", new_row, "tenant_code,lead_id")
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
    update_row("consult_leads", "lead_id", lead_id, {"status": status})
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
        summary="恢复默认业务测试数据。Supabase 模式下不会删除生产数据库记录。",
    )


def _set_assignment_status(assignment_id: str, status: str) -> None:
    df = assignments().copy()
    if "assignment_id" not in df.columns:
        return
    df.loc[df["assignment_id"] == assignment_id, "status"] = status
    st.session_state.op_assignments = df
    update_row("assignments", "assignment_id", assignment_id, {"status": status})
