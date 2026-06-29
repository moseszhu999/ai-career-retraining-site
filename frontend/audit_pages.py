from __future__ import annotations

import streamlit as st

from frontend.audit_log import audit_metrics, filter_audits, reset_audit_log
from frontend.permissions import permission_summary_html, can_manage_operations, forbidden_message


def audit_log_page() -> None:
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><span class='pill hot'>操作审计日志</span><h2>谁在什么时候操作了哪个业务对象</h2><p>用于企业内训交付留痕：记录操作者、角色、动作、对象、前后状态和摘要。</p></div>",
        unsafe_allow_html=True,
    )
    if not can_manage_operations():
        st.warning(forbidden_message("查看操作审计日志"))
        return

    metrics = audit_metrics()
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>审计记录</span><div class='metric'>{metrics['audit_count']}</div></div>
  <div class='card'><span class='mini'>Founder操作</span><div class='metric'>{metrics['founder_actions']}</div></div>
  <div class='card'><span class='mini'>学员操作</span><div class='metric'>{metrics['learner_actions']}</div></div>
  <div class='card'><span class='mini'>Proof相关</span><div class='metric'>{metrics['proof_actions']}</div></div>
</div>
""", unsafe_allow_html=True)

    left, right = st.columns([1.2, .8])
    with left:
        role_filter = st.selectbox("角色筛选", ["全部", "Founder", "学员", "系统"])
    with right:
        object_filter = st.selectbox("对象类型筛选", ["全部", "Assignment", "Submission", "Review", "ProofFile", "Lead", "System"])
    df = filter_audits(role=role_filter, object_type=object_filter)
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        st.info("当前筛选条件下没有审计记录。")
        return

    labels = [f"{r.audit_id} · {r.action} · {r.object_type}:{r.object_id}" for r in df.itertuples()]
    selected = st.selectbox("查看审计详情", labels)
    row = df.iloc[labels.index(selected)]
    st.markdown(f"""
<div class='detail'>
<h3>{row['action']}</h3>
<p><b>时间：</b>{row['time']}<br>
<b>操作者：</b>{row['actor']}（{row['role']}）<br>
<b>对象：</b>{row['object_type']} / {row['object_id']}<br>
<b>状态变化：</b>{row['before_status']} → {row['after_status']}<br>
<b>摘要：</b>{row['summary']}</p>
</div>
""", unsafe_allow_html=True)

    if st.button("重置审计日志", use_container_width=True):
        reset_audit_log()
        st.rerun()
