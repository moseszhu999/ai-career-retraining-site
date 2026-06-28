from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Skill Growth OS", page_icon="🚀", layout="wide")

st.markdown(
    """
<style>
.main .block-container{max-width:1180px;padding-top:.8rem;padding-bottom:4rem}
.app-nav{position:sticky;top:.35rem;z-index:999;margin-bottom:1rem;border:1px solid #c7d2fe;border-radius:1.35rem;background:rgba(255,255,255,.97);box-shadow:0 14px 34px rgba(15,23,42,.08);padding:.85rem 1rem;display:flex;justify-content:space-between;align-items:center;gap:1rem}.brand{display:flex;gap:.65rem;align-items:center;font-weight:980;color:#111827}.logo{width:40px;height:40px;border-radius:15px;background:linear-gradient(135deg,#4f46e5,#06b6d4);color:white;display:grid;place-items:center}.brand small{display:block;color:#64748b;font-weight:850}.nav-note{display:flex;gap:.42rem;flex-wrap:wrap}.pill{display:inline-block;border-radius:999px;padding:.3rem .68rem;font-size:.82rem;font-weight:900;border:1px solid #e2e8f0;background:#f8fafc;color:#475569;margin:.12rem .18rem .12rem 0}.hot{background:linear-gradient(90deg,#4f46e5,#06b6d4);border:none;color:white}.green{background:#dcfce7;color:#166534;border-color:#bbf7d0}.orange{background:#ffedd5;color:#9a3412;border-color:#fed7aa}.red{background:#fee2e2;color:#991b1b;border-color:#fecaca}.blue{background:#dbeafe;color:#1e40af;border-color:#bfdbfe}.purple{background:#ede9fe;color:#5b21b6;border-color:#ddd6fe}
.nav-panel{margin:.7rem 0 1.15rem;padding:.55rem;border:1px solid #e0e7ff;border-radius:1.2rem;background:#f8fafc}div[data-testid='stRadio']>label{display:none}div[role='radiogroup']{display:flex;flex-wrap:wrap;gap:.45rem}div[role='radiogroup'] label{border:1px solid #dbeafe!important;border-radius:999px!important;background:white!important;padding:.42rem .88rem!important}div[role='radiogroup'] label p{font-weight:950!important;color:#334155!important;font-size:.93rem!important}div[role='radiogroup'] label:has(input:checked){background:linear-gradient(90deg,#4f46e5,#06b6d4)!important}div[role='radiogroup'] label:has(input:checked) p{color:white!important}
.hero{border:1px solid #c7d2fe;border-radius:1.65rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 48%,#fff);padding:2rem;margin:1rem 0 1.2rem;box-shadow:0 18px 44px rgba(15,23,42,.08)}.hero h1{font-size:2.65rem;line-height:1.05;margin:.45rem 0;color:#0f172a;font-weight:980}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p{color:#475569;line-height:1.75;font-size:1.03rem;max-width:900px}.eyebrow{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}.section-title{font-size:1.55rem;font-weight:950;margin:1.25rem 0 .35rem;color:#0f172a}.section-sub{color:#64748b;line-height:1.65;margin-bottom:.8rem}.grid2{display:grid;grid-template-columns:1.12fr .88fr;gap:1rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card{border:1px solid #e2e8f0;border-radius:1.15rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045)}.card h3{margin:.15rem 0 .45rem;color:#111827}.card p{color:#64748b;line-height:1.58}.soft{background:#f8fafc;border-color:#dbeafe}.good{background:#f0fdf4;border-color:#bbf7d0}.warn{background:#fff7ed;border-color:#fed7aa}.metric{font-size:2rem;font-weight:950;color:#111827}.quote{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;line-height:1.65}.timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem}.timeline div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.timeline b{display:block;color:#4f46e5}.timeline span{display:block;font-size:.86rem;color:#475569;font-weight:850;margin:.15rem 0}.progress-shell{height:.7rem;border-radius:999px;background:#e2e8f0;overflow:hidden}.progress-bar{height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4)}.mini{font-size:.86rem;color:#64748b;line-height:1.55}.task-card{border-left:5px solid #6366f1}.system-line{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem;margin-top:1rem}.system-line div{background:white;border:1px solid #dbeafe;border-radius:1rem;padding:.9rem}.system-line b{display:block;color:#3730a3;margin-bottom:.2rem}.step{display:flex;gap:.65rem;align-items:flex-start;margin:.65rem 0}.num{min-width:28px;height:28px;border-radius:999px;background:#eef2ff;color:#3730a3;font-weight:950;display:grid;place-items:center}.proof{border:1px solid #e0e7ff;border-radius:1rem;padding:1rem;background:linear-gradient(180deg,#fff,#f8fafc)}.proof h3{margin:.1rem 0 .35rem;color:#111827}.proof p{color:#64748b}.package{border:1px solid #dbeafe;border-radius:1rem;padding:1rem;background:white}.package b{display:block;color:#0f172a;margin-bottom:.35rem}.owner-note{border:1px dashed #c7d2fe;background:#f8fafc;border-radius:1rem;padding:1rem;color:#475569;line-height:1.65}.workbench-head{border:1px solid #c7d2fe;border-radius:1.35rem;padding:1.2rem;background:linear-gradient(135deg,#ffffff,#eef2ff);margin:.8rem 0 1rem}.workbench-head h2{margin:.2rem 0;color:#0f172a;font-size:1.75rem}.workbench-head p{color:#475569;line-height:1.7}.focus-card{border:1px solid #c7d2fe;border-radius:1.2rem;background:white;padding:1rem;box-shadow:0 10px 24px rgba(79,70,229,.08)}.focus-card h3{margin:.1rem 0;color:#111827}.side-panel{border:1px solid #e2e8f0;border-radius:1.15rem;background:#f8fafc;padding:1rem}.standard-list{border:1px solid #e0e7ff;border-radius:1rem;background:white;padding:1rem}.next-box{border:1px solid #fed7aa;background:#fff7ed;border-radius:1rem;padding:1rem;color:#7c2d12;line-height:1.65}.action-box{border:1px solid #bbf7d0;background:#f0fdf4;border-radius:1rem;padding:1rem;color:#166534;line-height:1.65}.mode-tag{font-size:.78rem;font-weight:950;letter-spacing:.1em;color:#4f46e5;text-transform:uppercase}.portfolio-hero{border:1px solid #c7d2fe;border-radius:1.35rem;background:radial-gradient(circle at left,#ecfeff,#fff 55%);padding:1.25rem;margin:.8rem 0 1rem}.portfolio-hero h2{margin:.2rem 0;color:#0f172a;font-size:1.8rem}.portfolio-card{border:1px solid #e0e7ff;border-radius:1.15rem;background:white;padding:1rem;box-shadow:0 10px 24px rgba(15,23,42,.045);min-height:210px}.portfolio-card h3{margin:.15rem 0;color:#111827}.evidence-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem}.evidence{border:1px solid #e2e8f0;border-radius:1rem;background:#f8fafc;padding:.9rem}.evidence b{display:block;color:#0f172a;margin-bottom:.25rem}.score-ring{border-radius:1.2rem;border:1px solid #c7d2fe;background:linear-gradient(135deg,#eef2ff,#fff);padding:1rem;text-align:center}.score-ring .big{font-size:2.5rem;font-weight:980;color:#3730a3}.share-row{display:grid;grid-template-columns:repeat(3,1fr);gap:.65rem}.share-row div{border:1px dashed #c7d2fe;border-radius:1rem;background:#f8fafc;padding:.9rem;color:#475569}.review-box{border:1px solid #dbeafe;border-radius:1rem;background:white;padding:1rem;line-height:1.65;color:#475569}
@media(max-width:960px){.app-nav{align-items:flex-start;flex-direction:column}.nav-note{display:none}.grid2,.grid3,.grid4,.timeline,.system-line,.evidence-grid,.share-row{grid-template-columns:1fr}.hero h1{font-size:2rem}}
</style>
""",
    unsafe_allow_html=True,
)

PRODUCT_NAV = {
    "home": "首页",
    "tasks": "我的任务",
    "portfolio": "作品集",
    "consult": "咨询",
}

TASKS = pd.DataFrame(
    [
        ["Day 1", "目标拆解", "Agent已点评", 86, "5天成长路线图", "可进入作品集", 100, "已完成", "把目标拆成5天任务和可检查交付物"],
        ["Day 2", "测试用例作品", "AI已反馈", 64, "测试用例 + Bug报告", "补充权限、安全、边界", 70, "今日主任务", "围绕登录页面补齐测试用例和Bug报告模板"],
        ["Day 3", "复杂需求拆解", "待Agent点评", 0, "流程 + 异常分支", "等待Agent点评", 45, "等待点评", "把业务需求拆成角色、流程、输入输出和异常分支"],
        ["Day 4", "发表作品", "未开始", 0, "3分钟发表稿", "完成前序任务后开启", 0, "未解锁", "把作品整理成可发表、可面试、可汇报的表达"],
        ["Day 5", "30天行动计划", "未开始", 0, "成长计划", "完成作品后生成", 0, "未解锁", "根据前4天成果生成后续行动计划"],
    ],
    columns=["day", "title", "status", "score", "outcome", "next", "progress", "focus", "brief"],
)

PORTFOLIO = pd.DataFrame(
    [
        ["目标拆解", "5天成长路线图", "86", "可展示", "能说明目标、路径和交付物", "职业成长", "目标清晰、路径可执行、交付物可检查", "适合放入面试材料和培训前测报告"],
        ["测试用例作品", "测试用例 + Bug报告", "64", "修改中", "补齐权限、安全、边界后可展示", "软件测试", "已覆盖基础登录，缺少权限、安全和边界", "适合改造成软件测试入门作品"],
        ["复杂需求拆解", "流程 + 异常分支", "--", "待点评", "等待Agent正式点评", "业务分析", "已提交但尚未完成正式点评", "适合作为业务分析/测试分析作品候选"],
    ],
    columns=["作品", "证明材料", "评分", "状态", "说明", "方向", "Agent摘要", "展示建议"],
)

STATUS_CLASS = {"Agent已点评": "green", "AI已反馈": "orange", "待Agent点评": "blue", "未开始": "", "修改中": "orange", "可展示": "green", "待点评": "blue", "今日主任务": "purple", "已完成": "green", "等待点评": "blue", "未解锁": ""}


def chip(status: str) -> str:
    return f"<span class='pill {STATUS_CLASS.get(str(status), '')}'>{status}</span>"


def card(title: str, body: str, icon: str = "•", klass: str = "") -> str:
    return f"<div class='card {klass}'><h3>{icon} {title}</h3><p>{body}</p></div>"


def render_nav() -> str:
    st.markdown(
        """
<div class='app-nav'>
  <div class='brand'><div class='logo'>AI</div><div>AI Skill Growth OS<small>学员前台 · Agent反馈 · 作品集 · Founder后台</small></div></div>
  <div class='nav-note'><span class='pill'>页面优先</span><span class='pill'>学习工作台</span><span class='pill'>作品集详情</span><span class='pill hot'>v4.5.2 UI</span></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='nav-panel'>", unsafe_allow_html=True)
    page = st.radio("产品导航", list(PRODUCT_NAV.keys()), horizontal=True, format_func=lambda k: PRODUCT_NAV[k], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    return page


def render_home() -> None:
    done = 2
    total = 5
    pct = int(done / total * 100)
    st.markdown(
        f"""
<div class='hero'>
<span class='eyebrow'>PRODUCT FIRST · PAGE SPRINT</span>
<h1>让学员一打开就知道：<br><span>今天做什么，做到哪里，留下什么证明</span></h1>
<p><b>AI Skill Growth OS</b> 不是课程后台，而是任务驱动的成长产品。学员只需要完成任务、查看反馈、沉淀作品集；Founder 只处理异常、质检和高价值用户。</p>
<span class='pill hot'>继续今日任务</span><span class='pill'>查看Agent反馈</span><span class='pill'>生成作品集</span><span class='pill'>预约咨询</span>
<div style='margin-top:1rem'><div class='mini'>示例训练进度：{done}/{total} · {pct}%</div><div class='progress-shell'><div class='progress-bar' style='width:{pct}%'></div></div></div>
<div class='system-line'>
  <div><b>1. 首页</b><span>解释产品价值</span></div>
  <div><b>2. 我的任务</b><span>完成今日交付</span></div>
  <div><b>3. 作品集</b><span>沉淀证明材料</span></div>
  <div><b>4. 咨询</b><span>进入转化路径</span></div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>产品场景</div>", unsafe_allow_html=True)
    st.markdown("<div class='grid3'>" + "".join([
        card("个人成长", "适合职场新人、在岗提升、转岗跳槽。目标是每天完成一个可检查任务。", "🎯"),
        card("自由职业", "把技能变成服务包、样品案例、报价表达和可展示作品。", "💼"),
        card("一人公司", "Agent承担高频点评，Founder只看异常、质检、作品集候选和线索。", "🤖"),
    ]) + "</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>产品闭环</div>", unsafe_allow_html=True)
    st.markdown(
        """
<div class='grid4'>
  <div class='card soft'><h3>任务</h3><p>给用户一个明确的今日交付物。</p></div>
  <div class='card soft'><h3>反馈</h3><p>Agent指出缺口和下一步修改动作。</p></div>
  <div class='card soft'><h3>作品集</h3><p>通过任务沉淀成可展示证明。</p></div>
  <div class='card soft'><h3>咨询</h3><p>把成长需求转成付费线索。</p></div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_tasks() -> None:
    st.markdown(
        """
<div class='workbench-head'>
<span class='mode-tag'>MY TASKS WORKBENCH · PAGE FIRST</span>
<h2>今天只做一个任务：把草稿改成可检查作品</h2>
<p>这一页要让学员不用理解后台、不用找菜单，只知道：当前任务是什么、草稿写在哪里、Agent说要改什么、下一步点哪个按钮。</p>
</div>
""",
        unsafe_allow_html=True,
    )

    completed = int((TASKS["progress"] >= 100).sum())
    active = TASKS.iloc[1]
    pending = int((TASKS["status"] == "待Agent点评").sum())
    portfolio_ready = int((TASKS["status"] == "Agent已点评").sum())
    st.markdown(
        f"""
<div class='grid4'>
  <div class='card'><span class='mini'>当前任务</span><div class='metric'>{active['day']}</div><p>{active['title']}</p></div>
  <div class='card'><span class='mini'>已完成</span><div class='metric'>{completed}/5</div><p>至少一个结果可进入作品集。</p></div>
  <div class='card'><span class='mini'>等待点评</span><div class='metric'>{pending}</div><p>Founder后台未来只看这类异常/待处理。</p></div>
  <div class='card'><span class='mini'>作品候选</span><div class='metric'>{portfolio_ready}</div><p>高质量任务会进入作品集候选。</p></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>训练路径</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='timeline'>"
        + "".join(f"<div><b>{r['day']}</b><span>{r['title']}</span>{chip(r['focus'])}<div class='progress-shell'><div class='progress-bar' style='width:{int(r['progress'])}%'></div></div></div>" for _, r in TASKS.iterrows())
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>今日任务</div>", unsafe_allow_html=True)
    left, right = st.columns([1.15, .85])
    with left:
        labels = [f"{r['day']} · {r['title']}" for _, r in TASKS.iterrows()]
        label = st.selectbox("选择任务", labels, index=1)
        row = TASKS.iloc[labels.index(label)]
        st.markdown(
            f"""
<div class='focus-card'>
<h3>{row['day']} · {row['title']}</h3>
<p><b>任务说明：</b>{row['brief']}<br><b>交付物：</b>{row['outcome']}<br><b>状态：</b>{chip(row['status'])}<br><b>下一步：</b>{row['next']}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        draft = st.text_area(
            "作品草稿",
            value="目标：补齐登录页面测试能力\n\n当前草稿：\n1. 正常登录：输入正确用户名和密码，可以登录成功。\n2. 错误密码：提示密码错误。\n3. 空用户名：提示必须输入用户名。\n\n待补充：权限、安全、边界、Bug报告模板。",
            height=250,
        )
        st.caption(f"草稿字数：{len(draft)}。页面阶段仅做交互展示，后续接入保存到 Supabase。")
        c1, c2, c3 = st.columns(3)
        c1.button("保存草稿", type="primary")
        c2.button("请求AI反馈")
        c3.button("提交给Agent")

        st.markdown(
            """
<div class='action-box'>
<b>下一步行动</b><br>
先补齐“权限 / 安全 / 边界”三类测试点，再把每条测试点写成：前置条件 → 操作步骤 → 预期结果。
</div>
""",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("<div class='side-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Agent反馈预览</div>", unsafe_allow_html=True)
        st.markdown("<div class='quote'>【Agent反馈】\n你的草稿已经覆盖基础登录，但还不能成为作品集材料。\n\n优点：\n- 有正常和异常用例。\n- 能说明输入和预期。\n\n需要补充：\n1. 权限差异：普通用户/管理员/未授权用户。\n2. 安全场景：SQL注入、暴力尝试、锁定策略。\n3. 边界输入：超长用户名、特殊字符、空格。\n4. Bug报告模板：标题、步骤、实际结果、预期结果、严重度。\n\n建议：先补 6 条用例，再写 1 个Bug报告样例。</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>完成标准</div>", unsafe_allow_html=True)
        st.markdown(
            """
<div class='standard-list'>
<div class='step'><div class='num'>1</div><div><b>交付物明确</b><br><span class='mini'>能被别人打开检查，不是一句学习感想。</span></div></div>
<div class='step'><div class='num'>2</div><div><b>覆盖三类风险</b><br><span class='mini'>权限、安全、边界至少各有一个测试点。</span></div></div>
<div class='step'><div class='num'>3</div><div><b>表达可展示</b><br><span class='mini'>最终结果可以解释给面试官、客户或上级。</span></div></div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class='next-box'>
<b>页面设计意图</b><br>
右侧只放反馈、标准和下一步，不放后台数据。学员看到的是产品动作，不是数据库字段。
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_portfolio() -> None:
    approved = int((PORTFOLIO["状态"] == "可展示").sum())
    editing = int((PORTFOLIO["状态"] == "修改中").sum())
    pending = int((PORTFOLIO["状态"] == "待点评").sum())
    st.markdown(
        f"""
<div class='portfolio-hero'>
<span class='mode-tag'>PORTFOLIO PROOF PAGE · PAGE FIRST</span>
<h2>作品集不是任务列表，而是可展示证明</h2>
<p>这一页要让学员看到：哪些成果可以展示，为什么可以展示，还差什么，未来如何导出给面试官、客户或上级。</p>
<div class='grid4'>
  <div class='card'><span class='mini'>可展示</span><div class='metric'>{approved}</div><p>已经可以作为成长证明。</p></div>
  <div class='card'><span class='mini'>修改中</span><div class='metric'>{editing}</div><p>有价值，但还需要补强。</p></div>
  <div class='card'><span class='mini'>待点评</span><div class='metric'>{pending}</div><p>等待Agent或Founder确认。</p></div>
  <div class='card'><span class='mini'>导出能力</span><div class='metric'>Soon</div><p>后续支持PDF/分享链接。</p></div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>作品卡片</div>", unsafe_allow_html=True)
    cards_html = "<div class='grid3'>"
    for _, row in PORTFOLIO.iterrows():
        cards_html += f"""
<div class='portfolio-card'>
<h3>{row['作品']}</h3>
{chip(row['状态'])}<span class='pill purple'>{row['方向']}</span>
<p><b>证明材料：</b>{row['证明材料']}</p>
<p><b>评分：</b>{row['评分']}</p>
<p>{row['说明']}</p>
</div>
"""
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>作品详情</div>", unsafe_allow_html=True)
    selected = st.selectbox("选择一个作品查看详情", PORTFOLIO["作品"].tolist(), index=0)
    row = PORTFOLIO[PORTFOLIO["作品"] == selected].iloc[0]
    left, right = st.columns([1.15, .85])
    with left:
        st.markdown(
            f"""
<div class='focus-card'>
<h3>{row['作品']}</h3>
<p><b>方向：</b>{row['方向']}　{chip(row['状态'])}</p>
<p><b>证明材料：</b>{row['证明材料']}</p>
<p><b>展示建议：</b>{row['展示建议']}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
<div class='review-box'>
<b>Agent点评摘要</b><br>
{row['Agent摘要']}。<br><br>
<b>改进方向</b><br>
如果要成为更强的作品集材料，需要补充“背景 → 方法 → 结果 → 证据 → 复盘”。
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='section-title'>证明材料结构</div>", unsafe_allow_html=True)
        st.markdown(
            """
<div class='evidence-grid'>
  <div class='evidence'><b>背景</b><span class='mini'>为什么做这个任务，解决什么问题。</span></div>
  <div class='evidence'><b>方法</b><span class='mini'>你如何拆解、分析、设计或测试。</span></div>
  <div class='evidence'><b>结果</b><span class='mini'>最终产出了什么可检查材料。</span></div>
  <div class='evidence'><b>复盘</b><span class='mini'>Agent指出了什么，你如何改进。</span></div>
</div>
""",
            unsafe_allow_html=True,
        )
    with right:
        score_display = row["评分"] if row["评分"] != "--" else "待定"
        st.markdown(
            f"""
<div class='score-ring'>
<span class='mini'>作品评分</span>
<div class='big'>{score_display}</div>
<p>{row['状态']}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='section-title'>可展示检查</div>", unsafe_allow_html=True)
        st.markdown(
            """
<div class='standard-list'>
<div class='step'><div class='num'>1</div><div><b>别人能看懂</b><br><span class='mini'>不是内部笔记，而是可解释成果。</span></div></div>
<div class='step'><div class='num'>2</div><div><b>有证据</b><br><span class='mini'>有表格、文档、案例或截图支撑。</span></div></div>
<div class='step'><div class='num'>3</div><div><b>可复用</b><br><span class='mini'>能用于面试、汇报、客户样品或咨询转化。</span></div></div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-title'>导出 / 分享占位</div>", unsafe_allow_html=True)
    st.markdown(
        """
<div class='share-row'>
  <div><b>导出PDF</b><br><span class='mini'>后续生成作品集PDF。</span></div>
  <div><b>生成分享链接</b><br><span class='mini'>后续给面试官或客户查看。</span></div>
  <div><b>加入咨询材料</b><br><span class='mini'>后续把作品用于转化和销售。</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>作品集规则</div>", unsafe_allow_html=True)
    st.markdown(
        """
<div class='grid3'>
  <div class='card good'><h3>进入条件</h3><p>Agent已点评、评分达标、Founder或规则确认。</p></div>
  <div class='card warn'><h3>修改中</h3><p>有价值但还缺边界、表达或证明材料。</p></div>
  <div class='card soft'><h3>未来能力</h3><p>导出PDF、分享链接、面试作品包、客户样品页。</p></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.dataframe(PORTFOLIO, use_container_width=True, hide_index=True)


def render_consult() -> None:
    st.markdown("<div class='section-title'>咨询</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>咨询页先做成转化页面：识别用户身份、目标和痛点，生成咨询摘要。后续再保存到 consult_leads。</div>", unsafe_allow_html=True)

    st.markdown(
        """
<div class='grid3'>
  <div class='package'><b>个人成长版</b><span class='mini'>适合职场新人、在岗提升、转岗跳槽。</span></div>
  <div class='package'><b>自由职业版</b><span class='mini'>适合把技能包装成服务和样品案例。</span></div>
  <div class='package'><b>企业训练版</b><span class='mini'>适合部门新人训练、AI任务标准化。</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.form("consult_form_v452_pages"):
        name = st.text_input("姓名 / 称呼")
        contact = st.text_input("联系方式，选填")
        identity = st.selectbox("你现在属于哪类人？", ["职场新人", "在岗提升", "升职准备", "转岗 / 跳槽", "自由职业 / 副业接单", "企业培训负责人", "小微老板"])
        goal = st.selectbox("你最想解决什么？", ["学新技能", "提升现有技能", "做作品集", "升职表达", "换工作 / 高薪跳槽", "自由职业接单", "企业内训"])
        note = st.text_area("补充说明")
        submitted = st.form_submit_button("生成咨询摘要")

    if submitted:
        summary = f"【咨询摘要】\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n姓名：{name or '未填写'}\n联系方式：{contact or '未填写'}\n身份：{identity}\n目标：{goal}\n补充：{note or '无'}\n\n建议路径：先完成5天任务闭环，产出至少1个可展示作品，再判断是否进入长期训练或服务包装。"
        st.markdown(f"<div class='quote'>{summary}</div>", unsafe_allow_html=True)
        st.download_button("下载咨询摘要", data=summary, file_name="consult_summary.txt", mime="text/plain")


def render_founder_backdoor() -> None:
    with st.expander("Founder OS / 后台入口"):
        st.markdown(
            """
<div class='owner-note'>
普通用户前台只保留四个入口。Founder Console 是唯一后台页，继续单独 owner-gated。<br>
当前页面阶段不使用 st.page_link，避免 Streamlit 页面路径导致首页崩溃。需要进入后台时，从左侧页面列表打开 Founder_Agent_Console。
</div>
""",
            unsafe_allow_html=True,
        )


page = render_nav()
if page == "home":
    render_home()
elif page == "tasks":
    render_tasks()
elif page == "portfolio":
    render_portfolio()
else:
    render_consult()

render_founder_backdoor()
st.caption("AI Skill Growth OS · Portfolio Proof Page · v4.5.2")
