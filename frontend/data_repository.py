from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd
import streamlit as st
from supabase import Client, create_client

from frontend import operation_state as ops
from frontend.audit_log import audit_logs
from frontend.business_data import CLIENTS, COHORTS, LEARNERS, TASK_INSTANCES


@dataclass(frozen=True)
class RepositoryScope:
    """Current data access scope.

    v5.0 keeps session data as the safe default, but the Supabase adapter is no
    longer a placeholder. Set Streamlit secrets:

        DATA_BACKEND="supabase"
        SUPABASE_URL="https://...supabase.co"
        SUPABASE_SERVICE_ROLE_KEY="..."
        TENANT_CODE="demo"

    Then run supabase/production_schema_v5.sql and seed real rows.
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
    """Persistent repository adapter backed by Supabase tables.

    This is the first production cutover layer. It reads real tenant-scoped
    records from Supabase and returns the same DataFrame shapes expected by the
    Streamlit UI. Write operations are handled by operation_state action helpers
    in v5.0 write-through mode.
    """

    def __init__(self, scope: RepositoryScope) -> None:
        self.scope = scope
        self.client = _supabase_client()

    def _table(self, name: str, *, order_by: str | None = None) -> pd.DataFrame:
        try:
            query = self.client.table(name).select("*").eq("tenant_code", self.scope.tenant_code)
            if order_by:
                query = query.order(order_by)
            response = query.execute()
            return pd.DataFrame(response.data or [])
        except Exception as exc:  # pragma: no cover - shown in Streamlit runtime
            raise RuntimeError(
                f"Supabase table read failed: {name}. Run supabase/production_schema_v5.sql, "
                f"check tenant_code='{self.scope.tenant_code}', and verify secrets. Original error: {exc}"
            ) from exc

    def clients(self) -> pd.DataFrame:
        return self._table("clients", order_by="client_id")

    def cohorts(self) -> pd.DataFrame:
        return self._table("cohorts", order_by="cohort_id")

    def learners(self) -> pd.DataFrame:
        return self._table("learners", order_by="learner_id")

    def task_instances(self) -> pd.DataFrame:
        return self._table("task_instances", order_by="task_id")

    def assignments(self) -> pd.DataFrame:
        return self._table("assignments", order_by="assignment_id")

    def submissions(self) -> pd.DataFrame:
        return self._table("submissions", order_by="submission_id")

    def reviews(self) -> pd.DataFrame:
        return self._table("reviews", order_by="review_id")

    def proof_files(self) -> pd.DataFrame:
        return self._table("proof_files", order_by="proof_id")

    def consult_leads(self) -> pd.DataFrame:
        return self._table("consult_leads", order_by="lead_id")

    def audit_logs(self) -> pd.DataFrame:
        return self._table("audit_logs", order_by="time")

    def joined_records(self) -> pd.DataFrame:
        assignments = self.assignments()
        submissions = self.submissions()
        reviews = self.reviews()
        if assignments.empty:
            return assignments
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
        submission_view = _ensure_columns(submissions, submission_cols)
        merged = assignments.merge(
            submission_view[submission_cols].rename(columns={"status": "submission_status"}),
            on="assignment_id",
            how="left",
        )
        review_cols = ["submission_id", "reviewer", "score", "review_comment", "decision", "proof_ready"]
        review_view = _ensure_columns(reviews, review_cols)
        merged = merged.merge(review_view[review_cols], on="submission_id", how="left")
        return merged


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    safe = df.copy()
    for col in columns:
        if col not in safe.columns:
            safe[col] = pd.NA
    return safe


@st.cache_resource(show_spinner=False)
def _supabase_client() -> Client:
    url = str(st.secrets.get("SUPABASE_URL", ""))
    key = str(st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", ""))
    if not url or not key:
        raise RuntimeError(
            "Supabase backend requested but secrets are missing. Configure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY."
        )
    return create_client(url, key)


def current_scope() -> RepositoryScope:
    return RepositoryScope(
        tenant_code=str(st.secrets.get("TENANT_CODE", st.session_state.get("tenant_code", "demo"))) if hasattr(st, "secrets") else str(st.session_state.get("tenant_code", "demo")),
        role=str(st.session_state.get("role", "Founder")),
        client_id=st.session_state.get("current_client_id"),
        learner_id=st.session_state.get("student_id") or st.session_state.get("learner_id"),
    )


def get_repository() -> TrainingRepository:
    """Return the active repository implementation.

    Production:
        DATA_BACKEND="supabase"

    Safe local/demo default:
        DATA_BACKEND omitted or "session"
    """

    backend = str(st.secrets.get("DATA_BACKEND", "session")) if hasattr(st, "secrets") else "session"
    scope = current_scope()
    if backend == "supabase":
        return SupabaseRepository(scope)
    return SessionDataRepository(scope)
