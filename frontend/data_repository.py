from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.audit_log import audit_logs
from frontend.business_data import CLIENTS, COHORTS, LEARNERS, TASK_INSTANCES


@dataclass(frozen=True)
class RepositoryScope:
    """Current data access scope.

    v4.11 keeps the existing demo/session data as the default implementation,
    but all pages can migrate toward this repository boundary before the
    Supabase adapter is enabled.
    """

    tenant_code: str = "demo"
    role: str = "Founder"
    client_id: str | None = None
    learner_id: str | None = None


class TrainingRepository(Protocol):
    def clients(self) -> pd.DataFrame: ...
    def cohorts(self) -> pd.DataFrame: ...
    def learners(self) -> pd.DataFrame: ...
    def task_instances(self) -> pd.DataFrame: ...
    def assignments(self) -> pd.DataFrame: ...
    def submissions(self) -> pd.DataFrame: ...
    def reviews(self) -> pd.DataFrame: ...
    def proof_files(self) -> pd.DataFrame: ...
    def consult_leads(self) -> pd.DataFrame: ...
    def audit_logs(self) -> pd.DataFrame: ...
    def joined_records(self) -> pd.DataFrame: ...


class SessionDataRepository:
    """Repository adapter backed by the current Streamlit session DataFrames."""

    def __init__(self, scope: RepositoryScope) -> None:
        self.scope = scope

    def clients(self) -> pd.DataFrame:
        return CLIENTS.copy()

    def cohorts(self) -> pd.DataFrame:
        return COHORTS.copy()

    def learners(self) -> pd.DataFrame:
        return LEARNERS.copy()

    def task_instances(self) -> pd.DataFrame:
        return ops.task_instances().copy()

    def assignments(self) -> pd.DataFrame:
        return ops.assignments().copy()

    def submissions(self) -> pd.DataFrame:
        return ops.submissions().copy()

    def reviews(self) -> pd.DataFrame:
        return ops.reviews().copy()

    def proof_files(self) -> pd.DataFrame:
        return ops.proof_files().copy()

    def consult_leads(self) -> pd.DataFrame:
        return ops.consult_leads().copy()

    def audit_logs(self) -> pd.DataFrame:
        return audit_logs().copy()

    def joined_records(self) -> pd.DataFrame:
        return ops.joined_records().copy()


class SupabaseRepository:
    """Placeholder adapter for the persistent SaaS data backend.

    This class defines the exact interface the UI should depend on. It is not
    wired yet, so v4.11.0 remains safe for the public Streamlit demo.
    """

    def __init__(self, scope: RepositoryScope) -> None:
        self.scope = scope
        raise NotImplementedError(
            "SupabaseRepository is defined as the v4.11 migration target. "
            "Use SessionDataRepository until SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are configured."
        )


def current_scope() -> RepositoryScope:
    return RepositoryScope(
        tenant_code=str(st.session_state.get("tenant_code", "demo")),
        role=str(st.session_state.get("role", "Founder")),
        client_id=st.session_state.get("current_client_id"),
        learner_id=st.session_state.get("student_id") or st.session_state.get("learner_id"),
    )


def get_repository() -> TrainingRepository:
    """Return the active repository implementation.

    Future switch:
        st.secrets["DATA_BACKEND"] = "supabase"

    Current safe default:
        session DataFrames, preserving all v4.10 demo behavior.
    """

    backend = str(st.secrets.get("DATA_BACKEND", "session")) if hasattr(st, "secrets") else "session"
    scope = current_scope()
    if backend == "supabase":
        return SupabaseRepository(scope)
    return SessionDataRepository(scope)
