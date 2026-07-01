from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st

from frontend.audit_log import add_audit
from frontend.business_data import CLIENTS, COHORTS, LEARNERS
from frontend.exercise_bank import EXERCISES
from frontend.persistence import data_backend, is_supabase_enabled, supabase_client, tenant_code, upsert_row

CLIENT_COLUMNS = ["client_id", "client_name", "contact", "service_package", "contract_value", "currency", "status"]
COHORT_COLUMNS = ["cohort_id", "client_id", "cohort_name", "learner_count", "start_date", "end_date", "trainer", "status"]
LEARNER_COLUMNS = ["learner_id", "learner_name", "cohort_id", "role", "group", "status", "progress", "tasks_done", "proof_files"]
EXERCISE_COLUMNS = [
    "exercise_id",
    "module",
    "difficulty",
    "cohort_id",
    "related_task",
    "scenario",
    "question_type",
    "question",
    "options",
    "correct_option",
    "explanation",
    "required_output",
    "hint",
    "golden_solution",
    "rubric",
]

_TABLE_TO_STATE = {
    "clients": "prod_clients",
    "cohorts": "prod_cohorts",
    "learners": "prod_learners",
    "exercises": "prod_exercises",
}

_TABLE_TO_COLUMNS = {
    "clients": CLIENT_COLUMNS,
    "cohorts": COHORT_COLUMNS,
    "learners": LEARNER_COLUMNS,
    "exercises": EXERCISE_COLUMNS,
}

_TABLE_TO_SEED = {
    "clients": CLIENTS,
    "cohorts": COHORTS,
    "learners": LEARNERS,
    "exercises": EXERCISES,
}


def _empty(columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame(columns=columns)


def _normalize_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    if df.empty:
        return _empty(columns)
    result = df.copy()
    for column in columns:
        if column not in result.columns:
            result[column] = None
    return result[columns]


def _load_table_or_seed(table: str) -> pd.DataFrame:
    columns = _TABLE_TO_COLUMNS[table]
    seed_df = _normalize_columns(_TABLE_TO_SEED[table], columns)
    if not is_supabase_enabled():
        return seed_df.copy()
    try:
        response = supabase_client().table(table).select("*").eq("tenant_code", tenant_code()).execute()
        df = pd.DataFrame(response.data or [])
        if df.empty:
            return _empty(columns)
        if "tenant_code" in df.columns:
            df = df.drop(columns=["tenant_code"])
        return _normalize_columns(df, columns)
    except Exception as exc:
        st.error(f"Supabase load failed for {table}: {exc}")
        return _empty(columns)


def init_production_admin_state() -> None:
    """Load editable master data for v5.1 Production Admin Console."""
    for table, state_key in _TABLE_TO_STATE.items():
        if state_key not in st.session_state:
            st.session_state[state_key] = _load_table_or_seed(table)


def refresh_production_admin_state() -> None:
    for state_key in _TABLE_TO_STATE.values():
        st.session_state.pop(state_key, None)
    init_production_admin_state()


def clients() -> pd.DataFrame:
    init_production_admin_state()
    return st.session_state.prod_clients


def cohorts() -> pd.DataFrame:
    init_production_admin_state()
    return st.session_state.prod_cohorts


def learners() -> pd.DataFrame:
    init_production_admin_state()
    return st.session_state.prod_learners


def exercises() -> pd.DataFrame:
    init_production_admin_state()
    return st.session_state.prod_exercises


def _next_id(prefix: str, df: pd.DataFrame, column: str) -> str:
    today = datetime.now().strftime("%Y%m%d")
    return f"{prefix}-{today}-{len(df) + 1:03d}"


def _append_and_upsert(table: str, row: dict[str, Any], conflict_columns: str) -> None:
    state_key = _TABLE_TO_STATE[table]
    columns = _TABLE_TO_COLUMNS[table]
    df = st.session_state[state_key].copy()
    normalized_row = {column: row.get(column) for column in columns}
    st.session_state[state_key] = pd.concat([df, pd.DataFrame([normalized_row])], ignore_index=True)
    upsert_row(table, normalized_row, conflict_columns)


def add_client(*, client_id: str, client_name: str, contact: str, service_package: str, contract_value: int, currency: str, status: str) -> str:
    df = clients().copy()
    new_id = client_id.strip() or _next_id("client", df, "client_id")
    row = {
        "client_id": new_id,
        "client_name": client_name.strip(),
        "contact": contact.strip(),
        "service_package": service_package.strip(),
        "contract_value": int(contract_value),
        "currency": currency.strip() or "CNY",
        "status": status,
    }
    _append_and_upsert("clients", row, "tenant_code,client_id")
    add_audit("新增客户", "Client", new_id, "无", status, f"{client_name} · {service_package} · ¥{int(contract_value):,}")
    return new_id


def add_cohort(*, cohort_id: str, client_id: str, cohort_name: str, start_date: str, end_date: str, trainer: str, status: str) -> str:
    df = cohorts().copy()
    new_id = cohort_id.strip() or _next_id("cohort", df, "cohort_id")
    row = {
        "cohort_id": new_id,
        "client_id": client_id,
        "cohort_name": cohort_name.strip(),
        "learner_count": 0,
        "start_date": start_date,
        "end_date": end_date,
        "trainer": trainer.strip(),
        "status": status,
    }
    _append_and_upsert("cohorts", row, "tenant_code,cohort_id")
    add_audit("新增班级", "Cohort", new_id, "无", status, f"{cohort_name} · client={client_id}")
    return new_id


def add_learner(*, learner_id: str, learner_name: str, cohort_id: str, learner_group: str, role: str, status: str) -> str:
    df = learners().copy()
    new_id = learner_id.strip() or _next_id("learner", df, "learner_id")
    row = {
        "learner_id": new_id,
        "learner_name": learner_name.strip(),
        "cohort_id": cohort_id,
        "role": role or "学员",
        "group": learner_group.strip() or "默认组",
        "status": status,
        "progress": 0,
        "tasks_done": 0,
        "proof_files": 0,
    }
    _append_and_upsert("learners", row, "tenant_code,learner_id")
    _sync_cohort_learner_count(cohort_id)
    add_audit("新增学员", "Learner", new_id, "无", status, f"{learner_name} · cohort={cohort_id}")
    return new_id


def add_exercise(
    *,
    exercise_id: str,
    module: str,
    difficulty: str,
    cohort_id: str,
    related_task: str,
    scenario: str,
    question: str,
    options: list[str],
    correct_option: str,
    explanation: str,
    required_output: str,
    hint: str,
    golden_solution: str,
    rubric: str,
) -> str:
    df = exercises().copy()
    new_id = exercise_id.strip() or _next_id("ex", df, "exercise_id")
    row = {
        "exercise_id": new_id,
        "module": module.strip(),
        "difficulty": difficulty,
        "cohort_id": cohort_id,
        "related_task": related_task.strip(),
        "scenario": scenario.strip(),
        "question_type": "单选题",
        "question": question.strip(),
        "options": options,
        "correct_option": correct_option,
        "explanation": explanation.strip(),
        "required_output": required_output.strip(),
        "hint": hint.strip(),
        "golden_solution": golden_solution.strip(),
        "rubric": rubric.strip(),
    }
    _append_and_upsert("exercises", row, "tenant_code,exercise_id")
    add_audit("新增选择题", "Exercise", new_id, "无", "可分配", f"{module} · {related_task}")
    return new_id


def _sync_cohort_learner_count(cohort_id: str) -> None:
    cohort_df = cohorts().copy()
    if cohort_df.empty or "cohort_id" not in cohort_df.columns:
        return
    count = int((learners()["cohort_id"] == cohort_id).sum())
    cohort_df.loc[cohort_df["cohort_id"] == cohort_id, "learner_count"] = count
    st.session_state.prod_cohorts = cohort_df
    matches = cohort_df[cohort_df["cohort_id"] == cohort_id]
    if not matches.empty:
        upsert_row("cohorts", matches.iloc[0].to_dict(), "tenant_code,cohort_id")


def health_check() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    backend = data_backend()
    for table in ["clients", "cohorts", "learners", "exercises", "assignments", "submissions", "reviews", "proof_files", "consult_leads"]:
        if not is_supabase_enabled():
            local_key = _TABLE_TO_STATE.get(table)
            local_count = len(st.session_state.get(local_key, [])) if local_key else None
            rows.append({"table": table, "mode": backend, "status": "session", "rows_sampled": local_count, "message": "Session Demo mode"})
            continue
        try:
            response = supabase_client().table(table).select("*").eq("tenant_code", tenant_code()).limit(1000).execute()
            rows.append({"table": table, "mode": backend, "status": "ok", "rows_sampled": len(response.data or []), "message": "Supabase reachable"})
        except Exception as exc:
            rows.append({"table": table, "mode": backend, "status": "error", "rows_sampled": 0, "message": str(exc)[:180]})
    return pd.DataFrame(rows)


def production_mode_status() -> dict[str, str]:
    backend = data_backend()
    return {
        "backend": backend,
        "backend_label": "Supabase Persistent" if backend == "supabase" else "Session Demo",
        "tenant_code": tenant_code(),
    }
