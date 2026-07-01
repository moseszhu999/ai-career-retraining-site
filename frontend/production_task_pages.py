from __future__ import annotations

import json
from typing import Any

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend import production_state as prod
from frontend.state import chip, set_view


def _option_letter(option_text: str) -> str:
    return option_text.split(".", 1)[0].strip() if "." in option_text else option_text[:1]


def _options(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
        except Exception:
            pass
        if "\n" in value:
            return [line.strip() for line in value.splitlines() if line.strip()]
    return []


def _mcq_score(exercise: pd.Series, selected_option: str) -> int:
    selected = _option_letter(selected_option)
    correct = str(exercise.get("correct_option", "")).strip()
    if selected == correct:
        return 88 if str(exercise.get("difficulty", "")) != "高级" else 84
    return 62 if str(exercise.get("difficulty", "")) != "高级" else 58


def _mcq_payload(exercise: pd.Series, selected_option: str, note: str) -> dict[str, object]:
    selected = _option_letter(selected_option)
    correct = str(exercise.get("correct_option", "")).strip()
    return {
        "question_type": str(exercise.get("question_type", "单选题")),
        "selected_option": selected,
        "correct_option": correct,
        "is_correct": selected == correct,
        "auto_score": _mcq_score(exercise, selected_option),
        "answer_note": note,
    }


def _answer_summary(exercise: pd.Series, selected_option: str, note: str) -> str:
    payload = _mcq_payload(exercise, selected_option, note)
    result = "正确" if payload["is_correct"] else "需复习"
    summary = f"选择题作答：{selected_option}\n判定：{result}；正确选项：{payload['correct_option']}。"
    if note:
        summary += f"\n补充说明：{note}"
    return summary


def _ensure_submission(exercise: pd.Series, learner: pd.Series, selected_option: str, note: str) -> str:
    exercise_id = str(exercise["exercise_id"])
    learner_id = str(learner["learner_id"])
    existing = ops.assignments()
    matched = existing[(existing["exercise_id"] == exercise_id) & (existing["learner_id"] == learner_id)] if not existing.empty else existing
    if matched.empty:
        assignment_id = ops.assign_exercise(
            exercise_id=exercise_id,
            learner_id=learner_id,
            learner_name=str(learner["learner_name"]),
            cohort_id=str(learner["cohort_id"]),
            note=str(exercise.get("related_task", "生产题库分配")),
        )
    else:
        assignment_id = str(matched.iloc[0]["assignment_id"])
    return ops.submit_assignment(
        assignment_id=assignment_id,
        exercise_id=exercise_id,
        learner_id=learner_id,
        learner_name=str(learner["learner_name"]),
        answer_summary=_answer_summary(exercise, selected_option, note),
        **_mcq_payload(exercise, selected_option, note),
    )


def _records_for_learner(learner_id: str) -> pd.DataFrame:
    records = ops.review_queue_view()
    if records.empty or "learner_id" not in records.columns:
        return pd.DataFrame()
    return records[records["learner_id"] == learner_id]


def tasks_page() -> None:
    cohorts = prod.cohorts()
    learners = prod.learners()
    exercises = prod.exercises()
    st.markdown(
        "<div class='panel'><span class='pill hot'>v5.1 Production Task Console</span><h2>真实题库分配、提交、Agent Review</h2><p>这里直接读取 Admin Console / Supabase 的班级、学员、选择题。</p></div>",
        unsafe_allow_html=True,
    )
    a, b, c, d = st.columns(4)
    a.metric("Cohorts", len(cohorts))
    b.metric("Learners", len(learners))
    c.metric("Exercises", len(exercises))
    d.metric("Assignments", len(ops.assignments()))

    if cohorts.empty or learners.empty or exercises.empty:
        st.warning("生产任务台需要至少 1 个班级、1 个学员、1 道选择题。先去 Admin/Health 录入主数据。")
        if st.button("打开 Admin/Health", type="primary", use_container_width=True):
            set_view("admin")
            st.rerun()
        return

    cohort_labels = {f"{row['cohort_name']} · {row['cohort_id']}": str(row["cohort_id"]) for _, row in cohorts.iterrows()}
    cohort_label = st.selectbox("选择班级", list(cohort_labels.keys()))
    cohort_id = cohort_labels[cohort_label]
    learner_rows = learners[learners["cohort_id"] == cohort_id]
    exercise_rows = exercises[exercises["cohort_id"] == cohort_id]
    if learner_rows.empty:
        st.info("当前班级没有学员。")
        return
    if exercise_rows.empty:
        st.info("当前班级没有题目。")
        return

    learner_labels = {f"{row['learner_name']} · {row['learner_id']}": str(row["learner_id"]) for _, row in learner_rows.iterrows()}
    learner_label = st.selectbox("选择学员", list(learner_labels.keys()))
    learner = learner_rows[learner_rows["learner_id"] == learner_labels[learner_label]].iloc[0]

    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown("<div class='section'>可用选择题</div>", unsafe_allow_html=True)
        st.dataframe(exercise_rows[["exercise_id", "module", "difficulty", "related_task", "question_type", "question", "correct_option"]], use_container_width=True, hide_index=True)
        exercise_labels = {f"{row['related_task']} · {row['exercise_id']}": str(row["exercise_id"]) for _, row in exercise_rows.iterrows()}
        exercise_label = st.selectbox("选择题目", list(exercise_labels.keys()))
        exercise = exercise_rows[exercise_rows["exercise_id"] == exercise_labels[exercise_label]].iloc[0]
        st.markdown(
            f"<div class='editor'><h3>{exercise.get('related_task', '')}</h3>{chip(exercise.get('difficulty', ''))}<span class='pill purple'>{exercise.get('module', '')}</span><p><b>场景：</b>{exercise.get('scenario', '')}</p><p><b>题目：</b>{exercise.get('question', '')}</p></div>",
            unsafe_allow_html=True,
        )
        option_list = _options(exercise.get("options", []))
        selected_option = st.radio("选择答案", option_list, key=f"prod_answer_{exercise['exercise_id']}_{learner['learner_id']}") if option_list else ""
        note = st.text_area("补充说明", height=100, key=f"prod_note_{exercise['exercise_id']}_{learner['learner_id']}")
        c1, c2, c3 = st.columns(3)
        if c1.button("只分配", use_container_width=True):
            assignment_id = ops.assign_exercise(
                exercise_id=str(exercise["exercise_id"]),
                learner_id=str(learner["learner_id"]),
                learner_name=str(learner["learner_name"]),
                cohort_id=cohort_id,
                note=str(exercise.get("related_task", "生产题库分配")),
            )
            st.success(f"已分配：{assignment_id}")
            st.rerun()
        if c2.button("提交作答", use_container_width=True, disabled=not bool(selected_option)):
            submission_id = _ensure_submission(exercise, learner, selected_option, note)
            st.success(f"已提交：{submission_id}")
            st.rerun()
        if c3.button("提交并生成 Agent Review", type="primary", use_container_width=True, disabled=not bool(selected_option)):
            submission_id = _ensure_submission(exercise, learner, selected_option, note)
            score = _mcq_score(exercise, selected_option)
            ops.review_submission(
                submission_id=submission_id,
                reviewer="Agent",
                score=score,
                review_comment=f"Agent Review：{exercise.get('explanation', '')} {exercise.get('rubric', '')}",
                decision="待Founder确认" if score >= 80 else "需复习",
                proof_ready="候选" if score >= 80 else "否",
            )
            st.success(f"已生成 Review：{score} 分")
            st.rerun()
    with right:
        st.markdown("<div class='section'>解析 / 标准</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><b>提示</b><p>{exercise.get('hint', '')}</p></div>", unsafe_allow_html=True)
        with st.expander("解析"):
            st.write(exercise.get("explanation", ""))
        with st.expander("参考答案"):
            st.write(exercise.get("golden_solution", ""))
        with st.expander("评分标准"):
            st.write(exercise.get("rubric", ""))

    st.markdown("<div class='section'>当前学员记录</div>", unsafe_allow_html=True)
    records = _records_for_learner(str(learner["learner_id"]))
    display_cols = ["assignment_id", "exercise_id", "status", "selected_option", "correct_option", "is_correct", "auto_score", "score", "decision", "proof_ready", "review_route"]
    if records.empty:
        st.info("当前学员还没有记录。")
    else:
        st.dataframe(records[[c for c in display_cols if c in records.columns]], use_container_width=True, hide_index=True)
