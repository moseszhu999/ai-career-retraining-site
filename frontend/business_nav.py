from __future__ import annotations

import streamlit as st

from frontend.founder_context import founder_context_bar
from frontend.permissions import permission_summary_html
from frontend.persistence import data_backend, tenant_code
from frontend.state import chip, logout, set_view


def render_business_top() -> None:
    backend = data_backend()
    backend_label = "Supabase Persistent" if backend == "supabase" else "Session Demo"
    backend_class = "green" if backend == "supabase" else "orange"
    st.markdown(
        f"""
<div class='top executive-top'>
  <div class='brand'>AI Agent Governance OS<small>v5.2.0 · Executable Flow + Production Admin</small></div>
  <div>{chip(st.session_state.role)}<span class='pill'>{st.session_state.user_name}</span><span class='pill {backend_class}'>{backend_label}</span><span class='pill'>Tenant：{tenant_code()}</span><span class='pill'>最近：{st.session_state.last_event}</span></div>
</div>
""",
        unsafe_allow_html=True,
    )
    if st.session_state.role == "Founder":
        nav = [
            ("dashboard", "Dashboard"),
            ("admin", "Admin/Health"),
            ("workflow", "Executable Flow"),
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
            ("dashboard", "Dashboard"),
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
