from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend import operation_state as ops
from frontend.state import set_view


def _workflow_blueprints() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "process_id": "wf-001",
                "process_name": "Lead-to-Proposal Automation",
                "value_chain_stage": "Market / Lead -> Customer Need -> Solution / Proposal",
                "business_goal": "缩短售前响应时间，把客户需求转成可控提案。",
                "agent_work": "整理客户背景、提取需求、生成提案大纲、列出风险声明和后续动作。",
                "human_work": "确认真实购买场景、价格边界、承诺范围、客户关系和优先级。",
                "approval_rule": "涉及价格、承诺、客户可见材料时必须 Founder / Account Owner 批准。",
                "proof_output": "客户需求摘要、提案草稿、沟通记录、客户安全跟进报告。",
                "target_view": "consult",
            },
            {
                "process_id": "wf-002",
                "process_name": "Requirement-to-Delivery Automation",
                "value_chain_stage": "Customer Need -> Delivery / Execution -> Quality / Acceptance",
                "business_goal": "把需求、实现、测试、验收证据串成可审计交付链。",
                "agent_work": "总结需求、生成测试点、建议代码/报告草稿、检查异常分支和验收材料。",
                "human_work": "确认业务含义、影响范围、安全风险、合并决策和客户验收口径。",
                "approval_rule": "影响客户交付、代码合并、质量验收时必须 Reviewer / Founder 复核。",
                "proof_output": "Requirement Proof、测试证据、Review 记录、Proof File。",
                "target_view": "tasks",
            },
            {
                "process_id": "wf-003",
                "process_name": "Training-to-Readiness Automation",
                "value_chain_stage": "HR / Training -> Readiness Decision -> Manager Report",
                "business_goal": "把新人训练转成可评分、可复习、可证明的能力成长路径。",
                "agent_work": "生成选择题、自动评分、错题归类、模块正确率、Proof 候选。",
                "human_work": "确认题目质量、复核错题原因、决定是否进入 Proof Files。",
                "approval_rule": "Proof 候选进入客户报告前必须 Founder 确认。",
                "proof_output": "MCQ 正确率、错题复习、模块薄弱点、Proof Files、客户周报。",
                "target_view": "queue",
            },
            {
                "process_id": "wf-004",
                "process_name": "Support-to-Knowledge Automation",
                "value_chain_stage": "Customer Success / Support -> Knowledge Management",
                "business_goal": "把客户问题转成可复用知识和客户安全回复。",
                "agent_work": "总结问题、生成回复草稿、建议 FAQ/KB 条目、识别升级风险。",
                "human_work": "确认事实、客户上下文、语气、敏感信息和升级路径。",
                "approval_rule": "客户可见回复、知识库发布和升级判断必须人工确认。",
                "proof_output": "客户回复记录、KB 草稿、支持复盘、知识库更新摘要。",
                "target_view": "report",
            },
        ]
    )


def _swimlane_steps(process_name: str) -> pd.DataFrame:
    common = [
        ["01", "Business", "识别价值链痛点", "Founder / Business Owner", "选择要自动化的业务场景"],
        ["02", "Agent", "生成流程草案和任务拆解", "AI Agent", "输出可执行步骤和证据清单"],
        ["03", "Human", "确认业务边界和责任", "Process Owner / Instructor", "确认哪些能自动化、哪些必须人工"],
        ["04", "Agent", "执行自动化工作和初评", "AI Agent", "生成选择题、草稿、自动分、错题、Proof 候选"],
        ["05", "Human", "复核异常和风险", "Reviewer", "打回、要求复习、要求补证据"],
        ["06", "Approval", "批准进入 Proof / Report", "Founder / Approver", "决定客户可见输出"],
        ["07", "Report", "生成客户安全交付包", "Founder + Agent", "输出客户周报、Excel、Proof Files"],
    ]
    df = pd.DataFrame(common, columns=["step", "lane", "work", "owner", "approval_point"])
    df["process_name"] = process_name
    return df


def _lane_html(lane: str, steps: pd.DataFrame) -> str:
    rows = steps[steps["lane"] == lane]
    if rows.empty:
        return ""
    items = "".join(
        f"<div class='task-mini'><b>{r.step}. {r.work}</b><br><span class='mini'>{r.owner}</span><p>{r.approval_point}</p></div>"
        for r in rows.itertuples()
    )
    return f"<div class='list-panel'><h3>{lane}</h3>{items}</div>"


def workflow_blueprint_page() -> None:
    blueprints = _workflow_blueprints()
    queue = ops.review_queue_view()
    wrong = ops.wrong_answer_records()
    candidates = queue[queue["review_route"] == "Proof候选"] if not queue.empty and "review_route" in queue.columns else pd.DataFrame()

    st.markdown(
        """
<div class='executive-hero dashboard-hero'>
  <span class='pill hot'>Workflow Blueprint Center · v4.24.0</span>
  <h1>把业务流程设计成<br><span>Agent 泳道、人类泳道、审批泳道。</span></h1>
  <p>这里说明每个业务流程中，哪些工作交给 Agent，哪些工作由人类确认，哪些节点必须 Founder / Approver 批示。</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(f"""
<div class='grid4'>
  <div class='executive-metric'><span>业务流程</span><b>{len(blueprints)}</b><p>从价值链机会转成可执行流程。</p></div>
  <div class='executive-metric'><span>Review 待处理</span><b>{len(queue)}</b><p>Agent 输出进入复核队列。</p></div>
  <div class='executive-metric'><span>需复习</span><b>{len(wrong)}</b><p>错题和薄弱模块进入复习。</p></div>
  <div class='executive-metric'><span>Proof 候选</span><b>{len(candidates)}</b><p>等待 Founder 批示。</p></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='section'>业务流程蓝图</div>", unsafe_allow_html=True)
    st.dataframe(
        blueprints[["process_id", "process_name", "value_chain_stage", "business_goal", "approval_rule"]],
        use_container_width=True,
        hide_index=True,
    )

    selected_name = st.selectbox("选择流程查看泳道", blueprints["process_name"].tolist())
    blueprint = blueprints[blueprints["process_name"] == selected_name].iloc[0]
    steps = _swimlane_steps(selected_name)

    st.markdown(
        f"""
<div class='panel'>
  <span class='pill hot'>{blueprint['process_id']} · {blueprint['process_name']}</span>
  <h2>{blueprint['business_goal']}</h2>
  <p><b>价值链阶段：</b>{blueprint['value_chain_stage']}<br>
  <b>审批规则：</b>{blueprint['approval_rule']}<br>
  <b>Proof 输出：</b>{blueprint['proof_output']}</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section'>Agent / Human / Approval 泳道</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
<div class='grid4'>
  {_lane_html('Business', steps)}
  {_lane_html('Agent', steps)}
  {_lane_html('Human', steps)}
  {_lane_html('Approval', steps)}
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class='grid2'>
  {_lane_html('Report', steps)}
  <div class='card decision'><h3>当前流程批示口径</h3><p><b>Agent 做：</b>{blueprint['agent_work']}</p><p><b>人类做：</b>{blueprint['human_work']}</p><p><b>Founder 批示：</b>{blueprint['approval_rule']}</p></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section'>进入对应操作</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("进入该流程操作页", type="primary", use_container_width=True):
        set_view(str(blueprint["target_view"]))
        st.rerun()
    if c2.button("处理 Review Queue", use_container_width=True):
        set_view("queue")
        st.rerun()
    if c3.button("导出客户报告", use_container_width=True):
        set_view("export")
        st.rerun()

    st.markdown("<div class='section'>审批规则表</div>", unsafe_allow_html=True)
    rules = pd.DataFrame(
        [
            ["选错 / 自动分低于 80", "Agent 标记需复习", "讲师安排复习", "不进入 Proof"],
            ["选对 / 自动分 >= 80", "Agent 标记 Proof候选", "Reviewer 复核证据", "Founder 批准进入 Proof"],
            ["客户可见报告", "Agent 生成客户安全版", "Founder 检查字段白名单", "批准导出 / 发送"],
            ["价格、承诺、范围变化", "Agent 只做草案", "Account Owner 判断商业风险", "Founder 最终批示"],
        ],
        columns=["触发条件", "Agent 动作", "人类动作", "审批结果"],
    )
    st.dataframe(rules, use_container_width=True, hide_index=True)
