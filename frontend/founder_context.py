from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.business_data import CLIENTS, COHORTS, LEARNERS

DEFAULT_CLIENT_ID = "jhc"
DEFAULT_COHORT_ID = "jhc-2026-java"
DEFAULT_LEARNER_ID = "jhc-s01"


def ensure_founder_context() -> None:
    """Ensure Founder has a visible current operation scope.

    These values describe what the operator is currently looking at. They do
    not restrict permissions; they make the current business context visible.
    """
    st.session_state.setdefault("selected_client_id", DEFAULT_CLIENT_ID)
    st.session_state.setdefault("selected_cohort_id", DEFAULT_COHORT_ID)
    st.session_state.setdefault("selected_learner_id", DEFAULT_LEARNER_ID)
    st.session_state.setdefault("selected_assignment_id", "")


def set_client_context(client_id: str) -> None:
    ensure_founder_context()
    st.session_state.selected_client_id = client_id
    cohorts = COHORTS[COHORTS["client_id"] == client_id]
    if not cohorts.empty:
        set_cohort_context(str(cohorts.iloc[0]["cohort_id"]))


def set_cohort_context(cohort_id: str) -> None:
    ensure_founder_context()
    st.session_state.selected_cohort_id = cohort_id
    cohort = _row(COHORTS, "cohort_id", cohort_id)
    if cohort is not None:
        st.session_state.selected_client_id = str(cohort["client_id"])
    learners = LEARNERS[LEARNERS["cohort_id"] == cohort_id]
    if not learners.empty:
        st.session_state.selected_learner_id = str(learners.iloc[0]["learner_id"])


def set_learner_context(learner_id: str) -> None:
    ensure_founder_context()
    st.session_state.selected_learner_id = learner_id
    learner = _row(LEARNERS, "learner_id", learner_id)
    if learner is not None:
        st.session_state.selected_cohort_id = str(learner["cohort_id"])
        cohort = _row(COHORTS, "cohort_id", str(learner["cohort_id"]))
        if cohort is not None:
            st.session_state.selected_client_id = str(cohort["client_id"])


def set_assignment_context(assignment_id: str) -> None:
    ensure_founder_context()
    st.session_state.selected_assignment_id = assignment_id


def context_values() -> dict[str, str]:
    ensure_founder_context()
    client = _row(CLIENTS, "client_id", str(st.session_state.selected_client_id))
    cohort = _row(COHORTS, "cohort_id", str(st.session_state.selected_cohort_id))
    learner = _row(LEARNERS, "learner_id", str(st.session_state.selected_learner_id))
    return {
        "client": str(client["client_name"]) if client is not None else "未选择客户",
        "cohort": str(cohort["cohort_name"]) if cohort is not None else "未选择班级",
        "learner": str(learner["learner_name"]) if learner is not None else "未选择学员",
        "assignment": str(st.session_state.get("selected_assignment_id") or "未选择Assignment"),
    }


def founder_context_bar() -> str:
    values = context_values()
    return (
        "<div class='result-strip'>"
        f"<div><b>当前客户</b><br><span class='mini'>{values['client']}</span></div>"
        f"<div><b>当前班级</b><br><span class='mini'>{values['cohort']}</span></div>"
        f"<div><b>当前学员</b><br><span class='mini'>{values['learner']}</span></div>"
        f"<div><b>当前Assignment</b><br><span class='mini'>{values['assignment']}</span></div>"
        "</div>"
    )


def _row(df: pd.DataFrame, column: str, value: str) -> pd.Series | None:
    rows = df[df[column] == value]
    if rows.empty:
        return None
    return rows.iloc[0]
