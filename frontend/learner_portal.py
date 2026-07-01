from __future__ import annotations

import json
from typing import Any

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend import production_state as prod
from frontend.auth_context import current_learner, resolve_logged_in_learner_id
from frontend.state import chip


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
    return []


def _letter(option_text: str) -> str:
    return option_text.split(".", 1)[0].strip() if "." in option_text else option_text[:1]


def _score(exercise: pd.Series, selected: str) -> int:
    return 88 if _letter(selected) == str(exercise.get("correct_option", "")).strip() else 62


def _exercise(exercise_id: str) -> pd.Series | None:
    exercises = prod.exercises()
    if exercises.empty:
        return None
    rows = exercises[exercises["exercise_id"] == exercise_id]
    return None if rows.empty else rows.iloc[0]


def learner_portal_page() -> None:
    learner = current_learner()
    learner_id = resolve_logged_in_learner_id()
    assignments = ops.assignments()
    mine = assignments[assignments["learner_id"] == learner_id] if not assignments.empty and "learner_id" in assignments.columns else assignments.iloc[0:0]
    records = ops.joined_records()
    my_records = records[records["learner_id"] == learner_id] if not records.empty and "learner_id" in records.columns else records.iloc[0:0]
    proofs = ops.proof_files()
    my_proofs = proofs[proofs["learner_name"] == learner["learner_name"]] if not proofs.empty and "learner_name" in proofs.columns else proofs.iloc[0:0]

    st.markdown(f"<div class='panel'><span class='pill hot'>Learner Portal Preview</span><h2>{learner['learner_name']}</h2><p>Only assigned tasks are shown here.</p></div>", unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.metric("Assigned", len(mine))
    b.metric("Submitted", int((my_records["submission_id"].notna()).sum()) if not my_records.empty and "submission_id" in my_records.columns else 0)
    c.metric("Proof Files", len(my_proofs))

    if mine.empty:
        st.info("No assigned tasks yet. Founder should assign an exercise first.")
        return

    st.markdown("Assigned tasks")
    st.dataframe(mine, use_container_width=True, hide_index=True)
    labels = [f"{r.assignment_id} · {r.exercise_id} · {r.status}" for r in mine.itertuples()]
    selected = st.selectbox("Select assignment", labels)
    assignment_id = selected.split(" · ")[0]
    assignment = mine[mine["assignment_id"] == assignment_id].iloc[0]
    exercise = _exercise(str(assignment["exercise_id"]))
    if exercise is None:
        st.warning("Exercise detail was not found.")
        return

    st.markdown(f"<div class='detail'><h3>{exercise.get('related_task', '')}</h3>{chip(assignment['status'])}<p><b>Question:</b> {exercise.get('question', '')}</p></div>", unsafe_allow_html=True)
    options = _options(exercise.get("options", []))
    selected_option = st.radio("Answer", options, key=f"learner_portal_{assignment_id}") if options else ""
    note = st.text_area("Note", key=f"learner_note_{assignment_id}", height=100)
    if st.button("Submit and request Agent Review", type="primary", use_container_width=True, disabled=not bool(selected_option)):
        selected_letter = _letter(selected_option)
        correct = str(exercise.get("correct_option", "")).strip()
        score = _score(exercise, selected_option)
        summary = f"MCQ answer: {selected_option}. Result: {'correct' if selected_letter == correct else 'needs review'}; correct option: {correct}."
        if note:
            summary += f" Note: {note}"
        submission_id = ops.submit_assignment(
            assignment_id=assignment_id,
            exercise_id=str(assignment["exercise_id"]),
            learner_id=learner_id,
            learner_name=str(learner["learner_name"]),
            answer_summary=summary,
            question_type="单选题",
            selected_option=selected_letter,
            correct_option=correct,
            is_correct=selected_letter == correct,
            auto_score=score,
            answer_note=note,
        )
        ops.review_submission(
            submission_id=submission_id,
            reviewer="Agent",
            score=score,
            review_comment=str(exercise.get("explanation", "")),
            decision="待Founder确认" if score >= 80 else "需复习",
            proof_ready="候选" if score >= 80 else "否",
        )
        st.success("Submitted and reviewed.")
        st.rerun()

    st.markdown("My records")
    if my_records.empty:
        st.info("No records yet.")
    else:
        cols = [c for c in ["assignment_id", "exercise_id", "status", "selected_option", "correct_option", "is_correct", "auto_score", "decision", "proof_ready"] if c in my_records.columns]
        st.dataframe(my_records[cols], use_container_width=True, hide_index=True)
