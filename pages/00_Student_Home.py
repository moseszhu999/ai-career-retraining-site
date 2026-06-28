from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Skill Growth · Student Home", page_icon="🎯", layout="wide")

CSS = """
<style>
.main .block-container{max-width:1180px;padding-top:1rem;padding-bottom:4rem}
.hero{border:1px solid #c7d2fe;border-radius:1.6rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 48%,#fff);padding:2rem;margin:1rem 0 1.2rem;box-shadow:0 18px 44px rgba(15,23,42,.08)}
.hero h1{font-size:2.55rem;line-height:1.06;margin:.45rem 0;color:#0f172a;font-weight:980}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p{color:#475569;line-height:1.75;font-size:1.02rem;max-width:900px}.eyebrow{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}
.pill{display:inline-block;border-radius:999px;padding:.28rem .64rem;font-size:.82rem;font-weight:900;border:1px solid #e2e8f0;background:#f8fafc;color:#475569;margin:.15rem .2rem .15rem 0}.hot{background:linear-gradient(90deg,#4f46e5,#06b6d4);border:none;color:white}.green{background:#dcfce7;color:#166534;border-color:#bbf7d0}.orange{background:#ffedd5;color:#9a3412;border-color:#fed7aa}.red{background:#fee2e2;color:#991b1b;border-color:#fecaca}.blue{background:#dbeafe;color:#1e40af;border-color:#bfdbfe}
.grid2{display:grid;grid-template-columns:1.2fr .8fr;gap:1rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card{border:1px solid #e2e8f0;border-radius:1.15rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045)}.card h3{margin:.15rem 0 .45rem;color:#111827}.card p{color:#64748b;line-height:1.58}.soft{background:#f8fafc;border-color:#dbeafe}.good{background:#f0fdf4;border-color:#bbf7d0}.warn{background:#fff7ed;border-color:#fed7aa}.bad{background:#fef2f2;border-color:#fecaca}.dark{background:#0f172a;color:#e2e8f0}.dark p,.dark div,.dark b{color:#cbd5e1}.metric{font-size:2rem;font-weight:950;color:#111827}.section-title{font-size:1.55rem;font-weight:950;margin:1.2rem 0 .35rem;color:#0f172a}.section-sub{color:#64748b;line-height:1.65;margin-bottom:.8rem}.task-card{border-left:5px solid #6366f1}.quote{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;line-height:1.65}.quote b{color:white}.progress-shell{height:.7rem;border-radius:999px;background:#e2e8f0;overflow:hidden}.progress-bar{height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4)}.timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem}.timeline div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.timeline b{display:block;color:#4f46e5}.mini{font-size:.86rem;color:#64748b;line-height:1.55}
@media(max-width:960px){.grid2,.grid3,.grid4,.timeline{grid-template-columns:1fr}.hero h1{font-size:2rem}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

DEMO_TASKS = [
    {"day": "Day 1", "title": "目标拆解", "status": "Agent已点评", "score": 86, "outcome": "5天成长路线图", "next": "可进入作品集"},
    {"day": "Day 2", "title": "测试用例作品", "status": "AI已反馈", "score": 64, "outcome": "测试用例 + Bug报告", "next": "补充权限、安全、边界"},
    {"day": "Day 3", "title": "复杂需求拆解", "status": "待Agent点评", "score": 0, "outcome": "流程 + 异常分支", "next": "等待Agent点评"},
    {"day": "Day 4", "title": "发表作品", "status": "未开始", "score": 0, "outcome": "3分钟发表稿", "next": "完成前序任务后开启"},
    {"day": "Day 5", "title": "30天行动计划", "status": "未开始", "score": 0, "outcome": "成长计划", "next": "完成作品后生成"},
]

STATUS_CLASS = {
    "Agent已点评": "green",
    "AI已反馈": "orange",
    "待Agent点评": "blue",
    "未开始": "",
    "需重训": "red",
}


def get_secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return default


def db_ready() -> bool:
    return bool(get_secret("SUPABASE_URL") and get_secret("SUPABASE_ANON_KEY"))


def supabase_client():
    from supabase import create_client
    return create_client(get_secret("SUPABASE_URL"), get_secret("SUPABASE_ANON_KEY"))


def load_student_tasks(student_name: str) -> pd.DataFrame:
    if not db_ready() or not student_name.strip():
        return pd.DataFrame(DEMO_TASKS)
    try:
        res = (
            supabase_client()
            .table("task_instances")
            .select("student, task_key, status, draft, ai_feedback, teacher_review, score, portfolio, risk, updated_at")
            .eq("student", student_name.strip())
            .order("updated_at", desc=True)
            .limit(100)
            .execute()
        )
        rows = res.data or []
        if not rows:
            return pd.DataFrame(DEMO_TASKS)
        mapped: list[dict[str, Any]] = []
        for i, row in enumerate(rows, start=1):
            mapped.append(
                {
                    "day": f"Task {i}",
                    "title": str(row.get("task_key") or "训练任务"),
                    "status": str(row.get("status") or "未开始"),
                    "score": int(row.get("score") or 0),
                    "outcome": "真实任务交付物",
                    "next": str(row.get("risk") or "继续完成下一步"),
                    "draft": str(row.get("draft") or ""),
                    "ai_feedback": str(row.get("ai_feedback") or ""),
                    "teacher_review": str(row.get("teacher_review") or ""),
                    "portfolio": bool(row.get("portfolio") or False),
                }
            )
        return pd.DataFrame(mapped)
    except Exception:
        return pd.DataFrame(DEMO_TASKS)


def chip(status: str) -> str:
    return f"<span class='pill {STATUS_CLASS.get(status, '')}'>{status}</span>"


def render_hero(student_name: str, df: pd.DataFrame) -> None:
    done = int(df["status"].isin(["Agent已点评", "已入作品集", "Agent质检通过"]).sum()) if "status" in df else 0
    total = max(len(df), 1)
    percent = int(done / total * 100)
    who = student_name.strip() or "演示学员"
    st.markdown(
        f"""
<div class='hero'>
<span class='eyebrow'>STUDENT HOME · v4.3.4</span>
<h1>{who}，今天继续完成<br><span>你的 AI 技能作品集</span></h1>
<p><b>这里不是课程后台，而是你的训练工作台。</b> 每天只看一个任务、一个交付物、一次 Agent 反馈、一个下一步。系统会自动沉淀你的作品集证据。</p>
<span class='pill hot'>我的任务</span><span class='pill'>Agent反馈</span><span class='pill'>作品集</span><span class='pill'>下一步</span>
<div style='margin-top:1rem'><div class='mini'>训练进度：{done}/{total} · {percent}%</div><div class='progress-shell'><div class='progress-bar' style='width:{percent}%'></div></div></div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_metrics(df: pd.DataFrame) -> None:
    total = len(df)
    done = int(df["status"].isin(["Agent已点评", "已入作品集", "Agent质检通过"]).sum()) if "status" in df else 0
    pending = int(df["status"].isin(["待Agent点评", "待老师点评", "AI已反馈", "已提交"]).sum()) if "status" in df else 0
    portfolio = int(df.get("portfolio", pd.Series([False] * total)).fillna(False).astype(bool).sum()) if total else 0
    for col, (num, label) in zip(st.columns(4), [(total, "训练任务"), (done, "已点评"), (pending, "待反馈"), (portfolio, "作品集")]):
        col.markdown(f"<div class='card'><div class='metric'>{num}</div><p>{label}</p></div>", unsafe_allow_html=True)


def render_timeline(df: pd.DataFrame) -> None:
    st.markdown("<div class='section-title'>训练路径</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>学员端只显示业务语言：任务、交付物、反馈、作品集。不显示数据库表名。</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='timeline'>"
        + "".join(
            f"<div><b>{row['day']}</b><span>{row['title']}</span><br>{chip(str(row['status']))}</div>"
            for _, row in df.head(5).iterrows()
        )
        + "</div>",
        unsafe_allow_html=True,
    )


def render_task_workspace(df: pd.DataFrame) -> None:
    left, right = st.columns([1.15, .85])
    with left:
        st.markdown("<div class='section-title'>今日任务</div>", unsafe_allow_html=True)
        labels = [f"{row['day']} · {row['title']} · {row['status']}" for _, row in df.iterrows()]
        selected = st.selectbox("选择任务", labels)
        row = df.iloc[labels.index(selected)]
        st.markdown(
            f"""
<div class='card task-card'>
<h3>{row['day']} · {row['title']}</h3>
<p><b>交付物：</b>{row['outcome']}<br><b>当前状态：</b>{chip(str(row['status']))}<br><b>下一步：</b>{row['next']}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        draft_default = str(row.get("draft", "")) or "目标：完成一个可展示作品\n步骤：列出任务、输出物、检查标准\n结果：提交第一版草稿\n风险：还需要补充证据和边界条件"
        st.text_area("作品草稿", value=draft_default, height=190)
        c1, c2, c3 = st.columns(3)
        c1.button("保存草稿", type="primary")
        c2.button("请求AI反馈")
        c3.button("提交给Agent老师")
    with right:
        st.markdown("<div class='section-title'>Agent反馈</div>", unsafe_allow_html=True)
        feedback = str(row.get("ai_feedback", "")) or str(row.get("teacher_review", ""))
        if not feedback:
            feedback = "【Agent反馈】\n你的任务已经有方向，但还需要补充：\n1. 明确交付物；\n2. 列出检查标准；\n3. 增加真实例子；\n4. 说明下一步如何修改。"
        st.markdown(f"<div class='quote'>{feedback}</div>", unsafe_allow_html=True)


def render_portfolio(df: pd.DataFrame) -> None:
    st.markdown("<div class='section-title'>作品集进度</div>", unsafe_allow_html=True)
    rows = []
    for _, row in df.iterrows():
        status = "可展示" if str(row.get("status")) in ["Agent已点评", "已入作品集", "Agent质检通过"] or bool(row.get("portfolio", False)) else "修改中"
        rows.append([row.get("title"), row.get("score", 0) or "--", status, row.get("outcome")])
    st.dataframe(pd.DataFrame(rows, columns=["作品", "评分", "状态", "证明材料"]), use_container_width=True, hide_index=True)


def render_founder_hint() -> None:
    st.markdown("<div class='section-title'>Founder OS 入口</div>", unsafe_allow_html=True)
    st.markdown(
        """
<div class='grid3'>
<div class='card good'><h3>🤖 Agent点评</h3><p>学员提交后，Agent 批量生成评分、结论、修改建议。</p></div>
<div class='card soft'><h3>✅ Agent质检</h3><p>检查低分、草稿过短、点评过短，把异常交给你。</p></div>
<div class='card warn'><h3>📈 Founder Daily</h3><p>你每天只看风险、作品集、重训和下一步运营建议。</p></div>
</div>
""",
        unsafe_allow_html=True,
    )
    page_link = getattr(st, "page_link", None)
    if page_link:
        st.page_link("pages/99_Founder_Agent_Console.py", label="打开 Founder Agent Console", icon="🤖")


with st.sidebar:
    st.markdown("### 学员首页模式")
    student_name = st.text_input("学员名", value="真实学员A")
    st.caption("如果 Supabase 中没有该学员，会自动显示演示数据。")
    st.markdown("---")
    st.caption("下一步：v4.4 再加 Owner-only / Student Login。")

tasks = load_student_tasks(student_name)
render_hero(student_name, tasks)
render_metrics(tasks)
render_timeline(tasks)
render_task_workspace(tasks)
render_portfolio(tasks)
render_founder_hint()

st.caption(f"AI Skill Growth Platform · Student Home v4.3.4 · {datetime.now().strftime('%Y-%m-%d')}")
