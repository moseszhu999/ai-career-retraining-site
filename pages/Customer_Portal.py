from __future__ import annotations

import streamlit as st

from frontend.customer_pages import customer_portal_page
from frontend.operation_state import init_operation_state
from frontend.production_state import init_production_admin_state
from frontend.runtime_binding_v2 import bind_production_master_data
from frontend.state import init_state, login_as
from frontend.styles import apply_styles

st.set_page_config(page_title="Customer Portal", page_icon="📦", layout="wide")

apply_styles()
init_state()
init_production_admin_state()
init_operation_state()
bind_production_master_data()

if not st.session_state.logged_in or st.session_state.role not in ["客户", "Founder"]:
    st.markdown("Customer Portal Preview")
    st.write("Read-only customer view for reports and proof files.")
    if st.button("Enter Customer Demo", type="primary", use_container_width=True):
        login_as("客户", "Customer Demo")
        st.rerun()
else:
    customer_portal_page()
