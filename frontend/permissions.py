from __future__ import annotations

import streamlit as st

FOUNDER_ACTIONS = [
    "管理客户 / 班级 / 学员",
    "布置练习题",
    "处理 Review Queue",
    "确认进入 Proof Files",
    "要求重新提交",
    "修改 Leads 状态",
]

LEARNER_ACTIONS = [
    "查看自己的任务",
    "提交自己的作答",
    "请求自己的 Agent 初评",
    "查看自己的 Review",
    "查看自己的 Proof Files",
]


def role() -> str:
    return str(st.session_state.get("role", "访客"))


def is_founder() -> bool:
    return role() == "Founder"


def is_learner() -> bool:
    return role() == "学员"


def can_manage_operations() -> bool:
    return is_founder()


def can_assign_exercise() -> bool:
    return is_founder()


def can_confirm_proof() -> bool:
    return is_founder()


def can_request_resubmission() -> bool:
    return is_founder()


def can_update_leads() -> bool:
    return is_founder()


def can_submit_own_work(learner_id: str) -> bool:
    if is_founder():
        return True
    return str(st.session_state.get("learner_id", st.session_state.get("selected_learner_id", ""))) == str(learner_id)


def can_request_agent_review(learner_id: str) -> bool:
    return can_submit_own_work(learner_id)


def permission_summary_html() -> str:
    if is_founder():
        items = " / ".join(FOUNDER_ACTIONS)
        return f"<div class='ok'><b>当前权限：Founder运营权限</b><br>{items}</div>"
    if is_learner():
        items = " / ".join(LEARNER_ACTIONS)
        return f"<div class='ok'><b>当前权限：学员本人权限</b><br>{items}</div>"
    return "<div class='warn'><b>当前权限：访客</b><br>只能查看公开介绍，不能操作业务数据。</div>"


def forbidden_message(action: str) -> str:
    return f"当前角色不能执行：{action}。请切换到有权限的账号。"
