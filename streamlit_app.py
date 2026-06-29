from __future__ import annotations

import streamlit as st

from frontend.business_pages import (
    assignments_page,
    clients_page,
    cohorts_page,
    leads_page,
    learners_page,
    render_business_top,
)
from frontend.operation_state import init_operation_state
from frontend.pages import (
    founder_dashboard,
    founder_queue,
    portfolio_page,
    render_public_site,
    student_dashboard,
    tasks_page,
)
from frontend.state import init_state
from frontend.styles import apply_styles

st.set_page_config(page_title="AI Skill Growth OS", page_icon="🚀", layout="wide")

apply_styles()
init_state()
init_operation_state()

if not st.session_state.logged_in:
    render_public_site()
else:
    render_business_top()
    view = st.session_state.current_view
    if st.session_state.role == "Founder":
        if view == "dashboard":
            founder_dashboard()
        elif view == "clients":
            clients_page()
        elif view == "cohorts":
            cohorts_page()
        elif view == "learners":
            learners_page()
        elif view == "tasks":
            tasks_page()
        elif view == "assignments":
            assignments_page()
        elif view == "queue":
            founder_queue()
        elif view == "portfolio":
            portfolio_page()
        elif view == "consult":
            leads_page()
        else:
            founder_dashboard()
    else:
        if view == "dashboard":
            student_dashboard()
        elif view == "tasks":
            tasks_page()
        elif view == "assignments":
            assignments_page()
        elif view == "portfolio":
            portfolio_page()
        elif view == "consult":
            leads_page()
        else:
            student_dashboard()

st.caption("AI Skill Growth OS · Split Business Operation Console · v4.9.4")
