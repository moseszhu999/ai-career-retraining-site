from __future__ import annotations

import pandas as pd
import streamlit as st


WATERFALL_STAGES = [
    {
        "阶段": "01 战略分析",
        "核心问题": "企业为什么现在需要 AI Agent 治理，而不是再买一个 AI 工具？",
        "主要产物": "战略定位、目标客户、价值主张、业务边界、商业化假设",
        "验收门": "Founder 确认战略口径和不可销售边界",
    },
    {
        "阶段": "02 痛点把握",
        "核心问题": "客户在哪些重复工作、交付风险、人员能力证明上最痛？",
        "主要产物": "痛点清单、场景优先级、用户旅程、风险/证据需求",
        "验收门": "至少 3 个可落地试点场景进入架构设计",
    },
    {
        "阶段": "03 TOGAF 分层功能架构",
        "核心问题": "业务能力、应用模块、数据对象、技术组件如何一层层承接？",
        "主要产物": "业务架构、应用架构、数据架构、技术架构、能力-模块映射",
        "验收门": "每个模块都能追溯到痛点、能力和数据对象",
    },
    {
        "阶段": "04 数据架构",
        "核心问题": "哪些数据必须持久化，哪些证据必须可审计，哪些字段可给客户看？",
        "主要产物": "核心实体、数据关系、证据链、权限与可见性、报表口径",
        "验收门": "Proof File / Report 的数据来源可追溯",
    },
    {
        "阶段": "05 原型设计",
        "核心问题": "销售演示、Founder 后台、客户报告、学员/员工入口如何闭环？",
        "主要产物": "信息架构、页面清单、主流程、交互原型、演示路线",
        "验收门": "3 分钟销售演示和 15 分钟交付演示都能走通",
    },
    {
        "阶段": "06 技术架构",
        "核心问题": "从 Streamlit 原型如何演进到可登录、可持久化、可部署的网站？",
        "主要产物": "前端/后端/数据库/权限/部署/观测/安全架构",
        "验收门": "进入 v6 Production MVP 开发任务拆分",
    },
]


PAIN_POINTS = [
    [
        "企业老板 / 部门负责人",
        "AI 工具很多，但不知道哪些业务步骤真的能自动化",
        "自动化机会地图、价值链诊断、节省时间估算",
        "从“买工具”转向“重构流程”",
    ],
    [
        "交付经理 / 培训负责人",
        "员工会用 AI，但能力不可证明、结果不可验收",
        "任务、证据、评分、Proof File、客户安全报告",
        "把培训从上课变成可审计交付",
    ],
    [
        "一线员工 / 学员",
        "不知道如何把 AI 使用能力变成作品和岗位证明",
        "任务路线、错题记录、作品集、Proof 候选",
        "从学习过程沉淀成可展示成果",
    ],
    [
        "客户 / 合规 / 采购",
        "担心 AI 输出不可控、责任不清、证据不足",
        "审批流、证据链、责任角色、客户可见字段控制",
        "降低采购和验收阻力",
    ],
]


TOGAF_LAYERS = [
    [
        "业务架构 Business Architecture",
        "价值链诊断、痛点优先级、业务能力、流程、角色责任、治理规则",
        "Strategic Analysis Center / Pain Point Board / Capability Map / Governance Playbook",
    ],
    [
        "应用架构 Application Architecture",
        "把业务能力落成可操作模块：客户、场景、任务、评审、Proof、报告、导出",
        "Scenario Intake / Agent Workbench / Review Queue / Proof File / Report Center / Admin Console",
    ],
    [
        "数据架构 Data Architecture",
        "客户、场景、痛点、能力、任务、证据、审批、报告、审计日志",
        "Entity Model / Evidence Store / Permission View / KPI Mart / Export Dataset",
    ],
    [
        "技术架构 Technology Architecture",
        "Streamlit 原型、Supabase 持久化、权限、导出、部署、日志、安全边界",
        "Frontend Runtime / Repository Layer / Supabase / Export Service / Observability / Deployment",
    ],
]


CAPABILITY_MAP = [
    ["战略与售前", "客户画像、价值链诊断、AI 自动化机会评估、试点范围定义"],
    ["痛点与场景", "访谈记录、痛点归类、场景优先级、风险等级、客户价值假设"],
    ["Agent 工作治理", "任务资格判断、自动化等级、人类权限、审批规则、例外升级"],
    ["证据与能力证明", "提交记录、评分、错题、Proof 候选、作品集、客户可见证据"],
    ["交付与报告", "客户周报、管理层报告、Excel 导出、复盘建议、商业续约输入"],
    ["平台运营", "客户/班级/学员/题库/任务分配、Supabase 健康检查、审计日志"],
]


DATA_ENTITIES = [
    ["EnterpriseClient", "企业客户/部门/班级", "客户名称、行业、目标角色、试点范围、可见字段策略"],
    ["BusinessScenario", "业务场景", "价值链阶段、流程、角色、自动化目标、成功指标"],
    ["PainPoint", "痛点", "痛点类型、严重度、频率、影响金额/时间、证据需求"],
    ["Capability", "业务能力", "能力域、成熟度、关联流程、关联模块、KPI"],
    ["AgentWorkStep", "Agent 可执行步骤", "输入、输出、自动化等级、风险、人工确认点"],
    ["GovernancePolicy", "治理策略", "权限、审批规则、客户可见边界、不可销售承诺"],
    ["EvidenceRecord", "证据记录", "提交、评分、附件、哈希/版本、审计来源"],
    ["ProofFile", "能力证明文件", "候选来源、Founder 审批、客户展示摘要、状态"],
    ["ReadinessReport", "客户/管理层报告", "模块正确率、薄弱点、Proof 汇总、下一步建议"],
    ["AuditEvent", "审计事件", "用户、动作、时间、对象、前后状态、来源"],
]


PROTOTYPE_SCREENS = [
    ["Public Strategy Landing", "访客", "3 分钟讲清：战略定位、痛点、方法论、试点价值"],
    ["Waterfall Architecture", "Founder / 咨询顾问", "按瀑布阶段查看战略、痛点、TOGAF、数据、原型、技术"],
    ["Pain Point Board", "Founder / 客户负责人", "录入客户痛点，形成场景优先级和试点建议"],
    ["Capability Map", "Founder / 架构师", "把痛点映射到业务能力、应用模块和数据对象"],
    ["Agent Workbench", "Operator / 学员", "执行任务、提交证据、生成初评"],
    ["Review Queue", "Reviewer / Founder", "复核异常、审批 Proof、决定客户可见输出"],
    ["Report & Export Center", "Founder / 客户", "输出客户安全报告、Excel、续约输入"],
]


TECH_STACK = [
    ["Presentation", "Streamlit now; future Next.js/Vue admin console", "快速演示与后续产品化分离"],
    ["Application", "Python service modules + repository layer", "先保持低成本开发，再拆服务"],
    ["Data", "Supabase/Postgres + local session demo fallback", "客户、任务、证据、审批、报告可持久化"],
    ["Auth/RBAC", "Founder / Operator / Reviewer / Learner / Client Viewer", "不同角色看到不同数据和操作"],
    ["Evidence", "EvidenceRecord + AuditEvent + export snapshots", "Proof File 与客户报告必须可追溯"],
    ["Deployment", "Streamlit Community Cloud now; containerized deployment later", "从演示站平滑迁移到客户试点"],
    ["Observability", "health check, audit log, event timeline", "让交付过程可监控、可复盘"],
]


def _df(rows: list[list[str]], columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=columns)


def _section(title: str, body: str) -> None:
    st.markdown(
        f"""
<div class='panel'>
  <span class='pill hot'>Waterfall Delivery</span>
  <h2>{title}</h2>
  <p>{body}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def waterfall_architecture_page() -> None:
    st.markdown(
        """
<div class='executive-hero'>
  <div class='hero-glow'></div>
  <span class='pill hot'>v6.0 Waterfall Rebuild · Strategy → Pain → TOGAF → Data → Prototype → Technology</span>
  <h1>按照瀑布方法重做 AI Career Retraining Site</h1>
  <p>这页把项目从“功能堆叠”拉回到咨询公司标准交付链路：先明确战略，再抓客户痛点，然后用 TOGAF 分层承接功能架构、数据架构、原型设计和技术架构。</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section'>瀑布阶段总览</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(WATERFALL_STAGES), use_container_width=True, hide_index=True)

    _section(
        "01 战略分析",
        "战略口径从“AI 职业培训网站”升级为“企业 AI Agent 治理与能力证明系统”。客户购买的不是课程，而是价值链自动化诊断、可审计任务交付、Proof File 和管理层报告。",
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("目标客户", "小 B / 企业部门")
        st.caption("需要低成本导入 AI Agent，但缺少治理和验收体系。")
    with col2:
        st.metric("核心价值", "可证明的 AI 工作能力")
        st.caption("任务、证据、审批、报告形成闭环。")
    with col3:
        st.metric("商业入口", "诊断 + 试点 + 交付包")
        st.caption("先售卖咨询与试点，再产品化。")

    st.markdown("<div class='section'>02 痛点把握</div>", unsafe_allow_html=True)
    st.dataframe(
        _df(PAIN_POINTS, ["对象", "痛点", "系统回应", "商业意义"]),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("<div class='section'>03 TOGAF 分层功能架构</div>", unsafe_allow_html=True)
    st.dataframe(
        _df(TOGAF_LAYERS, ["TOGAF 层", "本项目要回答的问题", "落地模块"]),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("<div class='section'>业务能力地图</div>", unsafe_allow_html=True)
    st.dataframe(_df(CAPABILITY_MAP, ["能力域", "能力说明"]), use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>04 数据架构</div>", unsafe_allow_html=True)
    st.dataframe(_df(DATA_ENTITIES, ["核心实体", "业务含义", "关键字段"]), use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>05 原型设计</div>", unsafe_allow_html=True)
    st.dataframe(_df(PROTOTYPE_SCREENS, ["页面 / 原型", "主要用户", "设计目的"]), use_container_width=True, hide_index=True)

    st.markdown("<div class='section'>06 技术架构</div>", unsafe_allow_html=True)
    st.dataframe(_df(TECH_STACK, ["技术层", "建议方案", "设计理由"]), use_container_width=True, hide_index=True)

    st.markdown(
        """
<div class='panel'>
  <span class='pill green'>Next Build Gate</span>
  <h2>下一步进入 v6 Production MVP 拆分</h2>
  <p>优先级顺序：1）把痛点和场景做成可录入数据；2）把能力地图和 TOGAF 层做成可配置；3）把 Proof File 和 Report 的数据来源固定；4）再逐步替换 Streamlit 原型为正式 Web 架构。</p>
</div>
""",
        unsafe_allow_html=True,
    )
