from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend import production_state as prod
from frontend.business_data import LEARNERS as SEED_LEARNERS

DEFAULT_LEARNER_ID = "jhc-s01"


def _learners() -> pd.DataFrame:
    df = prod.learners()
    return df if not df.empty else SEED_LEARNERS


def is_founder() -> bool:
    return st.session_state.get("role") == "Founder"


def resolve_logged_in_learner_id() -> str:
    if is_founder():
        st.session_state.setdefault("selected_learner_id", DEFAULT_LEARNER_ID)
        return str(st.session_state.selected_learner_id)

    if st.session_state.get("learner_id"):
        return str(st.session_state.learner_id)

    learners = _learners()
    user_name = str(st.session_state.get("user_name", ""))
    matched = learners[learners["learner_name"] == user_name] if "learner_name" in learners.columns else learners.iloc[0:0]
    if not matched.empty:
        learner_id = str(matched.iloc[0]["learner_id"])
    elif not learners.empty:
        learner_id = str(learners.iloc[0]["learner_id"])
    else:
        learner_id = DEFAULT_LEARNER_ID
    st.session_state.learner_id = learner_id
    st.session_state.selected_learner_id = learner_id
    return learner_id


def current_learner() -> pd.Series:
    learners = _learners()
    learner_id = resolve_logged_in_learner_id()
    rows = learners[learners["learner_id"] == learner_id] if "learner_id" in learners.columns else learners.iloc[0:0]
    if rows.empty and not learners.empty:
        rows = learners.iloc[[0]]
    return rows.iloc[0]


def current_cohort_id() -> str:
    if is_founder():
        st.session_state.setdefault("selected_cohort_id", "jhc-2026-java")
        return str(st.session_state.selected_cohort_id)
    return str(current_learner()["cohort_id"])


def bind_demo_learner(learner_id: str = DEFAULT_LEARNER_ID) -> None:
    learners = _learners()
    rows = learners[learners["learner_id"] == learner_id] if "learner_id" in learners.columns else learners.iloc[0:0]
    if rows.empty and not learners.empty:
        rows = learners.iloc[[0]]
        learner_id = str(rows.iloc[0]["learner_id"])
    st.session_state.learner_id = learner_id
    st.session_state.selected_learner_id = learner_id
    if not rows.empty:
        st.session_state.user_name = str(rows.iloc[0]["learner_name"])
