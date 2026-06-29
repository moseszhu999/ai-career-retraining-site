from __future__ import annotations

from datetime import datetime

import streamlit as st

from frontend.data import TASKS, recommend_package
from frontend.state import ai_feedback_for, chip, history_html, log_event, login_as, logout, portfolio_df, set_view


def render_public_site() -> None:
    st.markdown("""
<div class='top'><div class='brand'>AI Skill Growth OS<small>任务驱动 · Agent反馈 · 作品集证明 · 咨询转化</small></div><div class='nav'><span class='pill'>功能</span><span class='pill'>场景</span><span class='pill'>流程</span><span class='pill'>FAQ</span><span class='pill hot'>进入体验</span></div></div>
""", unsafe_allow_html=True)
    left, right = st.columns([1.22, .78])
    with left:
        st.markdown("""
<div class='hero'><span class='pill hot'>登录前官网 · v4.7.6</span><h1>不是看课，而是每天完成一个<br><span>能变成作品集的任务</span></h1><p>AI Skill Growth OS 帮助个人、自由职业者和企业新人从“学习内容”进入“完成任务”。登录后会进入真实应用工作台：写草稿、请求AI反馈、提交Agent、沉淀作品集。</p><div class='hero-actions'><span class='pill hot'>体验学员工作台</span><span class='pill'>查看任务闭环</span><span class='pill'>生成咨询路径</span></div></div>
""", unsafe_allow_html=True)
        st.markdown("<div class='result-strip'><div><b>1</b><br><span class='mini'>今日主任务</span></div><div><b>3</b><br><span class='mini'>核心交付物</span></div><div><b>5</b><br><span class='mini'>天成长闭环</span></div><div><b>∞</b><br><span class='mini'>后续作品复用</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>适合的用户场景</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid3'><div class='card'><h3>个人成长 / 转岗</h3><p>每天完成一个可检查任务，最后沉淀成面试、汇报或自我提升材料。</p></div><div class='card'><h3>自由职业 / 一人公司</h3><p>把技能包装成服务样品、客户案例、报价表达和可交付证明。</p></div><div class='card'><h3>企业新人训练</h3><p>把部门高频任务变成训练卡，用Agent初评，主管只看异常和结果。</p></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>登录后会发生什么</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid4'><div class='flow-step'><b>1. 进入工作台</b><br><span class='mini'>看到当前任务、状态、草稿和下一步。</span></div><div class='flow-step'><b>2. 写草稿</b><br><span class='mini'>在任务编辑器中完成交付物。</span></div><div class='flow-step'><b>3. 请求反馈</b><br><span class='mini'>AI指出权限、安全、边界等缺口。</span></div><div class='flow-step'><b>4. 进入作品集</b><br><span class='mini'>提交Agent后成为作品候选。</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>FAQ</div>", unsafe_allow_html=True)
        st.markdown("<div class='faq'><b>这是课程平台吗？</b><br><span class='mini'>不是传统课程后台，核心是任务、反馈和作品集证明。</span></div><div class='faq'><b>现在接数据库了吗？</b><br><span class='mini'>当前先做前端交互，数据暂存在 session_state，后续接 Supabase。</span></div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='login-box'><div class='panel'><h2>进入体验</h2><p>先用前端 session 模拟登录。体验流程顺了，再接真实 Auth / Supabase。</p></div>", unsafe_allow_html=True)
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
        st.markdown("<div class='card'><h3>推荐体验顺序</h3><p>1. 学员Demo<br>2. 我的任务<br>3. 保存草稿 / 请求反馈 / 提交Agent<br>4. 作品集候选<br>5. 咨询漏斗<br>6. FounderDemo处理队列</p></div></div>", unsafe_allow_html=True)


def render_app_top() -> None:
    st.markdown(f"""
<div class='top'><div class='brand'>AI Skill Growth OS<small>Logged-in App · {st.session_state.role}</small></div><div>{chip(st.session_state.role)}<span class='pill'>{st.session_state.user_name}</span><span class='pill'>最近：{st.session_state.last_event}</span></div></div>
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
    next_text = "等待Agent点评" if st.session_state.submitted else "继续完成测试用例作品"
    st.markdown(f"""
<div class='hero'><span class='pill hot'>Student Dashboard · v4.7.6</span><h1>{st.session_state.user_name}，今天继续：<br><span>Day 2 · 测试用例作品</span></h1><p>这是登录后的学习工作台。你不需要找菜单，只要看清楚今天做什么、做到哪里、下一步是什么。</p><span class='pill'>任务状态：{st.session_state.task_status}</span><span class='pill'>AI反馈：{feedback_state}</span><span class='pill'>作品集：{candidate_state}</span><span class='pill'>线索：{st.session_state.lead_status}</span></div>
""", unsafe_allow_html=True)
    st.markdown(f"<div class='grid4'><div class='card'><span class='mini'>今日任务</span><div class='metric'>Day 2</div><p>测试用例作品</p></div><div class='card'><span class='mini'>训练进度</span><div class='metric'>40%</div><div class='progress'><div class='bar' style='width:40%'></div></div></div><div class='card'><span class='mini'>作品候选</span><div class='metric'>{1 if st.session_state.portfolio_candidate else 0}</div></div><div class='card'><span class='mini'>咨询状态</span><p>{chip(st.session_state.lead_status)}</p></div></div>", unsafe_allow_html=True)
    left, right = st.columns([1.25, .75])
    with left:
        st.markdown(f"<div class='next-action'><h2>下一步：{next_text}</h2><p>建议顺序：保存草稿 → 请求AI反馈 → 根据反馈补权限/安全/边界 → 提交Agent。</p><div class='progress'><div class='bar' style='width:{70 if st.session_state.task_status != '未开始' else 25}%'></div></div></div>", unsafe_allow_html=True)
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
        st.markdown("<div class='section'>学习路径</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid3'><div class='card'><h3>已完成</h3><p>目标拆解已经进入可展示作品。</p></div><div class='card decision'><h3>今日主任务</h3><p>补齐登录测试用例和Bug报告。</p></div><div class='card'><h3>下一阶段</h3><p>复杂需求拆解等待点评和复盘。</p></div></div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'><h3>最近AI反馈</h3><p>" + (st.session_state.ai_feedback[:120] + "..." if st.session_state.ai_feedback else "还没有请求AI反馈。") + "</p></div>", unsafe_allow_html=True)
        st.markdown(history_html(), unsafe_allow_html=True)


def founder_dashboard() -> None:
    pending = 1 if st.session_state.submitted else 0
    candidates = 1 if st.session_state.portfolio_candidate else 0
    leads = 1 if st.session_state.consult_summary else 0
    priority = "先处理咨询线索" if leads else ("先处理待点评作品" if pending else "暂无紧急事项")
    st.markdown(f"""
<div class='hero'><span class='pill hot'>Founder Dashboard · v4.7.6</span><h1>今天只看需要你决策的事</h1><p>Founder 首页不是普通后台，而是运营决策台：待点评、作品候选、咨询线索、最近操作和今日建议。</p><span class='pill'>今日建议：{priority}</span></div>
""", unsafe_allow_html=True)
    st.markdown(f"<div class='grid4'><div class='card decision'><span class='mini'>待Agent点评</span><div class='metric'>{pending}</div><p>来自学员提交。</p></div><div class='card decision'><span class='mini'>作品候选</span><div class='metric'>{candidates}</div><p>等待确认是否可展示。</p></div><div class='card decision'><span class='mini'>咨询线索</span><div class='metric'>{leads}</div><p>{chip(st.session_state.lead_status)}</p></div><div class='card'><span class='mini'>最近动作</span><p>{st.session_state.last_event}</p></div></div>", unsafe_allow_html=True)
    left, right = st.columns([1.2, .8])
    with left:
        st.markdown("<div class='section'>今日决策队列</div>", unsafe_allow_html=True)
        _render_founder_decisions()
    with right:
        st.markdown("<div class='section'>今日运营建议</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><h3>{priority}</h3><p>优先处理能影响转化和作品集质量的事项。</p></div>", unsafe_allow_html=True)
        st.markdown(history_html(), unsafe_allow_html=True)


def tasks_page() -> None:
    active = TASKS.iloc[int(st.session_state.active_task_index)]
    st.markdown("<div class='panel'><span class='pill hot'>My Tasks</span><h2>任务工作台</h2><p>左侧选任务，中间编辑交付物，右侧看反馈、状态和操作历史。</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='grid4'><div class='card'><span class='mini'>当前任务</span><div class='metric'>{active['day']}</div><p>{active['title']}</p></div><div class='card'><span class='mini'>任务状态</span><p>{chip(st.session_state.task_status)}</p></div><div class='card'><span class='mini'>草稿字数</span><div class='metric'>{len(st.session_state.draft)}</div></div><div class='card'><span class='mini'>作品候选</span><div class='metric'>{1 if st.session_state.portfolio_candidate else 0}</div></div></div>", unsafe_allow_html=True)
    left, mid, right = st.columns([.85, 1.35, .95])
    with left:
        st.markdown("<div class='task-rail'><h3>任务列表</h3>", unsafe_allow_html=True)
        for idx, row in TASKS.iterrows():
            active_class = " active" if idx == st.session_state.active_task_index else ""
            st.markdown(f"<div class='task-mini{active_class}'><b>{row['day']} · {row['title']}</b>{chip(row['focus'])}<div class='progress'><div class='bar' style='width:{row['progress']}%'></div></div></div>", unsafe_allow_html=True)
            if st.button(f"打开 {row['day']}", key=f"open_task_{idx}", use_container_width=True):
                st.session_state.active_task_index = int(idx)
                log_event(f"切换任务：{row['day']} {row['title']}")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with mid:
        st.markdown(f"<div class='editor'><h3>{active['day']} · {active['title']}</h3><p><b>任务说明：</b>{active['brief']}<br><b>交付物：</b>{active['outcome']}<br><b>状态：</b>{chip(st.session_state.task_status)}</p></div>", unsafe_allow_html=True)
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
        st.markdown(history_html(), unsafe_allow_html=True)


def portfolio_page() -> None:
    df = portfolio_df()
    visible_df = df
    st.markdown("<div class='panel'><span class='pill hot'>Portfolio</span><h2>作品集工作台</h2><p>作品集不只是卡片列表，而是证明材料管理页。</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='grid4'><div class='card'><span class='mini'>全部作品</span><div class='metric'>{len(df)}</div></div><div class='card'><span class='mini'>可展示</span><div class='metric'>{int((df['状态'] == '可展示').sum())}</div></div><div class='card'><span class='mini'>修改中</span><div class='metric'>{int((df['状态'] == '修改中').sum())}</div></div><div class='card'><span class='mini'>待点评</span><div class='metric'>{int((df['状态'] == '待点评').sum())}</div></div></div>", unsafe_allow_html=True)
    status_filter = st.selectbox("状态筛选", ["全部", "可展示", "修改中", "待点评"])
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
        st.markdown("<div class='list-panel'><h3>作品列表</h3>", unsafe_allow_html=True)
        for pos, (_, row) in enumerate(visible_df.iterrows()):
            active_class = " active" if pos == st.session_state.active_portfolio_index else ""
            st.markdown(f"<div class='list-item{active_class}'><b>{row['作品']}</b>{chip(row['状态'])}<span class='pill purple'>{row['方向']}</span><p class='mini'>{row['证明材料']}</p></div>", unsafe_allow_html=True)
            if st.button(f"查看作品 {pos + 1}", key=f"portfolio_open_{pos}", use_container_width=True):
                st.session_state.active_portfolio_index = pos
                log_event(f"查看作品：{row['作品']}")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with mid:
        st.markdown(f"<div class='detail'><h3>{active['作品']}</h3>{chip(active['状态'])}<span class='pill purple'>{active['方向']}</span><p><b>证明材料：</b>{active['证明材料']}<br><b>评分：</b>{active['评分']}<br><b>说明：</b>{active['说明']}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='quote'>【Agent点评摘要】\n{active['Agent摘要']}\n\n建议按“背景 → 方法 → 结果 → 证据 → 复盘”整理成可展示版本。</div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>证据结构</div>", unsafe_allow_html=True)
        st.markdown("<div class='evidence-grid'><div class='evidence'><b>背景</b><br><span class='mini'>为什么做这个作品。</span></div><div class='evidence'><b>方法</b><br><span class='mini'>如何拆解、设计或测试。</span></div><div class='evidence'><b>结果</b><br><span class='mini'>最终产出材料。</span></div><div class='evidence'><b>复盘</b><br><span class='mini'>如何根据反馈改进。</span></div></div>", unsafe_allow_html=True)
    with right:
        st.markdown(f"<div class='score-card'><span class='mini'>作品评分</span><br><b>{active['评分']}</b><p>{active['状态']}</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><h3>可展示检查</h3><p>1. 别人能看懂<br>2. 有证明材料<br>3. 可复用到面试/客户/汇报<br>4. 有Agent点评记录</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='share-grid'><div><b>导出PDF</b></div><div><b>分享链接</b></div><div><b>加入咨询材料</b></div></div>", unsafe_allow_html=True)
        st.markdown(history_html(), unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)


def consult_page() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Consult Funnel</span><h2>咨询转化漏斗</h2><p>咨询页把用户场景转成方案、摘要和Founder线索状态。</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='grid4'><div class='card'><span class='mini'>当前线索</span><div class='metric'>{1 if st.session_state.consult_summary else 0}</div></div><div class='card'><span class='mini'>线索状态</span><p>{chip(st.session_state.lead_status)}</p></div><div class='card'><span class='mini'>作品候选</span><div class='metric'>{1 if st.session_state.portfolio_candidate else 0}</div></div><div class='card'><span class='mini'>最近动作</span><p>{st.session_state.last_event}</p></div></div>", unsafe_allow_html=True)
    left, mid, right = st.columns([.95, 1.25, .95])
    with left:
        st.markdown("<div class='funnel-panel'><h3>1. 场景识别</h3><p class='mini'>先判断用户是谁、想解决什么。</p>", unsafe_allow_html=True)
        identity = st.selectbox("你现在属于哪类人？", ["职场新人", "在岗提升", "升职准备", "转岗 / 跳槽", "自由职业 / 副业接单", "企业培训负责人", "小微老板"])
        goal = st.selectbox("你最想解决什么？", ["学新技能", "提升现有技能", "做作品集", "升职表达", "换工作 / 高薪跳槽", "自由职业接单", "企业内训"])
        urgency = st.selectbox("希望多快看到结果？", ["先体验", "7天内", "30天内", "尽快转化/交付"])
        st.markdown("</div><div class='flow-step'><b>漏斗阶段</b><br>访问 → 识别场景 → 推荐方案 → 生成摘要 → Founder跟进</div>", unsafe_allow_html=True)
    package, reason, steps, deliverables = recommend_package(identity, goal)
    with mid:
        st.markdown(f"<div class='plan-card'><h3>2. 推荐方案：{package}</h3>{chip('推荐')}<p>{reason}</p></div>", unsafe_allow_html=True)
        for idx, step in enumerate(steps, start=1):
            st.markdown(f"<div class='step-line'><b>{idx}. {step}</b><br><span class='mini'>后续可接真实任务模板。</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='section'>适合交付物</div>", unsafe_allow_html=True)
        st.markdown("<div class='grid2'>" + "".join(f"<div class='card'><h3>{item}</h3><p>可作为咨询后续材料。</p></div>" for item in deliverables) + "</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='lead-card'><h3>3. 线索摘要</h3><p>生成后会进入Founder线索队列。</p>", unsafe_allow_html=True)
        with st.form("consult_form_v476"):
            name = st.text_input("姓名 / 称呼")
            contact = st.text_input("联系方式，选填")
            note = st.text_area("补充说明", placeholder="例如：我想转测试岗 / 我想把Java培训做成产品包")
            ok = st.form_submit_button("生成咨询摘要", type="primary")
        if ok:
            summary = f"【咨询摘要】\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n姓名：{name or '未填写'}\n联系方式：{contact or '未填写'}\n身份：{identity}\n目标：{goal}\n时效：{urgency}\n推荐路径：{package}\n推荐理由：{reason}\n建议步骤：{' → '.join(steps)}\n建议交付物：{' / '.join(deliverables)}\n补充：{note or '无'}"
            st.session_state.consult_summary = summary
            st.session_state.lead_status = "新线索"
            log_event("咨询摘要已生成，Founder线索+1")
            st.rerun()
        if st.session_state.consult_summary:
            st.markdown(f"<div class='quote'>{st.session_state.consult_summary}</div>", unsafe_allow_html=True)
            st.download_button("下载咨询摘要", data=st.session_state.consult_summary, file_name="consult_summary.txt", mime="text/plain")
        st.markdown("</div>", unsafe_allow_html=True)
        cta1, cta2 = st.columns(2)
        if cta1.button("加入Founder跟进", use_container_width=True):
            st.session_state.lead_status = "新线索"
            log_event("咨询线索已加入Founder跟进")
            st.rerun()
        if cta2.button("预约体验课", use_container_width=True):
            st.session_state.lead_status = "已预约"
            log_event("用户点击预约体验课")
            st.rerun()
        st.markdown(history_html(), unsafe_allow_html=True)


def founder_queue() -> None:
    st.markdown("<div class='panel'><span class='pill hot'>Founder Queue</span><h2>运营队列</h2><p>这里模拟 Founder 登录后的处理动作。</p></div>", unsafe_allow_html=True)
    _render_founder_decisions(empty_hint=True)


def _render_founder_decisions(empty_hint: bool = False) -> None:
    pending = bool(st.session_state.submitted)
    leads = bool(st.session_state.consult_summary)
    if not pending and not leads:
        if empty_hint:
            st.info("暂无待处理事项。用学员身份提交任务或生成咨询摘要后，这里会出现队列。")
        return
    if pending:
        st.markdown("<div class='queue-card decision'><h3>待点评：登录测试作品</h3><p>学员已提交草稿。建议先确认是否进入作品集，或打回补充权限/安全/边界。</p></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("确认进入作品集", type="primary", use_container_width=True):
            st.session_state.portfolio_approved = True
            st.session_state.task_status = "Agent已点评"
            log_event("Founder确认作品集")
            st.rerun()
        if c2.button("打回修改", use_container_width=True):
            st.session_state.task_status = "AI已反馈"
            st.session_state.submitted = False
            log_event("Founder打回修改")
            st.rerun()
    if leads:
        st.markdown(f"<div class='queue-card decision'><h3>咨询线索 {chip(st.session_state.lead_status)}</h3><p>{st.session_state.consult_summary.replace(chr(10), '<br>')}</p></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        if c1.button("已联系", use_container_width=True):
            st.session_state.lead_status = "已联系"
            log_event("Founder标记线索已联系")
            st.rerun()
        if c2.button("已预约", use_container_width=True):
            st.session_state.lead_status = "已预约"
            log_event("Founder标记线索已预约")
            st.rerun()
        if c3.button("已成交", type="primary", use_container_width=True):
            st.session_state.lead_status = "已成交"
            log_event("Founder标记线索已成交")
            st.rerun()
