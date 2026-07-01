from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend import production_state as prod
from frontend.state import chip, set_view


def _safe_cols(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=cols)
    return df[[c for c in cols if c in df.columns]]


def _label_map(df: pd.DataFrame, label_col: str, id_col: str) -> dict[str, str]:
    if df.empty:
        return {}
    return {f"{row[label_col]} · {row[id_col]}": str(row[id_col]) for _, row in df.iterrows()}


def _status_panel() -> None:
    status = prod.production_mode_status()
    backend_class = "green" if status["backend"] == "supabase" else "orange"
    st.markdown(
        f"""
<div class='panel'>
  <span class='pill hot'>v5.1 Production Admin Console</span>
  <h2>真实业务数据维护后台</h2>
  <p>Founder 在这里维护客户、班级、学员、选择题，并把题目分配给学员。Supabase 模式下写入生产表；Session Demo 模式下写入当前会话。</p>
  <span class='pill {backend_class}'>{status['backend_label']}</span><span class='pill'>Tenant：{status['tenant_code']}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def health_check_page() -> None:
    st.markdown("<div class='section'>Supabase Health Check / Production Mode</div>", unsafe_allow_html=True)
    status = prod.production_mode_status()
    a, b, c, d = st.columns(4)
    a.metric("Backend", status["backend_label"])
    b.metric("Tenant", status["tenant_code"])
    c.metric("Clients", len(prod.clients()))
    d.metric("Exercises", len(prod.exercises()))
    if st.button("重新检查 Supabase / 重新加载主数据", type="primary", use_container_width=True):
        prod.refresh_production_admin_state()
        st.session_state["prod_health_check"] = prod.health_check()
        st.rerun()
    health_df = st.session_state.get("prod_health_check")
    if health_df is None:
        health_df = prod.health_check()
        st.session_state["prod_health_check"] = health_df
    st.dataframe(health_df, use_container_width=True, hide_index=True)
    errors = health_df[health_df["status"] == "error"] if not health_df.empty else health_df
    if errors is not None and not errors.empty:
        st.error("有表无法访问。先执行 v5.1 schema，或检查 Supabase secrets / RLS / tenant_code。")
    else:
        st.success("Health Check 通过：当前数据层可用于 v5.1 录入和分配。")


def client_admin_page() -> None:
    st.markdown("<div class='section'>客户管理 · 新增客户</div>", unsafe_allow_html=True)
    clients_df = prod.clients()
    st.dataframe(_safe_cols(clients_df, ["client_id", "client_name", "contact", "service_package", "contract_value", "currency", "status"]), use_container_width=True, hide_index=True)
    with st.form("v51_client_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            client_id = st.text_input("客户ID（可空，系统自动生成）", placeholder="client-20260701-001")
            client_name = st.text_input("客户名称", placeholder="某软件公司 / 某培训机构")
            contact = st.text_input("联系人", placeholder="人材育成担当 / 校区负责人")
        with c2:
            service_package = st.text_input("服务包", placeholder="Java新人研修 Proof Sprint")
            contract_value = st.number_input("合同额", min_value=0, value=30000, step=1000)
            currency = st.selectbox("币种", ["CNY", "JPY", "USD"])
            status = st.selectbox("状态", ["待跟进", "进行中", "已完成", "暂停"])
        ok = st.form_submit_button("新增客户并写入数据层", type="primary")
    if ok:
        if not client_name.strip():
            st.warning("客户名称不能为空。")
        else:
            new_id = prod.add_client(
                client_id=client_id,
                client_name=client_name,
                contact=contact,
                service_package=service_package,
                contract_value=int(contract_value),
                currency=currency,
                status=status,
            )
            st.success(f"已新增客户：{new_id}")
            st.rerun()


def cohort_admin_page() -> None:
    st.markdown("<div class='section'>班级管理 · 新增班级</div>", unsafe_allow_html=True)
    clients_df = prod.clients()
    cohorts_df = prod.cohorts()
    st.dataframe(_safe_cols(cohorts_df, ["cohort_id", "client_id", "cohort_name", "learner_count", "start_date", "end_date", "trainer", "status"]), use_container_width=True, hide_index=True)
    client_options = _label_map(clients_df, "client_name", "client_id")
    if not client_options:
        st.warning("请先新增客户，再新增班级。")
        return
    with st.form("v51_cohort_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            client_label = st.selectbox("所属客户", list(client_options.keys()))
            cohort_id = st.text_input("班级ID（可空，系统自动生成）")
            cohort_name = st.text_input("班级名称", placeholder="2026 Java新人训练营")
        with c2:
            start_date = st.date_input("开始日期", value=date.today())
            end_date = st.date_input("结束日期", value=date.today())
            trainer = st.text_input("讲师 / 负责人", value="Zhu Moses")
            status = st.selectbox("状态", ["准备中", "进行中", "售前样板", "已完成", "暂停"])
        ok = st.form_submit_button("新增班级并写入数据层", type="primary")
    if ok:
        if not cohort_name.strip():
            st.warning("班级名称不能为空。")
        else:
            new_id = prod.add_cohort(
                cohort_id=cohort_id,
                client_id=client_options[client_label],
                cohort_name=cohort_name,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                trainer=trainer,
                status=status,
            )
            st.success(f"已新增班级：{new_id}")
            st.rerun()


def learner_admin_page() -> None:
    st.markdown("<div class='section'>学员管理 · 新增学员</div>", unsafe_allow_html=True)
    cohorts_df = prod.cohorts()
    learners_df = prod.learners()
    st.dataframe(_safe_cols(learners_df, ["learner_id", "learner_name", "cohort_id", "role", "group", "status", "progress", "tasks_done", "proof_files"]), use_container_width=True, hide_index=True)
    cohort_options = _label_map(cohorts_df, "cohort_name", "cohort_id")
    if not cohort_options:
        st.warning("请先新增班级，再新增学员。")
        return
    with st.form("v51_learner_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            cohort_label = st.selectbox("所属班级", list(cohort_options.keys()))
            learner_id = st.text_input("学员ID（可空，系统自动生成）")
            learner_name = st.text_input("学员姓名")
        with c2:
            learner_group = st.text_input("小组", value="A组")
            role = st.selectbox("角色", ["学员", "讲师", "客户观察员"])
            status = st.selectbox("状态", ["未开始", "进行中", "待Review", "需修改", "已确认"])
        ok = st.form_submit_button("新增学员并写入数据层", type="primary")
    if ok:
        if not learner_name.strip():
            st.warning("学员姓名不能为空。")
        else:
            new_id = prod.add_learner(
                learner_id=learner_id,
                learner_name=learner_name,
                cohort_id=cohort_options[cohort_label],
                learner_group=learner_group,
                role=role,
                status=status,
            )
            st.success(f"已新增学员：{new_id}")
            st.rerun()


def exercise_admin_page() -> None:
    st.markdown("<div class='section'>题库管理 · 新增选择题</div>", unsafe_allow_html=True)
    cohorts_df = prod.cohorts()
    exercises_df = prod.exercises()
    st.dataframe(_safe_cols(exercises_df, ["exercise_id", "module", "difficulty", "cohort_id", "related_task", "question_type", "question", "correct_option", "required_output"]), use_container_width=True, hide_index=True)
    cohort_options = _label_map(cohorts_df, "cohort_name", "cohort_id")
    if not cohort_options:
        st.warning("请先新增班级，再新增题目。")
        return
    with st.form("v51_exercise_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            cohort_label = st.selectbox("适用班级", list(cohort_options.keys()))
            exercise_id = st.text_input("题目ID（可空，系统自动生成）")
            module = st.text_input("模块", value="软件测试")
            difficulty = st.selectbox("难度", ["基础", "中级", "高级"])
            related_task = st.text_input("关联任务", placeholder="登录功能测试用例")
            required_output = st.text_input("要求交付物", placeholder="选择正确答案，并说明理由")
        with c2:
            question = st.text_area("题干", height=90)
            opt_a = st.text_input("A 选项")
            opt_b = st.text_input("B 选项")
            opt_c = st.text_input("C 选项")
            opt_d = st.text_input("D 选项")
            correct_option = st.selectbox("正确选项", ["A", "B", "C", "D"])
        scenario = st.text_area("业务场景", height=90)
        explanation = st.text_area("解析", height=80)
        hint = st.text_input("提示", placeholder="提醒学员注意业务边界")
        golden_solution = st.text_area("参考答案 / Golden Solution", height=80)
        rubric = st.text_input("评分标准", value="选择正确80%；补充说明20%。")
        ok = st.form_submit_button("新增选择题并写入数据层", type="primary")
    if ok:
        required_values = [module, related_task, question, opt_a, opt_b, opt_c, opt_d]
        if any(not str(v).strip() for v in required_values):
            st.warning("模块、关联任务、题干、四个选项不能为空。")
        else:
            options = [f"A. {opt_a}", f"B. {opt_b}", f"C. {opt_c}", f"D. {opt_d}"]
            new_id = prod.add_exercise(
                exercise_id=exercise_id,
                module=module,
                difficulty=difficulty,
                cohort_id=cohort_options[cohort_label],
                related_task=related_task,
                scenario=scenario,
                question=question,
                options=options,
                correct_option=correct_option,
                explanation=explanation,
                required_output=required_output,
                hint=hint,
                golden_solution=golden_solution,
                rubric=rubric,
            )
            st.success(f"已新增选择题：{new_id}")
            st.rerun()


def assignment_admin_page() -> None:
    st.markdown("<div class='section'>任务分配 · 把选择题分配给学员</div>", unsafe_allow_html=True)
    cohorts_df = prod.cohorts()
    learners_df = prod.learners()
    exercises_df = prod.exercises()
    if cohorts_df.empty or learners_df.empty or exercises_df.empty:
        st.warning("需要至少有 1 个班级、1 个学员、1 道选择题，才能分配任务。")
        return
    cohort_options = _label_map(cohorts_df, "cohort_name", "cohort_id")
    cohort_label = st.selectbox("选择班级", list(cohort_options.keys()), key="v51_assign_cohort")
    cohort_id = cohort_options[cohort_label]
    learner_rows = learners_df[learners_df["cohort_id"] == cohort_id]
    exercise_rows = exercises_df[exercises_df["cohort_id"] == cohort_id]
    if learner_rows.empty:
        st.warning("这个班级还没有学员。")
        return
    if exercise_rows.empty:
        st.warning("这个班级还没有可分配题目。")
        return
    learner_options = _label_map(learner_rows, "learner_name", "learner_id")
    exercise_options = _label_map(exercise_rows, "related_task", "exercise_id")
    with st.form("v51_assign_form"):
        learner_label = st.selectbox("选择学员", list(learner_options.keys()))
        exercise_label = st.selectbox("选择题目", list(exercise_options.keys()))
        note = st.text_input("分配备注", value="v5.1 Admin Console 分配")
        ok = st.form_submit_button("分配给学员并写入 Assignment", type="primary")
    if ok:
        learner = learner_rows[learner_rows["learner_id"] == learner_options[learner_label]].iloc[0]
        exercise_id = exercise_options[exercise_label]
        assignment_id = ops.assign_exercise(
            exercise_id=exercise_id,
            learner_id=str(learner["learner_id"]),
            learner_name=str(learner["learner_name"]),
            cohort_id=cohort_id,
            note=note,
        )
        st.success(f"已分配：{assignment_id} · {exercise_id} → {learner['learner_name']}")
        st.rerun()
    st.markdown("<div class='section'>已分配 Assignment</div>", unsafe_allow_html=True)
    assigned = ops.assignments()
    st.dataframe(_safe_cols(assigned, ["assignment_id", "exercise_id", "learner_id", "learner_name", "cohort_id", "status", "assigned_at", "due_date", "note"]), use_container_width=True, hide_index=True)


def production_admin_page() -> None:
    prod.init_production_admin_state()
    _status_panel()
    tabs = st.tabs(["Health Check", "客户", "班级", "学员", "题库", "任务分配"])
    with tabs[0]:
        health_check_page()
    with tabs[1]:
        client_admin_page()
    with tabs[2]:
        cohort_admin_page()
    with tabs[3]:
        learner_admin_page()
    with tabs[4]:
        exercise_admin_page()
    with tabs[5]:
        assignment_admin_page()
    c1, c2, c3 = st.columns(3)
    if c1.button("去客户页", use_container_width=True):
        set_view("clients")
        st.rerun()
    if c2.button("去 Assignment 管理", use_container_width=True):
        set_view("assignments")
        st.rerun()
    if c3.button("去 Audit", use_container_width=True):
        set_view("audit")
        st.rerun()
