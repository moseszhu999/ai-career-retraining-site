from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend import production_state as prod
from frontend.permissions import can_view_customer_report, forbidden_message, permission_summary_html


def _client_choice() -> tuple[str | None, pd.DataFrame]:
    clients = prod.clients()
    if clients.empty:
        return None, clients
    selected_id = st.session_state.get("current_client_id")
    if selected_id and selected_id in set(clients["client_id"].astype(str)):
        return str(selected_id), clients
    first_id = str(clients.iloc[0]["client_id"])
    st.session_state.current_client_id = first_id
    return first_id, clients


def _client_scope(client_id: str) -> dict[str, pd.DataFrame]:
    cohorts = prod.cohorts()
    learners = prod.learners()
    assignments = ops.assignments()
    reviews = ops.reviews()
    proofs = ops.proof_files()
    client_cohorts = cohorts[cohorts["client_id"] == client_id] if not cohorts.empty and "client_id" in cohorts.columns else cohorts.iloc[0:0]
    cohort_ids = set(client_cohorts["cohort_id"].astype(str)) if not client_cohorts.empty and "cohort_id" in client_cohorts.columns else set()
    client_learners = learners[learners["cohort_id"].astype(str).isin(cohort_ids)] if not learners.empty and "cohort_id" in learners.columns else learners.iloc[0:0]
    learner_names = set(client_learners["learner_name"].astype(str)) if not client_learners.empty and "learner_name" in client_learners.columns else set()
    client_assignments = assignments[assignments["cohort_id"].astype(str).isin(cohort_ids)] if not assignments.empty and "cohort_id" in assignments.columns else assignments.iloc[0:0]
    client_proofs = proofs[proofs["learner_name"].astype(str).isin(learner_names)] if not proofs.empty and "learner_name" in proofs.columns else proofs.iloc[0:0]
    return {"cohorts": client_cohorts, "learners": client_learners, "assignments": client_assignments, "reviews": reviews, "proofs": client_proofs}


def customer_portal_page() -> None:
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    if not can_view_customer_report():
        st.warning(forbidden_message("查看客户门户"))
        return
    client_id, clients = _client_choice()
    st.markdown("<div class='panel'><span class='pill hot'>Customer Portal · v5.3 Preview</span><h2>客户只读报告与交付包</h2><p>客户只能看客户范围内的班级、学员数量、Proof Files 和交付摘要。</p></div>", unsafe_allow_html=True)
    if client_id is None:
        st.info("暂无客户数据。Founder 需要先在 Admin/Health 创建客户。")
        return
    if st.session_state.get("role") == "Founder":
        labels = {f"{r.client_name} · {r.client_id}": str(r.client_id) for r in clients.itertuples()}
        label = st.selectbox("Founder 预览客户", list(labels.keys()))
        client_id = labels[label]
        st.session_state.current_client_id = client_id
    client = clients[clients["client_id"] == client_id].iloc[0]
    scoped = _client_scope(client_id)
    a, b, c, d = st.columns(4)
    a.metric("Client", str(client["client_name"]))
    b.metric("Cohorts", len(scoped["cohorts"]))
    c.metric("Learners", len(scoped["learners"]))
    d.metric("Proof Files", len(scoped["proofs"]))
    st.markdown("<div class='section'>客户交付摘要</div>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='detail'>
<h3>{client['client_name']}</h3>
<p><b>服务包：</b>{client.get('service_package', '')}<br><b>状态：</b>{client.get('status', '')}<br><b>客户可见说明：</b>本页面隐藏内部 Review 细节，只展示交付进展和已确认 Proof。</p>
</div>
""", unsafe_allow_html=True)
    st.markdown("<div class='section'>班级 / 学员</div>", unsafe_allow_html=True)
    st.dataframe(scoped["cohorts"], use_container_width=True, hide_index=True)
    st.dataframe(scoped["learners"], use_container_width=True, hide_index=True)
    st.markdown("<div class='section'>客户可见 Proof Files</div>", unsafe_allow_html=True)
    proofs = scoped["proofs"]
    if proofs.empty:
        st.info("暂无客户可见 Proof Files。")
    else:
        cols = [c for c in ["learner_name", "title", "status", "score", "evidence", "note"] if c in proofs.columns]
        st.dataframe(proofs[cols], use_container_width=True, hide_index=True)
    st.markdown("<div class='section'>客户报告 Markdown</div>", unsafe_allow_html=True)
    report = f"""# 客户交付报告\n\n客户：{client['client_name']}\n\n- 班级数：{len(scoped['cohorts'])}\n- 学员数：{len(scoped['learners'])}\n- Proof Files：{len(scoped['proofs'])}\n\n## 说明\n当前报告为客户只读版本，只展示客户可见数据，不展示内部审批细节。\n"""
    st.text_area("客户报告", value=report, height=260)
