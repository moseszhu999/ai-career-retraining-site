from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.persistence import is_supabase_enabled, supabase_client, tenant_code, update_row, upsert_row

COLUMNS = ["flow_id", "client_id", "cohort_id", "title", "status", "owner", "next_step", "updated_at"]


def load_rows() -> pd.DataFrame:
    if not is_supabase_enabled():
        return pd.DataFrame(columns=COLUMNS)
    try:
        response = supabase_client().table("flow_runs").select("*").eq("tenant_code", tenant_code()).execute()
        df = pd.DataFrame(response.data or [])
        if df.empty:
            return pd.DataFrame(columns=COLUMNS)
        if "tenant_code" in df.columns:
            df = df.drop(columns=["tenant_code"])
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = None
        return df[COLUMNS]
    except Exception as exc:
        st.warning(f"flow_runs read skipped: {exc}")
        return pd.DataFrame(columns=COLUMNS)


def save_row(row: dict[str, object]) -> None:
    upsert_row("flow_runs", row, "tenant_code,flow_id")


def save_status(flow_id: str, status: str, owner: str, next_step: str, updated_at: str) -> None:
    update_row("flow_runs", "flow_id", flow_id, {"status": status, "owner": owner, "next_step": next_step, "updated_at": updated_at})
