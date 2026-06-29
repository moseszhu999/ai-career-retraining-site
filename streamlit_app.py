from __future__ import annotations

import streamlit as st

from frontend.pages import (
    consult_page,
    founder_dashboard,
    founder_queue,
    portfolio_page,
    render_app_top,
    render_public_site,
    student_dashboard,
    tasks_page,
)
from frontend.state import init_state
from frontend.styles import apply_styles

st.set_page_config(page_title="AI Skill Growth OS", page_icon="🚀", layout="wide")

apply_styles()
init_state()

if not st.session_state.logged_in:
    render_public_site()
else:
    render_app_top()
    if st.session_state.role == "Founder":
        if st.session_state.current_view == "dashboard":
            founder_dashboard()
        elif st.session_state.current_view == "queue":
            founder_queue()
        elif st.session_state.current_view == "tasks":
            tasks_page()
        elif st.session_state.current_view == "portfolio":
            portfolio_page()
        else:
            consult_page()
    else:
        if st.session_state.current_view == "dashboard":
            student_dashboard()
        elif st.session_state.current_view == "tasks":
            tasks_page()
        elif st.session_state.current_view == "portfolio":
            portfolio_page()
        else:
            consult_page()

st.caption("AI Skill Growth OS · Assignment Submission Review Records · v4.9.2")
