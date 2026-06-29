from __future__ import annotations

from datetime import datetime
from typing import Literal

import pandas as pd
import streamlit as st

from frontend.data import TASKS, recommend_package
from frontend.state import ai_feedback_for, log_event, portfolio_df

LeadStatus = Literal["新线索", "已联系", "已预约", "已成交"]
TaskStatus = Literal["未开始", "进行中", "AI已反馈", "待Agent点评", "Agent已点评"]


# -----------------------------------------------------------------------------
# Frontend service layer
# -----------------------------------------------------------------------------
# Current implementation: session_state demo fallback.
# Future implementation: replace the bodies with Supabase/Auth/Agent calls.
# Pages should gradually call this module instead of directly mutating state.


def get_current_user() -> dict[str, str | bool]:
    return {
        "logged_in": bool(st.session_state.get("logged_in", False)),
        "role": str(st.session_state.get("role", "访客")),
        "user_name": str(st.session_state.get("user_name", "体验用户")),
    }


def get_tasks() -> pd.DataFrame:
    """Return task templates / task instances for the current user.

    Demo mode returns static TASKS. Supabase mode should merge templates with
    task_instances for the signed-in user.
    """
    return TASKS.copy()


def get_active_task() -> pd.Series:
    tasks = get_tasks()
    index = int(st.session_state.get("active_task_index", 1))
    index = max(0, min(index, len(tasks) - 1))
    return tasks.iloc[index]


def open_task(index: int) -> None:
    st.session_state.active_task_index = index
    task = get_tasks().iloc[index]
    log_event(f"切换任务：{task['day']} {task['title']}")


def get_task_status() -> str:
    return str(st.session_state.get("task_status", "未开始"))


def save_draft(draft: str | None = None) -> None:
    """Save current draft.

    Demo mode stores in session_state. Supabase mode should update
    task_instances.draft and task_instances.status.
    """
    if draft is not None:
        st.session_state.draft = draft
    st.session_state.draft_saved = True
    st.session_state.saved_at = datetime.now().strftime("%H:%M:%S")
    st.session_state.task_status = "进行中"
    log_event(f"草稿已保存 {st.session_state.saved_at}")


def request_ai_feedback(draft: str | None = None) -> str:
    """Request AI feedback for the current draft.

    Demo mode uses deterministic rule-based feedback. Later this should call an
    Agent service and persist feedback / agent_runs.
    """
    if draft is not None:
        st.session_state.draft = draft
    feedback = ai_feedback_for(st.session_state.draft)
    st.session_state.ai_feedback = feedback
    st.session_state.task_status = "AI已反馈"
    log_event("AI反馈已生成")
    return feedback


def submit_task_to_agent() -> None:
    """Submit current task for Agent / Founder review."""
    st.session_state.submitted = True
    st.session_state.portfolio_candidate = True
    st.session_state.task_status = "待Agent点评"
    log_event("已提交Agent，作品集候选+1")


def approve_portfolio_candidate(source: str = "Founder") -> None:
    st.session_state.portfolio_approved = True
    st.session_state.task_status = "Agent已点评"
    log_event(f"{source}确认作品集")


def request_portfolio_revision(source: str = "Founder") -> None:
    st.session_state.task_status = "AI已反馈"
    st.session_state.submitted = False
    st.session_state.portfolio_approved = False
    log_event(f"{source}打回修改")


def get_portfolio_items() -> pd.DataFrame:
    """Return portfolio items for the current user.

    Demo mode composes static items + current submitted candidate. Supabase mode
    should read portfolio_items and related reviews.
    """
    return portfolio_df()


def create_consult_summary(
    *,
    name: str,
    contact: str,
    identity: str,
    goal: str,
    urgency: str,
    note: str,
) -> str:
    package, reason, steps, deliverables = recommend_package(identity, goal)
    summary = (
        f"【咨询摘要】\n"
        f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"姓名：{name or '未填写'}\n"
        f"联系方式：{contact or '未填写'}\n"
        f"身份：{identity}\n"
        f"目标：{goal}\n"
        f"时效：{urgency}\n"
        f"推荐路径：{package}\n"
        f"推荐理由：{reason}\n"
        f"建议步骤：{' → '.join(steps)}\n"
        f"建议交付物：{' / '.join(deliverables)}\n"
        f"补充：{note or '无'}"
    )
    st.session_state.consult_summary = summary
    st.session_state.lead_status = "新线索"
    log_event("咨询摘要已生成，Founder线索+1")
    return summary


def update_lead_status(status: LeadStatus, source: str = "Founder") -> None:
    st.session_state.lead_status = status
    log_event(f"{source}标记线索{status}")


def get_founder_queue_counts() -> dict[str, int]:
    return {
        "pending_reviews": 1 if st.session_state.get("submitted") else 0,
        "portfolio_candidates": 1 if st.session_state.get("portfolio_candidate") else 0,
        "consult_leads": 1 if st.session_state.get("consult_summary") else 0,
    }
