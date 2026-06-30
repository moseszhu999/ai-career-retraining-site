from __future__ import annotations

import streamlit as st

from frontend.audit_pages import audit_log_page
from frontend.business_nav import render_business_top
from frontend.business_pages import (
    assignments_page,
    clients_page,
    cohorts_page,
    leads_page,
    learners_page,
    review_queue_page,
)
from frontend.executive_pages import founder_executive_dashboard, render_executive_public_site
from frontend.export_pages import export_page
from frontend.operation_state import init_operation_state
from frontend.pages import (
    portfolio_page,
    tasks_page,
)
from frontend.report_pages import delivery_report_page
from frontend.state import init_state
from frontend.student_business_pages import (
    student_home_page,
    student_proof_files_page,
    student_records_page,
    student_service_page,
    student_tasks_page,
)
from frontend.styles import apply_styles

st.set_page_config(page_title="AI Agent Governance & Readiness OS", page_icon="🚀", layout="wide")

apply_styles()
init_state()
init_operation_state()

if not st.session_state.logged_in:
    render_executive_public_site()
else:
    render_business_top()
    view = st.session_state.current_view
    if st.session_state.role == "Founder":
        if view == "dashboard":
            founder_executive_dashboard()
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
            review_queue_page()
        elif view == "portfolio":
            portfolio_page()
        elif view == "consult":
            leads_page()
        elif view == "report":
            delivery_report_page()
        elif view == "export":
            export_page()
        elif view == "audit":
            audit_log_page()
        else:
            founder_executive_dashboard()
    else:
        if view == "dashboard":
            student_home_page()
        elif view == "tasks":
            student_tasks_page()
        elif view == "assignments":
            student_records_page()
        elif view == "portfolio":
            student_proof_files_page()
        elif view == "consult":
            student_service_page()
        else:
            student_home_page()

st.caption("AI Agent Governance & Readiness OS · Executive Workflow Pack · v4.22.0")
