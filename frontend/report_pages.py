from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.data_repository import TrainingRepository, get_repository
from frontend.permissions import can_manage_operations, forbidden_message, permission_summary_html


def _status_count(df: pd.DataFrame, column: str, value: str) -> int:
    if df.empty or column not in df.columns:
        return 0
    return int((df[column] == value).sum())


def _count_unique(df: pd.DataFrame, column: str) -> int:
    if df.empty or column not in df.columns:
        return 0
    return int(df[column].nunique())


def _accuracy_text(total: int, correct: int) -> str:
    if total <= 0:
        return "0%"
    return f"{correct / total * 100:.1f}%"


def _operation_metrics(repo: TrainingRepository) -> dict[str, int]:
    reviews = repo.reviews()
    proof_files = repo.proof_files()
    leads = repo.consult_leads()
    op = ops.operation_metrics()
    return {
        "assignments": int(len(repo.assignments())),
        "submissions": int(len(repo.submissions())),
        "reviews": int(len(reviews)),
        "proof_ready": _status_count(reviews, "proof_ready", "是"),
        "need_revision": int((reviews["decision"].isin(["需修改", "需复习"])).sum()) if not reviews.empty and "decision" in reviews.columns else 0,
        "proof_files": int(len(proof_files)),
        "leads": int(len(leads)),
        "lead_value": int(leads["potential_value"].sum()) if not leads.empty and "potential_value" in leads.columns else 0,
        "mcq_total": int(op.get("mcq_total", 0)),
        "mcq_correct": int(op.get("mcq_correct", 0)),
    }


def _audit_metrics(repo: TrainingRepository) -> dict[str, int]:
    audits = repo.audit_logs()
    return {
        "audit_count": int(len(audits)),
        "founder_actions": _status_count(audits, "role", "Founder"),
        "learner_actions": _status_count(audits, "role", "学员"),
        "proof_actions": _status_count(audits, "object_type", "ProofFile"),
    }


def _module_lines() -> str:
    module_stats = ops.mcq_module_stats()
    if module_stats.empty:
        return "- 暂无选择题模块统计。"
    lines = []
    for row in module_stats.itertuples():
        lines.append(f"- {row.module}：{int(row.correct)}/{int(row.attempts)}，正确率 {row.accuracy}% ，错题 {int(row.wrong)}")
    return "\n".join(lines)


def _wrong_lines(limit: int = 8) -> str:
    wrong = ops.wrong_answer_records()
    if wrong.empty:
        return "- 当前没有错题记录。"
    lines = []
    for row in wrong.head(limit).itertuples():
        lines.append(
            f"- {row.learner_name}：{row.exercise_id} / {getattr(row, 'module', '')}，选择 {row.selected_option}，正确 {row.correct_option}"
        )
    return "\n".join(lines)


def _proof_candidate_lines(limit: int = 8) -> str:
    queue = ops.review_queue_view()
    if queue.empty or "review_route" not in queue.columns:
        return "- 暂无 Proof 候选。"
    candidates = queue[queue["review_route"] == "Proof候选"]
    if candidates.empty:
        return "- 暂无 Proof 候选。"
    lines = []
    for row in candidates.head(limit).itertuples():
        score = getattr(row, "score", None)
        auto_score = getattr(row, "auto_score", None)
        lines.append(
            f"- {row.learner_name}：{row.exercise_id}，选择 {row.selected_option}/{row.correct_option}，自动分 {auto_score}，Review 分 {score}"
        )
    return "\n".join(lines)


def _report_text(repo: TrainingRepository | None = None) -> str:
    repo = repo or get_repository()
    clients = repo.clients()
    cohorts = repo.cohorts()
    learners = repo.learners()
    records = repo.joined_records()
    reviews = repo.reviews()
    proofs = repo.proof_files()
    leads = repo.consult_leads()
    audits = repo.audit_logs()
    metrics = _operation_metrics(repo)

    learner_count = _count_unique(learners, "learner_id")
    assignment_count = int(len(repo.assignments()))
    submission_count = int(len(repo.submissions()))
    review_count = int(len(reviews))
    proof_ready_count = _status_count(reviews, "proof_ready", "是")
    need_revision = metrics["need_revision"]
    lead_value = int(leads["potential_value"].sum()) if not leads.empty and "potential_value" in leads.columns else 0
    mcq_total = metrics["mcq_total"]
    mcq_correct = metrics["mcq_correct"]
    mcq_accuracy = _accuracy_text(mcq_total, mcq_correct)

    top_proofs = proofs.sort_values("score", ascending=False).head(3) if not proofs.empty and "score" in proofs.columns else pd.DataFrame()
    revision_rows = records[records["decision"].isin(["需修改", "需复习"])] if not records.empty and "decision" in records.columns else pd.DataFrame()

    proof_lines = "\n".join(
        f"- {r.learner_name}：《{r.title}》{int(r.score)}分，状态：{r.status}"
        for r in top_proofs.itertuples()
    ) or "- 暂无可展示 Proof File。"

    revision_lines = "\n".join(
        f"- {r.learner_name}：{r.exercise_id}，当前状态：{r.status}，结论：{getattr(r, 'decision', '')}"
        for r in revision_rows.itertuples()
    ) or "- 暂无需修改记录。"

    lead_lines = "\n".join(
        f"- {r.client_name}：{r.need}，状态：{r.status}，金额：¥{int(r.potential_value):,}"
        for r in leads.itertuples()
    ) or "- 暂无线索。"

    latest_audits = audits.sort_values("time", ascending=False).head(5) if not audits.empty and "time" in audits.columns else pd.DataFrame()
    audit_lines = "\n".join(
        f"- {r.time}｜{r.actor}（{r.role}）｜{r.action}｜{r.object_type}:{r.object_id}｜{r.before_status}→{r.after_status}"
        for r in latest_audits.itertuples()
    ) or "- 暂无操作日志。"

    return f"""# 企业训练交付周报

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 一、总体进展
- 客户数：{len(clients)}
- 班级数：{len(cohorts)}
- 学员数：{learner_count}
- Assignment：{assignment_count}
- Submission：{submission_count}
- Review：{review_count}
- Proof Ready：{proof_ready_count}
- 需修改 / 需复习：{need_revision}

## 二、选择题训练表现
- 选择题提交：{mcq_total}
- 正确提交：{mcq_correct}
- 正确率：{mcq_accuracy}

### 模块正确率 / 薄弱点
{_module_lines()}

### 错题复习名单
{_wrong_lines()}

### Proof 候选
{_proof_candidate_lines()}

## 三、训练交付情况
本周训练围绕真实业务任务推进：软件测试、订单流转、日语发表、错误定位、Founder决策和服务包销售。当前系统已形成 Assignment → Submission → Review → Proof Files 的闭环，并新增选择题自动初评、模块正确率和错题复习机制。

## 四、优秀作品 / 可展示 Proof Files
{proof_lines}

## 五、需修改 / 风险提醒
{revision_lines}

## 六、线索与服务包进展
- 潜在线索金额：¥{lead_value:,}
{lead_lines}

## 七、Founder / 学员操作摘要
{audit_lines}

## 八、下周建议
- 优先处理“需复习”模块，按模块正确率最低项安排集中讲解。
- 将 Proof 候选逐条确认，合格后进入客户汇报材料。
- 对错题较多的学员安排二次练习。
- 对已预约 / 高金额 Leads 安排下一次沟通。
"""


def delivery_report_page() -> None:
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><span class='pill hot'>企业交付报表 / 周报</span><h2>选择题训练运营与客户交付报告</h2><p>汇总选择题提交、正确率、模块薄弱点、错题复习、Proof 候选和客户可见交付成果。</p></div>",
        unsafe_allow_html=True,
    )
    if not can_manage_operations():
        st.warning(forbidden_message("查看企业交付报表"))
        return

    repo = get_repository()
    learners = repo.learners()
    records = repo.joined_records()
    proofs = repo.proof_files()
    leads = repo.consult_leads()
    metrics = _operation_metrics(repo)
    audit_stat = _audit_metrics(repo)
    module_stats = ops.mcq_module_stats()
    wrong = ops.wrong_answer_records()
    queue = ops.review_queue_view()
    candidates = queue[queue["review_route"] == "Proof候选"] if not queue.empty and "review_route" in queue.columns else pd.DataFrame()

    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>训练学员</span><div class='metric'>{_count_unique(learners, 'learner_id')}</div></div>
  <div class='card'><span class='mini'>MCQ 正确率</span><div class='metric'>{_accuracy_text(metrics['mcq_total'], metrics['mcq_correct'])}</div></div>
  <div class='card'><span class='mini'>需复习</span><div class='metric'>{len(wrong)}</div></div>
  <div class='card'><span class='mini'>Proof 候选</span><div class='metric'>{len(candidates)}</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='section'>模块正确率 / 薄弱点</div>", unsafe_allow_html=True)
    if module_stats.empty:
        st.info("暂无模块统计。")
    else:
        st.dataframe(module_stats, use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>错题复习名单</div>", unsafe_allow_html=True)
    if wrong.empty:
        st.success("当前没有错题。")
    else:
        visible_cols = ["learner_name", "exercise_id", "module", "selected_option", "correct_option", "explanation"]
        st.dataframe(wrong[[col for col in visible_cols if col in wrong.columns]], use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>Proof 候选</div>", unsafe_allow_html=True)
    if candidates.empty:
        st.info("暂无 Proof 候选。")
    else:
        visible_cols = ["learner_name", "exercise_id", "module", "selected_option", "correct_option", "auto_score", "score", "decision", "proof_ready"]
        st.dataframe(candidates[[col for col in visible_cols if col in candidates.columns]], use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>训练状态分布</div>", unsafe_allow_html=True)
    if records.empty:
        st.info("暂无训练记录。")
    else:
        status_df = records.groupby("status", dropna=False).size().reset_index(name="count")
        st.dataframe(status_df, use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>优秀作品 / Proof Files</div>", unsafe_allow_html=True)
    if proofs.empty:
        st.info("暂无 Proof Files。")
    else:
        sort_col = "score" if "score" in proofs.columns else proofs.columns[0]
        st.dataframe(proofs.sort_values(sort_col, ascending=False), use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>线索进展</div>", unsafe_allow_html=True)
    if leads.empty:
        st.info("暂无 Leads。")
    else:
        agg_spec = {"count": ("lead_id", "count")}
        if "potential_value" in leads.columns:
            agg_spec["value"] = ("potential_value", "sum")
        lead_status_df = leads.groupby("status", dropna=False).agg(**agg_spec).reset_index()
        st.dataframe(lead_status_df, use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>审计记录概况</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([audit_stat]), use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>可复制周报正文</div>", unsafe_allow_html=True)
    report = _report_text(repo)
    st.text_area("企业交付周报 Markdown", value=report, height=620)
