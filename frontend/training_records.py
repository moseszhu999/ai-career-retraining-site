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
        ["sub-001", "asn-001", "ex-login-001", "jhc-s01", "佐藤拓海", "已提交", "2026-06-23 10:20", "补充了管理员/普通用户、连续失败、特殊字符、超长输入、空格处理、跳转回原页面。"],
        ["sub-002", "asn-002", "ex-order-002", "jhc-s02", "鈴木美咲", "已提交", "2026-06-24 15:40", "画出了订单主流程，并列出重复支付、退费、课耗回滚、跨校区结算异常。"],
        ["sub-003", "asn-003", "ex-jpqa-003", "jhc-s03", "田中悠真", "需修改", "2026-06-25 09:15", "写了不知道答案时的日语回复，但缺少会后补充和被指名回答场景。"],
        ["sub-004", "asn-004", "ex-bug-004", "jhc-s06", "山本結衣", "已确认", "2026-06-26 11:30", "完成错误定位报告，包含现象、日志、参数名不一致、修复和验证截图。"],
    ],
    columns=["submission_id", "assignment_id", "exercise_id", "learner_id", "learner_name", "status", "submitted_at", "answer_summary"],
)

REVIEWS = pd.DataFrame(
    [
        ["rev-001", "sub-001", "Agent", 76, "覆盖面不错，建议补充登录后返回原访问页面的验证截图。", "修改中", "否"],
        ["rev-002", "sub-002", "Agent", 84, "订单状态流转完整，异常分支具备业务价值。建议进入Founder确认。", "待Founder确认", "候选"],
        ["rev-003", "sub-003", "Agent", 61, "日语回答礼貌，但场景覆盖不足。需要补被指名回答和会后补充。", "需修改", "否"],
        ["rev-004", "sub-004", "Founder", 90, "证据完整，可用于客户汇报和学员发表。", "已确认", "是"],
    ],
    columns=["review_id", "submission_id", "reviewer", "score", "review_comment", "decision", "proof_ready"],
)


def get_training_record_metrics() -> dict[str, int]:
    return {
        "assignments": int(len(ASSIGNMENTS)),
        "submissions": int(len(SUBMISSIONS)),
        "reviews": int(len(REVIEWS)),
        "proof_ready": int((REVIEWS["proof_ready"] == "是").sum()),
        "need_revision": int((REVIEWS["decision"] == "需修改").sum()),
    }


def joined_records() -> pd.DataFrame:
    merged = ASSIGNMENTS.merge(
        SUBMISSIONS[["assignment_id", "submission_id", "submitted_at", "answer_summary"]],
        on="assignment_id",
        how="left",
    )
    merged = merged.merge(
        REVIEWS[["submission_id", "reviewer", "score", "decision", "proof_ready"]],
        on="submission_id",
        how="left",
    )
    return merged
