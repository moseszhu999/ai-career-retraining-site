from __future__ import annotations

from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.audit_log import audit_logs
from frontend.business_data import CLIENTS, COHORTS, LEARNERS
from frontend.permissions import can_manage_operations, forbidden_message, permission_summary_html
from frontend.report_pages import _report_text


def _csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def _excel_bytes(tables: dict[str, pd.DataFrame]) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in tables.items():
            safe_name = sheet_name[:31]
            df.to_excel(writer, index=False, sheet_name=safe_name)
    return output.getvalue()


def _export_tables() -> dict[str, pd.DataFrame]:
    return {
        "training_records": ops.joined_records(),
        "assignments": ops.assignments(),
        "submissions": ops.submissions(),
        "reviews": ops.reviews(),
        "proof_files": ops.proof_files(),
        "leads": ops.consult_leads(),
        "audit_logs": audit_logs(),
    }


def _client_tables(client_id: str) -> dict[str, pd.DataFrame]:
    client_df = CLIENTS[CLIENTS["client_id"] == client_id].copy()
    cohorts_df = COHORTS[COHORTS["client_id"] == client_id].copy()
    cohort_ids = cohorts_df["cohort_id"].tolist()
    learners_df = LEARNERS[LEARNERS["cohort_id"].isin(cohort_ids)].copy()
    learner_names = learners_df["learner_name"].tolist()
    learner_ids = learners_df["learner_id"].tolist()

    assignments_df = ops.assignments()[ops.assignments()["cohort_id"].isin(cohort_ids)].copy()
    assignment_ids = assignments_df["assignment_id"].tolist()
    submissions_df = ops.submissions()[ops.submissions()["assignment_id"].isin(assignment_ids)].copy()
    submission_ids = submissions_df["submission_id"].tolist()
    reviews_df = ops.reviews()[ops.reviews()["submission_id"].isin(submission_ids)].copy()
    records_df = ops.joined_records()[ops.joined_records()["cohort_id"].isin(cohort_ids)].copy()
    tasks_df = ops.task_instances()[ops.task_instances()["learner_id"].isin(learner_ids)].copy()
    proof_df = ops.proof_files()[ops.proof_files()["learner_name"].isin(learner_names)].copy()

    client_name = str(client_df.iloc[0]["client_name"]) if not client_df.empty else ""
    leads = ops.consult_leads()
    leads_df = leads[leads["client_name"] == client_name].copy()
    if leads_df.empty and client_name:
        leads_df = leads[leads["client_name"].str.contains(client_name[:4], na=False)].copy()

    audit_df = _client_audits(assignment_ids, submissions_df, reviews_df, proof_df, leads_df, learner_names)

    return {
        "client": client_df,
        "cohorts": cohorts_df,
        "learners": learners_df,
        "tasks": tasks_df,
        "training_records": records_df,
        "assignments": assignments_df,
        "submissions": submissions_df,
        "reviews": reviews_df,
        "proof_files": proof_df,
        "leads": leads_df,
        "audit_logs": audit_df,
    }


def _client_audits(
    assignment_ids: list[str],
    submissions_df: pd.DataFrame,
    reviews_df: pd.DataFrame,
    proof_df: pd.DataFrame,
    leads_df: pd.DataFrame,
    learner_names: list[str],
) -> pd.DataFrame:
    audits = audit_logs().copy()
    object_ids = set(assignment_ids)
    if not submissions_df.empty:
        object_ids.update(submissions_df["submission_id"].tolist())
    if not reviews_df.empty:
        object_ids.update(reviews_df["review_id"].tolist())
    if not proof_df.empty:
        object_ids.update(proof_df["proof_id"].tolist())
    if not leads_df.empty:
        object_ids.update(leads_df["lead_id"].tolist())

    if audits.empty:
        return audits
    mask = audits["object_id"].isin(object_ids)
    for name in learner_names:
        mask = mask | audits["summary"].str.contains(str(name), na=False)
    return audits[mask].copy()


def _client_report_text(client_id: str, tables: dict[str, pd.DataFrame]) -> str:
    client_name = str(tables["client"].iloc[0]["client_name"]) if not tables["client"].empty else client_id
    contract_value = int(tables["client"].iloc[0]["contract_value"]) if not tables["client"].empty else 0
    records = tables["training_records"]
    reviews = tables["reviews"]
    proofs = tables["proof_files"]
    leads = tables["leads"]
    audits = tables["audit_logs"]

    proof_ready = int((reviews["proof_ready"] == "是").sum()) if not reviews.empty else 0
    need_revision = int((reviews["decision"] == "需修改").sum()) if not reviews.empty else 0
    lead_value = int(leads["potential_value"].sum()) if not leads.empty else 0

    proof_lines = "\n".join(
        f"- {r.learner_name}：《{r.title}》{int(r.score)}分，状态：{r.status}"
        for r in proofs.sort_values("score", ascending=False).head(5).itertuples()
    ) or "- 暂无可展示 Proof File。"

    revision_rows = records[records["decision"] == "需修改"] if not records.empty and "decision" in records.columns else pd.DataFrame()
    revision_lines = "\n".join(
        f"- {r.learner_name}：{r.exercise_id}，状态：{r.status}，建议：{r.review_comment}"
        for r in revision_rows.itertuples()
    ) or "- 暂无需修改记录。"

    lead_lines = "\n".join(
        f"- {r.need}：{r.status}，金额：¥{int(r.potential_value):,}"
        for r in leads.itertuples()
    ) or "- 暂无客户线索。"

    audit_lines = "\n".join(
        f"- {r.time}｜{r.actor}｜{r.action}｜{r.object_type}:{r.object_id}｜{r.before_status}→{r.after_status}"
        for r in audits.sort_values("time", ascending=False).head(8).itertuples()
    ) or "- 暂无该客户相关操作日志。"

    return f"""# {client_name} 客户交付包周报

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
合同金额：¥{contract_value:,}

## 一、客户范围
- 客户：{client_name}
- 班级数：{len(tables['cohorts'])}
- 学员数：{len(tables['learners'])}
- 训练记录：{len(records)}
- Submission：{len(tables['submissions'])}
- Review：{len(reviews)}
- Proof Ready：{proof_ready}
- 需修改：{need_revision}

## 二、交付进展
该客户交付包围绕真实业务训练闭环推进：任务布置、学员提交、Agent/Founder Review、Proof Files 沉淀和后续服务包线索跟进。

## 三、优秀作品 / Proof Files
{proof_lines}

## 四、需修改与风险提醒
{revision_lines}

## 五、客户线索进展
- 当前客户相关潜在金额：¥{lead_value:,}
{lead_lines}

## 六、操作审计摘要
{audit_lines}

## 七、下周建议
- 先处理需修改记录，补齐证据和异常分支。
- 把高分 Proof Files 整理成客户汇报材料。
- 对客户线索安排下一次沟通，推动标准训练包续费或扩展。
"""


def export_page() -> None:
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><span class='pill hot'>数据导出</span><h2>CSV / Excel / Markdown 交付包</h2><p>支持全量导出和按客户导出，便于真实企业客户交付、备份和二次分析。</p></div>",
        unsafe_allow_html=True,
    )
    if not can_manage_operations():
        st.warning(forbidden_message("导出企业交付数据"))
        return

    tables = _export_tables()
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>训练记录</span><div class='metric'>{len(tables['training_records'])}</div></div>
  <div class='card'><span class='mini'>Proof Files</span><div class='metric'>{len(tables['proof_files'])}</div></div>
  <div class='card'><span class='mini'>Leads</span><div class='metric'>{len(tables['leads'])}</div></div>
  <div class='card'><span class='mini'>Audit Logs</span><div class='metric'>{len(tables['audit_logs'])}</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='section'>单表 CSV 导出</div>", unsafe_allow_html=True)
    export_options = {
        "训练记录 training_records.csv": "training_records",
        "Assignments assignments.csv": "assignments",
        "Submissions submissions.csv": "submissions",
        "Reviews reviews.csv": "reviews",
        "Proof Files proof_files.csv": "proof_files",
        "Leads leads.csv": "leads",
        "Audit Logs audit_logs.csv": "audit_logs",
    }
    selected = st.selectbox("选择要预览 / 导出的表", list(export_options.keys()))
    key = export_options[selected]
    df = tables[key]
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "下载当前表 CSV",
        data=_csv_bytes(df),
        file_name=f"{key}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("<div class='section'>完整 Excel 交付包</div>", unsafe_allow_html=True)
    st.download_button(
        "下载完整业务数据 Excel",
        data=_excel_bytes(tables),
        file_name="ai_skill_growth_os_delivery_pack.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    st.markdown("<div class='section'>按客户导出交付包</div>", unsafe_allow_html=True)
    client_options = dict(zip(CLIENTS["client_name"], CLIENTS["client_id"]))
    client_name = st.selectbox("选择客户", list(client_options.keys()))
    client_id = client_options[client_name]
    client_tables = _client_tables(client_id)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>客户班级</span><div class='metric'>{len(client_tables['cohorts'])}</div></div>
  <div class='card'><span class='mini'>客户学员</span><div class='metric'>{len(client_tables['learners'])}</div></div>
  <div class='card'><span class='mini'>客户训练记录</span><div class='metric'>{len(client_tables['training_records'])}</div></div>
  <div class='card'><span class='mini'>客户 Proof Files</span><div class='metric'>{len(client_tables['proof_files'])}</div></div>
</div>
""", unsafe_allow_html=True)
    preview_table = st.selectbox(
        "预览客户交付表",
        ["client", "cohorts", "learners", "tasks", "training_records", "proof_files", "leads", "audit_logs"],
    )
    st.dataframe(client_tables[preview_table], use_container_width=True, hide_index=True)
    st.download_button(
        "下载该客户 Excel 交付包",
        data=_excel_bytes(client_tables),
        file_name=f"{client_id}_delivery_pack.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    client_report = _client_report_text(client_id, client_tables)
    st.text_area("客户周报 Markdown 预览", value=client_report, height=420)
    st.download_button(
        "下载该客户周报 Markdown",
        data=client_report.encode("utf-8"),
        file_name=f"{client_id}_weekly_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown("<div class='section'>全量企业周报 Markdown</div>", unsafe_allow_html=True)
    report_markdown = _report_text()
    st.text_area("全量周报内容预览", value=report_markdown, height=360)
    st.download_button(
        "下载全量企业交付周报 Markdown",
        data=report_markdown.encode("utf-8"),
        file_name="enterprise_delivery_weekly_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown("<div class='section'>导出建议</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card'><h3>给客户</h3><p>优先交付客户专属 Markdown 周报 + 客户 Excel 交付包。</p></div>"
        "<div class='card'><h3>给内部运营</h3><p>导出完整 Excel，用于复盘训练质量、线索转化和审计追踪。</p></div>",
        unsafe_allow_html=True,
    )
