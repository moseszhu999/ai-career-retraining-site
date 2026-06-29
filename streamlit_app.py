from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Skill Growth OS", page_icon="🚀", layout="wide")

st.markdown(
    """
<style>
.main .block-container{max-width:1180px;padding-top:.7rem;padding-bottom:4rem}.site-top{border:1px solid #dbeafe;border-radius:1.25rem;background:rgba(255,255,255,.96);box-shadow:0 12px 30px rgba(15,23,42,.06);padding:.9rem 1rem;margin:.3rem 0 1rem;display:flex;justify-content:space-between;gap:1rem;align-items:center}.brand{font-size:1.18rem;font-weight:980;color:#0f172a}.brand small{display:block;color:#64748b;font-size:.82rem;font-weight:850}.landing-nav{display:flex;gap:.55rem;flex-wrap:wrap;align-items:center}.pill{display:inline-block;border-radius:999px;padding:.28rem .64rem;font-size:.8rem;font-weight:900;border:1px solid #e2e8f0;background:#f8fafc;color:#475569;margin:.1rem .16rem}.hot{background:linear-gradient(90deg,#4f46e5,#06b6d4);border:none;color:white}.green{background:#dcfce7;color:#166534;border-color:#bbf7d0}.orange{background:#ffedd5;color:#9a3412;border-color:#fed7aa}.blue{background:#dbeafe;color:#1e40af;border-color:#bfdbfe}.purple{background:#ede9fe;color:#5b21b6;border-color:#ddd6fe}.hero{border:1px solid #c7d2fe;border-radius:1.5rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 45%,#fff);padding:2rem;margin:.8rem 0 1rem}.hero h1{font-size:2.55rem;line-height:1.06;margin:.25rem 0;color:#0f172a}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p{max-width:860px;color:#475569;line-height:1.75;font-size:1.03rem}.section{font-size:1.45rem;font-weight:950;margin:1.2rem 0 .45rem;color:#0f172a}.grid2{display:grid;grid-template-columns:1.05fr .95fr;gap:1rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card{border:1px solid #e2e8f0;border-radius:1.1rem;background:white;padding:1rem;box-shadow:0 8px 20px rgba(15,23,42,.04)}.card h3{margin:.1rem 0 .45rem;color:#111827}.card p{color:#64748b;line-height:1.58}.metric{font-size:2rem;font-weight:980;color:#0f172a}.panel{border:1px solid #dbeafe;border-radius:1.2rem;background:linear-gradient(135deg,#fff,#f8fafc);padding:1.1rem;margin:.9rem 0}.panel h2{margin:.15rem 0;color:#0f172a}.quote{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;line-height:1.65}.progress{height:.65rem;border-radius:999px;background:#e2e8f0;overflow:hidden;margin-top:.45rem}.bar{height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4)}.ok{border:1px solid #bbf7d0;background:#f0fdf4;color:#166534;border-radius:1rem;padding:1rem}.warn{border:1px solid #fed7aa;background:#fff7ed;color:#7c2d12;border-radius:1rem;padding:1rem}.mini{font-size:.85rem;color:#64748b;line-height:1.55}.proof{border:1px solid #e0e7ff;border-radius:1rem;background:white;padding:1rem}.decision{border-left:5px solid #6366f1}.task-shell{display:grid;grid-template-columns:.85fr 1.35fr .95fr;gap:1rem;align-items:start}.task-rail,.portfolio-list,.funnel-panel{border:1px solid #e0e7ff;border-radius:1.1rem;background:#f8fafc;padding:.85rem}.task-mini,.portfolio-mini{border:1px solid #e2e8f0;border-radius:1rem;background:white;padding:.85rem;margin:.55rem 0}.task-mini.active,.portfolio-mini.active{border-color:#6366f1;box-shadow:0 8px 20px rgba(99,102,241,.12)}.task-mini b,.portfolio-mini b{display:block;color:#0f172a}.editor-panel,.portfolio-detail,.plan-card{border:1px solid #c7d2fe;border-radius:1.2rem;background:white;padding:1rem;box-shadow:0 10px 24px rgba(79,70,229,.06)}.side-stack{display:grid;gap:.85rem}.history{border:1px solid #e2e8f0;border-radius:1rem;background:white;padding:.9rem;max-height:260px;overflow:auto}.history-item{border-bottom:1px solid #f1f5f9;padding:.55rem 0;color:#475569}.history-item:last-child{border-bottom:none}.toolbar{display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem}.result-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem;margin:1rem 0}.result-strip div{border:1px solid #dbeafe;border-radius:1rem;background:white;padding:1rem}.flow-step{border:1px solid #e0e7ff;border-radius:1rem;background:#fff;padding:1rem}.flow-step b{display:block;color:#3730a3;margin-bottom:.35rem}.faq{border:1px solid #e2e8f0;border-radius:1rem;background:#fff;padding:1rem;margin:.55rem 0}.login-box{position:sticky;top:1rem}.trust-row,.hero-actions{display:flex;gap:.5rem;flex-wrap:wrap;margin:.75rem 0}.demo-window{border:1px solid #c7d2fe;border-radius:1.2rem;background:#0f172a;color:#e2e8f0;padding:1rem;line-height:1.7}.portfolio-shell{display:grid;grid-template-columns:.95fr 1.45fr .9fr;gap:1rem;align-items:start}.evidence-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.7rem}.evidence{border:1px dashed #c7d2fe;border-radius:1rem;background:#f8fafc;padding:.85rem}.share-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.55rem}.share-grid div{border:1px solid #e2e8f0;border-radius:1rem;background:white;padding:.75rem}.score-card{border:1px solid #c7d2fe;border-radius:1.2rem;background:linear-gradient(135deg,#eef2ff,#fff);padding:1rem;text-align:center}.score-card b{font-size:2.2rem;color:#3730a3}.consult-shell{display:grid;grid-template-columns:.95fr 1.25fr .95fr;gap:1rem;align-items:start}.step-line{border-left:4px solid #6366f1;background:#fff;border-radius:.85rem;padding:.75rem .9rem;margin:.6rem 0}.lead-card{border:1px solid #c7d2fe;border-radius:1.2rem;background:linear-gradient(135deg,#fff,#eef2ff);padding:1rem}.cta-row{display:grid;grid-template-columns:repeat(2,1fr);gap:.55rem}.funnel-stage{border:1px solid #e0e7ff;border-radius:1rem;background:#fff;padding:.8rem;margin:.55rem 0}.funnel-stage b{color:#3730a3}@media(max-width:900px){.site-top{display:block}.grid2,.grid3,.grid4,.task-shell,.toolbar,.result-strip,.portfolio-shell,.evidence-grid,.share-grid,.consult-shell,.cta-row{grid-template-columns:1fr}.hero h1{font-size:2rem}.hero-actions{display:block}}
</style>
""",
    unsafe_allow_html=True,
)

TASKS = pd.DataFrame(
    [
        ["Day 1", "目标拆解", "已完成", 100, "5天成长路线图", "把目标拆成5天任务和可检查交付物"],
        ["Day 2", "测试用例作品", "今日主任务", 70, "测试用例 + Bug报告", "围绕登录页面补齐测试用例和Bug报告模板"],
        ["Day 3", "复杂需求拆解", "等待点评", 45, "流程 + 异常分支", "把业务需求拆成角色、流程、输入输出和异常分支"],
        ["Day 4", "发表作品", "未解锁", 0, "3分钟发表稿", "把作品整理成可发表、可面试、可汇报的表达"],
        ["Day 5", "30天行动计划", "未解锁", 0, "成长计划", "根据前4天成果生成后续行动计划"],
    ],
    columns=["day", "title", "focus", "progress", "outcome", "brief"],
)

STATUS_CLASS = {
    "访客": "", "学员": "blue", "Founder": "hot", "未开始": "", "进行中": "purple", "AI已反馈": "orange", "待Agent点评": "blue", "Agent已点评": "green", "已完成": "green", "今日主任务": "purple", "等待点评": "blue", "未解锁": "", "可展示": "green", "修改中": "orange", "待点评": "blue", "新线索": "blue", "已联系": "purple", "已预约": "orange", "已成交": "green",
}


def init_state() -> None:
    defaults = {
        "logged_in": False,
        "role": "访客",
        "user_name": "体验用户",
        "current_view": "dashboard",
        "active_task_index": 1,
        "task_status": "未开始",
        "draft": "目标：补齐登录页面测试能力\n\n当前草稿：\n1. 正常登录：输入正确用户名和密码，可以登录成功。\n2. 错误密码：提示密码错误。\n3. 空用户名：提示必须输入用户名。\n\n待补充：权限、安全、边界、Bug报告模板。",
        "draft_saved": False,
        "saved_at": "",
        "ai_feedback": "",
        "submitted": False,
        "portfolio_candidate": False,
        "portfolio_approved": False,
        "active_portfolio_index": 0,
        "consult_summary": "",
        "lead_status": "新线索",
        "last_event": "尚未开始互动",
        "action_history": ["进入体验后，系统会记录你的关键操作。"],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def chip(text: str) -> str:
    return f"<span class='pill {STATUS_CLASS.get(str(text), '')}'>{text}</span>"


def set_view(view: str) -> None:
    st.session_state.current_view = view


def log_event(message: str) -> None:
    stamp = datetime.now().strftime("%H:%M:%S")
    entry = f"{stamp} · {message}"
    st.session_state.last_event = message
    st.session_state.action_history = [entry] + st.session_state.action_history[:9]


def login_as(role: str, name: str) -> None:
    st.session_state.logged_in = True
    st.session_state.role = role
    st.session_state.user_name = name or ("Founder" if role == "Founder" else "学员Demo")
    st.session_state.current_view = "dashboard"
    log_event(f"已登录：{role}")


def logout() -> None:
    st.session_state.logged_in = False
    st.session_state.role = "访客"
    st.session_state.user_name = "体验用户"
    st.session_state.current_view = "dashboard"
    log_event("已退出登录")


def ai_feedback_for(draft: str) -> str:
    missing = []
    if "权限" not in draft:
        missing.append("补权限差异：普通用户、管理员、未授权用户")
    if "SQL" not in draft and "注入" not in draft:
        missing.append("补安全场景：SQL注入、暴力尝试、锁定策略")
    if "边界" not in draft and "超长" not in draft:
        missing.append("补边界输入：超长用户名、特殊字符、空格")
    if "Bug" not in draft and "严重度" not in draft:
        missing.append("补Bug报告模板：标题、步骤、实际结果、预期结果、严重度")
    if not missing:
        missing.append("整理成作品集结构：背景 → 方法 → 结果 → 证据 → 复盘")
    return "【AI即时反馈】\n你的草稿已经具备基础结构。\n\n建议补充：\n" + "\n".join(f"{idx}. {item}" for idx, item in enumerate(missing, start=1)) + "\n\n下一步：补 6 条测试用例，再写 1 个完整 Bug 报告样例。"


def recommend_package(identity: str, goal: str) -> tuple[str, str, list[str], list[str]]:
    if "企业" in identity or "企业" in goal:
        return (
            "企业训练版",
            "适合部门新人训练、AI任务标准化和内部培训产品化。",
            ["梳理部门高频任务", "生成训练任务卡", "员工提交练习", "Agent初评", "主管看异常与日报"],
            ["部门高频任务地图", "员工练习包", "评分标准", "Founder/主管日报"],
        )
    if "自由职业" in identity or "小微老板" in identity or "自由职业" in goal or "接单" in goal:
        return (
            "自由职业版",
            "适合把技能包装成服务、样品案例、报价表达和客户交付物。",
            ["选择可售卖技能", "定义目标客户", "制作样品案例", "Agent打磨表达", "形成服务包"],
            ["服务方向定位", "样品案例", "报价表达", "客户沟通话术"],
        )
    return (
        "个人成长版",
        "适合职场新人、在岗提升、升职准备、转岗跳槽和作品集建设。",
        ["明确成长目标", "完成5天任务", "获得Agent反馈", "沉淀作品集", "生成30天行动计划"],
        ["5天成长路线图", "测试/业务分析作品", "Agent点评记录", "30天行动计划"],
    )


def portfolio_df() -> pd.DataFrame:
    rows = [
        ["目标拆解", "5天成长路线图", "86", "可展示", "职业成长", "目标清晰、路径可执行。", "把个人目标拆成5天任务，能说明路线和交付物。"],
        ["测试用例作品", "测试用例 + Bug报告", "64", "修改中", "软件测试", "还缺权限、安全、边界。", "已经覆盖基础登录，但需要补充权限、安全和边界测试。"],
        ["复杂需求拆解", "流程 + 异常分支", "--", "待点评", "业务分析", "等待Agent正式点评。", "适合作为业务分析或测试分析作品候选。"],
    ]
    if st.session_state.portfolio_candidate:
        status = "可展示" if st.session_state.portfolio_approved else "待点评"
        rows.append(["登录测试作品", "测试用例 + Bug报告草稿", "待定", status, "软件测试", "已提交给Agent，等待确认是否可展示。", "来自当前会话的提交记录，后续可沉淀成作品集材料。"])
    return pd.DataFrame(rows, columns=["作品", "证明材料", "评分", "状态", "方向", "说明", "Agent摘要"])


def render_public_top() -> None:
    st.markdown("""
<div class='site-top'>
  <div class='brand'>AI Skill Growth OS<small>任务驱动 · Agent反馈 · 作品集证明 · 咨询转化</small></div>
  <div class='landing-nav'><span class='pill'>功能</span><span class='pill'>场景</span><span class='pill'>流程</span><span class='pill'>FAQ</span><span class='pill hot'>进入体验</span></div>
</div>
""", unsafe_allow_html=True)


def render_public_site() -> None:
    render_public_top()
    left, right = st.columns([1.22, .78])
    with left:
        st.markdown("""
<div class='hero'>
<span class='pill hot'>登录前官网 · v4.7.4</span>
<h1>不是看课，而是每天完成一个<br><span>能变成作品集的任务</span></h1>
<p>AI Skill Growth OS 帮助个人、自由职业者和企业新人从“学习内容”进入“完成任务”。登录后会进入真实应用工作台：写草稿、请求AI反馈、提交Agent、沉淀作品集。</p>
<div class='hero-actions'><span class='pill hot'>体验学员工作台</span><span class='pill'>查看任务闭环</span><span class='pill'>生成咨询路径</span></div>
<div class='trust-row'><span class='pill green'>5天任务闭环</span><span class='pill blue'>Agent即时反馈</span><span class='pill purple'>作品集证明</span><span class='pill orange'>Founder运营队列</span></div>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class='result-strip'><div><b>1</b><br><span class='mini'>今日主任务</span></div><div><b>3</b><br><span class='mini'>核心交付物</span></div><div><b>5</b><br><span class='mini'>天成长闭环</span></div><div><b>∞</b><br><span class='mini'>后续作品复用</span></div></div>
""", unsafe_allow_html=True)
        st.markdown("<div class='section'>适合的用户场景</div>", unsafe_allow_html=True)
        st.markdown("""
<div class='grid3'>
  <div class='card'><h3>个人成长 / 转岗</h3><p>每天完成一个可检查任务，最后沉淀成面试、汇报或自我提升材料。</p></div>
  <div class='card'><h3>自由职业 / 一人公司</h3><p>把技能包装成服务样品、客户案例、报价表达和可交付证明。</p></div>
  <div class='card'><h3>企业新人训练</h3><p>把部门高频任务变成训练卡，用Agent初评，主管只看异常和结果。</p></div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<div class='section'>登录后会发生什么</div>", unsafe_allow_html=True)
        st.markdown("""
<div class='grid4'>
  <div class='flow-step'><b>1. 进入工作台</b><span class='mini'>看到当前任务、状态、草稿和下一步。</span></div>
  <div class='flow-step'><b>2. 写草稿</b><span class='mini'>在任务编辑器中完成交付物。</span></div>
  <div class='flow-step'><b>3. 请求反馈</b><span class='mini'>AI指出权限、安全、边界等缺口。</span></div>
  <div class='flow-step'><b>4. 进入作品集</b><span class='mini'>提交Agent后成为作品候选。</span></div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<div class='section'>FAQ</div>", unsafe_allow_html=True)
        st.markdown("""
<div class='faq'><b>这是课程平台吗？</b><br><span class='mini'>不是传统课程后台，核心是任务、反馈和作品集证明。</span></div>
<div class='faq'><b>现在接数据库了吗？</b><br><span class='mini'>当前先做前端交互，数据暂存在 session_state，后续接 Supabase。</span></div>
<div class='faq'><b>Founder 要做什么？</b><br><span class='mini'>Founder 不批改所有内容，只看待处理、候选、线索和异常。</span></div>
""", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<div class='panel'><h2>进入体验</h2><p>先用前端 session 模拟登录。体验流程顺了，再接真实 Auth / Supabase。</p></div>", unsafe_allow_html=True)
        with st.form("public_login_form"):
            name = st.text_input("姓名 / 体验名", value="学员Demo")
            role = st.selectbox("选择身份", ["学员", "Founder"])
            submitted = st.form_submit_button("进入网站", type="primary")
        if submitted:
            login_as(role, name)
            st.rerun()
        c1, c2 = st.columns(2)
        if c1.button("快速学员Demo"):
            login_as("学员", "学员Demo")
            st.rerun()
        if c2.button("快速FounderDemo"):
            login_as("Founder", "Founder")
            st.rerun()
        st.markdown("""
<div class='card'><h3>推荐体验顺序</h3><p>1. 学员Demo<br>2. 我的任务<br>3. 保存草稿 / 请求反馈 / 提交Agent<br>4. 作品集候选<br>5. 咨询漏斗<br>6. FounderDemo处理队列</p></div>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_app_top() -> None:
    st.markdown(f"""
<div class='site-top'>
  <div class='brand'>AI Skill Growth OS<small>Logged-in App · {st.session_state.role}</small></div>
  <div>{chip(st.session_state.role)}<span class='pill'>{st.session_state.user_name}</span><span class='pill'>最近：{st.session_state.last_event}</span></div>
</div>
""", unsafe_allow_html=True)
    nav = [("dashboard", "工作台"), ("tasks", "我的任务"), ("portfolio", "作品集"), ("consult", "咨询")]
    if st.session_state.role == "Founder":
        nav = [("dashboard", "Founder看板"), ("queue", "运营队列"), ("portfolio", "作品候选"), ("consult", "咨询线索")]
    cols = st.columns(len(nav) + 1)
    for col, (view, label) in zip(cols, nav):
        if col.button(label, type="primary" if st.session_state.current_view == view else "secondary", use_container_width=True):
            set_view(view)
            st.rerun()
    if cols[-1].button("退出", use_container_width=True):
        logout()
        st.rerun()


def student_dashboard() -> None:
    feedback_state = "已有反馈" if st.session_state.ai_feedback else "未请求"
    candidate_state = "有候选" if st.session_state.portfolio_candidate else "暂无候选"
    st.markdown(f"""
<div class='hero'>
<span class='pill hot'>登录后工作台</span>
<h1>{st.session_state.user_name}，今天继续：<br><span>Day 2 · 测试用例作品</span></h1>
<p>这里是登录后的真实应用入口。所有按钮都会改变当前会话状态。</p>
<span class='pill'>任务状态：{st.session_state.task_status}</span><span class='pill'>草稿字数：{len(st.session_state.draft)}</span><span class='pill'>AI反馈：{feedback_state}</span><span class='pill'>作品集：{candidate_state}</span><span class='pill'>线索：{st.session_state.lead_status}</span>
</div>
""", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>当前任务</span><div class='metric'>Day 2</div><p>测试用例作品</p></div>
  <div class='card'><span class='mini'>任务状态</span><p>{chip(st.session_state.task_status)}</p></div>
  <div class='card'><span class='mini'>作品候选</span><div class='metric'>{1 if st.session_state.portfolio_candidate else 0}</div></div>
  <div class='card'><span class='mini'>咨询摘要</span><div class='metric'>{1 if st.session_state.consult_summary else 0}</div></div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("继续今日任务", type="primary", use_container_width=True):
        set_view("tasks")
        st.rerun()
    if c2.button("查看作品集", use_container_width=True):
        set_view("portfolio")
        st.rerun()
    if c3.button("生成咨询路径", use_container_width=True):
        set_view("consult")
        st.rerun()


def founder_dashboard() -> None:
    pending = 1 if st.session_state.submitted else 0
    candidates = 1 if st.session_state.portfolio_candidate else 0
    leads = 1 if st.session_state.consult_summary else 0
    st.markdown("<div class='hero'><span class='pill hot'>Founder Dashboard</span><h1>今天只看需要你决策的事</h1><p>Founder 不翻所有数据，只处理待点评、作品候选、咨询线索和异常。</p></div>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card decision'><span class='mini'>待Agent点评</span><div class='metric'>{pending}</div><p>来自学员提交。</p></div>
  <div class='card decision'><span class='mini'>作品候选</span><div class='metric'>{candidates}</div><p>等待确认是否可展示。</p></div>
  <div class='card decision'><span class='mini'>咨询线索</span><div class='metric'>{leads}</div><p>{st.session_state.lead_status}</p></div>
  <div class='card'><span class='mini'>最近动作</span><p>{st.session_state.last_event}</p></div>
</div>
""", unsafe_allow_html=True)
    if st.session_state.submitted:
        st.markdown("<div class='section'>待处理任务</div>", unsafe_allow_html=True)
        st.markdown("<div class='card decision'><h3>登录测试作品</h3><p>学员已提交给Agent，等待确认作品集状态。</p></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("确认进入作品集", type="primary"):
            st.session_state.portfolio_approved = True
            st.session_state.task_status = "Agent已点评"
            log_event("Founder确认作品集")
            st.rerun()
        if c2.button("打回修改"):
            st.session_state.task_status = "AI已反馈"
            st.session_state.submitted = False
            log_event("Founder打回修改")
            st.rerun()


def tasks_page() -> None:
    active = TASKS.iloc[int(st.session_state.active_task_index)]
    st.markdown("<div class='panel'><span class='pill hot'>My Tasks</span><h2>任务工作台</h2><p>左侧选任务，中间编辑交付物，右侧看反馈、状态和操作历史。</p></div>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>当前任务</span><div class='metric'>{active['day']}</div><p>{active['title']}</p></div>
  <div class='card'><span class='mini'>任务状态</span><p>{chip(st.session_state.task_status)}</p></div>
  <div class='card'><span class='mini'>草稿字数</span><div class='metric'>{len(st.session_state.draft)}</div></div>
  <div class='card'><span class='mini'>作品候选</span><div class='metric'>{1 if st.session_state.portfolio_candidate else 0}</div></div>
</div>
""", unsafe_allow_html=True)
    left, mid, right = st.columns([.85, 1.35, .95])
    with left:
        st.markdown("<div class='task-rail'><h3>任务列表</h3><p class='mini'>点击切换任务。</p>", unsafe_allow_html=True)
        for idx, row in TASKS.iterrows():
            active_class = " active" if idx == st.session_state.active_task_index else ""
            st.markdown(f"<div class='task-mini{active_class}'><b>{row['day']} · {row['title']}</b>{chip(row['focus'])}<div class='progress'><div class='bar' style='width:{row['progress']}%'></div></div></div>", unsafe_allow_html=True)
            if st.button(f"打开 {row['day']}", key=f"open_task_{idx}", use_container_width=True):
                st.session_state.active_task_index = int(idx)
                log_event(f"切换任务：{row['day']} {row['title']}")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with mid:
        st.markdown(f"""
<div class='editor-panel'><h3>{active['day']} · {active['title']}</h3><p><b>任务说明：</b>{active['brief']}<br><b>交付物：</b>{active['outcome']}<br><b>状态：</b>{chip(st.session_state.task_status)}</p></div>
""", unsafe_allow_html=True)
        st.text_area("作品草稿", key="draft", height=310)
        c1, c2, c3 = st.columns(3)
        if c1.button("保存草稿", type="primary", use_container_width=True):
            st.session_state.draft_saved = True
            st.session_state.saved_at = datetime.now().strftime("%H:%M:%S")
            st.session_state.task_status = "进行中"
            log_event(f"草稿已保存 {st.session_state.saved_at}")
            st.rerun()
        if c2.button("请求AI反馈", use_container_width=True):
            st.session_state.ai_feedback = ai_feedback_for(st.session_state.draft)
            st.session_state.task_status = "AI已反馈"
            log_event("AI反馈已生成")
            st.rerun()
        if c3.button("提交给Agent", use_container_width=True):
            st.session_state.submitted = True
            st.session_state.portfolio_candidate = True
            st.session_state.task_status = "待Agent点评"
            log_event("已提交Agent，作品集候选+1")
            st.rerun()
        if st.session_state.submitted:
            st.markdown("<div class='ok'><b>已提交</b><br>当前任务已进入待Agent点评队列，作品集页会出现候选。</div>", unsafe_allow_html=True)
        elif st.session_state.draft_saved:
            st.markdown(f"<div class='ok'><b>已保存</b><br>保存时间：{st.session_state.saved_at}。下一步请求AI反馈或提交Agent。</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='warn'><b>下一步</b><br>先保存草稿，再请求AI反馈，最后提交Agent。</div>", unsafe_allow_html=True)
    with right:
        feedback = st.session_state.ai_feedback or "还没有请求AI反馈。\n\n点击“请求AI反馈”后，这里会根据当前草稿生成反馈。"
        st.markdown(f"<div class='quote'>{feedback}</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><h3>完成标准</h3><p>1. 交付物明确<br>2. 覆盖权限、安全、边界<br>3. 可进入作品集表达</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='history'><h3>操作历史</h3>" + "".join(f"<div class='history-item'>{item}</div>" for item in st.session_state.action_history) + "</div>", unsafe_allow_html=True)


def portfolio_page() -> None:
    df = portfolio_df()
    visible_df = df
    st.markdown("<div class='panel'><span class='pill hot'>Portfolio</span><h2>作品集工作台</h2><p>作品集不只是卡片列表，而是证明材料管理页。</p></div>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'><div class='card'><span class='mini'>全部作品</span><div class='metric'>{len(df)}</div></div><div class='card'><span class='mini'>可展示</span><div class='metric'>{int((df['状态'] == '可展示').sum())}</div></div><div class='card'><span class='mini'>修改中</span><div class='metric'>{int((df['状态'] == '修改中').sum())}</div></div><div class='card'><span class='mini'>待点评</span><div class='metric'>{int((df['状态'] == '待点评').sum())}</div></div></div>
""", unsafe_allow_html=True)
    f1, f2 = st.columns([.7, 1.3])
    with f1:
        status_filter = st.selectbox("状态筛选", ["全部", "可展示", "修改中", "待点评"])
    with f2:
        keyword = st.text_input("搜索作品", placeholder="输入作品名、方向或证明材料")
    if status_filter != "全部":
        visible_df = visible_df[visible_df["状态"] == status_filter]
    if keyword.strip():
        key = keyword.strip()
        visible_df = visible_df[visible_df.apply(lambda row: key in " ".join(str(v) for v in row.values), axis=1)]
    if visible_df.empty:
        st.info("没有匹配的作品。")
        return
    if st.session_state.active_portfolio_index >= len(visible_df):
        st.session_state.active_portfolio_index = 0
    active = visible_df.iloc[int(st.session_state.active_portfolio_index)]
    left, mid, right = st.columns([.95, 1.45, .9])
    with left:
        st.markdown("<div class='portfolio-list'><h3>作品列表</h3><p class='mini'>筛选后点击查看详情。</p>", unsafe_allow_html=True)
        for pos, (_, row) in enumerate(visible_df.iterrows()):
            active_class = " active" if pos == st.session_state.active_portfolio_index else ""
            st.markdown(f"<div class='portfolio-mini{active_class}'><b>{row['作品']}</b>{chip(row['状态'])}<span class='pill purple'>{row['方向']}</span><p class='mini'>{row['证明材料']}</p></div>", unsafe_allow_html=True)
            if st.button(f"查看作品 {pos + 1}", key=f"portfolio_open_{pos}", use_container_width=True):
                st.session_state.active_portfolio_index = pos
                log_event(f"查看作品：{row['作品']}")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with mid:
        st.markdown(f"<div class='portfolio-detail'><h3>{active['作品']}</h3>{chip(active['状态'])}<span class='pill purple'>{active['方向']}</span><p><b>证明材料：</b>{active['证明材料']}<br><b>评分：</b>{active['评分']}<br><b>说明：</b>{active['说明']}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='quote'>【Agent点评摘要】\n{active['Agent摘要']}\n\n建议按“背景 → 方法 → 结果 → 证据 → 复盘”整理成可展示版本。</div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>证据结构</div>", unsafe_allow_html=True)
        st.markdown("<div class='evidence-grid'><div class='evidence'><b>背景</b><br><span class='mini'>为什么做这个作品。</span></div><div class='evidence'><b>方法</b><br><span class='mini'>如何拆解、设计或测试。</span></div><div class='evidence'><b>结果</b><br><span class='mini'>最终产出材料。</span></div><div class='evidence'><b>复盘</b><br><span class='mini'>如何根据反馈改进。</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>导出 / 分享占位</div>", unsafe_allow_html=True)
        st.markdown("<div class='share-grid'><div><b>导出PDF</b><br><span class='mini'>后续生成作品集PDF。</span></div><div><b>分享链接</b><br><span class='mini'>后续给面试官或客户查看。</span></div><div><b>加入咨询材料</b><br><span class='mini'>后续用于转化。</span></div></div>", unsafe_allow_html=True)
    with right:
        st.markdown(f"<div class='score-card'><span class='mini'>作品评分</span><br><b>{active['评分']}</b><p>{active['状态']}</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><h3>可展示检查</h3><p>1. 别人能看懂<br>2. 有证明材料<br>3. 可复用到面试/客户/汇报<br>4. 有Agent点评记录</p></div>", unsafe_allow_html=True)
        if st.session_state.role == "Founder" and st.session_state.portfolio_candidate and not st.session_state.portfolio_approved:
            if st.button("Founder确认可展示", type="primary", use_container_width=True):
                st.session_state.portfolio_approved = True
                st.session_state.task_status = "Agent已点评"
                log_event("Founder在作品集页确认可展示")
                st.rerun()
            if st.button("Founder打回修改", use_container_width=True):
                st.session_state.task_status = "AI已反馈"
                st.session_state.submitted = False
                st.session_state.portfolio_approved = False
                log_event("Founder在作品集页打回修改")
                st.rerun()
        st.markdown("<div class='history'><h3>操作历史</h3>" + "".join(f"<div class='history-item'>{item}</div>" for item in st.session_state.action_history) + "</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)


def consult_page() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Consult Funnel</span><h2>咨询转化漏斗</h2><p>咨询页不再只是留言表单，而是把用户场景转成方案、摘要和Founder线索状态。</p></div>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>当前线索</span><div class='metric'>{1 if st.session_state.consult_summary else 0}</div></div>
  <div class='card'><span class='mini'>线索状态</span><p>{chip(st.session_state.lead_status)}</p></div>
  <div class='card'><span class='mini'>作品候选</span><div class='metric'>{1 if st.session_state.portfolio_candidate else 0}</div></div>
  <div class='card'><span class='mini'>最近动作</span><p>{st.session_state.last_event}</p></div>
</div>
""", unsafe_allow_html=True)
    left, mid, right = st.columns([.95, 1.25, .95])
    with left:
        st.markdown("<div class='funnel-panel'><h3>1. 场景识别</h3><p class='mini'>先判断用户是谁、想解决什么。</p>", unsafe_allow_html=True)
        identity = st.selectbox("你现在属于哪类人？", ["职场新人", "在岗提升", "升职准备", "转岗 / 跳槽", "自由职业 / 副业接单", "企业培训负责人", "小微老板"])
        goal = st.selectbox("你最想解决什么？", ["学新技能", "提升现有技能", "做作品集", "升职表达", "换工作 / 高薪跳槽", "自由职业接单", "企业内训"])
        urgency = st.selectbox("希望多快看到结果？", ["先体验", "7天内", "30天内", "尽快转化/交付"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='funnel-stage'><b>漏斗阶段</b><br>访问 → 识别场景 → 推荐方案 → 生成摘要 → Founder跟进</div>", unsafe_allow_html=True)
    package, reason, steps, deliverables = recommend_package(identity, goal)
    with mid:
        st.markdown(f"""
<div class='plan-card'>
<h3>2. 推荐方案：{package}</h3>
{chip('推荐')}
<p>{reason}</p>
</div>
""", unsafe_allow_html=True)
        for idx, step in enumerate(steps, start=1):
            st.markdown(f"<div class='step-line'><b>{idx}. {step}</b><br><span class='mini'>后续可接真实任务模板。</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>适合交付物</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid2'>" + "".join(f"<div class='card'><h3>{item}</h3><p>可作为咨询后续材料。</p></div>" for item in deliverables) + "</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='lead-card'><h3>3. 线索摘要</h3><p>生成后会进入Founder线索队列。</p>", unsafe_allow_html=True)
        with st.form("consult_form_v474"):
            name = st.text_input("姓名 / 称呼")
            contact = st.text_input("联系方式，选填")
            note = st.text_area("补充说明", placeholder="例如：我想转测试岗 / 我想把Java培训做成产品包")
            ok = st.form_submit_button("生成咨询摘要", type="primary")
        if ok:
            summary = (
                f"【咨询摘要】\n"
                f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"姓名：{name or '未填写'}\n联系方式：{contact or '未填写'}\n"
                f"身份：{identity}\n目标：{goal}\n时效：{urgency}\n"
                f"推荐路径：{package}\n推荐理由：{reason}\n"
                f"建议步骤：{' → '.join(steps)}\n"
                f"建议交付物：{' / '.join(deliverables)}\n补充：{note or '无'}"
            )
            st.session_state.consult_summary = summary
            st.session_state.lead_status = "新线索"
            log_event("咨询摘要已生成，Founder线索+1")
            st.rerun()
        if st.session_state.consult_summary:
            st.markdown(f"<div class='quote'>{st.session_state.consult_summary}</div>", unsafe_allow_html=True)
            st.download_button("下载咨询摘要", data=st.session_state.consult_summary, file_name="consult_summary.txt", mime="text/plain")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>下一步 CTA</div>", unsafe_allow_html=True)
        cta1, cta2 = st.columns(2)
        if cta1.button("加入Founder跟进", use_container_width=True):
            st.session_state.lead_status = "新线索"
            log_event("咨询线索已加入Founder跟进")
            st.rerun()
        if cta2.button("预约体验课", use_container_width=True):
            st.session_state.lead_status = "已预约"
            log_event("用户点击预约体验课")
            st.rerun()
        st.markdown("<div class='history'><h3>操作历史</h3>" + "".join(f"<div class='history-item'>{item}</div>" for item in st.session_state.action_history) + "</div>", unsafe_allow_html=True)


def founder_queue() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Founder Queue</span><h2>运营队列</h2><p>这里模拟 Founder 登录后的处理动作。</p></div>", unsafe_allow_html=True)
    if not st.session_state.submitted and not st.session_state.consult_summary:
        st.info("暂无待处理事项。用学员身份提交任务或生成咨询摘要后，这里会出现队列。")
        return
    if st.session_state.submitted:
        st.markdown("<div class='card decision'><h3>待点评：登录测试作品</h3><p>学员已提交草稿，等待 Founder/Agent 决策。</p></div>", unsafe_allow_html=True)
    if st.session_state.consult_summary:
        st.markdown(f"<div class='card decision'><h3>咨询线索 {chip(st.session_state.lead_status)}</h3><p>{st.session_state.consult_summary.replace(chr(10), '<br>')}</p></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        if c1.button("标记已联系", use_container_width=True):
            st.session_state.lead_status = "已联系"
            log_event("Founder标记线索已联系")
            st.rerun()
        if c2.button("标记已预约", use_container_width=True):
            st.session_state.lead_status = "已预约"
            log_event("Founder标记线索已预约")
            st.rerun()
        if c3.button("标记已成交", type="primary", use_container_width=True):
            st.session_state.lead_status = "已成交"
            log_event("Founder标记线索已成交")
            st.rerun()


init_state()

if not st.session_state.logged_in:
    render_public_site()
else:
    render_app_top()
    if st.session_state.role == "Founder":
        if st.session_state.current_view == "dashboard":
            founder_dashboard()
        elif st.session_state.current_view == "queue":
            founder_queue()
        elif st.session_state.current_view == "portfolio":
            portfolio_page()
        else:
            consult_page()
    else:
        if st.session_state.current_view == "dashboard":
            student_dashboard()
        elif st.session_state.current_view == "tasks":
            tasks_page()
        elif st.session_state.current_view == "portfolio":
            portfolio_page()
        else:
            consult_page()

st.caption("AI Skill Growth OS · Consult Conversion Funnel · v4.7.4")
