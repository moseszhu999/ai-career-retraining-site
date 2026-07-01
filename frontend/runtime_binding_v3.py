from __future__ import annotations

import pandas as pd

from frontend import business_pages, data_repository, executive_pages, operation_state, pages
from frontend import production_state as prod


def business_metrics() -> dict[str, int]:
    clients = prod.clients()
    cohorts = prod.cohorts()
    learners = prod.learners()
    op = operation_state.operation_metrics()
    return {
        "active_clients": int((clients["status"] == "进行中").sum()) if not clients.empty and "status" in clients.columns else 0,
        "active_cohorts": int((cohorts["status"].astype(str).str.contains("进行中|售前", regex=True)).sum()) if not cohorts.empty and "status" in cohorts.columns else 0,
        "learners": int(learners["learner_id"].nunique()) if not learners.empty and "learner_id" in learners.columns else 0,
        "pending_reviews": int(op.get("reviews", 0)),
        "proof_files": int(op.get("proof_files", 0)),
        "lead_value": int(op.get("lead_value", 0)),
    }


def exercise_metrics() -> dict[str, int]:
    exercises = prod.exercises()
    return {
        "exercise_count": int(len(exercises)),
        "module_count": int(exercises["module"].nunique()) if not exercises.empty and "module" in exercises.columns else 0,
        "basic_count": int((exercises["difficulty"] == "基础").sum()) if not exercises.empty and "difficulty" in exercises.columns else 0,
        "advanced_count": int((exercises["difficulty"] == "高级").sum()) if not exercises.empty and "difficulty" in exercises.columns else 0,
        "mcq_count": int((exercises["question_type"] == "单选题").sum()) if not exercises.empty and "question_type" in exercises.columns else 0,
    }


def bind_production_master_data() -> None:
    clients = prod.clients()
    cohorts = prod.cohorts()
    learners = prod.learners()
    exercises = prod.exercises()

    for module in (pages, business_pages, executive_pages, data_repository):
        module.CLIENTS = clients
        module.COHORTS = cohorts
    for module in (pages, business_pages, data_repository):
        module.LEARNERS = learners

    pages.EXERCISES = exercises
    pages.get_business_metrics = business_metrics
    pages.get_exercise_metrics = exercise_metrics
    executive_pages.get_business_metrics = business_metrics
    executive_pages.get_exercise_metrics = exercise_metrics

    operation_state.EXERCISES = exercises if not exercises.empty else pd.DataFrame(columns=["exercise_id", "module", "difficulty", "related_task", "question", "correct_option", "explanation", "hint"])
