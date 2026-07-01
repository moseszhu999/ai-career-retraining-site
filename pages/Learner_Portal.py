from __future__ import annotations

import streamlit as st

from frontend.learner_portal import learner_portal_page
from frontend.operation_state import init_operation_state
from frontend.production_state import init_production_admin_state
from frontend.runtime_binding_v2 import bind_production_master_data
from frontend.state import init_state, login_as
from frontend.styles import apply_styles

st.set_page_config(page_title="Learner Portal", page_icon="🎓", layout="wide")

apply_styles()
init_state()
init_production_admin_state()
init_operation_state()
bind_production_master_data()

if not st.session_state.logged_in or st.session_state.role != "学员":
    st.markdown("Learner Portal Preview")
    st.write("Assigned-task learner view. Use a learner name that exists in Admin data for exact binding.")
    name = st.text_input("Learner name", value="佐藤拓海")
    if st.button("Enter Learner Demo", type="primary", use_container_width=True):
        login_as("学员", name)
        st.rerun()
else:
    learner_portal_page()
