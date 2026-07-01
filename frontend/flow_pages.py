from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend import flow_runtime as flow
from frontend import production_state as prod


def executable_flow_page() -> None:
    flow.init()
    clients = prod.clients()
    cohorts = prod.cohorts()
    m = flow.metrics()
    st.markdown(
        "<div class='panel'><span class='pill hot'>v5.2 Executable Flow</span><h2>可执行流程状态机</h2><p>把原来的 Workflow 蓝图改成可创建、可推进、可查看卡点的执行台。</p></div>",
        unsafe_allow_html=True,
    )
    a, b, c, d, e = st.columns(5)
    a.metric("Total", m["total"])
    b.metric("Active", m["active"])
    c.metric("Agent", m["agent"])
    d.metric("Human", m["human"])
    e.metric("Proof Ready", m["proof_ready"])

    if clients.empty or cohorts.empty:
        st.warning("先到 Admin/Health 创建客户和班级，然后再创建可执行流程。")
        return

    left, right = st.columns([1.1, 0.9])
    with left:
        st.markdown("<div class='section'>创建流程</div>", unsafe_allow_html=True)
        client_options = {f"{r.client_name} · {r.client_id}": r.client_id for r in clients.itertuples()}
        client_label = st.selectbox("客户", list(client_options.keys()))
        client_id = client_options[client_label]
        cohort_rows = cohorts[cohorts["client_id"] == client_id]
        if cohort_rows.empty:
            st.info("这个客户还没有班级。")
        else:
            cohort_options = {f"{r.cohort_name} · {r.cohort_id}": r.cohort_id for r in cohort_rows.itertuples()}
            cohort_label = st.selectbox("班级", list(cohort_options.keys()))
            title = st.text_input("流程标题", value="Training-to-Proof Delivery Flow")
            if st.button("创建流程", type="primary", use_container_width=True):
                flow_id = flow.create(client_id=str(client_id), cohort_id=str(cohort_options[cohort_label]), title=title)
                st.success(f"已创建：{flow_id}")
                st.rerun()
    with right:
        st.markdown("<div class='section'>状态链</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='card'><p>draft → configured → assigned → submitted → agent_reviewed → human_reviewing → approved → proof_ready → exported</p></div>",
            unsafe_allow_html=True,
        )

    df = flow.rows()
    st.markdown("<div class='section'>流程待办</div>", unsafe_allow_html=True)
    if df.empty:
        st.info("暂无流程。")
        return
    st.dataframe(df, use_container_width=True, hide_index=True)
    labels = [f"{r.flow_id} · {r.title} · {r.status}" for r in df.itertuples()]
    selected = st.selectbox("选择流程", labels)
    flow_id = selected.split(" · ")[0]
    row = df[df["flow_id"] == flow_id].iloc[0]
    st.markdown(
        f"<div class='detail'><h3>{row['title']}</h3><span class='pill hot'>{row['status']}</span><p><b>Owner：</b>{row['owner']}<br><b>Next：</b>{row['next_step']}<br><b>Updated：</b>{row['updated_at']}</p></div>",
        unsafe_allow_html=True,
    )
    if row["next_step"] == "done":
        st.success("流程已导出完成。")
    elif st.button(f"推进到下一状态：{row['next_step']}", type="primary", use_container_width=True):
        next_status = flow.advance(flow_id)
        st.success(f"已推进到：{next_status}")
        st.rerun()

    board = df.groupby("status", dropna=False).size().reset_index(name="count")
    st.markdown("<div class='section'>卡点分布</div>", unsafe_allow_html=True)
    st.dataframe(board, use_container_width=True, hide_index=True)
