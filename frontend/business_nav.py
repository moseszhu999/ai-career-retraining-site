from __future__ import annotations

import streamlit as st

from frontend.founder_context import founder_context_bar
from frontend.permissions import permission_summary_html
from frontend.state import chip, logout, set_view


def render_business_top() -> None:
    st.markdown(
        f"""
<div class='top'>
  <div class='brand'>AI Skill Growth OS<small>v4.10.0 · Data Export Delivery Pack</small></div>
  <div>{chip(st.session_state.role)}<span class='pill'>{st.session_state.user_name}</span><span class='pill'>最近：{st.session_state.last_event}</span></div>
</div>
""",
        unsafe_allow_html=True,
    )
    if st.session_state.role == "Founder":
        nav = [
            ("dashboard", "运营首页"),
            ("clients", "客户"),
            ("cohorts", "班级"),
            ("learners", "学员"),
            ("tasks", "练习题"),
            ("assignments", "Assignments"),
            ("queue", "Review Queue"),
            ("portfolio", "Proof Files"),
            ("consult", "Leads"),
            ("report", "Reports"),
            ("export", "Exports"),
            ("audit", "Audit"),
        ]
    else:
        nav = [
            ("dashboard", "业务首页"),
            ("tasks", "练习题"),
            ("assignments", "我的记录"),
            ("portfolio", "Proof Files"),
            ("consult", "服务包"),
        ]
    cols = st.columns(len(nav) + 1)
    for col, (view, label) in zip(cols, nav):
        if col.button(label, type="primary" if st.session_state.current_view == view else "secondary", use_container_width=True):
            set_view(view)
            st.rerun()
    if cols[-1].button("退出", use_container_width=True):
        logout()
        st.rerun()
    if st.session_state.role == "Founder":
        st.markdown(founder_context_bar(), unsafe_allow_html=True)
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
