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
from frontend.exercise_bank import EXERCISES, get_exercise_metrics
from frontend.training_records import ASSIGNMENTS, SUBMISSIONS, REVIEWS, get_training_record_metrics, joined_records
from frontend.state import chip, log_event, login_as, logout, set_view


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


def _record_board(learner_id: str | None = None) -> None:
    records = joined_records()
    if learner_id:
        records = records[records["learner_id"] == learner_id]
    st.markdown("<div class='section'>Assignment / Submission / Review 记录</div>", unsafe_allow_html=True)
    st.dataframe(
        records[["assignment_id", "exercise_id", "learner_name", "status", "submitted_at", "score", "decision", "proof_ready"]],
        use_container_width=True,
        hide_index=True,
    )
    if records.empty:
        return
    labels = [f"{r.assignment_id} · {r.learner_name} · {r.exercise_id}" for r in records.itertuples()]
    selected = st.selectbox("查看训练记录详情", labels, key=f"record_select_{learner_id or 'all'}")
    row = records.iloc[labels.index(selected)]
    left, right = st.columns([1.2, .8])
    with left:
        st.markdown(f"""
<div class='detail'>
<h3>{row['exercise_id']} · {row['learner_name']}</h3>
{chip(row['status'])}
<p><b>布置时间：</b>{row['assigned_at']}<br><b>截止时间：</b>{row['due_date']}<br><b>提交时间：</b>{row['submitted_at'] if pd.notna(row['submitted_at']) else '未提交'}<br><b>提交摘要：</b>{row['answer_summary'] if pd.notna(row['answer_summary']) else '暂无'}</p>
</div>
""", unsafe_allow_html=True)
    with right:
        st.markdown(f"""
<div class='score-card'><span class='mini'>Review Score</span><br><b>{int(row['score']) if pd.notna(row['score']) else '--'}</b><p>{row['decision'] if pd.notna(row['decision']) else '未Review'}</p></div>
""", unsafe_allow_html=True)
        if st.button("标记进入 Proof Files", type="primary", use_container_width=True, key=f"proof_{row['assignment_id']}"):
            _record_event(f"{row['learner_name']} 的 {row['exercise_id']} 已标记进入 Proof Files")
            st.success("已写入业务操作记录。")
        if st.button("要求重新提交", use_container_width=True, key=f"redo_{row['assignment_id']}"):
            _record_event(f"要求 {row['learner_name']} 重新提交 {row['exercise_id']}")
            st.warning("已写入业务操作记录。")


def _render_exercise_bank(current_learner_name: str | None = None) -> None:
    st.markdown("<div class='section'>业务练习题库</div>", unsafe_allow_html=True)
    metrics = get_exercise_metrics()
    record_metrics = get_training_record_metrics()
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>练习题</span><div class='metric'>{metrics['exercise_count']}</div></div>
  <div class='card'><span class='mini'>已布置</span><div class='metric'>{record_metrics['assignments']}</div></div>
  <div class='card'><span class='mini'>已提交</span><div class='metric'>{record_metrics['submissions']}</div></div>
  <div class='card'><span class='mini'>已Review</span><div class='metric'>{record_metrics['reviews']}</div></div>
</div>
""", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        module = st.selectbox("练习模块", ["全部"] + sorted(EXERCISES["module"].unique().tolist()))
    with m2:
        difficulty = st.selectbox("难度", ["全部", "基础", "中级", "高级"])
    filtered = EXERCISES.copy()
    if module != "全部":
        filtered = filtered[filtered["module"] == module]
    if difficulty != "全部":
        filtered = filtered[filtered["difficulty"] == difficulty]
    st.dataframe(filtered[["exercise_id", "module", "difficulty", "related_task", "required_output"]], use_container_width=True, hide_index=True)
    if filtered.empty:
        st.info("当前筛选条件下没有练习题。")
        return
    labels = [f"{r.exercise_id} · {r.module} · {r.related_task}" for r in filtered.itertuples()]
    selected = st.selectbox("选择练习题", labels)
    exercise = filtered.iloc[labels.index(selected)]
    left, right = st.columns([1.2, .8])
    with left:
        st.markdown(f"""
<div class='editor'>
<h3>{exercise['related_task']}</h3>
{chip(exercise['difficulty'])}<span class='pill purple'>{exercise['module']}</span>
<p><b>业务场景：</b>{exercise['scenario']}</p>
<p><b>练习题：</b>{exercise['question']}</p>
<p><b>要求交付物：</b>{exercise['required_output']}</p>
</div>
""", unsafe_allow_html=True)
        answer_key = f"answer_{exercise['exercise_id']}_{_selected_learner_id()}"
        st.text_area("学员作答 / 练习草稿", key=answer_key, height=220, placeholder="在这里写测试用例、流程分析、Q&A表或服务包摘要。")
        c1, c2, c3 = st.columns(3)
        if c1.button("布置给当前学员", use_container_width=True, key=f"assign_{exercise['exercise_id']}"):
            target = current_learner_name or LEARNERS[LEARNERS["learner_id"] == _selected_learner_id()].iloc[0]["learner_name"]
            _record_event(f"已布置练习题 {exercise['exercise_id']} 给 {target}")
            st.success("已写入业务操作记录。")
        if c2.button("提交作答", use_container_width=True, key=f"submit_{exercise['exercise_id']}"):
            target = current_learner_name or LEARNERS[LEARNERS["learner_id"] == _selected_learner_id()].iloc[0]["learner_name"]
            _record_event(f"{target} 提交练习题 {exercise['exercise_id']}")
            st.success("已写入提交记录。")
        if c3.button("生成Review", type="primary", use_container_width=True, key=f"review_{exercise['exercise_id']}"):
            target = current_learner_name or LEARNERS[LEARNERS["learner_id"] == _selected_learner_id()].iloc[0]["learner_name"]
            _record_event(f"已生成 {target} 的练习题 {exercise['exercise_id']} Review")
            st.success("已写入Review记录。")
    with right:
        st.markdown(f"<div class='card'><h3>提示</h3><p>{exercise['hint']}</p></div>", unsafe_allow_html=True)
        with st.expander("查看标准答案 / Golden Solution"):
            st.write(exercise["golden_solution"])
        with st.expander("查看评分标准"):
            st.write(exercise["rubric"])
        st.markdown(_event_panel(), unsafe_allow_html=True)


def render_public_site() -> None:
    metrics = get_business_metrics()
    exercise_metrics = get_exercise_metrics()
    record_metrics = get_training_record_metrics()
    st.markdown("""
<div class='top'><div class='brand'>AI Skill Growth OS<small>Concrete Business Ops · Assignment / Submission / Review</small></div><div class='nav'><span class='pill'>Clients</span><span class='pill'>Cohorts</span><span class='pill'>Exercises</span><span class='pill'>Records</span><span class='pill hot'>进入业务系统</span></div></div>
""", unsafe_allow_html=True)
    left, right = st.columns([1.2, .8])
    with left:
        st.markdown("""
<div class='hero'><span class='pill hot'>业务运营版 · v4.9.2</span><h1>练习题不是展示，<br><span>要有布置、提交、Review记录</span></h1><p>当前测试业务固定为：信华信日本业务部 2026 Java新人训练营。系统现在追踪 Assignment、Submission、Review 和是否进入 Skill Proof Files。</p></div>
""", unsafe_allow_html=True)
        st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>业务练习题</span><div class='metric'>{exercise_metrics['exercise_count']}</div></div>
  <div class='card'><span class='mini'>布置记录</span><div class='metric'>{record_metrics['assignments']}</div></div>
  <div class='card'><span class='mini'>提交记录</span><div class='metric'>{record_metrics['submissions']}</div></div>
  <div class='card'><span class='mini'>Review记录</span><div class='metric'>{record_metrics['reviews']}</div></div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<div class='section'>实际业务闭环</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid4'><div class='flow-step'><b>1. 布置 Assignment</b><br><span class='mini'>练习题绑定学员和截止日期。</span></div><div class='flow-step'><b>2. 学员 Submission</b><br><span class='mini'>记录作答内容和提交时间。</span></div><div class='flow-step'><b>3. Agent / Founder Review</b><br><span class='mini'>评分、点评、决策。</span></div><div class='flow-step'><b>4. Proof 入库</b><br><span class='mini'>优秀结果进入 Proof Files。</span></div></div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='login-box'><div class='panel'><h2>进入业务系统</h2><p>选择学员或Founder身份，查看练习题库和训练记录。</p></div>", unsafe_allow_html=True)
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
        st.markdown("<div class='card'><h3>推荐操作顺序</h3><p>1. Founder运营Demo<br>2. 打开练习题库<br>3. 布置给当前学员<br>4. 提交作答<br>5. 生成Review<br>6. 在Review Queue确认是否进入Proof Files</p></div></div>", unsafe_allow_html=True)


def render_app_top() -> None:
    st.markdown(f"""
<div class='top'><div class='brand'>AI Skill Growth OS<small>Business Operation Site · {st.session_state.role}</small></div><div>{chip(st.session_state.role)}<span class='pill'>{st.session_state.user_name}</span><span class='pill'>最近：{st.session_state.last_event}</span></div></div>
""", unsafe_allow_html=True)
    nav = [("dashboard", "业务首页"), ("tasks", "练习题/任务"), ("portfolio", "Proof Files"), ("consult", "服务包/Leads")]
    if st.session_state.role == "Founder":
        nav = [("dashboard", "运营首页"), ("queue", "Review Queue"), ("tasks", "练习题库"), ("portfolio", "Proof Files"), ("consult", "Leads/服务包")]
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
    learner_records = joined_records()[joined_records()["learner_id"] == learner["learner_id"]]
    st.markdown(f"""
<div class='hero'><span class='pill hot'>学员业务首页 · v4.9.2</span><h1>{learner['learner_name']}：今天完成<br><span>{current_task['proof_task']}</span></h1><p>班级：{cohort['cohort_name']}。现在可以看到分配给你的练习、提交记录和Review结果。</p><span class='pill'>小组：{learner['group']}</span><span class='pill'>状态：{learner['status']}</span><span class='pill'>Assignments：{len(learner_records)}</span><span class='pill'>Proof Files：{learner['proof_files']}</span></div>
""", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>训练进度</span><div class='metric'>{learner['progress']}%</div><div class='progress'><div class='bar' style='width:{learner['progress']}%'></div></div></div>
  <div class='card'><span class='mini'>当前任务</span><div class='metric'>{current_task['day']}</div><p>{current_task['proof_task']}</p></div>
  <div class='card'><span class='mini'>我的练习记录</span><div class='metric'>{len(learner_records)}</div></div>
  <div class='card'><span class='mini'>当前分数</span><div class='metric'>{current_task['proof_score']}</div></div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("打开练习题 / Proof Task", type="primary", use_container_width=True):
        set_view("tasks")
        st.rerun()
    if c2.button("查看我的 Proof Files", use_container_width=True):
        set_view("portfolio")
        st.rerun()
    if c3.button("生成下一步训练路径", use_container_width=True):
        set_view("consult")
        st.rerun()
    _record_board(learner_id=learner["learner_id"])
    st.markdown(_event_panel(), unsafe_allow_html=True)


def founder_dashboard() -> None:
    metrics = get_business_metrics()
    exercise_metrics = get_exercise_metrics()
    record_metrics = get_training_record_metrics()
    st.markdown("""
<div class='hero'><span class='pill hot'>Founder运营首页 · v4.9.2</span><h1>现在是训练业务运营系统，<br><span>练习题有完整记录链</span></h1><p>这里直接管理客户、班级、学员、练习题、Assignment、Submission、Review、Proof Files 和 Leads。</p></div>
""", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card decision'><span class='mini'>练习题</span><div class='metric'>{exercise_metrics['exercise_count']}</div></div>
  <div class='card decision'><span class='mini'>布置</span><div class='metric'>{record_metrics['assignments']}</div></div>
  <div class='card decision'><span class='mini'>提交</span><div class='metric'>{record_metrics['submissions']}</div></div>
  <div class='card decision'><span class='mini'>Proof Ready</span><div class='metric'>{record_metrics['proof_ready']}</div></div>
</div>
""", unsafe_allow_html=True)
    left, right = st.columns([1.25, .75])
    with left:
        st.markdown("<div class='section'>客户与班级</div>", unsafe_allow_html=True)
        st.dataframe(CLIENTS[["client_name", "service_package", "contract_value", "status"]], use_container_width=True, hide_index=True)
        st.dataframe(COHORTS[["cohort_name", "learner_count", "start_date", "end_date", "trainer", "status"]], use_container_width=True, hide_index=True)
        _record_board()
    with right:
        st.markdown("<div class='section'>今日运营建议</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><h3>先看需修改和Proof Ready</h3><p>田中悠真需要补Q&A场景；山本結衣已可进入客户汇报材料。</p></div>", unsafe_allow_html=True)
        if st.button("处理 Review Queue", type="primary", use_container_width=True):
            set_view("queue")
            st.rerun()
        if st.button("打开练习题库", use_container_width=True):
            set_view("tasks")
            st.rerun()
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
    st.markdown("<div class='panel'><span class='pill hot'>Proof Task + Assignment Records</span><h2>按班级和学员处理真实训练任务</h2><p>这里的练习题不只是题库，还能形成 Assignment、Submission 和 Review 记录。</p></div>", unsafe_allow_html=True)
    st.dataframe(rows[["day", "proof_task", "business_context", "required_output", "status", "progress", "proof_score", "founder_decision"]], use_container_width=True, hide_index=True)
    if not rows.empty:
        task_labels = [f"{r.day} · {r.proof_task} · {r.status}" for r in rows.itertuples()]
        selected_label = st.selectbox("选择要操作的任务", task_labels)
        task = rows.iloc[task_labels.index(selected_label)]
        left, right = st.columns([1.2, .8])
        with left:
            st.markdown(f"""
<div class='editor'><h3>{task['proof_task']}</h3><p><b>学员：</b>{task['learner_name']}<br><b>业务场景：</b>{task['business_context']}<br><b>要求交付物：</b>{task['required_output']}<br><b>当前状态：</b>{chip(task['status'])}</p></div>
""", unsafe_allow_html=True)
            draft_key = f"draft_{task['task_id']}"
            st.session_state.setdefault(draft_key, task["draft"])
            st.text_area("Proof草稿 / 学员提交内容", key=draft_key, height=220)
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
    _render_exercise_bank(current_learner_name=learner_name)
    _record_board(learner_id=st.session_state.selected_learner_id)


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
    _record_board()


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
        with st.form("lead_form_v492"):
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
    pending = joined_records()
    st.markdown("<div class='panel'><span class='pill hot'>Review Queue</span><h2>Founder处理具体提交和线索</h2><p>这里显示 Assignment / Submission / Review 记录：哪些学员已提交，哪些需修改，哪些可进入Proof Files。</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='section'>待处理训练记录</div>", unsafe_allow_html=True)
    st.dataframe(pending[["assignment_id", "exercise_id", "learner_name", "status", "submitted_at", "score", "decision", "proof_ready"]], use_container_width=True, hide_index=True)
    if not pending.empty:
        label_map = {f"{r.assignment_id} · {r.learner_name} · {r.exercise_id}": r for r in pending.itertuples()}
        selected = st.selectbox("选择处理项", list(label_map.keys()))
        rec = label_map[selected]
        st.markdown(f"<div class='queue-card decision'><h3>{rec.learner_name} · {rec.exercise_id}</h3><p><b>提交摘要：</b>{rec.answer_summary if pd.notna(rec.answer_summary) else '暂无'}<br><b>分数：</b>{rec.score if pd.notna(rec.score) else '未评分'}<br><b>决策：</b>{rec.decision if pd.notna(rec.decision) else '未Review'}<br><b>Proof Ready：</b>{rec.proof_ready if pd.notna(rec.proof_ready) else '否'}</p></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        if c1.button("确认进入Proof Files", type="primary", use_container_width=True):
            _record_event(f"确认 {rec.learner_name} 的 {rec.exercise_id} 进入 Proof Files")
            st.success("已确认。")
        if c2.button("要求重新提交", use_container_width=True):
            _record_event(f"要求 {rec.learner_name} 重新提交 {rec.exercise_id}")
            st.warning("已打回。")
        if c3.button("标记已沟通", use_container_width=True):
            _record_event(f"已和 {rec.learner_name} 沟通 {rec.exercise_id}")
            st.info("已记录沟通。")
    st.markdown("<div class='section'>待跟进 Leads</div>", unsafe_allow_html=True)
    st.dataframe(CONSULT_LEADS[["client_name", "package", "need", "status", "potential_value"]], use_container_width=True, hide_index=True)
    st.markdown(_event_panel(), unsafe_allow_html=True)
