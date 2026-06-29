from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from frontend.business_data import (
    CLIENTS,
    COHORTS,
    CONSULT_LEADS,
    LEARNERS,
    PROOF_FILES,
    SERVICE_PACKAGES,
    TASK_INSTANCES,
    get_business_metrics,
)
from frontend.data import recommend_package
from frontend.state import chip, history_html, log_event, login_as, logout, set_view


def _events() -> list[str]:
    st.session_state.setdefault("business_events", ["业务测试数据已加载：JHC 2026 Java新人训练营。"])
    return st.session_state.business_events


def _record_event(message: str) -> None:
    stamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.business_events = [f"{stamp} · {message}"] + _events()[:10]
    log_event(message)


def _event_panel() -> str:
    return "<div class='history'><h3>业务操作记录</h3>" + "".join(
        f"<div class='history-item'>{item}</div>" for item in _events()
    ) + "</div>"


def _selected_cohort_id() -> str:
    st.session_state.setdefault("selected_cohort_id", "jhc-2026-java")
    return st.session_state.selected_cohort_id


def _selected_learner_id() -> str:
    st.session_state.setdefault("selected_learner_id", "jhc-s01")
    return st.session_state.selected_learner_id


def _task_rows_for_selection() -> pd.DataFrame:
    rows = TASK_INSTANCES[TASK_INSTANCES["cohort_id"] == _selected_cohort_id()]
    learner_id = _selected_learner_id()
    if learner_id:
        rows = rows[rows["learner_id"] == learner_id]
    return rows.copy()


def render_public_site() -> None:
    metrics = get_business_metrics()
    st.markdown("""
<div class='top'><div class='brand'>AI Skill Growth OS<small>Concrete Business Ops · JHC Java Training Demo</small></div><div class='nav'><span class='pill'>Clients</span><span class='pill'>Cohorts</span><span class='pill'>Proof Tasks</span><span class='pill'>Review Queue</span><span class='pill hot'>进入业务系统</span></div></div>
""", unsafe_allow_html=True)
    left, right = st.columns([1.2, .8])
    with left:
        st.markdown("""
<div class='hero'><span class='pill hot'>业务运营版 · v4.9.0</span><h1>从展示页变成<br><span>训练业务操作网站</span></h1><p>当前测试业务固定为：信华信日本业务部 2026 Java新人训练营。系统围绕真实业务对象运行：客户、班级、学员、Proof Task、Agent Review、Skill Proof File、咨询线索和服务包。</p></div>
""", unsafe_allow_html=True)
        st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>进行中客户</span><div class='metric'>{metrics['active_clients']}</div></div>
  <div class='card'><span class='mini'>训练班级</span><div class='metric'>{metrics['active_cohorts']}</div></div>
  <div class='card'><span class='mini'>测试学员</span><div class='metric'>{metrics['learners']}</div></div>
  <div class='card'><span class='mini'>潜在线索金额</span><div class='metric'>¥{metrics['lead_value']:,}</div></div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<div class='section'>具体业务数据</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid3'><div class='card'><h3>客户</h3><p>信华信日本业务部、比特顽童教育。</p></div><div class='card'><h3>班级</h3><p>2026 JHC Java新人训练营，13人，3个月交付。</p></div><div class='card'><h3>任务</h3><p>登录测试、订单流转、日语Q&A、Spring Boot错误定位。</p></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>业务操作闭环</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid4'><div class='flow-step'><b>1. 建班</b><br><span class='mini'>客户、班级、学员。</span></div><div class='flow-step'><b>2. 分配任务</b><br><span class='mini'>Proof Task 和交付物。</span></div><div class='flow-step'><b>3. Review</b><br><span class='mini'>Agent Review + Founder决策。</span></div><div class='flow-step'><b>4. 转化</b><br><span class='mini'>作品证明和服务包线索。</span></div></div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='login-box'><div class='panel'><h2>进入业务系统</h2><p>选择学员或Founder身份，使用内置测试数据操作 JHC Java 新人训练业务。</p></div>", unsafe_allow_html=True)
        with st.form("public_login_form"):
            name = st.text_input("姓名 / 体验名", value="学员Demo")
            role = st.selectbox("选择身份", ["学员", "Founder"])
            submitted = st.form_submit_button("进入业务系统", type="primary")
        if submitted:
            login_as(role, name)
            st.rerun()
        c1, c2 = st.columns(2)
        if c1.button("学员业务Demo"):
            login_as("学员", "佐藤拓海")
            st.session_state.selected_learner_id = "jhc-s01"
            st.rerun()
        if c2.button("Founder运营Demo"):
            login_as("Founder", "Founder")
            st.rerun()
        st.markdown("<div class='card'><h3>推荐操作顺序</h3><p>1. Founder运营Demo<br>2. 查看客户/班级/学员指标<br>3. 进入 Review Queue<br>4. 处理待Review任务<br>5. 进入 Leads 标记跟进<br>6. 切学员体验 Proof Task</p></div></div>", unsafe_allow_html=True)


def render_app_top() -> None:
    st.markdown(f"""
<div class='top'><div class='brand'>AI Skill Growth OS<small>Business Operation Site · {st.session_state.role}</small></div><div>{chip(st.session_state.role)}<span class='pill'>{st.session_state.user_name}</span><span class='pill'>最近：{st.session_state.last_event}</span></div></div>
""", unsafe_allow_html=True)
    nav = [("dashboard", "业务首页"), ("tasks", "Proof Tasks"), ("portfolio", "Proof Files"), ("consult", "服务包/Leads")]
    if st.session_state.role == "Founder":
        nav = [("dashboard", "运营首页"), ("queue", "Review Queue"), ("portfolio", "Proof Files"), ("consult", "Leads/服务包")]
    cols = st.columns(len(nav) + 1)
    for col, (view, label) in zip(cols, nav):
        if col.button(label, type="primary" if st.session_state.current_view == view else "secondary", use_container_width=True):
            set_view(view)
            st.rerun()
    if cols[-1].button("退出", use_container_width=True):
        logout()
        st.rerun()


def student_dashboard() -> None:
    learner = LEARNERS[LEARNERS["learner_id"] == _selected_learner_id()].iloc[0]
    cohort = COHORTS[COHORTS["cohort_id"] == learner["cohort_id"]].iloc[0]
    task_rows = TASK_INSTANCES[TASK_INSTANCES["learner_id"] == learner["learner_id"]]
    current_task = task_rows.iloc[0]
    st.markdown(f"""
<div class='hero'><span class='pill hot'>学员业务首页 · v4.9.0</span><h1>{learner['learner_name']}：今天完成<br><span>{current_task['proof_task']}</span></h1><p>班级：{cohort['cohort_name']}。这是具体业务数据，不是空白展示页。你可以查看任务、修改草稿、请求Review并提交。</p><span class='pill'>小组：{learner['group']}</span><span class='pill'>状态：{learner['status']}</span><span class='pill'>完成任务：{learner['tasks_done']}</span><span class='pill'>Proof Files：{learner['proof_files']}</span></div>
""", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>训练进度</span><div class='metric'>{learner['progress']}%</div><div class='progress'><div class='bar' style='width:{learner['progress']}%'></div></div></div>
  <div class='card'><span class='mini'>当前任务</span><div class='metric'>{current_task['day']}</div><p>{current_task['proof_task']}</p></div>
  <div class='card'><span class='mini'>当前分数</span><div class='metric'>{current_task['proof_score']}</div></div>
  <div class='card'><span class='mini'>Founder决策</span><p>{current_task['founder_decision']}</p></div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("打开当前 Proof Task", type="primary", use_container_width=True):
        set_view("tasks")
        st.rerun()
    if c2.button("查看我的 Proof Files", use_container_width=True):
        set_view("portfolio")
        st.rerun()
    if c3.button("生成下一步训练路径", use_container_width=True):
        set_view("consult")
        st.rerun()
    st.markdown("<div class='section'>我的任务清单</div>", unsafe_allow_html=True)
    st.dataframe(task_rows[["day", "proof_task", "business_context", "status", "progress", "proof_score"]], use_container_width=True, hide_index=True)
    st.markdown(_event_panel(), unsafe_allow_html=True)


def founder_dashboard() -> None:
    metrics = get_business_metrics()
    st.markdown("""
<div class='hero'><span class='pill hot'>Founder运营首页 · v4.9.0</span><h1>现在是训练业务运营系统，<br><span>不是展示Demo</span></h1><p>这里直接管理客户、班级、学员、Proof Task、Review Queue、Proof Files 和 Leads。</p></div>
""", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card decision'><span class='mini'>进行中客户</span><div class='metric'>{metrics['active_clients']}</div></div>
  <div class='card decision'><span class='mini'>训练学员</span><div class='metric'>{metrics['learners']}</div></div>
  <div class='card decision'><span class='mini'>待Review</span><div class='metric'>{metrics['pending_reviews']}</div></div>
  <div class='card decision'><span class='mini'>线索金额</span><div class='metric'>¥{metrics['lead_value']:,}</div></div>
</div>
""", unsafe_allow_html=True)
    left, right = st.columns([1.25, .75])
    with left:
        st.markdown("<div class='section'>客户与班级</div>", unsafe_allow_html=True)
        st.dataframe(CLIENTS[["client_name", "service_package", "contract_value", "status"]], use_container_width=True, hide_index=True)
        st.dataframe(COHORTS[["cohort_name", "learner_count", "start_date", "end_date", "trainer", "status"]], use_container_width=True, hide_index=True)
        c1, c2 = st.columns(2)
        if c1.button("处理 Review Queue", type="primary", use_container_width=True):
            set_view("queue")
            st.rerun()
        if c2.button("查看 Leads/服务包", use_container_width=True):
            set_view("consult")
            st.rerun()
    with right:
        st.markdown("<div class='section'>今日运营建议</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><h3>优先处理待Review任务</h3><p>鈴木美咲的订单状态流转拆解已经达到81分，可确认进入Proof Files。</p></div>", unsafe_allow_html=True)
        st.markdown(_event_panel(), unsafe_allow_html=True)


def tasks_page() -> None:
    cohort_options = dict(zip(COHORTS["cohort_name"], COHORTS["cohort_id"]))
    cohort_name = st.selectbox("选择班级", list(cohort_options.keys()), index=0)
    st.session_state.selected_cohort_id = cohort_options[cohort_name]
    learner_rows = LEARNERS[LEARNERS["cohort_id"] == st.session_state.selected_cohort_id]
    learner_options = dict(zip(learner_rows["learner_name"], learner_rows["learner_id"]))
    learner_name = st.selectbox("选择学员", list(learner_options.keys()), index=0)
    st.session_state.selected_learner_id = learner_options[learner_name]
    rows = _task_rows_for_selection()
    st.markdown("<div class='panel'><span class='pill hot'>Proof Task 业务操作</span><h2>按班级和学员处理真实训练任务</h2><p>这里的任务都绑定到具体学员、业务场景、交付物、Agent Review 和 Founder 决策。</p></div>", unsafe_allow_html=True)
    st.dataframe(rows[["day", "proof_task", "business_context", "required_output", "status", "progress", "proof_score", "founder_decision"]], use_container_width=True, hide_index=True)
    if rows.empty:
        st.warning("当前学员没有任务。")
        return
    task_labels = [f"{r.day} · {r.proof_task} · {r.status}" for r in rows.itertuples()]
    selected_label = st.selectbox("选择要操作的任务", task_labels)
    selected_idx = task_labels.index(selected_label)
    task = rows.iloc[selected_idx]
    left, right = st.columns([1.2, .8])
    with left:
        st.markdown(f"""
<div class='editor'><h3>{task['proof_task']}</h3><p><b>学员：</b>{task['learner_name']}<br><b>业务场景：</b>{task['business_context']}<br><b>要求交付物：</b>{task['required_output']}<br><b>当前状态：</b>{chip(task['status'])}</p></div>
""", unsafe_allow_html=True)
        draft_key = f"draft_{task['task_id']}"
        st.session_state.setdefault(draft_key, task["draft"])
        st.text_area("Proof草稿 / 学员提交内容", key=draft_key, height=260)
        c1, c2, c3 = st.columns(3)
        if c1.button("保存草稿", type="primary", use_container_width=True):
            _record_event(f"保存 {task['learner_name']} 的 {task['proof_task']} 草稿")
            st.success("已保存到当前会话测试数据。")
        if c2.button("生成Agent Review", use_container_width=True):
            st.session_state[f"review_{task['task_id']}"] = "Agent Review：已补充业务边界、异常分支、证据结构建议。"
            _record_event(f"生成 {task['learner_name']} 的 Agent Review")
            st.rerun()
        if c3.button("提交Founder决策", use_container_width=True):
            st.session_state[f"submitted_{task['task_id']}"] = True
            _record_event(f"{task['learner_name']} 的任务已进入 Review Queue")
            st.rerun()
    with right:
        review = st.session_state.get(f"review_{task['task_id']}", task["agent_review"])
        st.markdown(f"<div class='quote'>{review}</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><h3>Founder可执行动作</h3><p>确认进入Proof Files / 打回修改 / 标记已沟通。</p></div>", unsafe_allow_html=True)
        st.markdown(_event_panel(), unsafe_allow_html=True)


def portfolio_page() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Skill Proof Files 业务库</span><h2>按学员沉淀可展示作品证明</h2><p>这里不再是静态作品集，而是训练交付后的证明文件库。</p></div>", unsafe_allow_html=True)
    status = st.selectbox("状态筛选", ["全部", "可展示", "待Review", "修改中"])
    df = PROOF_FILES.copy()
    if status != "全部":
        df = df[df["status"] == status]
    st.dataframe(df, use_container_width=True, hide_index=True)
    if not df.empty:
        selected = st.selectbox("查看证明文件", [f"{r.learner_name} · {r.title}" for r in df.itertuples()])
        row = df.iloc[[f"{r.learner_name} · {r.title}" for r in df.itertuples()].index(selected)]
        left, right = st.columns([1.2, .8])
        with left:
            st.markdown(f"<div class='detail'><h3>{row['title']}</h3>{chip(row['status'])}<p><b>学员：</b>{row['learner_name']}<br><b>证据：</b>{row['evidence']}<br><b>说明：</b>{row['note']}</p></div>", unsafe_allow_html=True)
            st.markdown("<div class='evidence-grid'><div class='evidence'><b>背景</b><br>来自真实训练任务。</div><div class='evidence'><b>方法</b><br>学员完成草稿并接受Review。</div><div class='evidence'><b>结果</b><br>形成可展示证明。</div><div class='evidence'><b>复盘</b><br>记录修改建议和Founder确认。</div></div>", unsafe_allow_html=True)
        with right:
            st.markdown(f"<div class='score-card'><span class='mini'>Proof Score</span><br><b>{row['score']}</b><p>{row['status']}</p></div>", unsafe_allow_html=True)
            if st.button("标记为客户汇报材料", type="primary", use_container_width=True):
                _record_event(f"{row['learner_name']} 的 {row['title']} 已标记为客户汇报材料")
                st.success("已标记。")
            st.markdown(_event_panel(), unsafe_allow_html=True)


def consult_page() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Leads / 服务包运营</span><h2>把训练交付转成可销售服务包</h2><p>这里管理真实测试线索、服务包报价和跟进状态。</p></div>", unsafe_allow_html=True)
    left, right = st.columns([1.15, .85])
    with left:
        st.markdown("<div class='section'>服务包</div>", unsafe_allow_html=True)
        st.dataframe(SERVICE_PACKAGES, use_container_width=True, hide_index=True)
        st.markdown("<div class='section'>线索列表</div>", unsafe_allow_html=True)
        st.dataframe(CONSULT_LEADS, use_container_width=True, hide_index=True)
    with right:
        st.markdown("<div class='lead-card'><h3>新增测试线索</h3><p>用于模拟真实业务：客户、需求、预算、状态。</p>", unsafe_allow_html=True)
        with st.form("lead_form_v490"):
            client = st.text_input("客户名", value="某软件外包公司")
            need = st.text_input("需求", value="Java新人训练标准包")
            budget = st.number_input("预算 / 潜在金额", min_value=0, value=30000, step=1000)
            note = st.text_area("备注", value="希望把新人培训从讲师交付转成标准任务包。")
            ok = st.form_submit_button("生成测试线索", type="primary")
        if ok:
            _record_event(f"新增线索：{client} · {need} · ¥{budget:,}")
            st.success("测试线索已加入业务操作记录。")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("标记 JHC 线索已预约", use_container_width=True):
            _record_event("JHC Java新人训练标准包线索已标记为已预约")
            st.success("状态已更新到操作记录。")
        if st.button("标记比特顽童线索已联系", use_container_width=True):
            _record_event("比特顽童讲师训练包线索已标记为已联系")
            st.success("状态已更新到操作记录。")
        st.markdown(_event_panel(), unsafe_allow_html=True)


def founder_queue() -> None:
    pending = TASK_INSTANCES[TASK_INSTANCES["status"].isin(["待Review", "需修改"])]
    st.markdown("<div class='panel'><span class='pill hot'>Review Queue</span><h2>Founder处理具体任务和线索</h2><p>这里显示真实测试队列：哪些学员待Review，哪些线索待跟进。</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='section'>待处理 Proof Tasks</div>", unsafe_allow_html=True)
    st.dataframe(pending[["learner_name", "day", "proof_task", "status", "proof_score", "founder_decision"]], use_container_width=True, hide_index=True)
    if not pending.empty:
        label_map = {f"{r.learner_name} · {r.proof_task} · {r.status}": r for r in pending.itertuples()}
        selected = st.selectbox("选择处理项", list(label_map.keys()))
        task = label_map[selected]
        st.markdown(f"<div class='queue-card decision'><h3>{task.learner_name} · {task.proof_task}</h3><p><b>场景：</b>{task.business_context}<br><b>Agent Review：</b>{task.agent_review}<br><b>当前决策：</b>{task.founder_decision}</p></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        if c1.button("确认进入Proof Files", type="primary", use_container_width=True):
            _record_event(f"确认 {task.learner_name} 的 {task.proof_task} 进入 Proof Files")
            st.success("已确认。")
        if c2.button("打回修改", use_container_width=True):
            _record_event(f"打回 {task.learner_name} 的 {task.proof_task} 修改")
            st.warning("已打回。")
        if c3.button("标记已沟通", use_container_width=True):
            _record_event(f"已和 {task.learner_name} 沟通 {task.proof_task}")
            st.info("已记录沟通。")
    st.markdown("<div class='section'>待跟进 Leads</div>", unsafe_allow_html=True)
    st.dataframe(CONSULT_LEADS[["client_name", "package", "need", "status", "potential_value"]], use_container_width=True, hide_index=True)
    st.markdown(_event_panel(), unsafe_allow_html=True)
