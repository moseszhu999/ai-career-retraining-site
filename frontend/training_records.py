from __future__ import annotations

import pandas as pd

ASSIGNMENTS = pd.DataFrame(
    [
        ["asn-001", "ex-login-001", "jhc-s01", "佐藤拓海", "jhc-2026-java", "已布置", "2026-06-22", "2026-06-23", "补齐登录测试边界"],
        ["asn-002", "ex-order-002", "jhc-s02", "鈴木美咲", "jhc-2026-java", "已提交", "2026-06-23", "2026-06-24", "订单状态流转练习"],
        ["asn-003", "ex-jpqa-003", "jhc-s03", "田中悠真", "jhc-2026-java", "需修改", "2026-06-24", "2026-06-25", "发表会Q&A补强"],
        ["asn-004", "ex-bug-004", "jhc-s06", "山本結衣", "jhc-2026-java", "已确认", "2026-06-25", "2026-06-26", "错误定位报告"],
        ["asn-005", "ex-founder-005", "jhc-s02", "鈴木美咲", "jhc-2026-java", "待Review", "2026-06-26", "2026-06-27", "Founder决策模拟"],
    ],
    columns=["assignment_id", "exercise_id", "learner_id", "learner_name", "cohort_id", "status", "assigned_at", "due_date", "note"],
)

SUBMISSIONS = pd.DataFrame(
    [
        [
            "sub-001",
            "asn-001",
            "ex-login-001",
            "jhc-s01",
            "佐藤拓海",
            "已提交",
            "2026-06-23 10:20",
            "选择题作答：C. 覆盖角色权限、连续失败锁定、特殊字符、超长输入、空格处理、登录后跳转。\n判定：正确；正确选项：C。",
            "单选题",
            "C",
            "C",
            True,
            88,
            "补充登录测试边界。",
        ],
        [
            "sub-002",
            "asn-002",
            "ex-order-002",
            "jhc-s02",
            "鈴木美咲",
            "已提交",
            "2026-06-24 15:40",
            "选择题作答：C. 需要说明创建、支付、上课扣课耗、余额变化、结课/结转，并覆盖重复支付、退费、课耗回滚、跨校区结算等异常。\n判定：正确；正确选项：C。",
            "单选题",
            "C",
            "C",
            True,
            88,
            "订单状态覆盖较完整。",
        ],
        [
            "sub-003",
            "asn-003",
            "ex-jpqa-003",
            "jhc-s03",
            "田中悠真",
            "需修改",
            "2026-06-25 09:15",
            "选择题作答：A. たぶん大丈夫だと思います。詳しくは分かりません。\n判定：需复习；正确选项：C。",
            "单选题",
            "A",
            "C",
            False,
            62,
            "日语回答需要更礼貌和职业化。",
        ],
        [
            "sub-004",
            "asn-004",
            "ex-bug-004",
            "jhc-s06",
            "山本結衣",
            "已确认",
            "2026-06-26 11:30",
            "选择题作答：C. 检查 Controller 参数、Service 方法、Mapper 接口 @Param、Mapper XML 中的占位符名称是否一致。\n判定：正确；正确选项：C。",
            "单选题",
            "C",
            "C",
            True,
            88,
            "能识别 MyBatis 参数绑定链路。",
        ],
    ],
    columns=[
        "submission_id",
        "assignment_id",
        "exercise_id",
        "learner_id",
        "learner_name",
        "status",
        "submitted_at",
        "answer_summary",
        "question_type",
        "selected_option",
        "correct_option",
        "is_correct",
        "auto_score",
        "answer_note",
    ],
)

REVIEWS = pd.DataFrame(
    [
        ["rev-001", "sub-001", "Agent", 88, "选择正确。建议补充登录后返回原访问页面的验证截图。", "待Founder确认", "候选"],
        ["rev-002", "sub-002", "Agent", 88, "选择正确。订单状态流转和异常分支具备业务价值。", "待Founder确认", "候选"],
        ["rev-003", "sub-003", "Agent", 62, "选择错误。遇到不知道的问题时不应含糊回答，应确认后补充。", "需复习", "否"],
        ["rev-004", "sub-004", "Founder", 90, "证据完整，可用于客户汇报和学员发表。", "已确认", "是"],
    ],
    columns=["review_id", "submission_id", "reviewer", "score", "review_comment", "decision", "proof_ready"],
)


def get_training_record_metrics() -> dict[str, int]:
    correct_series = SUBMISSIONS["is_correct"].fillna(False) if "is_correct" in SUBMISSIONS else pd.Series(dtype=bool)
    return {
        "assignments": int(len(ASSIGNMENTS)),
        "submissions": int(len(SUBMISSIONS)),
        "reviews": int(len(REVIEWS)),
        "proof_ready": int((REVIEWS["proof_ready"] == "是").sum()),
        "need_revision": int((REVIEWS["decision"].isin(["需修改", "需复习"])).sum()),
        "mcq_correct": int(correct_series.sum()),
    }


def joined_records() -> pd.DataFrame:
    submission_cols = [
        "assignment_id",
        "submission_id",
        "submitted_at",
        "answer_summary",
        "question_type",
        "selected_option",
        "correct_option",
        "is_correct",
        "auto_score",
        "answer_note",
    ]
    merged = ASSIGNMENTS.merge(
        SUBMISSIONS[submission_cols],
        on="assignment_id",
        how="left",
    )
    merged = merged.merge(
        REVIEWS[["submission_id", "reviewer", "score", "decision", "proof_ready"]],
        on="submission_id",
        how="left",
    )
    return merged
