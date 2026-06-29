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


def _pick(df: pd.DataFrame, cols: list[str], names: dict[str, str]) -> pd.DataFrame:
    selected = [c for c in cols if c in df.columns]
    public = df.loc[:, selected].copy() if not df.empty else pd.DataFrame(columns=selected)
    return public.rename(columns=names)


PUBLIC_NAMES = {
    "client_name": "客户名称", "service_package": "服务包", "status": "状态",
    "cohort_name": "班级名称", "learner_count": "学员数", "start_date": "开始日期", "end_date": "结束日期", "trainer": "讲师",
    "learner_name": "学员", "group": "小组", "progress": "进度", "tasks_done": "完成任务数", "proof_files": "作品证明数",
    "day": "训练日", "proof_task": "训练任务", "business_context": "业务场景", "required_output": "要求产出", "proof_score": "作品分",
    "exercise_id": "训练编号", "assigned_at": "布置日期", "due_date": "截止日期", "submitted_at": "提交时间",
    "answer_summary": "提交摘要", "submission_status": "提交状态", "score": "分数", "review_comment": "交付反馈",
    "decision": "评审结论", "proof_ready": "可作为作品证明", "title": "作品标题", "evidence": "证据材料",
    "package": "服务方向", "need": "需求内容",
}


def _public_leads(leads: pd.DataFrame) -> pd.DataFrame:
    public = _pick(leads, ["package", "need", "status"], PUBLIC_NAMES)
    status_text = {
        "新线索": "需求已记录，待进一步确认范围。",
        "已预约": "已安排后续沟通。",
        "跟进中": "需求沟通进行中。",
        "已转化": "已进入正式服务推进。",
    }
    if not public.empty:
        public["业务状态说明"] = public["状态"].map(status_text).fillna("需求已记录，等待后续沟通。")
    else:
        public["业务状态说明"] = []
    return public


def _public_updates(audits: pd.DataFrame) -> pd.DataFrame:
    if audits.empty:
        return pd.DataFrame(columns=["更新时间", "交付事件", "状态变化"])
    action_names = {
        "布置练习题": "训练任务已安排",
        "提交作答": "学员提交已记录",
        "生成/更新Review": "交付评审已更新",
        "确认进入Proof Files": "作品证明已确认",
        "要求重新提交": "修改任务已安排",
        "新增Proof File": "作品证明已新增",
        "新增Lead": "后续需求已记录",
        "更新Lead状态": "后续需求状态已更新",
    }
    rows = []
    for row in audits.sort_values("time", ascending=False).itertuples():
        if row.action == "重置测试数据":
            continue
        rows.append({
            "更新时间": row.time,
            "交付事件": action_names.get(row.action, "交付状态已更新"),
            "状态变化": f"{row.before_status} → {row.after_status}",
        })
    return pd.DataFrame(rows, columns=["更新时间", "交付事件", "状态变化"])


def _client_public_tables(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {
        "客户概况": _pick(tables["client"], ["client_name", "service_package", "status"], PUBLIC_NAMES),
        "班级概况": _pick(tables["cohorts"], ["cohort_name", "learner_count", "start_date", "end_date", "trainer", "status"], PUBLIC_NAMES),
        "学员进展": _pick(tables["learners"], ["learner_name", "group", "status", "progress", "tasks_done", "proof_files"], PUBLIC_NAMES),
        "训练任务": _pick(tables["tasks"], ["day", "learner_name", "proof_task", "business_context", "required_output", "status", "progress", "proof_score"], PUBLIC_NAMES),
        "训练记录": _pick(tables["training_records"], ["learner_name", "exercise_id", "status", "assigned_at", "due_date", "submitted_at", "submission_status", "score", "decision", "proof_ready", "review_comment"], PUBLIC_NAMES),
        "提交摘要": _pick(tables["submissions"], ["learner_name", "exercise_id", "status", "submitted_at", "answer_summary"], PUBLIC_NAMES),
        "交付评审": _pick(tables["reviews"], ["score", "review_comment", "decision", "proof_ready"], PUBLIC_NAMES),
        "作品证明": _pick(tables["proof_files"], ["learner_name", "title", "status", "score", "evidence"], PUBLIC_NAMES),
        "后续需求状态": _public_leads(tables["leads"]),
        "交付更新摘要": _public_updates(tables["audit_logs"]),
        "字段控制说明": pd.DataFrame([
            ["客户范围", "仅包含所选客户相关数据"],
            ["字段白名单", "不导出内部备注、原始审计、Founder/Agent 操作字段"],
            ["金额脱敏", "不展示合同金额和潜在线索金额，用业务状态说明替代"],
        ], columns=["控制项", "客户版规则"]),
    }


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

    return f"""# {client_name} 客户交付包周报（内部版）

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


def _client_public_report_text(client_id: str, public_tables: dict[str, pd.DataFrame], raw_tables: dict[str, pd.DataFrame]) -> str:
    client_name = str(raw_tables["client"].iloc[0]["client_name"]) if not raw_tables["client"].empty else client_id
    service_package = str(raw_tables["client"].iloc[0]["service_package"]) if not raw_tables["client"].empty else "AI Skill Growth OS"
    records, reviews = raw_tables["training_records"], raw_tables["reviews"]
    proof_ready = int((reviews["proof_ready"] == "是").sum()) if not reviews.empty else 0
    need_revision = int((reviews["decision"] == "需修改").sum()) if not reviews.empty else 0

    proofs = public_tables["作品证明"]
    proof_lines = "- 暂无可展示作品证明。" if proofs.empty else "\n".join(
        f"- {r['学员']}：《{r['作品标题']}》，状态：{r['状态']}，分数：{int(r['分数'])}"
        for _, r in proofs.sort_values("分数", ascending=False).head(5).iterrows()
    )

    revision_rows = records[records["decision"] == "需修改"] if not records.empty and "decision" in records.columns else pd.DataFrame()
    revision_lines = "- 暂无需修改记录。" if revision_rows.empty else "\n".join(
        f"- {r.learner_name}：训练编号 {r.exercise_id}，当前结论：{r.decision}；交付反馈：{r.review_comment}"
        for r in revision_rows.itertuples()
    )

    leads = public_tables["后续需求状态"]
    lead_lines = "- 暂无需要单独跟进的后续需求。" if leads.empty else "\n".join(
        f"- {r['需求内容']}：{r['业务状态说明']}"
        for _, r in leads.iterrows()
    )

    return f"""# {client_name} 训练交付周报（客户版）

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
服务包：{service_package}

> 本报告为客户交付版，仅包含该客户范围内的训练进展、作品证明、修改事项和后续沟通状态；不包含内部审计日志、内部备注、其他客户信息或潜在线索金额。

## 一、交付范围
- 客户：{client_name}
- 班级数：{len(raw_tables['cohorts'])}
- 学员数：{len(raw_tables['learners'])}
- 训练记录：{len(records)}
- 已完成评审：{len(reviews)}
- 可作为作品证明：{proof_ready}
- 需继续修改：{need_revision}

## 二、本周交付进展
本周训练继续围绕真实业务任务推进，覆盖任务布置、学员提交、交付评审、作品证明沉淀和后续需求确认。当前交付重点是提高学员产出的可展示性，并把高质量作业沉淀为可复用的 Proof Files。

## 三、优秀作品 / Proof Files
{proof_lines}

## 四、需修改与风险提醒
{revision_lines}

## 五、后续需求状态
{lead_lines}

## 六、下周计划
- 优先处理需修改记录，补齐证据、异常分支和可展示材料。
- 将已达标作品整理为客户汇报和学员发表素材。
- 继续跟进后续需求状态，确认是否扩展为标准化训练服务包。
"""


def export_page() -> None:
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><span class='pill hot'>数据导出</span><h2>CSV / Excel / Markdown 交付包</h2><p>支持全量导出、内部客户包和对外客户包，便于真实企业客户交付、备份和二次分析。</p></div>",
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

    st.markdown("<div class='section'>完整 Excel 交付包（内部版）</div>", unsafe_allow_html=True)
    st.info("内部版保留全量业务字段、原始 Leads 金额和审计日志，仅用于 Founder 运营复盘。")
    st.download_button(
        "下载完整业务数据 Excel（内部版）",
        data=_excel_bytes(tables),
        file_name="ai_skill_growth_os_internal_delivery_pack.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    st.markdown("<div class='section'>按客户导出交付包</div>", unsafe_allow_html=True)
    client_options = dict(zip(CLIENTS["client_name"], CLIENTS["client_id"]))
    client_name = st.selectbox("选择客户", list(client_options.keys()))
    client_id = client_options[client_name]
    raw_client_tables = _client_tables(client_id)
    export_version = st.radio("交付包版本", ["客户版（脱敏字段白名单）", "内部版（客户范围完整）"], horizontal=True)
    customer_mode = export_version.startswith("客户版")
    client_tables = _client_public_tables(raw_client_tables) if customer_mode else raw_client_tables

    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>客户班级</span><div class='metric'>{len(raw_client_tables['cohorts'])}</div></div>
  <div class='card'><span class='mini'>客户学员</span><div class='metric'>{len(raw_client_tables['learners'])}</div></div>
  <div class='card'><span class='mini'>客户训练记录</span><div class='metric'>{len(raw_client_tables['training_records'])}</div></div>
  <div class='card'><span class='mini'>客户 Proof Files</span><div class='metric'>{len(raw_client_tables['proof_files'])}</div></div>
</div>
""", unsafe_allow_html=True)
    if customer_mode:
        st.success("客户版已启用字段白名单：隐藏合同金额、潜在线索金额、内部备注、Founder/Agent 操作细节和原始审计日志。")
    else:
        st.warning("内部版仅限 Founder 运营使用：保留客户范围内的完整明细、金额和审计日志。")

    preview_table = st.selectbox("预览客户交付表", list(client_tables.keys()))
    st.dataframe(client_tables[preview_table], use_container_width=True, hide_index=True)

    suffix = "customer" if customer_mode else "internal"
    st.download_button(
        "下载该客户 Excel 交付包",
        data=_excel_bytes(client_tables),
        file_name=f"{client_id}_{suffix}_delivery_pack_v4_10_2.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    client_report = _client_public_report_text(client_id, client_tables, raw_client_tables) if customer_mode else _client_report_text(client_id, raw_client_tables)
    st.text_area("客户周报 Markdown 预览", value=client_report, height=420)
    st.download_button(
        "下载该客户周报 Markdown",
        data=client_report.encode("utf-8"),
        file_name=f"{client_id}_{suffix}_weekly_report_v4_10_2.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown("<div class='section'>全量企业周报 Markdown（内部版）</div>", unsafe_allow_html=True)
    report_markdown = _report_text()
    st.text_area("全量周报内容预览", value=report_markdown, height=360)
    st.download_button(
        "下载全量企业交付周报 Markdown（内部版）",
        data=report_markdown.encode("utf-8"),
        file_name="enterprise_internal_delivery_weekly_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown("<div class='section'>导出建议</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card'><h3>给客户</h3><p>优先交付客户版 Markdown 周报 + 客户版 Excel。客户版只含字段白名单，不含内部备注、金额线索和原始审计日志。</p></div>"
        "<div class='card'><h3>给内部运营</h3><p>导出完整 Excel 或内部版客户包，用于复盘训练质量、线索转化和审计追踪。</p></div>",
        unsafe_allow_html=True,
    )
