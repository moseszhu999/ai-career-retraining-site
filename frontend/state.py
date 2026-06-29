from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from frontend.data import DEFAULT_DRAFT, STATUS_CLASS


def init_state() -> None:
    defaults = {
        "logged_in": False,
        "role": "访客",
        "user_name": "体验用户",
        "current_view": "dashboard",
        "active_task_index": 1,
        "task_status": "未开始",
        "draft": DEFAULT_DRAFT,
        "draft_saved": False,
        "saved_at": "",
        "ai_feedback": "",
        "submitted": False,
        "portfolio_candidate": False,
        "portfolio_approved": False,
        "active_portfolio_index": 0,
        "consult_summary": "",
        "lead_status": "新线索",
        "last_event": "尚未开始互动",
        "action_history": ["进入体验后，系统会记录你的关键操作。"],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def chip(text: str) -> str:
    return f"<span class='pill {STATUS_CLASS.get(str(text), '')}'>{text}</span>"


def set_view(view: str) -> None:
    st.session_state.current_view = view


def log_event(message: str) -> None:
    stamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.last_event = message
    st.session_state.action_history = [f"{stamp} · {message}"] + st.session_state.action_history[:9]


def login_as(role: str, name: str) -> None:
    st.session_state.logged_in = True
    st.session_state.role = role
    st.session_state.user_name = name or ("Founder" if role == "Founder" else "学员Demo")
    st.session_state.current_view = "dashboard"
    log_event(f"已登录：{role}")


def logout() -> None:
    st.session_state.logged_in = False
    st.session_state.role = "访客"
    st.session_state.user_name = "体验用户"
    st.session_state.current_view = "dashboard"
    log_event("已退出登录")


def ai_feedback_for(draft: str) -> str:
    missing = []
    if "权限" not in draft:
        missing.append("补权限差异：普通用户、管理员、未授权用户")
    if "SQL" not in draft and "注入" not in draft:
        missing.append("补安全场景：SQL注入、暴力尝试、锁定策略")
    if "边界" not in draft and "超长" not in draft:
        missing.append("补边界输入：超长用户名、特殊字符、空格")
    if "Bug" not in draft and "严重度" not in draft:
        missing.append("补Bug报告模板：标题、步骤、实际结果、预期结果、严重度")
    if not missing:
        missing.append("整理成作品集结构：背景 → 方法 → 结果 → 证据 → 复盘")
    return "【AI即时反馈】\n你的草稿已经具备基础结构。\n\n建议补充：\n" + "\n".join(
        f"{idx}. {item}" for idx, item in enumerate(missing, start=1)
    ) + "\n\n下一步：补 6 条测试用例，再写 1 个完整 Bug 报告样例。"


def portfolio_df() -> pd.DataFrame:
    rows = [
        ["目标拆解", "5天成长路线图", "86", "可展示", "职业成长", "目标清晰、路径可执行。", "把个人目标拆成5天任务，能说明路线和交付物。"],
        ["测试用例作品", "测试用例 + Bug报告", "64", "修改中", "软件测试", "还缺权限、安全、边界。", "已经覆盖基础登录，但需要补充权限、安全和边界测试。"],
        ["复杂需求拆解", "流程 + 异常分支", "--", "待点评", "业务分析", "等待Agent正式点评。", "适合作为业务分析或测试分析作品候选。"],
    ]
    if st.session_state.portfolio_candidate:
        status = "可展示" if st.session_state.portfolio_approved else "待点评"
        rows.append(["登录测试作品", "测试用例 + Bug报告草稿", "待定", status, "软件测试", "已提交给Agent，等待确认是否可展示。", "来自当前会话的提交记录，后续可沉淀成作品集材料。"])
    return pd.DataFrame(rows, columns=["作品", "证明材料", "评分", "状态", "方向", "说明", "Agent摘要"])


def history_html() -> str:
    return "<div class='history'><h3>操作历史</h3>" + "".join(
        f"<div class='history-item'>{item}</div>" for item in st.session_state.action_history
    ) + "</div>"
