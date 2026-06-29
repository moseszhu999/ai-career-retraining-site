from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.business_data import LEARNERS

DEFAULT_LEARNER_ID = "jhc-s01"


def is_founder() -> bool:
    return st.session_state.get("role") == "Founder"


def resolve_logged_in_learner_id() -> str:
    """Return the learner_id bound to the logged-in learner.

    Founder users may switch selected learners elsewhere. Student users should
    never be asked to select a learner after login; this function binds them to
    their own learner row. In demo mode, unknown student names fall back to the
    default JHC learner.
    """
    if is_founder():
        st.session_state.setdefault("selected_learner_id", DEFAULT_LEARNER_ID)
        return str(st.session_state.selected_learner_id)

    if st.session_state.get("learner_id"):
        return str(st.session_state.learner_id)

    user_name = str(st.session_state.get("user_name", ""))
    matched = LEARNERS[LEARNERS["learner_name"] == user_name]
    learner_id = str(matched.iloc[0]["learner_id"]) if not matched.empty else DEFAULT_LEARNER_ID
    st.session_state.learner_id = learner_id
    st.session_state.selected_learner_id = learner_id
    return learner_id


def current_learner() -> pd.Series:
    learner_id = resolve_logged_in_learner_id()
    rows = LEARNERS[LEARNERS["learner_id"] == learner_id]
    if rows.empty:
        rows = LEARNERS[LEARNERS["learner_id"] == DEFAULT_LEARNER_ID]
    return rows.iloc[0]


def current_cohort_id() -> str:
    if is_founder():
        st.session_state.setdefault("selected_cohort_id", "jhc-2026-java")
        return str(st.session_state.selected_cohort_id)
    return str(current_learner()["cohort_id"])


def bind_demo_learner(learner_id: str = DEFAULT_LEARNER_ID) -> None:
    rows = LEARNERS[LEARNERS["learner_id"] == learner_id]
    if rows.empty:
        learner_id = DEFAULT_LEARNER_ID
        rows = LEARNERS[LEARNERS["learner_id"] == learner_id]
    st.session_state.learner_id = learner_id
    st.session_state.selected_learner_id = learner_id
    st.session_state.user_name = str(rows.iloc[0]["learner_name"])
