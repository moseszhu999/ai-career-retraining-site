from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st
from supabase import Client, create_client


@st.cache_resource(show_spinner=False)
def supabase_client() -> Client:
    url = str(st.secrets.get("SUPABASE_URL", ""))
    key = str(st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", ""))
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required for Supabase persistence.")
    return create_client(url, key)


def data_backend() -> str:
    try:
        return str(st.secrets.get("DATA_BACKEND", "session"))
    except Exception:
        return "session"


def tenant_code() -> str:
    try:
        return str(st.secrets.get("TENANT_CODE", st.session_state.get("tenant_code", "demo")))
    except Exception:
        return str(st.session_state.get("tenant_code", "demo"))


def is_supabase_enabled() -> bool:
    return data_backend() == "supabase"


def clean_value(value: Any) -> Any:
    if value is pd.NA:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            return value
    return value


def clean_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: clean_value(value) for key, value in row.items()}


def with_tenant(row: dict[str, Any]) -> dict[str, Any]:
    return clean_row({"tenant_code": tenant_code(), **row})


def upsert_row(table: str, row: dict[str, Any], conflict_columns: str) -> None:
    if not is_supabase_enabled():
        return
    try:
        supabase_client().table(table).upsert(with_tenant(row), on_conflict=conflict_columns).execute()
    except Exception as exc:
        st.error(f"Supabase write failed: {table}. {exc}")
        raise


def insert_row(table: str, row: dict[str, Any]) -> None:
    if not is_supabase_enabled():
        return
    try:
        supabase_client().table(table).insert(with_tenant(row)).execute()
    except Exception as exc:
        st.error(f"Supabase insert failed: {table}. {exc}")
        raise


def update_row(table: str, key_column: str, key_value: str, values: dict[str, Any]) -> None:
    if not is_supabase_enabled():
        return
    try:
        supabase_client().table(table).update(clean_row(values)).eq("tenant_code", tenant_code()).eq(key_column, key_value).execute()
    except Exception as exc:
        st.error(f"Supabase update failed: {table}.{key_column}={key_value}. {exc}")
        raise
