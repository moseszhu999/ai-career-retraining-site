from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.business_data import CLIENTS, COHORTS, LEARNERS, SERVICE_PACKAGES
from frontend.founder_context import (
    founder_context_bar,
    set_assignment_context,
    set_client_context,
    set_cohort_context,
    set_learner_context,
)
from frontend.permissions import (
    can_confirm_proof,
    can_request_resubmission,
    can_update_leads,
    forbidden_message,
    permission_summary_html,
)
from frontend.state import chip, logout, set_view


def _cols(df: pd.DataFrame, names: list[str]) -> list[str]:
    return [c for c in names if c in df.columns]


def _accuracy_text(total: int, correct: int) -> str:
    if total <= 0:
        return "0%"
    return f"{correct / total * 100:.1f}%"


def render_business_top() -> None:
    st.markdown(
        f"""
<div class='top'>
  <div class='brand'>AI Skill Growth OS<small>v4.20.0 · MCQ Analytics</small></div>
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


def clients_page() -> None:
    op = ops.operation_metrics()
    st.markdown("<div class='panel'><span class='pill hot'>客户管理</span><h2>客户、合同金额、服务包状态</h2><p>选择客户后会同步更新 Founder 当前运营视角。</p></div>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>客户数</span><div class='metric'>{len(CLIENTS)}</div></div>
  <div class='card'><span class='mini'>进行中</span><div class='metric'>{int((CLIENTS['status']=='进行中').sum())}</div></div>
  <div class='card'><span class='mini'>合同额</span><div class='metric'>¥{int(CLIENTS['contract_value'].sum()):,}</div></div>
  <div class='card'><span class='mini'>线索金额</span><div class='metric'>¥{op['lead_value']:,}</div></div>
</div>
""", unsafe_allow_html=True)
    st.dataframe(CLIENTS, use_container_width=True, hide_index=True)
    selected = st.selectbox("查看客户", CLIENTS["client_name"].tolist())
    row = CLIENTS[CLIENTS["client_name"] == selected].iloc[0]
    set_client_context(str(row["client_id"]))
    related_cohorts = COHORTS[COHORTS["client_id"] == row["client_id"]]
    related_leads = ops.consult_leads()[ops.consult_leads()["client_name"].str.contains(str(row["client_name"]).split("教育")[0], na=False)]
    left, right = st.columns([1.1, .9])
    with left:
        st.markdown(f"<div class='detail'><h3>{row['client_name']}</h3>{chip(row['status'])}<p><b>联系人：</b>{row['contact']}<br><b>服务包：</b>{row['service_package']}<br><b>合同额：</b>¥{int(row['contract_value']):,}</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>关联班级</div>", unsafe_allow_html=True)
        st.dataframe(related_cohorts, use_container_width=True, hide_index=True)
    with right:
        st.markdown("<div class='section'>关联线索</div>", unsafe_allow_html=True)
        if related_leads.empty:
            st.info("暂无匹配线索。")
        else:
            st.dataframe(related_leads, use_container_width=True, hide_index=True)
        if st.button("进入 Leads 跟进", type="primary", use_container_width=True):
            set_view("consult")
            st.rerun()


def cohorts_page() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>班级管理</span><h2>班级、周期、讲师、训练状态</h2><p>选择班级后会同步当前客户和默认学员。</p></div>", unsafe_allow_html=True)
    st.dataframe(COHORTS, use_container_width=True, hide_index=True)
    selected = st.selectbox("选择班级", COHORTS["cohort_name"].tolist())
    cohort = COHORTS[COHORTS["cohort_name"] == selected].iloc[0]
    set_cohort_context(str(cohort["cohort_id"]))
    learners = LEARNERS[LEARNERS["cohort_id"] == cohort["cohort_id"]]
    tasks = ops.task_instances()[ops.task_instances()["cohort_id"] == cohort["cohort_id"]]
    records = ops.joined_records()[ops.joined_records()["cohort_id"] == cohort["cohort_id"]]
    mcq = records[records["question_type"] == "单选题"] if "question_type" in records.columns else records.iloc[0:0]
    correct = int(mcq["is_correct"].fillna(False).sum()) if not mcq.empty else 0
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>学员</span><div class='metric'>{len(learners)}</div></div>
  <div class='card'><span class='mini'>Assignments</span><div class='metric'>{len(records)}</div></div>
  <div class='card'><span class='mini'>选择题正确率</span><div class='metric'>{_accuracy_text(len(mcq), correct)}</div></div>
  <div class='card'><span class='mini'>平均进度</span><div class='metric'>{int(learners['progress'].mean()) if not learners.empty else 0}%</div></div>
</div>
""", unsafe_allow_html=True)
    st.markdown("<div class='section'>班级学员</div>", unsafe_allow_html=True)
    st.dataframe(learners, use_container_width=True, hide_index=True)
    st.markdown("<div class='section'>班级任务</div>", unsafe_allow_html=True)
    st.dataframe(tasks[["learner_name", "day", "proof_task", "status", "progress", "proof_score"]], use_container_width=True, hide_index=True)
    module_stats = ops.mcq_module_stats()
    if not module_stats.empty:
        st.markdown("<div class='section'>模块正确率 / 薄弱点</div>", unsafe_allow_html=True)
        st.dataframe(module_stats, use_container_width=True, hide_index=True)


def learners_page() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>学员管理</span><h2>学员进度、任务、提交、Proof状态</h2><p>选择学员后，顶部当前运营视角会同步到该学员。</p></div>", unsafe_allow_html=True)
    cohort_names = ["全部"] + COHORTS["cohort_name"].tolist()
    cohort_name = st.selectbox("班级筛选", cohort_names)
    df = LEARNERS.copy()
    if cohort_name != "全部":
        cohort_id = COHORTS[COHORTS["cohort_name"] == cohort_name].iloc[0]["cohort_id"]
        df = df[df["cohort_id"] == cohort_id]
        set_cohort_context(str(cohort_id))
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        return
    selected = st.selectbox("选择学员", df["learner_name"].tolist())
    learner = df[df["learner_name"] == selected].iloc[0]
    set_learner_context(str(learner["learner_id"]))
    records = ops.joined_records()[ops.joined_records()["learner_id"] == learner["learner_id"]]
    proofs = ops.proof_files()[ops.proof_files()["learner_name"] == learner["learner_name"]]
    tasks = ops.task_instances()[ops.task_instances()["learner_id"] == learner["learner_id"]]
    wrong = ops.wrong_answer_records(str(learner["learner_id"]))
    mcq = records[records["question_type"] == "单选题"] if "question_type" in records.columns else records.iloc[0:0]
    correct = int(mcq["is_correct"].fillna(False).sum()) if not mcq.empty else 0
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>进度</span><div class='metric'>{learner['progress']}%</div></div>
  <div class='card'><span class='mini'>选择题正确率</span><div class='metric'>{_accuracy_text(len(mcq), correct)}</div></div>
  <div class='card'><span class='mini'>错题数</span><div class='metric'>{len(wrong)}</div></div>
  <div class='card'><span class='mini'>Proof Files</span><div class='metric'>{len(proofs)}</div></div>
</div>
""", unsafe_allow_html=True)
    st.markdown("<div class='section'>任务</div>", unsafe_allow_html=True)
    st.dataframe(tasks[["day", "proof_task", "business_context", "status", "progress", "proof_score"]], use_container_width=True, hide_index=True)
    st.markdown("<div class='section'>Assignment / Submission / Review</div>", unsafe_allow_html=True)
    record_cols = _cols(records, ["assignment_id", "exercise_id", "selected_option", "correct_option", "is_correct", "auto_score", "score", "decision", "proof_ready"])
    st.dataframe(records[record_cols], use_container_width=True, hide_index=True)
    if not wrong.empty:
        st.markdown("<div class='section'>错题复习</div>", unsafe_allow_html=True)
        wrong_cols = _cols(wrong, ["exercise_id", "module", "related_task", "selected_option", "correct_option", "explanation", "hint"])
        st.dataframe(wrong[wrong_cols], use_container_width=True, hide_index=True)


def assignments_page() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Assignment 管理</span><h2>布置、提交、Review、Proof Ready 状态表</h2><p>选择题提交现在带结构化字段：选择项、正确项、是否正确、自动分数。</p></div>", unsafe_allow_html=True)
    records = ops.review_queue_view()
    metrics = ops.operation_metrics()
    a, b, c, d, e = st.columns(5)
    a.metric("Assignments", len(ops.assignments()))
    b.metric("Submissions", len(ops.submissions()))
    c.metric("MCQ 正确", metrics.get("mcq_correct", 0))
    d.metric("MCQ 正确率", _accuracy_text(metrics.get("mcq_total", 0), metrics.get("mcq_correct", 0)))
    e.metric("Proof Ready", int((ops.reviews()["proof_ready"] == "是").sum()))
    status_filter = st.selectbox("状态筛选", ["全部"] + sorted(records["status"].dropna().unique().tolist()))
    view = records if status_filter == "全部" else records[records["status"] == status_filter]
    cols = _cols(view, ["assignment_id", "exercise_id", "learner_name", "status", "selected_option", "correct_option", "is_correct", "auto_score", "score", "decision", "proof_ready", "review_route"])
    st.dataframe(view[cols], use_container_width=True, hide_index=True)
    if view.empty:
        return
    labels = [f"{r.assignment_id} · {r.learner_name} · {r.exercise_id}" for r in view.itertuples()]
    selected = st.selectbox("选择记录操作", labels)
    row = view.iloc[labels.index(selected)]
    set_assignment_context(str(row["assignment_id"]))
    set_learner_context(str(row["learner_id"]))
    st.markdown(f"<div class='queue-card decision'><h3>{row['learner_name']} · {row['exercise_id']}</h3><p><b>选择：</b>{row.get('selected_option', '暂无')} / 正确：{row.get('correct_option', '暂无')} / 是否正确：{row.get('is_correct', '暂无')}<br><b>自动分数：</b>{row.get('auto_score', '暂无')} · <b>Review 分数：</b>{row['score'] if pd.notna(row.get('score')) else '未评分'}<br><b>分流：</b>{row.get('review_route', '未分流')}<br><b>提交摘要：</b>{row['answer_summary'] if pd.notna(row.get('answer_summary')) else '暂无'}</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("确认进入 Proof Files", type="primary", use_container_width=True, disabled=not can_confirm_proof()):
        ops.mark_assignment_proof_ready(str(row["assignment_id"]))
        st.success("已确认并生成/更新 Proof File。")
        st.rerun()
    if c2.button("要求重新提交", use_container_width=True, disabled=not can_request_resubmission()):
        ops.request_resubmission(str(row["assignment_id"]))
        st.warning("已更新为需修改。")
        st.rerun()
    if c3.button("去 Review Queue", use_container_width=True):
        set_view("queue")
        st.rerun()
    if not can_confirm_proof():
        st.warning(forbidden_message("确认 Proof / 打回修改"))


def review_queue_page() -> None:
    records = ops.review_queue_view()
    module_stats = ops.mcq_module_stats()
    metrics = ops.operation_metrics()
    st.markdown("<div class='panel'><span class='pill hot'>Review Queue</span><h2>Founder处理选择题提交</h2><p>队列按选择题结果自动分流：选错→需复习；选对且分数达标→Proof候选；其他→Founder复核。</p></div>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>MCQ 提交</span><div class='metric'>{metrics.get('mcq_total', 0)}</div></div>
  <div class='card'><span class='mini'>正确</span><div class='metric'>{metrics.get('mcq_correct', 0)}</div></div>
  <div class='card'><span class='mini'>正确率</span><div class='metric'>{_accuracy_text(metrics.get('mcq_total', 0), metrics.get('mcq_correct', 0))}</div></div>
  <div class='card'><span class='mini'>需复习</span><div class='metric'>{len(ops.wrong_answer_records())}</div></div>
</div>
""", unsafe_allow_html=True)
    if not module_stats.empty:
        st.markdown("<div class='section'>模块正确率 / 优先复习模块</div>", unsafe_allow_html=True)
        st.dataframe(module_stats, use_container_width=True, hide_index=True)
    route_filter = st.selectbox("分流筛选", ["全部"] + sorted(records["review_route"].dropna().unique().tolist())) if not records.empty else "全部"
    view = records if route_filter == "全部" else records[records["review_route"] == route_filter]
    cols = _cols(view, ["assignment_id", "exercise_id", "module", "learner_name", "selected_option", "correct_option", "is_correct", "auto_score", "score", "decision", "proof_ready", "review_route"])
    st.dataframe(view[cols], use_container_width=True, hide_index=True)
    if view.empty:
        return
    labels = [f"{r.assignment_id} · {r.learner_name} · {r.exercise_id}" for r in view.itertuples()]
    selected = st.selectbox("选择处理项", labels)
    rec = view.iloc[labels.index(selected)]
    set_assignment_context(str(rec["assignment_id"]))
    set_learner_context(str(rec["learner_id"]))
    st.markdown(f"<div class='queue-card decision'><h3>{rec['learner_name']} · {rec['exercise_id']}</h3><p><b>模块：</b>{rec.get('module', '暂无')}<br><b>选择：</b>{rec.get('selected_option', '暂无')} / 正确：{rec.get('correct_option', '暂无')} / 是否正确：{rec.get('is_correct', '暂无')}<br><b>自动分数：</b>{rec.get('auto_score', '暂无')} · <b>Review：</b>{rec['score'] if pd.notna(rec.get('score')) else '未评分'}<br><b>分流：</b>{rec.get('review_route', '未分流')}<br><b>解析：</b>{rec.get('explanation', '暂无')}<br><b>提交摘要：</b>{rec['answer_summary'] if pd.notna(rec.get('answer_summary')) else '暂无'}</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("确认进入Proof Files", type="primary", use_container_width=True, disabled=not can_confirm_proof()):
        ops.mark_assignment_proof_ready(str(rec["assignment_id"]))
        st.success("已确认进入 Proof Files。")
        st.rerun()
    if c2.button("要求重新提交", use_container_width=True, disabled=not can_request_resubmission()):
        ops.request_resubmission(str(rec["assignment_id"]))
        st.warning("已要求重新提交。")
        st.rerun()
    if c3.button("标记已沟通", use_container_width=True, disabled=not can_request_resubmission()):
        st.info("已记录沟通。")
    if not can_confirm_proof():
        st.warning(forbidden_message("处理 Review Queue"))


def leads_page() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Leads / 服务包</span><h2>服务包报价、销售线索、跟进状态</h2><p>这里是把训练交付转成产品化收入的业务页。修改线索状态需要 Founder 权限。</p></div>", unsafe_allow_html=True)
    leads = ops.consult_leads()
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>服务包</span><div class='metric'>{len(SERVICE_PACKAGES)}</div></div>
  <div class='card'><span class='mini'>线索数</span><div class='metric'>{len(leads)}</div></div>
  <div class='card'><span class='mini'>潜在金额</span><div class='metric'>¥{int(leads['potential_value'].sum()):,}</div></div>
  <div class='card'><span class='mini'>已成交</span><div class='metric'>{int((leads['status']=='已成交').sum())}</div></div>
</div>
""", unsafe_allow_html=True)
    left, right = st.columns([1.2, .8])
    with left:
        st.markdown("<div class='section'>服务包</div>", unsafe_allow_html=True)
        st.dataframe(SERVICE_PACKAGES, use_container_width=True, hide_index=True)
        st.markdown("<div class='section'>线索</div>", unsafe_allow_html=True)
        st.dataframe(leads, use_container_width=True, hide_index=True)
        if not leads.empty:
            labels = [f"{r.lead_id} · {r.client_name} · {r.status}" for r in leads.itertuples()]
            selected = st.selectbox("选择线索改状态", labels)
            lead_id = selected.split(" · ")[0]
            c1, c2, c3 = st.columns(3)
            if c1.button("已联系", use_container_width=True, disabled=not can_update_leads()):
                ops.update_lead_status(lead_id, "已联系")
                st.rerun()
            if c2.button("已预约", use_container_width=True, disabled=not can_update_leads()):
                ops.update_lead_status(lead_id, "已预约")
                st.rerun()
            if c3.button("已成交", type="primary", use_container_width=True, disabled=not can_update_leads()):
                ops.update_lead_status(lead_id, "已成交")
                st.rerun()
            if not can_update_leads():
                st.warning(forbidden_message("修改 Leads 状态"))
    with right:
        st.markdown("<div class='lead-card'><h3>新增线索</h3><p>写入当前会话 Leads 表。需要 Founder 权限。</p>", unsafe_allow_html=True)
        with st.form("lead_form_v497"):
            client = st.text_input("客户名", value="某软件外包公司")
            package = st.text_input("服务包", value="企业训练版")
            need = st.text_input("需求", value="Java新人训练标准包")
            budget = st.number_input("预算 / 潜在金额", min_value=0, value=30000, step=1000)
            note = st.text_area("备注", value="希望把新人培训从讲师交付转成标准任务包。")
            ok = st.form_submit_button("新增线索", type="primary", disabled=not can_update_leads())
        if ok:
            ops.add_lead(client_name=client, package=package, need=need, potential_value=int(budget), note=note)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
