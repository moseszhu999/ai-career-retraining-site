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
.hero{border:1px solid #c7d2fe;border-radius:1.65rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 48%,#fff);padding:2rem;margin:1rem 0 1.2rem;box-shadow:0 18px 44px rgba(15,23,42,.08)}.hero h1{font-size:2.65rem;line-height:1.05;margin:.45rem 0;color:#0f172a;font-weight:980}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p{color:#475569;line-height:1.75;font-size:1.03rem;max-width:900px}.eyebrow{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}.section-title{font-size:1.55rem;font-weight:950;margin:1.25rem 0 .35rem;color:#0f172a}.section-sub{color:#64748b;line-height:1.65;margin-bottom:.8rem}.grid2{display:grid;grid-template-columns:1.12fr .88fr;gap:1rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card{border:1px solid #e2e8f0;border-radius:1.15rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045)}.card h3{margin:.15rem 0 .45rem;color:#111827}.card p{color:#64748b;line-height:1.58}.soft{background:#f8fafc;border-color:#dbeafe}.good{background:#f0fdf4;border-color:#bbf7d0}.warn{background:#fff7ed;border-color:#fed7aa}.metric{font-size:2rem;font-weight:950;color:#111827}.quote{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;line-height:1.65}.timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem}.timeline div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.timeline b{display:block;color:#4f46e5}.timeline span{display:block;font-size:.86rem;color:#475569;font-weight:850;margin:.15rem 0}.progress-shell{height:.7rem;border-radius:999px;background:#e2e8f0;overflow:hidden}.progress-bar{height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4)}.mini{font-size:.86rem;color:#64748b;line-height:1.55}.task-card{border-left:5px solid #6366f1}.system-line{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem;margin-top:1rem}.system-line div{background:white;border:1px solid #dbeafe;border-radius:1rem;padding:.9rem}.system-line b{display:block;color:#3730a3;margin-bottom:.2rem}.step{display:flex;gap:.65rem;align-items:flex-start;margin:.65rem 0}.num{min-width:28px;height:28px;border-radius:999px;background:#eef2ff;color:#3730a3;font-weight:950;display:grid;place-items:center}.proof{border:1px solid #e0e7ff;border-radius:1rem;padding:1rem;background:linear-gradient(180deg,#fff,#f8fafc)}.proof h3{margin:.1rem 0 .35rem;color:#111827}.proof p{color:#64748b}.package{border:1px solid #dbeafe;border-radius:1rem;padding:1rem;background:white}.package b{display:block;color:#0f172a;margin-bottom:.35rem}.owner-note{border:1px dashed #c7d2fe;background:#f8fafc;border-radius:1rem;padding:1rem;color:#475569;line-height:1.65}
@media(max-width:960px){.app-nav{align-items:flex-start;flex-direction:column}.nav-note{display:none}.grid2,.grid3,.grid4,.timeline,.system-line{grid-template-columns:1fr}.hero h1{font-size:2rem}}
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
        ["Day 1", "目标拆解", "Agent已点评", 86, "5天成长路线图", "可进入作品集", 100],
        ["Day 2", "测试用例作品", "AI已反馈", 64, "测试用例 + Bug报告", "补充权限、安全、边界", 70],
        ["Day 3", "复杂需求拆解", "待Agent点评", 0, "流程 + 异常分支", "等待Agent点评", 45],
        ["Day 4", "发表作品", "未开始", 0, "3分钟发表稿", "完成前序任务后开启", 0],
        ["Day 5", "30天行动计划", "未开始", 0, "成长计划", "完成作品后生成", 0],
    ],
    columns=["day", "title", "status", "score", "outcome", "next", "progress"],
)

PORTFOLIO = pd.DataFrame(
    [
        ["目标拆解", "5天成长路线图", "86", "可展示", "能说明目标、路径和交付物"],
        ["测试用例作品", "测试用例 + Bug报告", "64", "修改中", "补齐权限、安全、边界后可展示"],
        ["复杂需求拆解", "流程 + 异常分支", "--", "待点评", "等待Agent正式点评"],
    ],
    columns=["作品", "证明材料", "评分", "状态", "说明"],
)

STATUS_CLASS = {"Agent已点评": "green", "AI已反馈": "orange", "待Agent点评": "blue", "未开始": "", "修改中": "orange", "可展示": "green", "待点评": "blue"}


def chip(status: str) -> str:
    return f"<span class='pill {STATUS_CLASS.get(str(status), '')}'>{status}</span>"


def card(title: str, body: str, icon: str = "•", klass: str = "") -> str:
    return f"<div class='card {klass}'><h3>{icon} {title}</h3><p>{body}</p></div>"


def render_nav() -> str:
    st.markdown(
        """
<div class='app-nav'>
  <div class='brand'><div class='logo'>AI</div><div>AI Skill Growth OS<small>学员前台 · Agent反馈 · 作品集 · Founder后台</small></div></div>
  <div class='nav-note'><span class='pill'>页面优先</span><span class='pill'>任务卡</span><span class='pill'>作品集</span><span class='pill hot'>v4.5 UI</span></div>
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
    st.markdown("<div class='section-title'>我的任务</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>页面阶段先用示例数据，先把任务卡、反馈区、操作按钮和下一步说明做清楚。后续 v4.5 再接 Supabase。</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='timeline'>"
        + "".join(f"<div><b>{r['day']}</b><span>{r['title']}</span>{chip(r['status'])}<div class='progress-shell'><div class='progress-bar' style='width:{int(r['progress'])}%'></div></div></div>" for _, r in TASKS.iterrows())
        + "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.12, .88])
    with left:
        labels = [f"{r['day']} · {r['title']}" for _, r in TASKS.iterrows()]
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
        st.text_area(
            "作品草稿",
            value="目标：补齐登录页面测试能力\n步骤：列正常、异常、边界、安全场景\n输出：测试用例表 + Bug报告模板\n风险：还缺权限和SQL注入场景",
            height=210,
        )
        c1, c2, c3 = st.columns(3)
        c1.button("保存草稿", type="primary")
        c2.button("请求AI反馈")
        c3.button("提交给Agent")

    with right:
        st.markdown("<div class='quote'>【Agent反馈预览】\n你的草稿方向正确，但还缺少：\n1. 权限差异；\n2. 边界值输入；\n3. SQL注入场景；\n4. 每条用例的预期结果。\n\n下一步：把每个测试点改成“前置条件 → 操作步骤 → 预期结果”。</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>完成标准</div>", unsafe_allow_html=True)
        st.markdown(
            """
<div class='card'>
<div class='step'><div class='num'>1</div><div><b>交付物明确</b><br><span class='mini'>能被别人打开检查，而不是一句感想。</span></div></div>
<div class='step'><div class='num'>2</div><div><b>覆盖边界</b><br><span class='mini'>正常、异常、权限、安全、边界至少覆盖三类。</span></div></div>
<div class='step'><div class='num'>3</div><div><b>可进入作品集</b><br><span class='mini'>最终结果可以解释给面试官、客户或上级。</span></div></div>
</div>
""",
            unsafe_allow_html=True,
        )


def render_portfolio() -> None:
    st.markdown("<div class='section-title'>作品集</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>作品集不是任务列表，而是“可展示证明”。页面阶段先展示卡片形态和状态口径。</div>", unsafe_allow_html=True)

    st.markdown("<div class='grid3'>", unsafe_allow_html=True)
    for _, row in PORTFOLIO.iterrows():
        st.markdown(
            f"""
<div class='proof'>
<h3>{row['作品']}</h3>
<p><b>证明材料：</b>{row['证明材料']}</p>
<p><b>评分：</b>{row['评分']}　<b>状态：</b>{chip(row['状态'])}</p>
<p>{row['说明']}</p>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

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

    with st.form("consult_form_v45_pages"):
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
st.caption("AI Skill Growth OS · Page First Sprint · v4.5")
