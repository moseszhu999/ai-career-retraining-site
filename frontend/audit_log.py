from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

AUDIT_COLUMNS = [
    "audit_id",
    "time",
    "actor",
    "role",
    "action",
    "object_type",
    "object_id",
    "before_status",
    "after_status",
    "summary",
]

SEED_AUDITS = [
    {
        "audit_id": "aud-001",
        "time": "2026-06-29 09:00",
        "actor": "System",
        "role": "系统",
        "action": "初始化测试业务数据",
        "object_type": "System",
        "object_id": "demo-state",
        "before_status": "空",
        "after_status": "已加载",
        "summary": "加载 JHC Java 新人训练营测试业务数据。",
    }
]


def init_audit_log() -> None:
    if "op_audit_logs" not in st.session_state:
        st.session_state.op_audit_logs = pd.DataFrame(SEED_AUDITS, columns=AUDIT_COLUMNS)


def audit_logs() -> pd.DataFrame:
    init_audit_log()
    return st.session_state.op_audit_logs


def add_audit(
    *,
    action: str,
    object_type: str,
    object_id: str,
    before_status: str = "",
    after_status: str = "",
    summary: str = "",
) -> str:
    init_audit_log()
    df = audit_logs().copy()
    audit_id = f"aud-{len(df) + 1:03d}"
    new_row = {
        "audit_id": audit_id,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor": str(st.session_state.get("user_name", "System")),
        "role": str(st.session_state.get("role", "系统")),
        "action": action,
        "object_type": object_type,
        "object_id": object_id,
        "before_status": before_status,
        "after_status": after_status,
        "summary": summary,
    }
    st.session_state.op_audit_logs = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return audit_id


def audit_metrics() -> dict[str, int]:
    df = audit_logs()
    return {
        "audit_count": int(len(df)),
        "founder_actions": int((df["role"] == "Founder").sum()),
        "learner_actions": int((df["role"] == "学员").sum()),
        "proof_actions": int((df["object_type"] == "ProofFile").sum()),
    }


def filter_audits(*, role: str = "全部", object_type: str = "全部") -> pd.DataFrame:
    df = audit_logs().copy()
    if role != "全部":
        df = df[df["role"] == role]
    if object_type != "全部":
        df = df[df["object_type"] == object_type]
    return df.sort_values("time", ascending=False)


def reset_audit_log() -> None:
    st.session_state.pop("op_audit_logs", None)
    init_audit_log()
