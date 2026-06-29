from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.auth_context import current_learner, resolve_logged_in_learner_id
from frontend.business_data import COHORTS, SERVICE_PACKAGES
from frontend.exercise_bank import EXERCISES
from frontend.permissions import (
    can_request_agent_review,
    can_submit_own_work,
    forbidden_message,
    permission_summary_html,
)
from frontend.state import chip, set_view


def _student_learner() -> pd.Series:
    learner = current_learner()
    st.session_state.selected_learner_id = str(learner["learner_id"])
    st.session_state.selected_cohort_id = str(learner["cohort_id"])
    return learner


def _student_records() -> pd.DataFrame:
    learner_id = resolve_logged_in_learner_id()
    return ops.joined_records()[ops.joined_records()["learner_id"] == learner_id]


def _student_tasks() -> pd.DataFrame:
    learner_id = resolve_logged_in_learner_id()
    return ops.task_instances()[ops.task_instances()["learner_id"] == learner_id]


def _student_proofs(learner_name: str) -> pd.DataFrame:
    return ops.proof_files()[ops.proof_files()["learner_name"] == learner_name]


def student_home_page() -> None:
    learner = _student_learner()
    cohort = COHORTS[COHORTS["cohort_id"] == learner["cohort_id"]].iloc[0]
    tasks = _student_tasks()
    records = _student_records()
    proofs = _student_proofs(str(learner["learner_name"]))
    current_task = tasks.iloc[0] if not tasks.empty else None
    title = current_task["proof_task"] if current_task is not None else "暂无任务"
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(f"""
<div class='hero'><span class='pill hot'>我的业务首页 · v4.9.7</span><h1>{learner['learner_name']}：今天完成<br><span>{title}</span></h1><p>你已经登录为学员，系统会自动绑定你的学员档案，不需要再选择班级或选择学员。你只能操作自己的作答和记录。</p><span class='pill'>班级：{cohort['cohort_name']}</span><span class='pill'>小组：{learner['group']}</span><span class='pill'>状态：{learner['status']}</span></div>
""", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>训练进度</span><div class='metric'>{learner['progress']}%</div></div>
  <div class='card'><span class='mini'>我的任务</span><div class='metric'>{len(tasks)}</div></div>
  <div class='card'><span class='mini'>我的记录</span><div class='metric'>{len(records)}</div></div>
  <div class='card'><span class='mini'>我的 Proof Files</span><div class='metric'>{len(proofs)}</div></div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("打开我的练习题", type="primary", use_container_width=True):
        set_view("tasks")
        st.rerun()
    if c2.button("查看我的记录", use_container_width=True):
        set_view("assignments")
        st.rerun()
    if c3.button("查看我的 Proof Files", use_container_width=True):
        set_view("portfolio")
        st.rerun()
    st.markdown("<div class='section'>我的任务</div>", unsafe_allow_html=True)
    if tasks.empty:
        st.info("当前没有分配给你的任务。")
    else:
        st.dataframe(tasks[["day", "proof_task", "business_context", "status", "progress", "proof_score"]], use_container_width=True, hide_index=True)
    st.markdown("<div class='section'>我的 Assignment / Submission / Review</div>", unsafe_allow_html=True)
    if records.empty:
        st.info("当前没有你的训练记录。")
    else:
        st.dataframe(records[["assignment_id", "exercise_id", "status", "submitted_at", "score", "decision", "proof_ready"]], use_container_width=True, hide_index=True)


def student_tasks_page() -> None:
    learner = _student_learner()
    learner_id = str(learner["learner_id"])
    tasks = _student_tasks()
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(f"""
<div class='panel'><span class='pill hot'>我的练习题 / Proof Task</span><h2>{learner['learner_name']} 的训练任务</h2><p>学员端只显示你自己的任务和练习，不再出现班级/学员选择器。提交和 Agent 初评只允许本人操作。</p></div>
""", unsafe_allow_html=True)
    if tasks.empty:
        st.info("当前没有任务。")
    else:
        st.dataframe(tasks[["day", "proof_task", "business_context", "required_output", "status", "progress", "proof_score"]], use_container_width=True, hide_index=True)
        labels = [f"{r.day} · {r.proof_task} · {r.status}" for r in tasks.itertuples()]
        selected_label = st.selectbox("选择我的任务", labels)
        task = tasks.iloc[labels.index(selected_label)]
        st.markdown(f"""
<div class='editor'><h3>{task['proof_task']}</h3>{chip(task['status'])}<p><b>业务场景：</b>{task['business_context']}<br><b>要求交付物：</b>{task['required_output']}</p></div>
""", unsafe_allow_html=True)
        draft_key = f"student_draft_{task['task_id']}"
        st.session_state.setdefault(draft_key, task["draft"])
        st.text_area("我的作答 / Proof 草稿", key=draft_key, height=220)
    st.markdown("<div class='section'>可练习题库</div>", unsafe_allow_html=True)
    module = st.selectbox("练习模块", ["全部"] + sorted(EXERCISES["module"].unique().tolist()))
    filtered = EXERCISES if module == "全部" else EXERCISES[EXERCISES["module"] == module]
    st.dataframe(filtered[["exercise_id", "module", "difficulty", "related_task", "required_output"]], use_container_width=True, hide_index=True)
    if filtered.empty:
        return
    labels = [f"{r.exercise_id} · {r.related_task}" for r in filtered.itertuples()]
    selected = st.selectbox("选择练习题", labels)
    exercise = filtered.iloc[labels.index(selected)]
    st.markdown(f"""
<div class='editor'><h3>{exercise['related_task']}</h3>{chip(exercise['difficulty'])}<span class='pill purple'>{exercise['module']}</span><p><b>业务场景：</b>{exercise['scenario']}</p><p><b>练习题：</b>{exercise['question']}</p><p><b>要求交付物：</b>{exercise['required_output']}</p></div>
""", unsafe_allow_html=True)
    answer_key = f"student_answer_{exercise['exercise_id']}_{learner_id}"
    answer = st.text_area("我的练习作答", key=answer_key, height=220)
    c1, c2 = st.columns(2)
    can_submit = can_submit_own_work(learner_id)
    if c1.button("提交我的作答", type="primary", use_container_width=True, disabled=not can_submit):
        assignment_id = ops.assign_exercise(
            exercise_id=str(exercise["exercise_id"]),
            learner_id=learner_id,
            learner_name=str(learner["learner_name"]),
            cohort_id=str(learner["cohort_id"]),
            note=str(exercise["related_task"]),
        )
        ops.submit_assignment(
            assignment_id=assignment_id,
            exercise_id=str(exercise["exercise_id"]),
            learner_id=learner_id,
            learner_name=str(learner["learner_name"]),
            answer_summary=answer or "学员已提交练习作答。",
        )
        st.success("已提交到我的训练记录。")
        st.rerun()
    if c2.button("生成我的 Agent Review", use_container_width=True, disabled=not can_request_agent_review(learner_id)):
        records = ops.joined_records()
        mine = records[(records["exercise_id"] == exercise["exercise_id"]) & (records["learner_id"] == learner_id)]
        if mine.empty:
            st.warning("请先提交作答。")
        else:
            submission_id = str(mine.iloc[-1]["submission_id"])
            score = 82 if exercise["difficulty"] != "高级" else 78
            ops.review_submission(
                submission_id=submission_id,
                reviewer="Agent",
                score=score,
                review_comment=f"Agent Review：{exercise['rubric']}。",
                decision="待Founder确认" if score >= 80 else "需修改",
                proof_ready="候选" if score >= 80 else "否",
            )
            st.success("Agent Review 已生成。")
            st.rerun()
    if not can_submit:
        st.warning(forbidden_message("提交该学员作答"))
    with st.expander("查看提示"):
        st.write(exercise["hint"])


def student_records_page() -> None:
    learner = _student_learner()
    records = _student_records()
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(f"<div class='panel'><span class='pill hot'>我的训练记录</span><h2>{learner['learner_name']} 的 Assignment / Submission / Review</h2><p>只显示当前登录学员自己的记录。</p></div>", unsafe_allow_html=True)
    if records.empty:
        st.info("暂无训练记录。")
        return
    st.dataframe(records[["assignment_id", "exercise_id", "status", "submitted_at", "answer_summary", "score", "decision", "proof_ready"]], use_container_width=True, hide_index=True)
    labels = [f"{r.assignment_id} · {r.exercise_id} · {r.status}" for r in records.itertuples()]
    selected = st.selectbox("查看我的记录详情", labels)
    row = records.iloc[labels.index(selected)]
    st.markdown(f"""
<div class='detail'><h3>{row['exercise_id']}</h3>{chip(row['status'])}<p><b>提交时间：</b>{row['submitted_at'] if pd.notna(row['submitted_at']) else '未提交'}<br><b>提交摘要：</b>{row['answer_summary'] if pd.notna(row['answer_summary']) else '暂无'}<br><b>Review：</b>{row['decision'] if pd.notna(row['decision']) else '未Review'}<br><b>Proof Ready：</b>{row['proof_ready'] if pd.notna(row['proof_ready']) else '否'}</p></div>
""", unsafe_allow_html=True)


def student_proof_files_page() -> None:
    learner = _student_learner()
    proofs = _student_proofs(str(learner["learner_name"]))
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(f"<div class='panel'><span class='pill hot'>我的 Proof Files</span><h2>{learner['learner_name']} 的作品证明</h2><p>只显示当前登录学员自己的 Proof Files。</p></div>", unsafe_allow_html=True)
    if proofs.empty:
        st.info("暂无 Proof Files。完成练习并通过 Founder 确认后会出现在这里。")
        return
    st.dataframe(proofs, use_container_width=True, hide_index=True)
    selected = st.selectbox("查看我的 Proof File", [f"{r.proof_id} · {r.title}" for r in proofs.itertuples()])
    row = proofs.iloc[[f"{r.proof_id} · {r.title}" for r in proofs.itertuples()].index(selected)]
    st.markdown(f"<div class='detail'><h3>{row['title']}</h3>{chip(row['status'])}<p><b>分数：</b>{row['score']}<br><b>证据：</b>{row['evidence']}<br><b>说明：</b>{row['note']}</p></div>", unsafe_allow_html=True)


def student_service_page() -> None:
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown("<div class='panel'><span class='pill hot'>服务包</span><h2>可选训练服务包</h2><p>学员端只展示服务包，不展示销售线索后台。</p></div>", unsafe_allow_html=True)
    st.dataframe(SERVICE_PACKAGES, use_container_width=True, hide_index=True)
