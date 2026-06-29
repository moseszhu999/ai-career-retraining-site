from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.business_data import CLIENTS, COHORTS, LEARNERS, SERVICE_PACKAGES, get_business_metrics
from frontend.exercise_bank import EXERCISES, get_exercise_metrics
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
    rows = ops.task_instances()[ops.task_instances()["cohort_id"] == _selected_cohort_id()]
    learner_id = _selected_learner_id()
    if learner_id:
        rows = rows[rows["learner_id"] == learner_id]
    return rows.copy()


def _ensure_assignment(exercise_id: str, learner_id: str, learner_name: str, cohort_id: str, note: str) -> str:
    records = ops.joined_records()
    found = records[(records["exercise_id"] == exercise_id) & (records["learner_id"] == learner_id)]
    if not found.empty:
        return str(found.iloc[0]["assignment_id"])
    return ops.assign_exercise(
        exercise_id=exercise_id,
        learner_id=learner_id,
        learner_name=learner_name,
        cohort_id=cohort_id,
        note=note,
    )


def _ensure_submission(exercise_id: str, learner_id: str, learner_name: str, cohort_id: str, answer: str) -> str:
    assignment_id = _ensure_assignment(exercise_id, learner_id, learner_name, cohort_id, f"{exercise_id} 自动布置")
    return ops.submit_assignment(
        assignment_id=assignment_id,
        exercise_id=exercise_id,
        learner_id=learner_id,
        learner_name=learner_name,
        answer_summary=answer or "已提交练习作答。",
    )


def _record_board(learner_id: str | None = None) -> None:
    records = ops.joined_records()
    if learner_id:
        records = records[records["learner_id"] == learner_id]
    st.markdown("<div class='section'>Assignment / Submission / Review 状态表</div>", unsafe_allow_html=True)
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
        if st.button("确认进入 Proof Files", type="primary", use_container_width=True, key=f"proof_{row['assignment_id']}"):
            ops.mark_assignment_proof_ready(str(row["assignment_id"]))
            _record_event(f"{row['learner_name']} 的 {row['exercise_id']} 已进入 Proof Files")
            st.rerun()
        if st.button("要求重新提交", use_container_width=True, key=f"redo_{row['assignment_id']}"):
            ops.request_resubmission(str(row["assignment_id"]))
            _record_event(f"要求 {row['learner_name']} 重新提交 {row['exercise_id']}")
            st.rerun()


def _render_exercise_bank(current_learner_name: str | None = None) -> None:
    st.markdown("<div class='section'>业务练习题库</div>", unsafe_allow_html=True)
    metrics = get_exercise_metrics()
    op_metrics = ops.operation_metrics()
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>练习题</span><div class='metric'>{metrics['exercise_count']}</div></div>
  <div class='card'><span class='mini'>已布置</span><div class='metric'>{op_metrics['assignments']}</div></div>
  <div class='card'><span class='mini'>已提交</span><div class='metric'>{op_metrics['submissions']}</div></div>
  <div class='card'><span class='mini'>已Review</span><div class='metric'>{op_metrics['reviews']}</div></div>
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
    learner = LEARNERS[LEARNERS["learner_id"] == _selected_learner_id()].iloc[0]
    learner_id = str(learner["learner_id"])
    learner_name = current_learner_name or str(learner["learner_name"])
    cohort_id = str(learner["cohort_id"])
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
        answer_key = f"answer_{exercise['exercise_id']}_{learner_id}"
        answer = st.text_area("学员作答 / 练习草稿", key=answer_key, height=220, placeholder="在这里写测试用例、流程分析、Q&A表或服务包摘要。")
        c1, c2, c3 = st.columns(3)
        if c1.button("布置给当前学员", use_container_width=True, key=f"assign_{exercise['exercise_id']}"):
            assignment_id = ops.assign_exercise(
                exercise_id=str(exercise["exercise_id"]),
                learner_id=learner_id,
                learner_name=learner_name,
                cohort_id=cohort_id,
                note=str(exercise["related_task"]),
            )
            _record_event(f"已布置 {assignment_id} · {exercise['exercise_id']} 给 {learner_name}")
            st.rerun()
        if c2.button("提交作答", use_container_width=True, key=f"submit_{exercise['exercise_id']}"):
            submission_id = _ensure_submission(str(exercise["exercise_id"]), learner_id, learner_name, cohort_id, answer)
            _record_event(f"{learner_name} 提交 {submission_id} · {exercise['exercise_id']}")
            st.rerun()
        if c3.button("生成Review", type="primary", use_container_width=True, key=f"review_{exercise['exercise_id']}"):
            submission_id = _ensure_submission(str(exercise["exercise_id"]), learner_id, learner_name, cohort_id, answer)
            score = 82 if exercise["difficulty"] != "高级" else 78
            decision = "待Founder确认" if score >= 80 else "需修改"
            proof_ready = "候选" if score >= 80 else "否"
            ops.review_submission(
                submission_id=submission_id,
                reviewer="Agent",
                score=score,
                review_comment=f"Agent Review：{exercise['rubric']}。当前作答已生成初评。",
                decision=decision,
                proof_ready=proof_ready,
            )
            _record_event(f"已生成 {learner_name} 的 {exercise['exercise_id']} Review：{score}分")
            st.rerun()
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
    op_metrics = ops.operation_metrics()
    st.markdown("""
<div class='top'><div class='brand'>AI Skill Growth OS<small>Concrete Business Ops · Mutable State Tables</small></div><div class='nav'><span class='pill'>Clients</span><span class='pill'>Cohorts</span><span class='pill'>Exercises</span><span class='pill'>State Machine</span><span class='pill hot'>进入业务系统</span></div></div>
""", unsafe_allow_html=True)
    left, right = st.columns([1.2, .8])
    with left:
        st.markdown("""
<div class='hero'><span class='pill hot'>业务运营版 · v4.9.3</span><h1>练习题进入<br><span>可编辑业务状态机</span></h1><p>当前测试业务固定为：信华信日本业务部 2026 Java新人训练营。系统现在不仅展示 Assignment、Submission、Review，还会在按钮操作后更新当前会话数据表。</p></div>
""", unsafe_allow_html=True)
        st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>业务练习题</span><div class='metric'>{exercise_metrics['exercise_count']}</div></div>
  <div class='card'><span class='mini'>布置记录</span><div class='metric'>{op_metrics['assignments']}</div></div>
  <div class='card'><span class='mini'>Proof Files</span><div class='metric'>{op_metrics['proof_files']}</div></div>
  <div class='card'><span class='mini'>线索金额</span><div class='metric'>¥{op_metrics['lead_value']:,}</div></div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<div class='section'>实际业务状态机</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid4'><div class='flow-step'><b>1. 布置</b><br><span class='mini'>新增 Assignment 行。</span></div><div class='flow-step'><b>2. 提交</b><br><span class='mini'>新增或更新 Submission。</span></div><div class='flow-step'><b>3. Review</b><br><span class='mini'>新增或更新 Review。</span></div><div class='flow-step'><b>4. 入库</b><br><span class='mini'>新增 Proof File。</span></div></div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='login-box'><div class='panel'><h2>进入业务系统</h2><p>选择学员或Founder身份，操作会实时改变当前会话表。</p></div>", unsafe_allow_html=True)
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
        st.markdown("<div class='card'><h3>推荐操作顺序</h3><p>1. 打开练习题库<br>2. 布置给当前学员<br>3. 提交作答<br>4. 生成Review<br>5. 在Review Queue确认进入Proof Files<br>6. 去Proof Files查看新增证明</p></div></div>", unsafe_allow_html=True)


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
    if cols[-1].button("重置测试数据", use_container_width=True):
        ops.reset_operation_state()
        _record_event("已重置当前会话业务状态表")
        st.rerun()


def student_dashboard() -> None:
    learner = LEARNERS[LEARNERS["learner_id"] == _selected_learner_id()].iloc[0]
    cohort = COHORTS[COHORTS["cohort_id"] == learner["cohort_id"]].iloc[0]
    task_rows = ops.task_instances()[ops.task_instances()["learner_id"] == learner["learner_id"]]
    current_task = task_rows.iloc[0]
    learner_records = ops.joined_records()[ops.joined_records()["learner_id"] == learner["learner_id"]]
    st.markdown(f"""
<div class='hero'><span class='pill hot'>学员业务首页 · v4.9.3</span><h1>{learner['learner_name']}：今天完成<br><span>{current_task['proof_task']}</span></h1><p>班级：{cohort['cohort_name']}。现在可以看到分配给你的练习、提交记录、Review结果和Proof状态。</p><span class='pill'>小组：{learner['group']}</span><span class='pill'>状态：{learner['status']}</span><span class='pill'>Assignments：{len(learner_records)}</span><span class='pill'>Proof Files：{len(ops.proof_files()[ops.proof_files()['learner_name'] == learner['learner_name']])}</span></div>
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
    _record_board(learner_id=str(learner["learner_id"]))
    st.markdown(_event_panel(), unsafe_allow_html=True)


def founder_dashboard() -> None:
    metrics = get_business_metrics()
    exercise_metrics = get_exercise_metrics()
    op_metrics = ops.operation_metrics()
    st.markdown("""
<div class='hero'><span class='pill hot'>Founder运营首页 · v4.9.3</span><h1>现在是训练业务运营系统，<br><span>按钮会改变业务状态</span></h1><p>这里直接管理客户、班级、学员、练习题、Assignment、Submission、Review、Proof Files 和 Leads。</p></div>
""", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card decision'><span class='mini'>练习题</span><div class='metric'>{exercise_metrics['exercise_count']}</div></div>
  <div class='card decision'><span class='mini'>布置</span><div class='metric'>{op_metrics['assignments']}</div></div>
  <div class='card decision'><span class='mini'>Proof Files</span><div class='metric'>{op_metrics['proof_files']}</div></div>
  <div class='card decision'><span class='mini'>线索金额</span><div class='metric'>¥{op_metrics['lead_value']:,}</div></div>
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
        st.markdown("<div class='card'><h3>处理候选和需修改</h3><p>确认优秀提交进入 Proof Files；对证据不足的记录要求重新提交。</p></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='panel'><span class='pill hot'>Proof Task + Editable Records</span><h2>按班级和学员处理真实训练任务</h2><p>布置、提交、Review 会真实更新当前会话状态表。</p></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='panel'><span class='pill hot'>Skill Proof Files 业务库</span><h2>按学员沉淀可展示作品证明</h2><p>这里会显示通过状态机新增的 Proof Files。</p></div>", unsafe_allow_html=True)
    status = st.selectbox("状态筛选", ["全部", "可展示", "待Review", "修改中"])
    df = ops.proof_files().copy()
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
    st.markdown("<div class='panel'><span class='pill hot'>Leads / 服务包运营</span><h2>把训练交付转成可销售服务包</h2><p>新增线索和状态变更会真实更新当前会话 Leads 表。</p></div>", unsafe_allow_html=True)
    left, right = st.columns([1.15, .85])
    with left:
        st.markdown("<div class='section'>服务包</div>", unsafe_allow_html=True)
        st.dataframe(SERVICE_PACKAGES, use_container_width=True, hide_index=True)
        st.markdown("<div class='section'>线索列表</div>", unsafe_allow_html=True)
        leads_df = ops.consult_leads()
        st.dataframe(leads_df, use_container_width=True, hide_index=True)
        if not leads_df.empty:
            lead_labels = [f"{r.lead_id} · {r.client_name} · {r.status}" for r in leads_df.itertuples()]
            selected_lead = st.selectbox("选择线索改状态", lead_labels)
            lead_id = selected_lead.split(" · ")[0]
            c1, c2, c3 = st.columns(3)
            if c1.button("标记已联系", use_container_width=True):
                ops.update_lead_status(lead_id, "已联系")
                _record_event(f"{lead_id} 已标记为已联系")
                st.rerun()
            if c2.button("标记已预约", use_container_width=True):
                ops.update_lead_status(lead_id, "已预约")
                _record_event(f"{lead_id} 已标记为已预约")
                st.rerun()
            if c3.button("标记已成交", type="primary", use_container_width=True):
                ops.update_lead_status(lead_id, "已成交")
                _record_event(f"{lead_id} 已标记为已成交")
                st.rerun()
    with right:
        st.markdown("<div class='lead-card'><h3>新增测试线索</h3><p>用于模拟真实业务：客户、需求、预算、状态。</p>", unsafe_allow_html=True)
        with st.form("lead_form_v493"):
            client = st.text_input("客户名", value="某软件外包公司")
            package = st.text_input("服务包", value="企业训练版")
            need = st.text_input("需求", value="Java新人训练标准包")
            budget = st.number_input("预算 / 潜在金额", min_value=0, value=30000, step=1000)
            note = st.text_area("备注", value="希望把新人培训从讲师交付转成标准任务包。")
            ok = st.form_submit_button("新增线索到状态表", type="primary")
        if ok:
            lead_id = ops.add_lead(client_name=client, package=package, need=need, potential_value=int(budget), note=note)
            _record_event(f"新增线索 {lead_id}：{client} · {need} · ¥{budget:,}")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(_event_panel(), unsafe_allow_html=True)


def founder_queue() -> None:
    pending = ops.joined_records()
    st.markdown("<div class='panel'><span class='pill hot'>Review Queue</span><h2>Founder处理具体提交和线索</h2><p>确认、打回、沟通都会更新当前会话状态表。</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='section'>待处理训练记录</div>", unsafe_allow_html=True)
    st.dataframe(pending[["assignment_id", "exercise_id", "learner_name", "status", "submitted_at", "score", "decision", "proof_ready"]], use_container_width=True, hide_index=True)
    if not pending.empty:
        label_map = {f"{r.assignment_id} · {r.learner_name} · {r.exercise_id}": r for r in pending.itertuples()}
        selected = st.selectbox("选择处理项", list(label_map.keys()))
        rec = label_map[selected]
        st.markdown(f"<div class='queue-card decision'><h3>{rec.learner_name} · {rec.exercise_id}</h3><p><b>提交摘要：</b>{rec.answer_summary if pd.notna(rec.answer_summary) else '暂无'}<br><b>分数：</b>{rec.score if pd.notna(rec.score) else '未评分'}<br><b>决策：</b>{rec.decision if pd.notna(rec.decision) else '未Review'}<br><b>Proof Ready：</b>{rec.proof_ready if pd.notna(rec.proof_ready) else '否'}</p></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        if c1.button("确认进入Proof Files", type="primary", use_container_width=True):
            ops.mark_assignment_proof_ready(str(rec.assignment_id))
            _record_event(f"确认 {rec.learner_name} 的 {rec.exercise_id} 进入 Proof Files")
            st.rerun()
        if c2.button("要求重新提交", use_container_width=True):
            ops.request_resubmission(str(rec.assignment_id))
            _record_event(f"要求 {rec.learner_name} 重新提交 {rec.exercise_id}")
            st.rerun()
        if c3.button("标记已沟通", use_container_width=True):
            _record_event(f"已和 {rec.learner_name} 沟通 {rec.exercise_id}")
            st.info("已记录沟通。")
    st.markdown("<div class='section'>待跟进 Leads</div>", unsafe_allow_html=True)
    st.dataframe(ops.consult_leads()[["client_name", "package", "need", "status", "potential_value"]], use_container_width=True, hide_index=True)
    st.markdown(_event_panel(), unsafe_allow_html=True)
