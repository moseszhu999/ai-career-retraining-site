from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Skill Growth · Product App", page_icon="🚀", layout="wide")

st.markdown(
    """
<style>
.main .block-container{max-width:1180px;padding-top:.8rem;padding-bottom:4rem}
.app-nav{position:sticky;top:.4rem;z-index:999;margin-bottom:1rem;border:1px solid #c7d2fe;border-radius:1.3rem;background:rgba(255,255,255,.96);box-shadow:0 14px 34px rgba(15,23,42,.08);padding:.78rem 1rem;display:flex;justify-content:space-between;align-items:center;gap:1rem}.brand{display:flex;gap:.6rem;align-items:center;font-weight:980;color:#111827}.logo{width:38px;height:38px;border-radius:14px;background:linear-gradient(135deg,#4f46e5,#06b6d4);color:white;display:grid;place-items:center}.brand small{display:block;color:#64748b;font-weight:850}.nav-note{display:flex;gap:.42rem;flex-wrap:wrap}.pill{display:inline-block;border-radius:999px;padding:.28rem .64rem;font-size:.82rem;font-weight:900;border:1px solid #e2e8f0;background:#f8fafc;color:#475569;margin:.15rem .2rem .15rem 0}.hot{background:linear-gradient(90deg,#4f46e5,#06b6d4);border:none;color:white}.green{background:#dcfce7;color:#166534;border-color:#bbf7d0}.orange{background:#ffedd5;color:#9a3412;border-color:#fed7aa}.red{background:#fee2e2;color:#991b1b;border-color:#fecaca}.blue{background:#dbeafe;color:#1e40af;border-color:#bfdbfe}
.nav-panel{margin:.7rem 0 1.1rem;padding:.55rem;border:1px solid #e0e7ff;border-radius:1.2rem;background:#f8fafc}div[data-testid='stRadio']>label{display:none}div[role='radiogroup']{display:flex;flex-wrap:wrap;gap:.45rem}div[role='radiogroup'] label{border:1px solid #dbeafe!important;border-radius:999px!important;background:white!important;padding:.42rem .85rem!important}div[role='radiogroup'] label p{font-weight:950!important;color:#334155!important;font-size:.93rem!important}div[role='radiogroup'] label:has(input:checked){background:linear-gradient(90deg,#4f46e5,#06b6d4)!important}div[role='radiogroup'] label:has(input:checked) p{color:white!important}
.hero{border:1px solid #c7d2fe;border-radius:1.6rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 48%,#fff);padding:2rem;margin:1rem 0 1.2rem;box-shadow:0 18px 44px rgba(15,23,42,.08)}.hero h1{font-size:2.55rem;line-height:1.06;margin:.45rem 0;color:#0f172a;font-weight:980}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p{color:#475569;line-height:1.75;font-size:1.02rem;max-width:900px}.eyebrow{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}.section-title{font-size:1.55rem;font-weight:950;margin:1.2rem 0 .35rem;color:#0f172a}.section-sub{color:#64748b;line-height:1.65;margin-bottom:.8rem}.grid2{display:grid;grid-template-columns:1.15fr .85fr;gap:1rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card{border:1px solid #e2e8f0;border-radius:1.15rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045)}.card h3{margin:.15rem 0 .45rem;color:#111827}.card p{color:#64748b;line-height:1.58}.soft{background:#f8fafc;border-color:#dbeafe}.good{background:#f0fdf4;border-color:#bbf7d0}.warn{background:#fff7ed;border-color:#fed7aa}.metric{font-size:2rem;font-weight:950;color:#111827}.quote{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;line-height:1.65}.timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem}.timeline div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.timeline b{display:block;color:#4f46e5}.progress-shell{height:.7rem;border-radius:999px;background:#e2e8f0;overflow:hidden}.progress-bar{height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4)}.mini{font-size:.86rem;color:#64748b;line-height:1.55}.task-card{border-left:5px solid #6366f1}
@media(max-width:960px){.app-nav{align-items:flex-start;flex-direction:column}.nav-note{display:none}.grid2,.grid3,.grid4,.timeline{grid-template-columns:1fr}.hero h1{font-size:2rem}}
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
        ["Day 1", "目标拆解", "Agent已点评", 86, "5天成长路线图", "可进入作品集"],
        ["Day 2", "测试用例作品", "AI已反馈", 64, "测试用例 + Bug报告", "补充权限、安全、边界"],
        ["Day 3", "复杂需求拆解", "待Agent点评", 0, "流程 + 异常分支", "等待Agent点评"],
        ["Day 4", "发表作品", "未开始", 0, "3分钟发表稿", "完成前序任务后开启"],
        ["Day 5", "30天行动计划", "未开始", 0, "成长计划", "完成作品后生成"],
    ],
    columns=["day", "title", "status", "score", "outcome", "next"],
)

STATUS_CLASS = {"Agent已点评": "green", "AI已反馈": "orange", "待Agent点评": "blue", "未开始": ""}


def chip(status: str) -> str:
    return f"<span class='pill {STATUS_CLASS.get(status, '')}'>{status}</span>"


def render_nav() -> str:
    st.markdown(
        """
<div class='app-nav'>
  <div class='brand'><div class='logo'>AI</div><div>AI Skill Growth<small>一人公司 · Agent OS · v4.3.6.1</small></div></div>
  <div class='nav-note'><span class='pill'>学员端</span><span class='pill'>任务卡</span><span class='pill'>Agent反馈</span><span class='pill hot'>作品集</span></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='nav-panel'>", unsafe_allow_html=True)
    page = st.radio("产品导航", list(PRODUCT_NAV.keys()), horizontal=True, format_func=lambda k: PRODUCT_NAV[k], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    return page


def render_home() -> None:
    done = 1
    total = 5
    pct = 20
    st.markdown(
        f"""
<div class='hero'>
<span class='eyebrow'>DEFAULT PRODUCT HOME</span>
<h1>每天完成一个任务，<br><span>自动沉淀一个作品集</span></h1>
<p><b>普通用户只需要看四个入口：</b>首页、我的任务、作品集、咨询。后台、SQL、SOP、运营看板、Founder Console 都不要放在普通导航里。</p>
<span class='pill hot'>我的任务</span><span class='pill'>Agent反馈</span><span class='pill'>作品集</span><span class='pill'>下一步</span>
<div style='margin-top:1rem'><div class='mini'>训练进度：{done}/{total} · {pct}%</div><div class='progress-shell'><div class='progress-bar' style='width:{pct}%'></div></div></div>
</div>
""",
        unsafe_allow_html=True,
    )
    cards = [
        ("🎯", "今天做什么", "系统只给一个主任务，避免学员被菜单和后台概念淹没。"),
        ("🤖", "怎么修改", "Agent 直接指出缺什么、怎么改、下一步交什么。"),
        ("📁", "留下什么", "每个通过任务都沉淀成作品集证据。"),
    ]
    st.markdown("<div class='grid3'>" + "".join(f"<div class='card'><h3>{i} {t}</h3><p>{b}</p></div>" for i, t, b in cards) + "</div>", unsafe_allow_html=True)


def render_tasks() -> None:
    st.markdown("<div class='section-title'>我的任务</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>这里只显示产品语言：任务、交付物、状态、下一步。不要显示 task_instances、reviews、RLS 这种后台词。</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='timeline'>"
        + "".join(f"<div><b>{r.day}</b><span>{r.title}</span><br>{chip(r.status)}</div>" for _, r in TASKS.iterrows())
        + "</div>",
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.15, .85])
    with left:
        labels = [f"{r.day} · {r.title}" for _, r in TASKS.iterrows()]
        label = st.selectbox("选择任务", labels, index=1)
        row = TASKS.iloc[labels.index(label)]
        st.markdown(
            f"""
<div class='card task-card'>
<h3>{row['day']} · {row['title']}</h3>
<p><b>交付物：</b>{row['outcome']}<br><b>状态：</b>{chip(row['status'])}<br><b>下一步：</b>{row['next']}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        st.text_area("作品草稿", value="目标：补齐登录页面测试能力\n步骤：列正常、异常、边界、安全场景\n输出：测试用例表 + Bug报告模板\n风险：还缺权限和SQL注入场景", height=190)
        c1, c2, c3 = st.columns(3)
        c1.button("保存草稿", type="primary")
        c2.button("请求AI反馈")
        c3.button("提交给Agent老师")
    with right:
        st.markdown("<div class='quote'>【Agent反馈】\n你的草稿方向正确，但还缺少：\n1. 权限差异；\n2. 边界值输入；\n3. SQL注入场景；\n4. 每条用例的预期结果。\n\n下一步：把每个测试点改成“前置条件 → 操作步骤 → 预期结果”。</div>", unsafe_allow_html=True)


def render_portfolio() -> None:
    st.markdown("<div class='section-title'>作品集</div>", unsafe_allow_html=True)
    rows = [
        ["目标拆解", "86", "可展示", "5天成长路线图"],
        ["测试用例作品", "64", "修改中", "测试用例 + Bug报告"],
        ["复杂需求拆解", "--", "待点评", "流程 + 异常分支"],
    ]
    st.dataframe(pd.DataFrame(rows, columns=["作品", "评分", "状态", "证明材料"]), use_container_width=True, hide_index=True)
    st.markdown("<div class='card good'><h3>作品集规则</h3><p>只有 Agent 已点评、质检通过，或者 Founder 手动确认的任务，才进入作品集。这样平台卖的是训练结果，不是课程时长。</p></div>", unsafe_allow_html=True)


def render_consult() -> None:
    st.markdown("<div class='section-title'>咨询</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>咨询页是转化入口，普通用户不需要看到报价后台，只需要知道适不适合自己。</div>", unsafe_allow_html=True)
    with st.form("consult_form_v4361"):
        name = st.text_input("姓名 / 称呼")
        identity = st.selectbox("你现在属于哪类人？", ["职场新人", "在岗提升", "升职准备", "转岗 / 跳槽", "自由职业 / 副业接单", "企业培训负责人", "小微老板"])
        goal = st.selectbox("你最想解决什么？", ["学新技能", "提升现有技能", "做作品集", "升职表达", "换工作 / 高薪跳槽", "自由职业接单", "企业内训"])
        note = st.text_area("补充说明")
        submitted = st.form_submit_button("生成咨询摘要")
    if submitted:
        summary = f"【咨询摘要】\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n姓名：{name or '未填写'}\n身份：{identity}\n目标：{goal}\n补充：{note or '无'}"
        st.markdown(f"<div class='quote'>{summary}</div>", unsafe_allow_html=True)
        st.download_button("下载咨询摘要", data=summary, file_name="consult_summary.txt", mime="text/plain")


def render_founder_backdoor() -> None:
    with st.expander("Founder / Owner 入口"):
        st.caption("普通用户导航不显示后台。Founder Console 继续单独 owner-gated。")
        st.info("请从左侧页面列表打开 Founder_Agent_Console / Student_Home / Product_App。此处不再使用 st.page_link，避免不同 Streamlit 版本或页面路径导致首页崩溃。")


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
st.caption("AI Skill Growth Platform · Default Product Home · v4.3.6.1")
