from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.audit_log import audit_logs, audit_metrics
from frontend.business_data import CLIENTS, COHORTS, LEARNERS
from frontend.permissions import can_manage_operations, forbidden_message, permission_summary_html


def _status_count(df: pd.DataFrame, column: str, value: str) -> int:
    if df.empty or column not in df.columns:
        return 0
    return int((df[column] == value).sum())


def _report_text() -> str:
    records = ops.joined_records()
    proofs = ops.proof_files()
    leads = ops.consult_leads()
    audits = audit_logs()

    learner_count = int(LEARNERS["learner_id"].nunique())
    assignment_count = int(len(ops.assignments()))
    submission_count = int(len(ops.submissions()))
    review_count = int(len(ops.reviews()))
    proof_ready_count = _status_count(ops.reviews(), "proof_ready", "是")
    need_revision = _status_count(ops.reviews(), "decision", "需修改")
    lead_value = int(leads["potential_value"].sum()) if not leads.empty else 0

    top_proofs = proofs.sort_values("score", ascending=False).head(3) if not proofs.empty else pd.DataFrame()
    revision_rows = records[records["decision"] == "需修改"] if "decision" in records.columns else pd.DataFrame()

    proof_lines = "\n".join(
        f"- {r.learner_name}：《{r.title}》{int(r.score)}分，状态：{r.status}"
        for r in top_proofs.itertuples()
    ) or "- 暂无可展示 Proof File。"

    revision_lines = "\n".join(
        f"- {r.learner_name}：{r.exercise_id}，当前状态：{r.status}"
        for r in revision_rows.itertuples()
    ) or "- 暂无需修改记录。"

    lead_lines = "\n".join(
        f"- {r.client_name}：{r.need}，状态：{r.status}，金额：¥{int(r.potential_value):,}"
        for r in leads.itertuples()
    ) or "- 暂无线索。"

    latest_audits = audits.sort_values("time", ascending=False).head(5)
    audit_lines = "\n".join(
        f"- {r.time}｜{r.actor}（{r.role}）｜{r.action}｜{r.object_type}:{r.object_id}｜{r.before_status}→{r.after_status}"
        for r in latest_audits.itertuples()
    ) or "- 暂无操作日志。"

    return f"""# 企业训练交付周报

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 一、总体进展
- 客户数：{len(CLIENTS)}
- 班级数：{len(COHORTS)}
- 学员数：{learner_count}
- Assignment：{assignment_count}
- Submission：{submission_count}
- Review：{review_count}
- Proof Ready：{proof_ready_count}
- 需修改：{need_revision}

## 二、训练交付情况
本周训练围绕真实业务任务推进：软件测试、订单流转、日语发表、错误定位、Founder决策和服务包销售。当前系统已形成 Assignment → Submission → Review → Proof Files 的闭环。

## 三、优秀作品 / 可展示 Proof Files
{proof_lines}

## 四、需修改 / 风险提醒
{revision_lines}

## 五、线索与服务包进展
- 潜在线索金额：¥{lead_value:,}
{lead_lines}

## 六、Founder / 学员操作摘要
{audit_lines}

## 七、下周建议
- 优先处理需修改记录，补齐证据和边界条件。
- 将 Proof Ready 的作品整理成客户汇报材料。
- 对已预约 / 高金额 Leads 安排下一次沟通。
- 继续把讲师交付沉淀成标准任务包、评分标准和 Proof Files 模板。
"""


def delivery_report_page() -> None:
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><span class='pill hot'>企业交付报表 / 周报</span><h2>一键生成客户能看懂的训练交付报告</h2><p>汇总训练人数、提交、Review、Proof Ready、需修改名单、优秀作品、线索进展和操作摘要。</p></div>",
        unsafe_allow_html=True,
    )
    if not can_manage_operations():
        st.warning(forbidden_message("查看企业交付报表"))
        return

    records = ops.joined_records()
    proofs = ops.proof_files()
    leads = ops.consult_leads()
    metrics = ops.operation_metrics()
    audit_stat = audit_metrics()

    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>训练学员</span><div class='metric'>{LEARNERS['learner_id'].nunique()}</div></div>
  <div class='card'><span class='mini'>提交记录</span><div class='metric'>{metrics['submissions']}</div></div>
  <div class='card'><span class='mini'>Proof Files</span><div class='metric'>{metrics['proof_files']}</div></div>
  <div class='card'><span class='mini'>审计记录</span><div class='metric'>{audit_stat['audit_count']}</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='section'>训练状态分布</div>", unsafe_allow_html=True)
    if records.empty:
        st.info("暂无训练记录。")
    else:
        status_df = records.groupby("status", dropna=False).size().reset_index(name="count")
        st.dataframe(status_df, use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>需修改名单</div>", unsafe_allow_html=True)
    revision_rows = records[records["decision"] == "需修改"] if not records.empty and "decision" in records.columns else pd.DataFrame()
    if revision_rows.empty:
        st.success("当前没有需修改记录。")
    else:
        st.dataframe(
            revision_rows[["assignment_id", "exercise_id", "learner_name", "status", "score", "decision", "review_comment"]],
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("<div class='section'>优秀作品 / Proof Files</div>", unsafe_allow_html=True)
    if proofs.empty:
        st.info("暂无 Proof Files。")
    else:
        st.dataframe(proofs.sort_values("score", ascending=False), use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>线索进展</div>", unsafe_allow_html=True)
    if leads.empty:
        st.info("暂无 Leads。")
    else:
        lead_status_df = leads.groupby("status", dropna=False).agg(
            count=("lead_id", "count"),
            value=("potential_value", "sum"),
        ).reset_index()
        st.dataframe(lead_status_df, use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>可复制周报正文</div>", unsafe_allow_html=True)
    report = _report_text()
    st.text_area("企业交付周报 Markdown", value=report, height=520)
