from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.business_data import CLIENTS, COHORTS, LEARNERS, get_business_metrics
from frontend.exercise_bank import get_exercise_metrics
from frontend.state import login_as, set_view


def _accuracy_text(total: int, correct: int) -> str:
    if total <= 0:
        return "0%"
    return f"{correct / total * 100:.1f}%"


def _proof_candidates() -> pd.DataFrame:
    queue = ops.review_queue_view()
    if queue.empty or "review_route" not in queue.columns:
        return pd.DataFrame()
    return queue[queue["review_route"] == "Proof候选"].copy()


def _agent_human_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["价值链诊断", "提取访谈纪要、归类人工环节、生成机会草案", "确认客户真实痛点、选择优先价值链阶段", "Business Owner / Founder"],
            ["业务流程设计", "把人工步骤拆成可自动化任务，生成流程草稿", "确认流程边界、责任分工、例外路径", "Process Owner"],
            ["任务执行", "生成选择题、任务 Brief、代码/报告/测试草稿", "确认业务意图、范围、客户承诺边界", "Agent Operator / Instructor"],
            ["证据与初评", "记录选择项、正确项、自动分、错题、Proof 候选", "复核异常、确认是否需要重做或补证据", "Reviewer"],
            ["审批与发布", "建议分流：需复习 / Proof候选 / Founder复核", "最终批准进入 Proof Files 或客户报告", "Founder / Approver"],
            ["客户交付", "生成客户安全周报、Excel、复习建议", "决定客户可见字段、价格和后续商业动作", "Founder / Account Owner"],
        ],
        columns=["业务环节", "Agent 做", "人类做 / 批示", "责任角色"],
    )


def _workflow_html() -> str:
    return """
<div class='workflow-strip'>
  <div class='workflow-node blm'><span>01</span><b>BLM / 价值链</b><p>定位价值链痛点、人工成本、可自动化机会。</p></div>
  <div class='workflow-arrow'>→</div>
  <div class='workflow-node process'><span>02</span><b>业务流程</b><p>拆人工步骤，定义 Agent 自动化点和人类审批点。</p></div>
  <div class='workflow-arrow'>→</div>
  <div class='workflow-node agent'><span>03</span><b>Agent 执行</b><p>生成任务、选择题、草稿、初评和证据包。</p></div>
  <div class='workflow-arrow'>→</div>
  <div class='workflow-node human'><span>04</span><b>人类审批</b><p>复核风险、确认 Proof、决定客户可见输出。</p></div>
  <div class='workflow-arrow'>→</div>
  <div class='workflow-node proof'><span>05</span><b>Proof / Report</b><p>输出客户安全周报、Proof Files、复习建议。</p></div>
</div>
"""


def render_executive_public_site() -> None:
    business_metrics = get_business_metrics()
    exercise_metrics = get_exercise_metrics()
    op = ops.operation_metrics()
    candidates = _proof_candidates()
    accuracy = _accuracy_text(op.get("mcq_total", 0), op.get("mcq_correct", 0))

    st.markdown("""
<div class='executive-hero'>
  <div class='hero-glow'></div>
  <span class='pill hot'>Value Chain AI Agent Governance OS · v4.22.0</span>
  <h1>让 AI Agent 替代价值链中的重复工作，<br><span>同时保留证据、审批和责任链。</span></h1>
  <p>从 BLM 价值链诊断开始，落到业务流程，再进入 Agent 执行、人类批示、Proof Files 和客户安全报告。不是 AI 工具演示，而是企业级自动化治理闭环。</p>
  <div class='hero-actions'><span class='pill green'>价值链自动化诊断</span><span class='pill blue'>Agent / Human 分工</span><span class='pill purple'>Proof Files</span><span class='pill orange'>客户安全交付包</span></div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class='grid4'>
  <div class='executive-metric'><span>客户 / 班级</span><b>{len(CLIENTS)} / {len(COHORTS)}</b><p>从企业客户、部门或班级切入。</p></div>
  <div class='executive-metric'><span>选择题任务</span><b>{exercise_metrics.get('mcq_count', 0)}</b><p>低操作成本，适合真实训练运营。</p></div>
  <div class='executive-metric'><span>MCQ 正确率</span><b>{accuracy}</b><p>直接形成模块薄弱点和复习建议。</p></div>
  <div class='executive-metric'><span>Proof 候选</span><b>{len(candidates)}</b><p>可进入客户汇报和作品证明。</p></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='section'>产品主流程</div>", unsafe_allow_html=True)
    st.markdown(_workflow_html(), unsafe_allow_html=True)

    left, right = st.columns([1.15, .85])
    with left:
        st.markdown("""
<div class='panel'><span class='pill hot'>Agent / Human / Approval Design</span><h2>不是让 Agent 乱跑，而是把每一步责任写清楚</h2><p>企业真正购买的不是“AI 会生成内容”，而是：哪些工作可以自动化、哪些必须人类审批、哪些证据可以对客户展示。</p></div>
""", unsafe_allow_html=True)
        st.dataframe(_agent_human_matrix(), use_container_width=True, hide_index=True)

    with right:
        st.markdown("""
<div class='login-box'><div class='lux-login'><span class='pill hot'>进入工作台</span><h2>Executive Demo Login</h2><p>Founder 看运营、审批和客户交付；学员看选择题、错题和 Proof Files。</p>
""", unsafe_allow_html=True)
        with st.form("executive_login_form"):
            name = st.text_input("姓名 / 体验名", value="Founder")
            role = st.selectbox("选择身份", ["Founder", "学员"])
            submitted = st.form_submit_button("进入 Agent 治理工作台", type="primary")
        if submitted:
            login_as(role, name)
            if role == "学员":
                st.session_state.selected_learner_id = "jhc-s01"
            st.rerun()
        c1, c2 = st.columns(2)
        if c1.button("Founder 控制台", type="primary", use_container_width=True):
            login_as("Founder", "Founder")
            st.rerun()
        if c2.button("学员体验", use_container_width=True):
            login_as("学员", "佐藤拓海")
            st.session_state.selected_learner_id = "jhc-s01"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section'>客户看到的不是后台，而是可解释结果</div>", unsafe_allow_html=True)
    st.markdown("""
<div class='grid3'>
  <div class='card decision'><h3>1. 价值链机会图</h3><p>说明哪些人工环节能被 Agent 自动化，预估节省时间和风险。</p></div>
  <div class='card decision'><h3>2. 治理流程图</h3><p>说明 Agent 做什么、人类复核什么、Founder 批示什么。</p></div>
  <div class='card decision'><h3>3. Proof 交付包</h3><p>输出选择题表现、模块正确率、错题复习、Proof Files 和客户周报。</p></div>
</div>
""", unsafe_allow_html=True)


def founder_executive_dashboard() -> None:
    op = ops.operation_metrics()
    module_stats = ops.mcq_module_stats()
    wrong = ops.wrong_answer_records()
    candidates = _proof_candidates()
    queue = ops.review_queue_view()
    accuracy = _accuracy_text(op.get("mcq_total", 0), op.get("mcq_correct", 0))

    st.markdown(f"""
<div class='executive-hero dashboard-hero'>
  <span class='pill hot'>Founder Command Center · v4.22.0</span>
  <h1>Agent 工作进入企业流程前，<br><span>先看证据、风险、审批和客户可见性。</span></h1>
  <p>这里不是普通后台首页，而是 Founder 的运营驾驶舱：看价值链自动化进展、选择题质量、Review 分流、Proof 候选、客户交付动作。</p>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class='grid4'>
  <div class='executive-metric'><span>MCQ 正确率</span><b>{accuracy}</b><p>{op.get('mcq_correct', 0)} / {op.get('mcq_total', 0)} 正确</p></div>
  <div class='executive-metric'><span>需复习</span><b>{len(wrong)}</b><p>错题进入复习名单。</p></div>
  <div class='executive-metric'><span>Proof 候选</span><b>{len(candidates)}</b><p>等待 Founder 批示。</p></div>
  <div class='executive-metric'><span>客户交付资产</span><b>{op.get('proof_files', 0)}</b><p>已沉淀 Proof Files。</p></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='section'>端到端治理流程</div>", unsafe_allow_html=True)
    st.markdown(_workflow_html(), unsafe_allow_html=True)

    st.markdown("<div class='section'>Agent 做什么 / 人类做什么 / 谁批示</div>", unsafe_allow_html=True)
    st.dataframe(_agent_human_matrix(), use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>Founder 今日处理台</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("处理 Review Queue", type="primary", use_container_width=True):
        set_view("queue")
        st.rerun()
    if c2.button("查看报表", use_container_width=True):
        set_view("report")
        st.rerun()
    if c3.button("导出客户包", use_container_width=True):
        set_view("export")
        st.rerun()
    if c4.button("管理练习题", use_container_width=True):
        set_view("tasks")
        st.rerun()

    left, right = st.columns([1.05, .95])
    with left:
        st.markdown("<div class='section'>模块薄弱点</div>", unsafe_allow_html=True)
        if module_stats.empty:
            st.info("暂无模块正确率。")
        else:
            st.dataframe(module_stats, use_container_width=True, hide_index=True)
        st.markdown("<div class='section'>Review 分流预览</div>", unsafe_allow_html=True)
        if queue.empty:
            st.info("暂无 Review Queue。")
        else:
            cols = [c for c in ["learner_name", "exercise_id", "module", "selected_option", "correct_option", "is_correct", "auto_score", "review_route"] if c in queue.columns]
            st.dataframe(queue[cols].head(8), use_container_width=True, hide_index=True)
    with right:
        st.markdown("<div class='section'>客户价值叙事</div>", unsafe_allow_html=True)
        st.markdown("""
<div class='card decision'><h3>客户买到什么？</h3><p>不是买选择题，也不是买 AI 工具；客户买的是一套能证明“AI Agent 替代了哪些人工环节，同时风险仍可控”的运营证据。</p></div>
<div class='card'><h3>下一步批示</h3><p>优先处理 Proof 候选；对错题集中模块安排复习；将达标 Proof Files 输出到客户安全周报。</p></div>
""", unsafe_allow_html=True)
        if not candidates.empty:
            st.markdown("<div class='section'>Proof 候选</div>", unsafe_allow_html=True)
            cols = [c for c in ["learner_name", "exercise_id", "module", "auto_score", "score", "decision", "proof_ready"] if c in candidates.columns]
            st.dataframe(candidates[cols].head(5), use_container_width=True, hide_index=True)
