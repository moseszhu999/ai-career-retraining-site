from __future__ import annotations

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI 职场技能成长",
    page_icon="🚀",
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
    ("小团队管理", "从自己干到带团队", "把团队高频任务标准化、模板化"),
]

ROLE_ROWS = [
    ("行政 / 人事", "会议纪要、制度、SOP、招聘沟通、数据说明"),
    ("销售 / 商务", "客户画像、跟进话术、方案初稿、报价说明、成交复盘"),
    ("客服 / 售后", "问题分类、回复模板、知识库、满意度复盘"),
    ("运营 / 市场", "活动方案、内容日历、数据复盘、转化话术"),
    ("老师 / 培训师", "课程设计、练习设计、反馈、发表会、教学复盘"),
    ("IT / 项目新人", "需求理解、测试用例、Bug 报告、日报周报、发表说明"),
    ("小微老板", "市场调研、文案、报价、客户沟通、流程清单"),
]

SKILL_ROWS = [
    ("学新技能", "用 AI 生成学习路径、解释概念、给例子、拆练习"),
    ("做任务", "把学习目标变成真实工作任务，而不是只看教程"),
    ("被纠错", "让 AI 做第一轮反馈：遗漏、逻辑、格式、表达、风险"),
    ("再修改", "根据反馈修改，形成第二版、第三版成果"),
    ("做作品", "把练习变成能给老板、客户或面试官看的作品"),
    ("会表达", "能说明自己怎么学、怎么做、怎么用 AI 提升结果"),
]

PROGRAM_ROWS = [
    ("2 小时体验课", "99 元建议", "选一个技能目标，现场完成一个微型任务和 AI 学习路径"),
    ("1 天技能入门营", "699 元建议", "学会一个技能的学习-练习-纠错-交付闭环"),
    ("5 天技能成长营", "3999 元建议", "形成 1 套技能成长路径 + 3 个可展示作品"),
    ("4 周技能跃迁小班", "8000–20000 元", "围绕升职、转岗或跳槽目标，打磨作品集和表达"),
    ("企业内训", "3 万元起", "把新人培养、在岗提升和部门技能训练做成 AI 工作流"),
]

DELIVERABLES = [
    ("🧭", "技能成长路线图", "明确要学什么、为什么学、学到什么程度。"),
    ("🧪", "任务练习闭环", "学习、练习、AI 反馈、修改、提交。"),
    ("📦", "3 个可展示作品", "用作品证明自己学会了，而不是只说会。"),
    ("⚙️", "个人 AI 学习工作流", "以后学新技能可以继续复用。"),
    ("🎤", "成果发表稿", "能向老板、面试官或客户说明自己的能力。"),
    ("🧾", "升职 / 转岗表达", "把技能成长写进简历、面试和内部晋升沟通。"),
]


def pick(lang: str, zh: str, en: str) -> str:
    return zh if lang == "zh" else en


def card(icon: str, title: str, body: str):
    st.markdown(f"<div class='card'><b>{icon} {title}</b><p>{body}</p></div>", unsafe_allow_html=True)


def hero(lang: str):
    title = pick(lang, "AI 职场技能成长", "AI Workplace Skill Growth")
    subtitle = pick(
        lang,
        "不只面向新人。职场人只要想学新技能、提升技能、升职、转岗或跳槽高薪，都需要一套 AI 辅助的学习-练习-纠错-作品闭环。",
        "Not just for new hires. Any professional who wants to learn a new skill, improve current skills, get promoted, switch roles, or pursue higher-paying jobs needs an AI-assisted learn-practice-feedback-portfolio loop.",
    )
    st.markdown(
        f"<div class='hero'><div class='eyebrow'>AI Skill Growth for Professionals</div><h1>🚀 {title}</h1><p><b>{pick(lang, '用 AI 更快学会新技能，并做出可展示的工作成果。', 'Use AI to learn new skills faster and produce visible work outcomes.')}</b><br>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def growth_loop(lang: str):
    labels = [
        ("01", pick(lang, "定目标", "Set goal")),
        ("02", pick(lang, "学知识", "Learn")),
        ("03", pick(lang, "做任务", "Practice")),
        ("04", pick(lang, "被纠错", "Feedback")),
        ("05", pick(lang, "出作品", "Portfolio")),
    ]
    st.markdown("<div class='loop'>" + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in labels) + "</div>", unsafe_allow_html=True)


def render_home(lang: str):
    hero(lang)
    growth_loop(lang)

    st.markdown(pick(lang, "### 网站只卖一件事", "### The website sells one thing"))
    st.markdown(
        pick(
            lang,
            "不是 AI 工具课，不是 Prompt 课，也不是单纯办公提效。核心是：**用 AI 帮职场人学习新技能、提升技能，并形成可展示的工作成果。**",
            "Not a tool course, not a prompt course, and not just office productivity. The core promise: **help professionals learn and improve skills with AI, then produce visible work outcomes.**",
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
            "<h3>首个转化目标</h3><p><b>2 小时体验课：</b>选择一个技能目标，现场完成一个微型任务和 AI 学习路径。</p><p><b>主产品：</b>5 天技能成长营，形成 1 套技能成长路径 + 3 个可展示作品。</p>",
            "<h3>First conversion target</h3><p><b>2-hour demo:</b> choose a skill goal and complete one micro task plus an AI learning path.</p><p><b>Main product:</b> a 5-day skill growth camp that creates one skill growth path and three visible artifacts.</p>",
        )
        + "</div>",
        unsafe_allow_html=True,
    )


def render_paths(lang: str):
    st.markdown(pick(lang, "## 成长路径", "## Growth paths"))
    st.markdown(pick(lang, "同一套 AI 学习方法，可以服务不同阶段的职场人。", "The same AI learning method can serve professionals at different career stages."))
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

    st.markdown(pick(lang, "### 可训练岗位技能", "### Trainable job skills"))
    st.dataframe(
        pd.DataFrame([{pick(lang, "岗位 / 方向", "Role / track"): a, pick(lang, "可训练技能", "Trainable skills"): b} for a, b in ROLE_ROWS]),
        use_container_width=True,
        hide_index=True,
    )


def render_portfolio(lang: str):
    st.markdown(pick(lang, "## 作品集", "## Portfolio"))
    st.markdown(pick(lang, "升职、转岗、跳槽时，最有说服力的不是一句“我会 AI”，而是可检查作品。", "For promotion, role switching, and job hunting, the most convincing proof is not saying 'I know AI'—it is reviewable work artifacts."))
    examples = [
        ("销售", "客户画像 + 跟进话术 + 成交复盘"),
        ("运营", "活动方案 + 内容日历 + 数据复盘"),
        ("行政", "会议纪要 + 行动项表 + SOP"),
        ("IT / 测试", "需求理解 + 测试用例 + Bug 报告"),
        ("培训师", "课程设计 + 练习任务 + Q&A 脚本"),
        ("求职转岗", "AI 化简历 + 岗位作品 + 面试表达稿"),
    ]
    st.dataframe(
        pd.DataFrame([{pick(lang, "方向", "Track"): a, pick(lang, "作品示例", "Artifact examples"): b} for a, b in examples]),
        use_container_width=True,
        hide_index=True,
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
    st.markdown(pick(lang, "不要按讲师小时数卖。按技能成长成果卖：学习路径、任务闭环、AI 反馈、作品集、升职/转岗表达。", "Do not sell instructor hours. Sell skill-growth outcomes: learning paths, task loops, AI feedback, portfolios, and promotion/job-switch narratives."))


def render_faq(lang: str):
    st.markdown("## FAQ")
    with st.expander(pick(lang, "这是不是只适合新人？", "Is this only for new hires?")):
        st.write(pick(lang, "不是。新人、想升职的人、转岗的人、跳槽高薪的人、想带团队的人都适合。", "No. It is for new hires, professionals seeking promotion, role switchers, higher-paying job seekers, and team leads."))
    with st.expander(pick(lang, "这是不是 AI 办公提效课？", "Is this just an AI office productivity course?")):
        st.write(pick(lang, "不是。提效只是副产品，核心是学习新技能、提升技能，并做出可展示成果。", "No. Productivity is a byproduct. The core is learning and improving skills, then producing visible outcomes."))
    with st.expander(pick(lang, "会不会承诺就业、涨薪或证书？", "Do you promise employment, salary increase, or certificates?")):
        st.write(pick(lang, "不承诺。课程交付技能路径、作品集和表达能力，不做官方职业资格承诺。", "No. The course delivers skill paths, portfolios, and communication ability. It does not promise official qualifications."))
    with st.expander(pick(lang, "为什么不做 K12 或补习？", "Why not K12 tutoring?")):
        st.write(pick(lang, "K12 学科补习监管风险高，本项目只做成人职业技能成长和企业内训。", "K12 subject tutoring carries high regulatory risk. This project focuses on adult skill growth and company training."))


def main():
    lang = st.sidebar.radio(TEXT["zh"]["lang_label"], ["zh", "en"], format_func=lambda x: "中文" if x == "zh" else "English")
    page = st.sidebar.radio(
        TEXT[lang]["nav"],
        ["home", "paths", "skills", "portfolio", "company", "pricing", "faq"],
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
    elif page == "company":
        render_company(lang)
    elif page == "pricing":
        render_pricing(lang)
    else:
        render_faq(lang)

    st.sidebar.markdown("---")
    st.sidebar.caption("AI Workplace Skill Growth · public site v1.1")


if __name__ == "__main__":
    main()
