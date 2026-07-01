from __future__ import annotations

import pandas as pd

from frontend import business_pages
from frontend import operation_state
from frontend import pages
from frontend import production_state as prod


def _business_metrics() -> dict[str, int]:
    clients = prod.clients()
    cohorts = prod.cohorts()
    learners = prod.learners()
    return {
        "active_clients": int((clients["status"] == "进行中").sum()) if not clients.empty and "status" in clients.columns else 0,
        "active_cohorts": int((cohorts["status"].astype(str).str.contains("进行中|售前", regex=True)).sum()) if not cohorts.empty and "status" in cohorts.columns else 0,
        "learners": int(learners["learner_id"].nunique()) if not learners.empty and "learner_id" in learners.columns else 0,
        "pending_reviews": 0,
        "proof_files": 0,
        "lead_value": 0,
    }


def _exercise_metrics() -> dict[str, int]:
    exercises = prod.exercises()
    return {
        "exercise_count": int(len(exercises)),
        "module_count": int(exercises["module"].nunique()) if not exercises.empty and "module" in exercises.columns else 0,
        "basic_count": int((exercises["difficulty"] == "基础").sum()) if not exercises.empty and "difficulty" in exercises.columns else 0,
        "advanced_count": int((exercises["difficulty"] == "高级").sum()) if not exercises.empty and "difficulty" in exercises.columns else 0,
        "mcq_count": int((exercises["question_type"] == "单选题").sum()) if not exercises.empty and "question_type" in exercises.columns else 0,
    }


def bind_production_master_data() -> None:
    """Point legacy display/work pages to v5.1 editable master data.

    Older modules imported CLIENTS / COHORTS / LEARNERS / EXERCISES from seed files.
    v5.1 keeps those pages alive but rebinds their module globals to the Admin Console
    data loaded from Supabase or session state.
    """
    clients = prod.clients()
    cohorts = prod.cohorts()
    learners = prod.learners()
    exercises = prod.exercises()

    for module in (pages, business_pages):
        module.CLIENTS = clients
        module.COHORTS = cohorts
        module.LEARNERS = learners
    pages.EXERCISES = exercises
    pages.get_business_metrics = _business_metrics
    pages.get_exercise_metrics = _exercise_metrics

    operation_state.EXERCISES = exercises

    if exercises.empty:
        operation_state.EXERCISES = pd.DataFrame(columns=["exercise_id", "module", "difficulty", "related_task", "question", "correct_option", "explanation", "hint"])
