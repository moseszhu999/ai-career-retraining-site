from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Skill Growth OS", page_icon="🚀", layout="wide")

st.markdown(
    """
<style>
.main .block-container{max-width:1160px;padding-top:.8rem;padding-bottom:4rem}.top{border:1px solid #c7d2fe;border-radius:1.3rem;background:white;box-shadow:0 12px 30px rgba(15,23,42,.07);padding:.9rem 1rem;margin-bottom:.8rem;display:flex;justify-content:space-between;gap:1rem;align-items:center}.brand{font-size:1.15rem;font-weight:950;color:#111827}.brand small{display:block;color:#64748b;font-size:.82rem}.pill{display:inline-block;border-radius:999px;padding:.28rem .62rem;font-size:.8rem;font-weight:900;border:1px solid #e2e8f0;background:#f8fafc;color:#475569;margin:.1rem .15rem}.hot{background:linear-gradient(90deg,#4f46e5,#06b6d4);border:none;color:white}.green{background:#dcfce7;color:#166534;border-color:#bbf7d0}.orange{background:#ffedd5;color:#9a3412;border-color:#fed7aa}.blue{background:#dbeafe;color:#1e40af;border-color:#bfdbfe}.purple{background:#ede9fe;color:#5b21b6;border-color:#ddd6fe}.hero,.panel{border:1px solid #c7d2fe;border-radius:1.25rem;background:linear-gradient(135deg,#fff,#eef2ff);padding:1.2rem;margin:.8rem 0}.hero h1{font-size:2.2rem;line-height:1.1;margin:.2rem 0;color:#0f172a}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p,.panel p{color:#475569;line-height:1.7}.grid2{display:grid;grid-template-columns:1.1fr .9fr;gap:1rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card{border:1px solid #e2e8f0;border-radius:1rem;background:white;padding:1rem;box-shadow:0 8px 20px rgba(15,23,42,.04)}.card h3{margin:.1rem 0 .45rem;color:#111827}.card p{color:#64748b;line-height:1.55}.metric{font-size:2rem;font-weight:950;color:#111827}.quote{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;line-height:1.65}.timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem}.timeline div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.8rem;text-align:center}.progress{height:.65rem;border-radius:999px;background:#e2e8f0;overflow:hidden}.bar{height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4)}.section{font-size:1.45rem;font-weight:950;margin:1.2rem 0 .45rem;color:#0f172a}.mini{font-size:.85rem;color:#64748b;line-height:1.55}.ok{border:1px solid #bbf7d0;background:#f0fdf4;color:#166534;border-radius:1rem;padding:1rem}.warn{border:1px solid #fed7aa;background:#fff7ed;color:#7c2d12;border-radius:1rem;padding:1rem}.proof{border:1px solid #e0e7ff;border-radius:1rem;background:white;padding:1rem}@media(max-width:900px){.top{display:block}.grid2,.grid3,.grid4,.timeline{grid-template-columns:1fr}.hero h1{font-size:1.8rem}}
</style>
""",
    unsafe_allow_html=True,
)

NAV = {"home": "首页", "tasks": "我的任务", "portfolio": "作品集", "consult": "咨询"}
TASKS = pd.DataFrame(
    [
        ["Day 1", "目标拆解", "已完成", 100],
        ["Day 2", "测试用例作品", "今日主任务", 70],
        ["Day 3", "复杂需求拆解", "等待点评", 45],
        ["Day 4", "发表作品", "未解锁", 0],
        ["Day 5", "30天行动计划", "未解锁", 0],
    ],
    columns=["day", "title", "focus", "progress"],
)
STATUS_CLASS = {"访客": "", "学员": "blue", "Founder": "hot", "未开始": "", "进行中": "purple", "AI已反馈": "orange", "待Agent点评": "blue", "已保存": "green", "可展示": "green", "修改中": "orange", "待点评": "blue"}


def init_state() -> None:
    defaults = {
        "role": "访客",
        "user_name": "体验用户",
        "page": "home",
        "task_status": "未开始",
        "draft": "目标：补齐登录页面测试能力\n\n当前草稿：\n1. 正常登录：输入正确用户名和密码，可以登录成功。\n2. 错误密码：提示密码错误。\n3. 空用户名：提示必须输入用户名。\n\n待补充：权限、安全、边界、Bug报告模板。",
        "draft_saved": False,
        "saved_at": "",
        "ai_feedback": "",
        "submitted": False,
        "portfolio_candidate": False,
        "consult_summary": "",
        "last_event": "尚未开始互动",
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def chip(text: str) -> str:
    return f"<span class='pill {STATUS_CLASS.get(str(text), '')}'>{text}</span>"


def feedback_for(draft: str) -> str:
    missing = []
    if "权限" not in draft:
        missing.append("权限差异")
    if "SQL" not in draft and "注入" not in draft:
        missing.append("SQL注入 / 安全场景")
    if "边界" not in draft and "超长" not in draft:
        missing.append("边界输入")
    if "Bug" not in draft and "严重度" not in draft:
        missing.append("Bug报告模板")
    if not missing:
        missing.append("把结果整理成：背景 → 方法 → 结果 → 证据 → 复盘")
    return "【AI即时反馈】\n你的草稿已经具备基础结构。\n\n下一步重点补充：\n" + "\n".join(f"{i}. {m}" for i, m in enumerate(missing, 1)) + "\n\n建议：先补 6 条测试用例，再写 1 个完整 Bug 报告样例。"


def recommend_package(identity: str, goal: str) -> tuple[str, str, list[str]]:
    if "企业" in identity or "企业" in goal:
        return "企业训练版", "适合部门新人训练、AI任务标准化和内部培训产品化。", ["梳理部门高频任务", "生成训练任务卡", "员工提交练习", "Agent初评", "主管看异常与日报"]
    if "自由职业" in identity or "小微老板" in identity or "自由职业" in goal or "接单" in goal:
        return "自由职业版", "适合把技能包装成服务、样品案例、报价表达和客户交付物。", ["选择可售卖技能", "定义目标客户", "制作样品案例", "Agent打磨表达", "形成服务包"]
    return "个人成长版", "适合职场新人、在岗提升、升职准备、转岗跳槽和作品集建设。", ["明确成长目标", "完成5天任务", "获得Agent反馈", "沉淀作品集", "生成30天行动计划"]


def top_nav() -> str:
    st.markdown(
        f"""
<div class='top'>
  <div class='brand'>AI Skill Growth OS<small>Session Interaction Demo · v4.6.0</small></div>
  <div>{chip(st.session_state.role)}<span class='pill'>{st.session_state.user_name}</span><span class='pill'>最近：{st.session_state.last_event}</span></div>
</div>
""",
        unsafe_allow_html=True,
    )
    page = st.radio("产品导航", list(NAV.keys()), format_func=lambda k: NAV[k], horizontal=True, key="page", label_visibility="collapsed")
    return page


def login_panel() -> None:
    with st.expander("登录 / 切换体验身份", expanded=st.session_state.role == "访客"):
        with st.form("login_form"):
            role = st.selectbox("身份", ["访客", "学员", "Founder"], index=["访客", "学员", "Founder"].index(st.session_state.role))
            name = st.text_input("姓名 / 体验名", value=st.session_state.user_name)
            ok = st.form_submit_button("进入体验")
        if ok:
            st.session_state.role = role
            st.session_state.user_name = name or "体验用户"
            st.session_state.last_event = f"进入{role}体验"
            st.session_state.page = "tasks" if role == "学员" else "home"
            st.rerun()
        c1, c2, c3 = st.columns(3)
        if c1.button("快速进入学员Demo"):
            st.session_state.role = "学员"
            st.session_state.user_name = "学员Demo"
            st.session_state.page = "tasks"
            st.session_state.last_event = "进入学员Demo"
            st.rerun()
        if c2.button("快速进入FounderDemo"):
            st.session_state.role = "Founder"
            st.session_state.user_name = "Founder"
            st.session_state.page = "home"
            st.session_state.last_event = "进入FounderDemo"
            st.rerun()
        if c3.button("重置体验状态"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            init_state()
            st.rerun()


def home() -> None:
    if st.session_state.role == "学员":
        feedback_state = "已有反馈" if st.session_state.ai_feedback else "未请求"
        candidate_state = "有候选" if st.session_state.portfolio_candidate else "暂无候选"
        st.markdown(
            f"""
<div class='hero'>
<span class='pill hot'>登录后首页</span>
<h1>{st.session_state.user_name}，今天继续：<br><span>Day 2 · 测试用例作品</span></h1>
<p>你现在不是在看介绍，而是在一个任务流程里。保存草稿、请求反馈、提交Agent都会改变状态。</p>
<span class='pill'>任务状态：{st.session_state.task_status}</span><span class='pill'>草稿字数：{len(st.session_state.draft)}</span><span class='pill'>AI反馈：{feedback_state}</span><span class='pill'>作品集：{candidate_state}</span>
</div>
""",
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        if c1.button("继续今日任务", type="primary"):
            st.session_state.page = "tasks"
            st.rerun()
        if c2.button("查看作品集"):
            st.session_state.page = "portfolio"
            st.rerun()
        if c3.button("生成咨询路径"):
            st.session_state.page = "consult"
            st.rerun()
        return

    if st.session_state.role == "Founder":
        pending = 1 if st.session_state.submitted else 0
        candidates = 1 if st.session_state.portfolio_candidate else 0
        leads = 1 if st.session_state.consult_summary else 0
        st.markdown("<div class='hero'><span class='pill hot'>Founder Dashboard</span><h1>今天只看需要你决策的事</h1><p>Founder 不翻所有数据，只处理待点评、作品集候选、咨询线索和异常。</p></div>", unsafe_allow_html=True)
        st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>待Agent点评</span><div class='metric'>{pending}</div><p>来自学员提交。</p></div>
  <div class='card'><span class='mini'>作品候选</span><div class='metric'>{candidates}</div><p>等待确认是否可展示。</p></div>
  <div class='card'><span class='mini'>咨询线索</span><div class='metric'>{leads}</div><p>来自咨询摘要。</p></div>
  <div class='card'><span class='mini'>最近动作</span><p>{st.session_state.last_event}</p></div>
</div>
""", unsafe_allow_html=True)
        return

    st.markdown("""
<div class='hero'>
<span class='pill hot'>未登录访客</span>
<h1>先体验一次任务闭环：<br><span>登录后才是真产品</span></h1>
<p>请在上方切换到“学员Demo”。登录后你可以保存草稿、请求AI反馈、提交Agent，并看到作品集候选出现。</p>
</div>
""", unsafe_allow_html=True)
    st.markdown("<div class='grid3'><div class='card'><h3>1. 登录</h3><p>进入学员身份。</p></div><div class='card'><h3>2. 做任务</h3><p>保存草稿并请求反馈。</p></div><div class='card'><h3>3. 状态变化</h3><p>提交后进入作品集候选。</p></div></div>", unsafe_allow_html=True)


def tasks() -> None:
    if st.session_state.role == "访客":
        st.warning("请先切换到“学员Demo”，再体验任务互动。")
        return
    st.markdown("<div class='panel'><span class='pill hot'>My Tasks Workbench</span><h2>今天只做一个任务：把草稿改成可检查作品</h2><p>这里的按钮会真实改变当前会话状态。</p></div>", unsafe_allow_html=True)
    pending = 1 if st.session_state.task_status == "待Agent点评" else 0
    candidate = 1 if st.session_state.portfolio_candidate else 0
    st.markdown(f"""
<div class='grid4'>
  <div class='card'><span class='mini'>当前任务</span><div class='metric'>Day 2</div><p>测试用例作品</p></div>
  <div class='card'><span class='mini'>任务状态</span><p>{chip(st.session_state.task_status)}</p></div>
  <div class='card'><span class='mini'>等待点评</span><div class='metric'>{pending}</div></div>
  <div class='card'><span class='mini'>作品候选</span><div class='metric'>{candidate}</div></div>
</div>
""", unsafe_allow_html=True)
    st.markdown("<div class='section'>训练路径</div>", unsafe_allow_html=True)
    st.markdown("<div class='timeline'>" + "".join(f"<div><b>{r.day}</b><span>{r.title}</span><br>{chip(r.focus)}<div class='progress'><div class='bar' style='width:{r.progress}%'></div></div></div>" for _, r in TASKS.iterrows()) + "</div>", unsafe_allow_html=True)
    left, right = st.columns([1.1, .9])
    with left:
        st.markdown(f"<div class='card'><h3>Day 2 · 测试用例作品</h3><p><b>交付物：</b>测试用例 + Bug报告<br><b>状态：</b>{chip(st.session_state.task_status)}<br><b>下一步：</b>{'等待Agent点评' if st.session_state.submitted else '补充权限、安全、边界后提交'}</p></div>", unsafe_allow_html=True)
        st.text_area("作品草稿", key="draft", height=260)
        st.caption(f"草稿字数：{len(st.session_state.draft)}。当前数据仅保存在 session_state。")
        c1, c2, c3 = st.columns(3)
        if c1.button("保存草稿", type="primary"):
            st.session_state.draft_saved = True
            st.session_state.saved_at = datetime.now().strftime("%H:%M:%S")
            st.session_state.task_status = "进行中"
            st.session_state.last_event = f"草稿已保存 {st.session_state.saved_at}"
            st.rerun()
        if c2.button("请求AI反馈"):
            st.session_state.ai_feedback = feedback_for(st.session_state.draft)
            st.session_state.task_status = "AI已反馈"
            st.session_state.last_event = "AI反馈已生成"
            st.rerun()
        if c3.button("提交给Agent"):
            st.session_state.submitted = True
            st.session_state.portfolio_candidate = True
            st.session_state.task_status = "待Agent点评"
            st.session_state.last_event = "已提交Agent，作品集候选+1"
            st.rerun()
        if st.session_state.submitted:
            st.markdown("<div class='ok'><b>已提交</b><br>当前任务已进入待Agent点评队列，作品集页会出现候选。</div>", unsafe_allow_html=True)
        elif st.session_state.draft_saved:
            st.markdown(f"<div class='ok'><b>已保存</b><br>保存时间：{st.session_state.saved_at}。下一步请求AI反馈或提交Agent。</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='warn'><b>下一步</b><br>先保存草稿，再请求AI反馈，最后提交Agent。</div>", unsafe_allow_html=True)
    with right:
        feedback = st.session_state.ai_feedback or "还没有请求AI反馈。\n\n点击左侧“请求AI反馈”后，这里会根据当前草稿生成反馈。"
        st.markdown(f"<div class='quote'>{feedback}</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><h3>完成标准</h3><p>1. 交付物明确<br>2. 覆盖权限、安全、边界<br>3. 可进入作品集表达</p></div>", unsafe_allow_html=True)


def portfolio() -> None:
    rows = [
        ["目标拆解", "5天成长路线图", "86", "可展示", "职业成长", "目标清晰、路径可执行。"],
        ["测试用例作品", "测试用例 + Bug报告", "64", "修改中", "软件测试", "还缺权限、安全、边界。"],
        ["复杂需求拆解", "流程 + 异常分支", "--", "待点评", "业务分析", "等待Agent正式点评。"],
    ]
    if st.session_state.portfolio_candidate:
        rows.append(["登录测试作品", "测试用例 + Bug报告草稿", "待定", "待点评", "软件测试", "已提交给Agent，等待确认是否可展示。"])
    df = pd.DataFrame(rows, columns=["作品", "证明材料", "评分", "状态", "方向", "说明"])
    st.markdown("<div class='panel'><span class='pill hot'>Portfolio Proof</span><h2>作品集会根据任务状态变化</h2><p>提交给Agent后，这里会出现新的候选作品。</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='grid3'>" + "".join(f"<div class='proof'><h3>{r.作品}</h3>{chip(r.状态)}<span class='pill purple'>{r.方向}</span><p><b>证明材料：</b>{r.证明材料}</p><p><b>评分：</b>{r.评分}</p><p>{r.说明}</p></div>" for _, r in df.iterrows()) + "</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)


def consult() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Consult Conversion</span><h2>先判断适不适合，再推荐训练路径</h2><p>生成摘要后，Founder视角会看到咨询线索 +1。</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        identity = st.selectbox("你现在属于哪类人？", ["职场新人", "在岗提升", "升职准备", "转岗 / 跳槽", "自由职业 / 副业接单", "企业培训负责人", "小微老板"])
    with c2:
        goal = st.selectbox("你最想解决什么？", ["学新技能", "提升现有技能", "做作品集", "升职表达", "换工作 / 高薪跳槽", "自由职业接单", "企业内训"])
    package, reason, steps = recommend_package(identity, goal)
    st.markdown(f"<div class='card'><h3>推荐路径：{package}</h3><p>{reason}</p><p>{' → '.join(steps)}</p></div>", unsafe_allow_html=True)
    with st.form("consult_form_v460"):
        name = st.text_input("姓名 / 称呼")
        contact = st.text_input("联系方式，选填")
        note = st.text_area("补充说明")
        ok = st.form_submit_button("生成咨询摘要")
    if ok:
        summary = f"【咨询摘要】\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n姓名：{name or '未填写'}\n联系方式：{contact or '未填写'}\n身份：{identity}\n目标：{goal}\n推荐路径：{package}\n推荐理由：{reason}\n建议步骤：{' → '.join(steps)}\n补充：{note or '无'}"
        st.session_state.consult_summary = summary
        st.session_state.last_event = "咨询摘要已生成，Founder线索+1"
        st.markdown(f"<div class='quote'>{summary}</div>", unsafe_allow_html=True)
        st.download_button("下载咨询摘要", data=summary, file_name="consult_summary.txt", mime="text/plain")
        st.success("已生成咨询摘要。切换Founder体验后首页会显示咨询线索。")
    st.markdown("<div class='grid3'><div class='card'><h3>保存为咨询线索</h3><p>后续写入 consult_leads。</p></div><div class='card'><h3>预约体验课</h3><p>后续接日历。</p></div><div class='card'><h3>发送Founder提醒</h3><p>后续接邮件/Webhook。</p></div></div>", unsafe_allow_html=True)


init_state()
page = top_nav()
login_panel()

if page == "home":
    home()
elif page == "tasks":
    tasks()
elif page == "portfolio":
    portfolio()
else:
    consult()

with st.expander("Founder OS / 后台入口"):
    st.markdown("普通用户前台只保留四个入口。Founder Console 是唯一后台页，继续单独 owner-gated。当前页面阶段不使用 st.page_link，避免 Streamlit 路径崩溃。")

st.caption("AI Skill Growth OS · Session Interaction Demo · v4.6.0")
