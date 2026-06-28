from __future__ import annotations

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI 时代职业再训练",
    page_icon="🧭",
    layout="wide",
)

st.markdown(
    """
<style>
.main .block-container{max-width:1120px;padding-top:1rem;padding-bottom:3rem}
.hero{padding:2.2rem;border:1px solid #c7d2fe;border-radius:1.35rem;background:linear-gradient(135deg,#eef2ff 0%,#f8fafc 58%,#ecfeff 100%);box-shadow:0 14px 38px rgba(15,23,42,.08);margin-bottom:1rem}
.hero h1{margin:0 0 .75rem 0;font-size:2.75rem;line-height:1.08;color:#0f172a}.hero p{font-size:1.1rem;color:#475569;line-height:1.72;max-width:900px}.eyebrow{font-size:.8rem;letter-spacing:.13em;color:#4f46e5;font-weight:900;text-transform:uppercase}.hero b{color:#312e81}
.card{border:1px solid #e2e8f0;border-radius:1rem;background:#fff;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.04);min-height:132px;margin-bottom:.8rem}.card b{color:#0f172a}.card p{color:#64748b;line-height:1.58}.card strong{color:#4338ca}
.loop{display:grid;grid-template-columns:repeat(5,1fr);gap:.65rem;margin:1rem 0}.loop div{border:1px solid #c7d2fe;background:#fff;border-radius:1rem;padding:.85rem;text-align:center}.loop b{display:block;color:#4f46e5}.loop span{font-weight:850;color:#312e81;font-size:.82rem}
.cta{border:1px solid #bbf7d0;background:#f0fdf4;border-radius:1.2rem;padding:1.2rem;margin:1.2rem 0;box-shadow:0 8px 24px rgba(15,23,42,.04)}.cta h3{margin-top:0;color:#14532d}.cta b{color:#166534}
.warn{border:1px solid #fed7aa;background:#fff7ed;border-radius:1rem;padding:1rem;margin:.8rem 0;color:#7c2d12}.dark{background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;white-space:pre-wrap}
@media (max-width:900px){.loop{grid-template-columns:repeat(2,1fr)}.hero h1{font-size:2rem}}
</style>
""",
    unsafe_allow_html=True,
)

TEXT = {
    "zh": {
        "nav": "导航",
        "lang_label": "语言 / Language",
        "home": "首页",
        "courses": "训练营",
        "workflow": "岗位工作流",
        "company": "企业内训",
        "pricing": "报价",
        "faq": "FAQ",
    },
    "en": {
        "nav": "Navigation",
        "lang_label": "语言 / Language",
        "home": "Home",
        "courses": "Programs",
        "workflow": "Job Workflows",
        "company": "Company Training",
        "pricing": "Pricing",
        "faq": "FAQ",
    },
}

UPGRADE_ROWS = [
    ("普通文员", "AI 行政助理", "通知、会议纪要、制度、SOP、数据说明"),
    ("普通销售", "AI 销售运营", "客户画像、跟进话术、方案初稿、复盘报告"),
    ("普通客服", "AI 客户成功助理", "问题分类、回复模板、满意度复盘、知识库"),
    ("普通运营", "AI 内容与活动运营", "活动方案、数据分析、内容日历、转化话术"),
    ("普通老师", "AI 课程设计师", "课件、练习、反馈、发表会、教学复盘"),
    ("小微老板", "AI 小团队经营者", "调研、文案、报价、客户沟通、流程管理"),
    ("求职者", "AI 作品集候选人", "AI 化简历、岗位作品集、面试表达稿"),
]

WORKFLOW_ROWS = [
    ("信息检索", "从零散资料中找到可用信息"),
    ("调研分析", "把市场、客户、竞品整理成判断"),
    ("文档写作", "写通知、总结、方案、制度、SOP"),
    ("表格说明", "把数据结论写成老板能看懂的话"),
    ("PPT 汇报", "形成大纲、页面结构、讲稿和 Q&A"),
    ("销售沟通", "生成客户跟进、异议处理和成交复盘"),
    ("运营方案", "做活动计划、内容排期和执行清单"),
    ("岗位作品集", "沉淀可展示的 AI 工作成果"),
]

PROGRAM_ROWS = [
    ("2 小时体验课", "99 元建议", "看懂 AI 岗位升级，不学空概念，现场完成 1 个微型岗位任务"),
    ("1 天入门营", "699 元建议", "拆一个岗位流程，形成一个 AI 工作流"),
    ("5 天训练营", "3999 元建议", "形成个人 AI 岗位工作流 + 3 个可展示作品"),
    ("4 周小班", "8000–20000 元", "围绕一个岗位方向，打磨作品集和转型表达"),
    ("企业内训", "3 万元起", "给部门做 AI 工作流模板包和落地建议"),
]

DELIVERABLES = [
    ("🧭", "岗位升级路线图", "不是泛泛学 AI，而是明确自己岗位如何升级。"),
    ("⚙️", "个人 AI 工作流", "把真实任务拆成可重复执行的 AI 流程。"),
    ("📦", "3 个工作作品", "调研报告、PPT 汇报、客户沟通或运营方案。"),
    ("🗂️", "提示词模板包", "沉淀自己岗位可复用的高频模板。"),
    ("🎤", "成果发表", "能向老板、客户或面试官讲清楚自己怎么用 AI 工作。"),
    ("🧾", "转型表达稿", "用于简历、自我介绍、面试和内部晋升沟通。"),
]


def pick(lang: str, zh: str, en: str) -> str:
    return zh if lang == "zh" else en


def card(icon: str, title: str, body: str):
    st.markdown(f"<div class='card'><b>{icon} {title}</b><p>{body}</p></div>", unsafe_allow_html=True)


def hero(lang: str):
    title = pick(lang, "AI 时代职业再训练", "AI-Era Career Retraining")
    subtitle = pick(
        lang,
        "AI 不是一个工具课。它正在重写每个岗位的工作方式。我们训练成年人用 AI 重做真实岗位流程：调研、文档、表格、PPT、销售、运营、客服、培训和管理。",
        "This is not another AI tool course. AI is rewriting how jobs work. We train adults to rebuild real job workflows with AI: research, documents, spreadsheets, slides, sales, operations, customer service, training, and management.",
    )
    st.markdown(
        f"<div class='hero'><div class='eyebrow'>AI Career Retraining</div><h1>🧭 {title}</h1><p><b>{pick(lang, '把普通岗位，升级成 AI 工作流岗位。', 'Upgrade ordinary roles into AI workflow roles.')}</b><br>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def workflow_loop(lang: str):
    labels = [
        ("01", pick(lang, "选岗位", "Pick role")),
        ("02", pick(lang, "拆流程", "Map workflow")),
        ("03", pick(lang, "用 AI 重做", "Rebuild with AI")),
        ("04", pick(lang, "形成作品", "Create artifacts")),
        ("05", pick(lang, "发表证明", "Present proof")),
    ]
    st.markdown("<div class='loop'>" + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in labels) + "</div>", unsafe_allow_html=True)


def render_home(lang: str):
    hero(lang)
    workflow_loop(lang)

    st.markdown(pick(lang, "### 网站只卖一件事", "### The website sells one thing"))
    st.markdown(
        pick(
            lang,
            "不是 Prompt 课，不是工具大全，不是办公小技巧。核心是：**成年人如何把自己的岗位升级成 AI 工作流岗位，并带走可展示的作品。**",
            "Not a prompt course, not a tool directory, not office tricks. The core promise: **adults upgrade their roles into AI workflow roles and leave with demonstrable work artifacts.**",
        )
    )

    st.markdown(pick(lang, "### 普通岗位怎么升级", "### How ordinary roles upgrade"))
    st.dataframe(
        pd.DataFrame(
            [
                {
                    pick(lang, "现在的岗位", "Current role"): a,
                    pick(lang, "升级后的定位", "Upgraded role"): b,
                    pick(lang, "训练任务", "Training tasks"): c,
                }
                for a, b, c in UPGRADE_ROWS
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(pick(lang, "### 学员最终带走什么", "### What participants take away"))
    cols = st.columns(3)
    for i, (icon, title, body) in enumerate(DELIVERABLES):
        with cols[i % 3]:
            card(icon, title, body)

    st.markdown(
        "<div class='cta'>"
        + pick(
            lang,
            "<h3>首个转化目标</h3><p><b>2 小时体验课：</b>让学员现场完成一个微型岗位任务，并看见自己的岗位升级路径。</p><p><b>主产品：</b>5 天训练营，形成 1 套 AI 岗位工作流 + 3 个可展示作品。</p>",
            "<h3>First conversion target</h3><p><b>2-hour demo class:</b> participants complete one small role-based task and see their own upgrade path.</p><p><b>Main product:</b> a 5-day camp that creates one AI job workflow and three demonstrable artifacts.</p>",
        )
        + "</div>",
        unsafe_allow_html=True,
    )


def render_courses(lang: str):
    st.markdown(pick(lang, "## 训练营设计", "## Program design"))
    st.markdown(pick(lang, "课程阶梯从低门槛体验课开始，但主题始终是岗位升级，而不是单纯提效。", "The ladder starts with a low-friction demo class, but the theme is always role upgrade, not simple productivity hacks."))
    st.dataframe(
        pd.DataFrame(
            [
                {pick(lang, "产品", "Program"): a, pick(lang, "建议价", "Suggested price"): b, pick(lang, "交付", "Deliverable"): c}
                for a, b, c in PROGRAM_ROWS
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(pick(lang, "### 5 天主课", "### 5-day core program"))
    days = [
        ("Day 1", "AI 时代岗位地图", "判断自己岗位会被 AI 改写的部分，确定升级方向"),
        ("Day 2", "岗位流程拆解", "把自己的高频任务拆成可自动化、可协作、可交付的流程"),
        ("Day 3", "AI 工作流搭建", "用 AI 完成调研、文档、表格、PPT、沟通中的关键节点"),
        ("Day 4", "岗位作品集", "打磨 3 个能展示的工作作品，而不是只保存聊天记录"),
        ("Day 5", "成果发表与转型表达", "用作品证明自己会用 AI 工作，形成简历/面试/内部汇报表达"),
    ]
    st.dataframe(
        pd.DataFrame([{pick(lang, "天数", "Day"): d, pick(lang, "主题", "Theme"): t, pick(lang, "成果", "Output"): o} for d, t, o in days]),
        use_container_width=True,
        hide_index=True,
    )


def render_workflow(lang: str):
    st.markdown(pick(lang, "## AI 岗位工作流", "## AI job workflows"))
    st.markdown(pick(lang, "真正值钱的不是会问 AI，而是会把一个岗位流程拆开、重组，并交付可检查的结果。", "The valuable skill is not asking AI questions. It is decomposing and rebuilding a job workflow, then delivering reviewable outputs."))
    cols = st.columns(4)
    for i, (name, desc) in enumerate(WORKFLOW_ROWS):
        with cols[i % 4]:
            card("⚙️", name, desc)

    st.markdown(pick(lang, "### 示例：销售运营工作流", "### Example: sales operations workflow"))
    st.markdown(
        "<div class='dark'>"
        + pick(
            lang,
            "客户信息 → 客户画像 → 需求假设 → 跟进话术 → 方案初稿 → 报价说明 → 异议处理 → 成交复盘",
            "Customer info → persona → need hypothesis → follow-up script → proposal draft → quote explanation → objection handling → deal review",
        )
        + "</div>",
        unsafe_allow_html=True,
    )


def render_company(lang: str):
    st.markdown(pick(lang, "## 企业内训", "## Company training"))
    st.markdown(pick(lang, "企业内训不应只是 AI 讲座，而要形成部门级 AI 工作流模板。", "Company training should not be an AI lecture. It should produce department-level AI workflow templates."))
    cols = st.columns(3)
    items = [
        ("半天诊断", "收集部门高频任务，形成 AI 场景清单。"),
        ("1 天工作坊", "完成部门模板包：周报、纪要、客户回复、PPT、数据说明。"),
        ("4 周落地", "围绕真实流程迭代，形成可执行的部门 AI 工作手册。"),
    ]
    for col, (title, body) in zip(cols, items):
        with col:
            card("🏢", title, body)
    st.markdown(
        "<div class='warn'>"
        + pick(
            lang,
            "企业数据必须脱敏；不上传商业秘密、客户隐私、合同原文、财务敏感数据。关键输出必须人工审核。",
            "Company data must be sanitized. Do not upload trade secrets, customer privacy, contract originals, or sensitive financial data. Critical outputs require human review.",
        )
        + "</div>",
        unsafe_allow_html=True,
    )


def render_pricing(lang: str):
    st.markdown(pick(lang, "## 报价", "## Pricing"))
    st.dataframe(
        pd.DataFrame(
            [
                {pick(lang, "产品", "Product"): a, pick(lang, "价格", "Price"): b, pick(lang, "定位", "Positioning"): c}
                for a, b, c in PROGRAM_ROWS
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(pick(lang, "不要按讲师小时数卖。按岗位升级成果卖：AI 工作流、作品集、转型表达、部门模板包。", "Do not sell instructor hours. Sell role upgrade outcomes: AI workflows, portfolio artifacts, transition narratives, and department templates."))


def render_faq(lang: str):
    st.markdown("## FAQ")
    with st.expander(pick(lang, "这是不是 AI 办公提效课？", "Is this just an AI office productivity course?")):
        st.write(pick(lang, "不是。办公提效只是入口，核心是岗位升级和 AI 工作流。", "No. Office productivity is only an entry point. The core is role upgrade and AI workflows."))
    with st.expander(pick(lang, "会不会承诺就业、涨薪或证书？", "Do you promise employment, salary increase, or certificates?")):
        st.write(pick(lang, "不承诺。课程交付作品、工作流和表达能力，不做官方职业资格承诺。", "No. The course delivers artifacts, workflows, and communication ability. It does not promise official qualifications."))
    with st.expander(pick(lang, "适合零基础吗？", "Is it suitable for beginners?")):
        st.write(pick(lang, "适合普通职场人。不需要编程，但需要带着真实工作任务来练。", "Yes for ordinary office workers. No coding is required, but participants should bring real work tasks."))
    with st.expander(pick(lang, "为什么不做 K12 或补习？", "Why not K12 tutoring?")):
        st.write(pick(lang, "K12 学科补习监管风险高，本项目只做成人职业能力和企业工作流训练。", "K12 subject tutoring carries high regulatory risk. This project focuses on adult vocational capability and company workflows."))


def main():
    lang = st.sidebar.radio(TEXT["zh"]["lang_label"], ["zh", "en"], format_func=lambda x: "中文" if x == "zh" else "English")
    page = st.sidebar.radio(
        TEXT[lang]["nav"],
        ["home", "courses", "workflow", "company", "pricing", "faq"],
        format_func=lambda key: TEXT[lang][key],
    )

    if page == "home":
        render_home(lang)
    elif page == "courses":
        render_courses(lang)
    elif page == "workflow":
        render_workflow(lang)
    elif page == "company":
        render_company(lang)
    elif page == "pricing":
        render_pricing(lang)
    else:
        render_faq(lang)

    st.sidebar.markdown("---")
    st.sidebar.caption("AI Career Retraining · public site v1.0")


if __name__ == "__main__":
    main()
