from __future__ import annotations

from io import BytesIO

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.audit_log import audit_logs
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


def export_page() -> None:
    st.markdown(permission_summary_html(), unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><span class='pill hot'>数据导出</span><h2>CSV / Excel / Markdown 交付包</h2><p>导出训练记录、Proof Files、Leads、Audit Logs 和企业交付周报，便于客户交付、备份和二次分析。</p></div>",
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

    st.markdown("<div class='section'>企业周报 Markdown</div>", unsafe_allow_html=True)
    report_markdown = _report_text()
    st.text_area("周报内容预览", value=report_markdown, height=420)
    st.download_button(
        "下载企业交付周报 Markdown",
        data=report_markdown.encode("utf-8"),
        file_name="enterprise_delivery_weekly_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown("<div class='section'>导出建议</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card'><h3>给客户</h3><p>优先交付 Markdown 周报 + Proof Files CSV。</p></div>"
        "<div class='card'><h3>给内部运营</h3><p>导出完整 Excel，用于复盘训练质量、线索转化和审计追踪。</p></div>",
        unsafe_allow_html=True,
    )
