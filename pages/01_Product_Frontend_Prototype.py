from __future__ import annotations

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Product Frontend Prototype", page_icon="✨", layout="wide")

st.markdown(
    """
<style>
.main .block-container{max-width:1180px;padding-top:1rem;padding-bottom:4rem}
.hero{border:1px solid #c7d2fe;border-radius:1.6rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 48%,#fff);padding:2rem;margin:1rem 0 1.2rem;box-shadow:0 18px 44px rgba(15,23,42,.08)}
.hero h1{font-size:2.75rem;line-height:1.05;margin:.5rem 0;color:#0f172a;font-weight:980}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p{color:#475569;line-height:1.75;font-size:1.02rem;max-width:900px}.eyebrow{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}
.pill,.status{display:inline-block;border-radius:999px;padding:.28rem .64rem;font-size:.82rem;font-weight:900;border:1px solid #e2e8f0;background:#f8fafc;color:#475569;margin:.15rem .2rem .15rem 0}.pill.hot{background:linear-gradient(90deg,#4f46e5,#06b6d4);border:none;color:white}.pill.green{background:#dcfce7;color:#166534;border-color:#bbf7d0}.pill.orange{background:#ffedd5;color:#9a3412;border-color:#fed7aa}.pill.red{background:#fee2e2;color:#991b1b;border-color:#fecaca}
.section-title{font-size:1.55rem;font-weight:950;margin:1.2rem 0 .35rem;color:#0f172a}.section-sub{color:#64748b;line-height:1.65;margin-bottom:.8rem}.grid2{display:grid;grid-template-columns:1.15fr .85fr;gap:1rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.9rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card{border:1px solid #e2e8f0;border-radius:1.15rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045)}.card h3{margin:.15rem 0 .45rem;color:#111827}.card p{color:#64748b;line-height:1.58}.soft{background:#f8fafc;border-color:#dbeafe}.green{background:#f0fdf4;border-color:#bbf7d0}.orange{background:#fff7ed;border-color:#fed7aa}.dark{background:#0f172a;color:#e2e8f0}.dark p,.dark div{color:#cbd5e1}.metric{font-size:2rem;font-weight:950;color:#111827}.task{border-left:5px solid #6366f1}.timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem}.timeline div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.timeline b{display:block;color:#4f46e5}.quote{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;line-height:1.65}
@media(max-width:960px){.grid2,.grid3,.grid4,.timeline{grid-template-columns:1fr}.hero h1{font-size:2.1rem}}
</style>
""",
    unsafe_allow_html=True,
)

TASKS = pd.DataFrame(
    [
        {"day": "Day 1", "title": "目标拆解", "status": "Agent已点评", "score": 86, "outcome": "5天成长路线图", "risk": "正常"},
        {"day": "Day 2", "title": "测试用例作品", "status": "AI已反馈", "score": 64, "outcome": "测试用例 + Bug报告", "risk": "需补边界"},
        {"day": "Day 3", "title": "复杂需求拆解", "status": "待Agent点评", "score": 0, "outcome": "流程 + 异常分支", "risk": "等待点评"},
        {"day": "Day 4", "title": "发表作品", "status": "未开始", "score": 0, "outcome": "3分钟发表稿", "risk": "等待"},
        {"day": "Day 5", "title": "30天行动计划", "status": "未开始", "score": 0, "outcome": "成长计划", "risk": "等待"},
    ]
)

STATUS_CLASS = {
    "Agent已点评": "green",
    "AI已反馈": "orange",
    "待Agent点评": "orange",
    "未开始": "",
}


def status_chip(text: str) -> str:
    cls = STATUS_CLASS.get(text, "")
    return f"<span class='pill {cls}'>{text}</span>"


def render_hero() -> None:
    st.markdown(
        """
<div class='hero'>
<span class='eyebrow'>PRODUCT FRONTEND SPRINT · v4.3.3</span>
<h1>把 AI 训练平台做成<br><span>用户一眼能懂的产品</span></h1>
<p><b>定位：一人公司 + AI Agent 教育系统。</b> 用户看到的是清晰路径、任务卡、Agent反馈、作品集进度；你看到的是待处理、风险、质检和日报。不是请老师交付，而是 Agent OS 承担高频运营。</p>
<span class='pill hot'>Student Journey</span><span class='pill'>Agent Teacher</span><span class='pill'>Portfolio</span><span class='pill'>Founder OS</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_value_metrics() -> None:
    cols = st.columns(4)
    values = [("5", "天训练路径"), ("3", "个作品集证据"), ("2", "轮Agent反馈"), ("1", "个Founder控制台")]
    for col, (num, label) in zip(cols, values):
        col.markdown(f"<div class='card'><div class='metric'>{num}</div><p>{label}</p></div>", unsafe_allow_html=True)


def render_student_journey() -> None:
    st.markdown("<div class='section-title'>学员端：不用懂系统，只要按任务往前走</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>前端重点不是展示数据库，而是让学员知道：我今天做什么、交什么、怎么改、最后能沉淀什么作品。</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='timeline'>"
        + "".join(
            f"<div><b>{row.day}</b><span>{row.title}</span><br>{status_chip(row.status)}</div>"
            for _, row in TASKS.iterrows()
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown("### 今日任务卡")
        selected = st.selectbox("选择任务", TASKS["title"].tolist(), index=1)
        row = TASKS[TASKS["title"] == selected].iloc[0]
        st.markdown(
            f"""
<div class='card task'>
<h3>{row['day']} · {row['title']}</h3>
<p><b>交付物：</b>{row['outcome']}<br><b>当前状态：</b>{status_chip(row['status'])}<br><b>风险：</b>{row['risk']}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        draft = st.text_area(
            "作品草稿",
            value="目标：补齐登录页面测试能力\n步骤：先列正常、异常、边界、安全场景\n输出：测试用例表 + Bug报告模板\n风险：还缺少权限和SQL注入场景",
            height=180,
        )
        c1, c2, c3 = st.columns(3)
        c1.button("保存草稿", type="primary")
        c2.button("请求AI反馈")
        c3.button("提交给Agent老师")
    with right:
        st.markdown("### Agent 即时反馈")
        st.markdown(
            """
<div class='quote'>【AI反馈】
你的草稿已经有目标和步骤，但还缺少：
1. 边界值输入；
2. 权限差异；
3. 安全测试；
4. 预期结果字段。

下一步：把每个测试点改成“前置条件 → 操作步骤 → 预期结果”。</div>
""",
            unsafe_allow_html=True,
        )


def render_agent_and_founder() -> None:
    st.markdown("<div class='section-title'>Founder视角：你只处理方向、异常和产品迭代</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>前端要把你的工作压缩成几个明确按钮：运行点评、运行质检、看日报、处理风险。</div>", unsafe_allow_html=True)
    cards = [
        ("🤖", "Agent点评队列", "待Agent点评 3 条；点击后批量生成评分、结论、修改建议。", "green"),
        ("✅", "Agent质检队列", "待质检 2 条；检查点评是否过短、低分、草稿过短。", "soft"),
        ("📈", "Founder Daily", "今日风险、作品集数量、重训任务、下一步运营建议。", "orange"),
    ]
    st.markdown(
        "<div class='grid3'>"
        + "".join(f"<div class='card {cls}'><h3>{icon} {title}</h3><p>{body}</p></div>" for icon, title, body, cls in cards)
        + "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1])
    with left:
        st.markdown("### Founder Daily 预览")
        st.markdown(
            """
<div class='quote'>【Founder Daily】
任务总数：5
待Agent点评：1
待Agent质检：1
需关注：1

今日建议：
1. 先处理 Day 3 待点评；
2. Day 2 需要补安全与权限边界；
3. 暂时不要增加真人交付，继续强化Agent闭环。</div>
""",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("### 作品集前台展示")
        portfolio = pd.DataFrame(
            [
                ["目标拆解", "86", "可展示", "成长路线图"],
                ["测试用例作品", "64", "修改中", "测试用例 + Bug报告"],
                ["复杂需求拆解", "--", "待点评", "流程图 + 异常分支"],
            ],
            columns=["作品", "评分", "状态", "证明材料"],
        )
        st.dataframe(portfolio, use_container_width=True, hide_index=True)


def render_product_rules() -> None:
    st.markdown("<div class='section-title'>前端产品规则</div>", unsafe_allow_html=True)
    rules = [
        ("少给菜单", "普通用户最多看到：首页、我的任务、作品集、咨询入口。"),
        ("强任务卡", "每个任务都必须有交付物、标准、按钮、反馈、下一步。"),
        ("弱后台感", "不要让学员看到 courses / task_instances / reviews 这种数据库语言。"),
        ("老板视角独立", "Founder Console 是后台，不和学员端混在一起。"),
    ]
    st.markdown(
        "<div class='grid4'>" + "".join(f"<div class='card'><h3>{a}</h3><p>{b}</p></div>" for a, b in rules) + "</div>",
        unsafe_allow_html=True,
    )


render_hero()
render_value_metrics()
render_student_journey()
render_agent_and_founder()
render_product_rules()

st.caption("AI Skill Growth Platform · Product Frontend Prototype · v4.3.3")
