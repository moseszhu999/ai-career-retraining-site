from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from frontend import flow_store

STEPS = ["draft", "configured", "assigned", "submitted", "agent_reviewed", "human_reviewing", "approved", "proof_ready", "exported"]
NEXT_STEP = dict(zip(STEPS[:-1], STEPS[1:]))
COLUMNS = ["flow_id", "client_id", "cohort_id", "title", "status", "owner", "next_step", "updated_at"]


def init() -> None:
    if "flow_runs" not in st.session_state:
        stored = flow_store.load_rows()
        st.session_state.flow_runs = stored if not stored.empty else pd.DataFrame(columns=COLUMNS)


def rows() -> pd.DataFrame:
    init()
    return st.session_state.flow_runs


def create(client_id: str, cohort_id: str, title: str) -> str:
    df = rows().copy()
    flow_id = f"flow-{len(df) + 1:03d}"
    row = {
        "flow_id": flow_id,
        "client_id": client_id,
        "cohort_id": cohort_id,
        "title": title,
        "status": "draft",
        "owner": "Founder",
        "next_step": "configured",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.flow_runs = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    flow_store.save_row(row)
    return flow_id


def advance(flow_id: str) -> str | None:
    df = rows().copy()
    found = df[df["flow_id"] == flow_id]
    if found.empty:
        return None
    idx = found.index[0]
    current = str(df.loc[idx, "status"])
    nxt = NEXT_STEP.get(current)
    if not nxt:
        return None
    owner = "Agent" if nxt == "submitted" else "Human" if nxt in ["agent_reviewed", "human_reviewing"] else "Founder"
    next_step = NEXT_STEP.get(nxt, "done")
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.loc[idx, "status"] = nxt
    df.loc[idx, "owner"] = owner
    df.loc[idx, "next_step"] = next_step
    df.loc[idx, "updated_at"] = updated_at
    st.session_state.flow_runs = df
    flow_store.save_status(flow_id, nxt, owner, next_step, updated_at)
    return nxt


def metrics() -> dict[str, int]:
    df = rows()
    if df.empty:
        return {"total": 0, "active": 0, "agent": 0, "human": 0, "proof_ready": 0, "exported": 0}
    return {
        "total": int(len(df)),
        "active": int((df["status"] != "exported").sum()),
        "agent": int((df["owner"] == "Agent").sum()),
        "human": int((df["owner"] == "Human").sum()),
        "proof_ready": int((df["status"] == "proof_ready").sum()),
        "exported": int((df["status"] == "exported").sum()),
    }
