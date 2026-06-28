from __future__ import annotations

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI 技能成长教育平台",
    page_icon="🚀",
    layout="wide",
)

st.markdown(
    """
<style>
.main .block-container{max-width:1120px;padding-top:1rem;padding-bottom:3rem}
.hero{padding:2.2rem;border:1px solid #c7d2fe;border-radius:1.35rem;background:linear-gradient(135deg,#eef2ff 0%,#f8fafc 58%,#ecfeff 100%);box-shadow:0 14px 38px rgba(15,23,42,.08);margin-bottom:1rem}
.hero h1{margin:0 0 .75rem 0;font-size:2.75rem;line-height:1.08;color:#0f172a}.hero p{font-size:1.1rem;color:#475569;line-height:1.72;max-width:920px}.eyebrow{font-size:.8rem;letter-spacing:.13em;color:#4f46e5;font-weight:900;text-transform:uppercase}.hero b{color:#312e81}
.card{border:1px solid #e2e8f0;border-radius:1rem;background:#fff;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.04);min-height:132px;margin-bottom:.8rem}.card b{color:#0f172a}.card p{color:#64748b;line-height:1.58}.card strong{color:#4338ca}
.loop{display:grid;grid-template-columns:repeat(5,1fr);gap:.65rem;margin:1rem 0}.loop div{border:1px solid #c7d2fe;background:#fff;border-radius:1rem;padding:.85rem;text-align:center}.loop b{display:block;color:#4f46e5}.loop span{font-weight:850;color:#312e81;font-size:.82rem}
.cta{border:1px solid #bbf7d0;background:#f0fdf4;border-radius:1.2rem;padding:1.2rem;margin:1.2rem 0;box-shadow:0 8px 24px rgba(15,23,42,.04)}.cta h3{margin-top:0;color:#14532d}.cta b{color:#166534}
.warn{border:1px solid #fed7aa;background:#fff7ed;border-radius:1rem;padding:1rem;margin:.8rem 0;color:#7c2d12}.dark{background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;white-space:pre-wrap}.small{font-size:.9rem;color:#64748b}
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
        "paths": "成长路径",
        "skills": "技能训练",
        "portfolio": "作品集",
        "freelance": "自由职业",
        "company": "企业内训",
        "pricing": "报价",
        "faq": "FAQ",
    },
    "en": {
        "nav": "Navigation",
        "lang_label": "语言 / Language",
        "home": "Home",
        "paths": "Growth Paths",
        "skills": "Skill Training",
        "portfolio": "Portfolio",
        "freelance": "Freelance",
        "company": "Company Training",
        "pricing": "Pricing",
        "faq": "FAQ",
    },
}

MOTIVE_ROWS = [
    ("新人上手", "从不会到能做", "学习岗位基础技能，完成第一个可检查任务"),
    ("在岗提升", "从能做到账户价值更高", "把重复任务做成 AI 工作流，提升交付质量"),
    ("升职准备", "从执行者到负责人", "学会分析、汇报、复盘和带新人"),
    ("转岗换工作", "从旧岗位到新岗位", "补齐新岗位技能，形成可展示作品集"),
    ("跳槽高薪", "从会说到有证据", "用作品、流程和表达证明能力"),
    ("自由职业增收", "从会技能到能接单赚钱", "学习可出售技能，形成服务包、报价和交付作品"),
    ("小团队管理", "从自己干到带团队", "把团队高频任务标准化、模板化"),
]

ROLE_ROWS = [
    ("行政 / 人事", "会议纪要、制度、SOP、招聘沟通、数据说明"),
    ("销售 / 商务", "客户画像、跟进话术、方案初稿、报价说明、成交复盘"),
    ("客服 / 售后", "问题分类、回复模板、知识库、满意度复盘"),
    ("运营 / 市场", "活动方案、内容日历、数据复盘、转化话术"),
    ("老师 / 培训师", "课程设计、练习设计、反馈、发表会、教学复盘"),
    ("IT / 项目人员", "需求理解、测试用例、Bug 报告、日报周报、发表说明"),
    ("自由职业者", "获客定位、服务包设计、报价单、交付 SOP、客户沟通、案例展示"),
    ("小微老板", "市场调研、文案、报价、客户沟通、流程清单"),
]

SKILL_ROWS = [
    ("学新技能", "用 AI 生成学习路径、解释概念、给例子、拆练习"),
    ("做任务", "把学习目标变成真实工作任务，而不是只看教程"),
    ("被纠错", "让 AI 做第一轮反馈：遗漏、逻辑、格式、表达、风险"),
    ("再修改", "根据反馈修改，形成第二版、第三版成果"),
    ("做作品", "把练习变成能给老板、客户或面试官看的作品"),
    ("变服务", "把技能包装成自由职业服务包、报价和交付流程"),
    ("会表达", "能说明自己怎么学、怎么做、怎么用 AI 提升结果"),
]

FREELANCE_ROWS = [
    ("选技能", "选择能变现的技能方向：文案、PPT、运营、自动化、课程设计、数据说明等"),
    ("做样品", "用 AI 辅助完成 2-3 个可展示样品，而不是只写能力介绍"),
    ("包装服务", "把技能变成清楚的服务包：交付内容、周期、边界、价格"),
    ("获客表达", "写主页简介、私信话术、报价说明、案例说明"),
    ("交付流程", "形成需求确认、初稿、修改、验收、复盘的 SOP"),
    ("提价路径", "从低价单到标准化服务，再到高价值项目"),
]

PROGRAM_ROWS = [
    ("2 小时体验课", "99 元建议", "选一个技能目标，现场完成一个微型任务和 AI 学习路径"),
    ("1 天技能入门营", "699 元建议", "学会一个技能的学习-练习-纠错-交付闭环"),
    ("5 天技能成长营", "3999 元建议", "形成 1 套技能成长路径 + 3 个可展示作品"),
    ("5 天自由职业技能变现营", "4999 元建议", "形成 1 个服务包 + 3 个样品 + 报价/获客/交付 SOP"),
    ("4 周技能跃迁小班", "8000–20000 元", "围绕升职、转岗、跳槽或自由职业目标，打磨作品集和表达"),
    ("企业内训", "3 万元起", "把新人培养、在岗提升和部门技能训练做成 AI 工作流"),
]

DELIVERABLES = [
    ("🧭", "技能成长路线图", "明确要学什么、为什么学、学到什么程度。"),
    ("🧪", "任务练习闭环", "学习、练习、AI 反馈、修改、提交。"),
    ("📦", "3 个可展示作品", "用作品证明自己学会了，而不是只说会。"),
    ("⚙️", "个人 AI 学习工作流", "以后学新技能可以继续复用。"),
    ("💼", "自由职业服务包", "把技能包装成可报价、可交付的服务。"),
    ("🎤", "成果发表稿", "能向老板、客户或面试官说明自己的能力。"),
    ("🧾", "升职 / 转岗 / 接单表达", "把技能成长写进简历、面试、主页和客户沟通。"),
]


def pick(lang: str, zh: str, en: str) -> str:
    return zh if lang == "zh" else en


def card(icon: str, title: str, body: str):
    st.markdown(f"<div class='card'><b>{icon} {title}</b><p>{body}</p></div>", unsafe_allow_html=True)


def hero(lang: str):
    title = pick(lang, "AI 技能成长教育平台", "AI Skill Growth Education Platform")
    subtitle = pick(
        lang,
        "面向职场人和自由职业者：新人上手、在岗提升、升职、转岗、跳槽高薪、自由职业增收，都可以用 AI 建立学习-练习-纠错-作品-变现闭环。",
        "For professionals and freelancers: onboarding, upskilling, promotion, role switching, higher-paying jobs, and freelance income growth can all be supported by an AI-powered learn-practice-feedback-portfolio-monetization loop.",
    )
    st.markdown(
        f"<div class='hero'><div class='eyebrow'>AI Skill Growth Platform</div><h1>🚀 {title}</h1><p><b>{pick(lang, '用 AI 更快学会新技能，并做出可展示、可交付、可变现的成果。', 'Use AI to learn new skills faster and produce visible, deliverable, monetizable outcomes.')}</b><br>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def growth_loop(lang: str):
    labels = [
        ("01", pick(lang, "定目标", "Set goal")),
        ("02", pick(lang, "学技能", "Learn")),
        ("03", pick(lang, "做任务", "Practice")),
        ("04", pick(lang, "出作品", "Portfolio")),
        ("05", pick(lang, "变价值", "Monetize")),
    ]
    st.markdown("<div class='loop'>" + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in labels) + "</div>", unsafe_allow_html=True)


def render_home(lang: str):
    hero(lang)
    growth_loop(lang)

    st.markdown(pick(lang, "### 平台只做一件事", "### The platform does one thing"))
    st.markdown(
        pick(
            lang,
            "不是 AI 工具课，不是 Prompt 课，也不是单纯办公提效。核心是：**用 AI 帮职场人和自由职业者学习新技能、提升技能，并形成可展示、可交付、可变现的成果。**",
            "Not a tool course, not a prompt course, and not just office productivity. The core promise: **help professionals and freelancers learn or improve skills with AI, then produce visible, deliverable, monetizable outcomes.**",
        )
    )

    st.markdown(pick(lang, "### 谁会需要", "### Who needs this"))
    st.dataframe(
        pd.DataFrame(
            [
                {pick(lang, "场景", "Scenario"): a, pick(lang, "目标", "Goal"): b, pick(lang, "训练重点", "Training focus"): c}
                for a, b, c in MOTIVE_ROWS
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(pick(lang, "### 最终带走什么", "### What participants take away"))
    cols = st.columns(3)
    for i, (icon, title, body) in enumerate(DELIVERABLES):
        with cols[i % 3]:
            card(icon, title, body)

    st.markdown(
        "<div class='cta'>"
        + pick(
            lang,
            "<h3>首个转化目标</h3><p><b>2 小时体验课：</b>选择一个技能目标，现场完成一个微型任务和 AI 学习路径。</p><p><b>主产品：</b>5 天技能成长营 / 5 天自由职业技能变现营，形成作品、服务包或升职转岗表达。</p>",
            "<h3>First conversion target</h3><p><b>2-hour demo:</b> choose a skill goal and complete one micro task plus an AI learning path.</p><p><b>Main product:</b> a 5-day skill growth camp or freelance monetization camp that creates artifacts, service packages, or promotion/job-switch narratives.</p>",
        )
        + "</div>",
        unsafe_allow_html=True,
    )


def render_paths(lang: str):
    st.markdown(pick(lang, "## 成长路径", "## Growth paths"))
    st.markdown(pick(lang, "同一套 AI 学习方法，可以服务不同阶段的职场人和自由职业者。", "The same AI learning method can serve professionals and freelancers at different stages."))
    st.dataframe(
        pd.DataFrame(
            [
                {pick(lang, "场景", "Scenario"): a, pick(lang, "目标", "Goal"): b, pick(lang, "训练重点", "Training focus"): c}
                for a, b, c in MOTIVE_ROWS
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_skills(lang: str):
    st.markdown(pick(lang, "## 技能训练", "## Skill training"))
    st.markdown(pick(lang, "AI 的价值不是替你偷懒，而是把学习变成可训练闭环。", "AI's value is not doing less work. It turns learning into a trainable loop."))
    cols = st.columns(3)
    for i, (name, desc) in enumerate(SKILL_ROWS):
        with cols[i % 3]:
            card("🧠", name, desc)

    st.markdown(pick(lang, "### 可训练岗位 / 变现技能", "### Trainable job / monetizable skills"))
    st.dataframe(
        pd.DataFrame([{pick(lang, "方向", "Track"): a, pick(lang, "可训练技能", "Trainable skills"): b} for a, b in ROLE_ROWS]),
        use_container_width=True,
        hide_index=True,
    )


def render_portfolio(lang: str):
    st.markdown(pick(lang, "## 作品集", "## Portfolio"))
    st.markdown(pick(lang, "升职、转岗、跳槽、接单时，最有说服力的不是一句“我会 AI”，而是可检查作品。", "For promotion, role switching, job hunting, and freelancing, the most convincing proof is not saying 'I know AI'—it is reviewable work artifacts."))
    examples = [
        ("销售", "客户画像 + 跟进话术 + 成交复盘"),
        ("运营", "活动方案 + 内容日历 + 数据复盘"),
        ("行政", "会议纪要 + 行动项表 + SOP"),
        ("IT / 测试", "需求理解 + 测试用例 + Bug 报告"),
        ("培训师", "课程设计 + 练习任务 + Q&A 脚本"),
        ("自由职业者", "服务包 + 报价单 + 样品案例 + 交付 SOP"),
        ("求职转岗", "AI 化简历 + 岗位作品 + 面试表达稿"),
    ]
    st.dataframe(
        pd.DataFrame([{pick(lang, "方向", "Track"): a, pick(lang, "作品示例", "Artifact examples"): b} for a, b in examples]),
        use_container_width=True,
        hide_index=True,
    )


def render_freelance(lang: str):
    st.markdown(pick(lang, "## 自由职业者：学新技能，赚更多钱", "## Freelancers: learn new skills, earn more"))
    st.markdown(pick(lang, "自由职业者的问题不是只缺技能，而是缺一整套从技能到收入的路径。", "Freelancers do not only need skills. They need a path from skill to income."))
    st.dataframe(
        pd.DataFrame([{pick(lang, "阶段", "Stage"): a, pick(lang, "训练内容", "Training content"): b} for a, b in FREELANCE_ROWS]),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(
        "<div class='dark'>"
        + pick(
            lang,
            "技能学习 → 样品作品 → 服务包 → 报价单 → 获客话术 → 交付 SOP → 复盘提价",
            "Skill learning → sample artifacts → service package → quote sheet → client outreach script → delivery SOP → review and price-up path",
        )
        + "</div>",
        unsafe_allow_html=True,
    )


def render_company(lang: str):
    st.markdown(pick(lang, "## 企业内训", "## Company training"))
    st.markdown(pick(lang, "企业需要的不只是 AI 讲座，而是新人上手、在岗提升和部门技能训练体系。", "Companies need more than an AI lecture: they need onboarding, upskilling, and department skill-training systems."))
    cols = st.columns(3)
    items = [
        ("新人上手", "把学习路径、任务练习、AI 反馈和老师点评标准化。"),
        ("在岗提升", "把部门高频任务做成 AI 学习与工作流模板。"),
        ("转岗培养", "围绕新岗位能力做作品集和成果发表。"),
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
                {pick(lang, "产品", "Product"): a, pick(lang, "价格", "Price"): b, pick(lang, "交付", "Deliverable"): c}
                for a, b, c in PROGRAM_ROWS
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(pick(lang, "不要按讲师小时数卖。按技能成长成果卖：学习路径、任务闭环、AI 反馈、作品集、服务包、升职/转岗/接单表达。", "Do not sell instructor hours. Sell skill-growth outcomes: learning paths, task loops, AI feedback, portfolios, service packages, and promotion/job-switch/freelance narratives."))


def render_faq(lang: str):
    st.markdown("## FAQ")
    with st.expander(pick(lang, "这是不是只适合新人？", "Is this only for new hires?")):
        st.write(pick(lang, "不是。新人、想升职的人、转岗的人、跳槽高薪的人、自由职业者、想带团队的人都适合。", "No. It is for new hires, professionals seeking promotion, role switchers, higher-paying job seekers, freelancers, and team leads."))
    with st.expander(pick(lang, "自由职业者能学什么？", "What can freelancers learn?")):
        st.write(pick(lang, "学可出售技能，做样品，包装服务包，写报价，设计获客话术和交付 SOP。", "They learn monetizable skills, build samples, package services, write quotes, design outreach scripts, and create delivery SOPs."))
    with st.expander(pick(lang, "这是不是 AI 办公提效课？", "Is this just an AI office productivity course?")):
        st.write(pick(lang, "不是。提效只是副产品，核心是学习新技能、提升技能，并做出可展示成果。", "No. Productivity is a byproduct. The core is learning and improving skills, then producing visible outcomes."))
    with st.expander(pick(lang, "会不会承诺就业、涨薪、接单收入或证书？", "Do you promise employment, salary increase, freelance income, or certificates?")):
        st.write(pick(lang, "不承诺。平台交付技能路径、作品集、服务包和表达能力，不做官方职业资格或收入保证。", "No. The platform delivers skill paths, portfolios, service packages, and communication ability. It does not promise official qualifications or income."))
    with st.expander(pick(lang, "为什么不做 K12 或补习？", "Why not K12 tutoring?")):
        st.write(pick(lang, "K12 学科补习监管风险高，本项目只做成人职业技能成长、自由职业技能训练和企业内训。", "K12 subject tutoring carries high regulatory risk. This project focuses on adult skill growth, freelance skill training, and company training."))


def main():
    lang = st.sidebar.radio(TEXT["zh"]["lang_label"], ["zh", "en"], format_func=lambda x: "中文" if x == "zh" else "English")
    page = st.sidebar.radio(
        TEXT[lang]["nav"],
        ["home", "paths", "skills", "portfolio", "freelance", "company", "pricing", "faq"],
        format_func=lambda key: TEXT[lang][key],
    )

    if page == "home":
        render_home(lang)
    elif page == "paths":
        render_paths(lang)
    elif page == "skills":
        render_skills(lang)
    elif page == "portfolio":
        render_portfolio(lang)
    elif page == "freelance":
        render_freelance(lang)
    elif page == "company":
        render_company(lang)
    elif page == "pricing":
        render_pricing(lang)
    else:
        render_faq(lang)

    st.sidebar.markdown("---")
    st.sidebar.caption("AI Skill Growth Platform · public site v1.2")


if __name__ == "__main__":
    main()
