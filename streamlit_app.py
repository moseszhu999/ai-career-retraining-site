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
:root{
  --ink:#0f172a;--muted:#64748b;--brand:#4f46e5;--brand2:#06b6d4;--green:#22c55e;--soft:#eef2ff;--line:#e2e8f0;
}
.main .block-container{max-width:1160px;padding-top:1rem;padding-bottom:3rem}
section{margin:2.1rem 0}.section-kicker{font-size:.82rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase;color:var(--brand);margin-bottom:.2rem}.section-title{font-size:1.7rem;font-weight:950;color:var(--ink);line-height:1.22;margin:.1rem 0 .35rem}.section-sub{color:var(--muted);font-size:1rem;line-height:1.75;max-width:820px}
.hero-wrap{padding:2.1rem;border:1px solid #c7d2fe;border-radius:1.55rem;background:radial-gradient(circle at 82% 16%,#cffafe 0,#eef2ff 34%,#f8fafc 76%);box-shadow:0 18px 50px rgba(15,23,42,.09);margin-bottom:1.2rem}.hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:1.6rem;align-items:center}.eyebrow{font-size:.78rem;letter-spacing:.13em;color:var(--brand);font-weight:950;text-transform:uppercase}.hero-title{margin:.4rem 0 .75rem;font-size:3.08rem;line-height:1.03;color:var(--ink);font-weight:980}.hero-title span{background:linear-gradient(90deg,var(--brand),var(--brand2));-webkit-background-clip:text;color:transparent}.hero-copy{font-size:1.12rem;color:#475569;line-height:1.75;max-width:720px}.hero-copy b{color:#312e81}.cta-row{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.1rem}.btn{display:inline-block;border-radius:999px;padding:.78rem 1.08rem;font-weight:900;text-decoration:none}.btn-primary{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white;box-shadow:0 10px 22px rgba(79,70,229,.25)}.btn-secondary{background:white;color:#3730a3;border:1px solid #c7d2fe}.hero-tags{margin-top:1rem}.pill{display:inline-block;border-radius:999px;background:white;color:#3730a3;border:1px solid #c7d2fe;padding:.28rem .62rem;margin:.15rem;font-weight:850;font-size:.83rem}.visual{position:relative;min-height:390px;border:1px solid #dbeafe;border-radius:1.4rem;background:linear-gradient(160deg,#fff,#eef2ff 55%,#ecfeff);overflow:hidden;box-shadow:inset 0 1px 0 rgba(255,255,255,.85)}.visual:before{content:"";position:absolute;width:230px;height:230px;border-radius:50%;background:rgba(79,70,229,.12);right:-60px;top:-60px}.visual:after{content:"";position:absolute;width:190px;height:190px;border-radius:50%;background:rgba(6,182,212,.16);left:-50px;bottom:-50px}.screen{position:absolute;left:34px;right:34px;top:35px;padding:1rem;border-radius:1rem;background:#0f172a;color:#e2e8f0;box-shadow:0 18px 36px rgba(15,23,42,.25);z-index:2}.screen b{color:#93c5fd}.screen-line{height:9px;background:#334155;border-radius:999px;margin:.55rem 0}.screen-line.short{width:65%}.float-card{position:absolute;z-index:3;background:white;border:1px solid #e2e8f0;border-radius:1rem;padding:.85rem;box-shadow:0 14px 30px rgba(15,23,42,.13);color:var(--ink);font-weight:900}.float-card small{display:block;color:var(--muted);font-weight:700;margin-top:.25rem}.fc1{left:26px;bottom:118px}.fc2{right:28px;bottom:74px}.fc3{left:145px;bottom:24px}.path-ribbon{position:absolute;left:34px;right:34px;top:210px;display:grid;grid-template-columns:repeat(5,1fr);gap:.45rem;z-index:3}.path-ribbon div{background:white;border:1px solid #c7d2fe;border-radius:.8rem;padding:.6rem .4rem;text-align:center}.path-ribbon b{display:block;color:var(--brand);font-size:.85rem}.path-ribbon span{display:block;color:#312e81;font-size:.75rem;font-weight:900}.statbar{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem;margin-top:1rem}.stat{background:white;border:1px solid #e0e7ff;border-radius:1rem;padding:.8rem;text-align:center}.stat b{display:block;font-size:1.5rem;color:var(--brand)}.stat span{font-size:.82rem;color:var(--muted);font-weight:800}
.card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.card{border:1px solid var(--line);border-radius:1.08rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045);min-height:132px}.card b{color:var(--ink);font-size:1.02rem}.card p{color:var(--muted);line-height:1.58;margin:.45rem 0 0}.card .icon{font-size:1.45rem;margin-right:.2rem}.pain-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem}.pain{background:#fff7ed;border:1px solid #fed7aa;border-radius:1rem;padding:.9rem;color:#7c2d12;font-weight:850}.flow{display:grid;grid-template-columns:repeat(6,1fr);gap:.55rem}.flow div{background:linear-gradient(180deg,#fff,#f8fafc);border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.flow b{display:block;color:var(--brand)}.flow span{font-size:.82rem;font-weight:850;color:#312e81}.artifact-wall{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.artifact{border:1px solid #dbeafe;border-radius:1rem;padding:.9rem;background:linear-gradient(180deg,#fff,#eff6ff);min-height:112px}.artifact b{color:#1e3a8a}.artifact p{color:var(--muted);line-height:1.5}.program-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.program{border:1px solid #dbeafe;border-radius:1.05rem;background:white;padding:1rem;box-shadow:0 8px 20px rgba(15,23,42,.045)}.program .price{font-weight:950;color:#16a34a;margin:.45rem 0}.program b{color:var(--ink)}.bottom-cta{padding:1.4rem;border-radius:1.25rem;background:linear-gradient(135deg,#0f172a,#312e81);color:white}.bottom-cta h3{margin:.1rem 0 .4rem;font-size:1.65rem}.bottom-cta p{color:#dbeafe;line-height:1.7}.table-note{color:var(--muted);font-size:.94rem;line-height:1.7}.warn{border:1px solid #fed7aa;background:#fff7ed;border-radius:1rem;padding:1rem;margin:.8rem 0;color:#7c2d12}.dark{background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;white-space:pre-wrap}.small{font-size:.9rem;color:var(--muted)}
@media (max-width:960px){.hero-grid{grid-template-columns:1fr}.hero-title{font-size:2.25rem}.visual{min-height:360px}.card-grid,.pain-grid,.program-grid{grid-template-columns:1fr}.flow{grid-template-columns:repeat(2,1fr)}.artifact-wall{grid-template-columns:repeat(2,1fr)}.statbar{grid-template-columns:repeat(2,1fr)}}
</style>
""",
    unsafe_allow_html=True,
)

TEXT = {
    "zh": {"nav":"导航","lang_label":"语言 / Language","home":"首页","paths":"成长路径","skills":"技能训练","portfolio":"作品集","freelance":"自由职业","company":"企业内训","pricing":"报价","faq":"FAQ"},
    "en": {"nav":"Navigation","lang_label":"语言 / Language","home":"Home","paths":"Growth Paths","skills":"Skill Training","portfolio":"Portfolio","freelance":"Freelance","company":"Company Training","pricing":"Pricing","faq":"FAQ"},
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


def pick(lang: str, zh: str, en: str) -> str:
    return zh if lang == "zh" else en


def section(kicker: str, title: str, sub: str = ""):
    st.markdown(f"<section><div class='section-kicker'>{kicker}</div><div class='section-title'>{title}</div><div class='section-sub'>{sub}</div></section>", unsafe_allow_html=True)


def html_card(icon: str, title: str, body: str):
    return f"<div class='card'><b><span class='icon'>{icon}</span>{title}</b><p>{body}</p></div>"


def render_home(lang: str):
    if lang == "zh":
        hero_title = "AI 技能成长<br><span>教育平台</span>"
        hero_copy = "面向职场人和自由职业者：新人上手、在岗提升、升职、转岗、跳槽高薪、自由职业增收，都可以用 AI 建立学习-练习-纠错-作品-变现闭环。"
        cta1, cta2 = "预约 2 小时体验课", "查看课程产品"
    else:
        hero_title = "AI Skill Growth<br><span>Education Platform</span>"
        hero_copy = "For professionals and freelancers: onboarding, upskilling, promotion, role switching, higher-paying jobs, and freelance income growth can all be supported by an AI-powered learn-practice-feedback-portfolio-monetization loop."
        cta1, cta2 = "Book a 2-hour demo", "View programs"

    st.markdown(
        f"""
<div class='hero-wrap'>
  <div class='hero-grid'>
    <div>
      <div class='eyebrow'>AI Skill Growth Platform</div>
      <h1 class='hero-title'>{hero_title}</h1>
      <p class='hero-copy'><b>{pick(lang, '用 AI 更快学会新技能，并做出可展示、可交付、可变现的成果。', 'Use AI to learn new skills faster and produce visible, deliverable, monetizable outcomes.')}</b><br>{hero_copy}</p>
      <div class='cta-row'><span class='btn btn-primary'>{cta1}</span><span class='btn btn-secondary'>{cta2}</span></div>
      <div class='hero-tags'><span class='pill'>新人上手</span><span class='pill'>在岗提升</span><span class='pill'>升职跳槽</span><span class='pill'>自由职业接单</span><span class='pill'>企业内训</span></div>
      <div class='statbar'><div class='stat'><b>5</b><span>步成长闭环</span></div><div class='stat'><b>3+</b><span>可展示作品</span></div><div class='stat'><b>2h</b><span>低门槛体验</span></div><div class='stat'><b>B/C</b><span>个人+企业</span></div></div>
    </div>
    <div class='visual'>
      <div class='screen'><b>AI Skill Coach</b><div class='screen-line'></div><div class='screen-line short'></div><div class='screen-line'></div><div class='screen-line short'></div></div>
      <div class='path-ribbon'><div><b>01</b><span>定目标</span></div><div><b>02</b><span>学技能</span></div><div><b>03</b><span>做任务</span></div><div><b>04</b><span>出作品</span></div><div><b>05</b><span>变价值</span></div></div>
      <div class='float-card fc1'>📦 作品集<small>能展示，不空谈</small></div>
      <div class='float-card fc2'>💼 服务包<small>能报价，能交付</small></div>
      <div class='float-card fc3'>🎤 表达稿<small>升职 / 面试 / 接单</small></div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    section("WHO", "谁会需要这个平台", "不是只适合新人。凡是需要学习新技能、提升技能、证明能力或把技能变现的人，都有使用场景。")
    who_cards = [
        ("🌱", "新人上手", "从不会到能做，完成第一个可检查任务。"),
        ("📈", "在岗提升", "把重复任务变成 AI 工作流，提升交付质量。"),
        ("🧗", "升职准备", "从执行者升级为能分析、汇报、复盘的人。"),
        ("🔁", "转岗跳槽", "补齐新岗位技能，用作品证明能力。"),
        ("💼", "自由职业增收", "把技能包装成服务包、报价和交付 SOP。"),
        ("🏢", "企业内训", "把新人培养和在岗提升做成标准化体系。"),
    ]
    st.markdown("<div class='card-grid'>" + "".join(html_card(*c) for c in who_cards) + "</div>", unsafe_allow_html=True)

    section("PAIN", "你真正卡住的地方", "很多人不是没有资料，而是不知道怎么学、怎么练、怎么判断自己做得对不对。")
    pains = ["学了很多教程，还是做不出任务", "没人及时纠错，不知道哪里错", "不会把技能变成作品集", "升职或面试时说不清能力", "自由职业不知道如何报价和交付", "企业培训听完课，没有可检查成果"]
    st.markdown("<div class='pain-grid'>" + "".join(f"<div class='pain'>⚠️ {p}</div>" for p in pains) + "</div>", unsafe_allow_html=True)

    section("METHOD", "AI 技能成长闭环", "把学习从“看资料”变成“有目标、有任务、有反馈、有作品、有价值”的训练流程。")
    flow = [("01", "定目标"), ("02", "学技能"), ("03", "做任务"), ("04", "AI 反馈"), ("05", "出作品"), ("06", "变价值")]
    st.markdown("<div class='flow'>" + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in flow) + "</div>", unsafe_allow_html=True)

    section("OUTCOME", "最终带走什么", "成果必须能被老板、面试官、客户或自己复盘检查。")
    outcomes = [
        ("🧭", "技能成长路线图", "明确要学什么、学到什么程度。"),
        ("🧪", "任务练习闭环", "学习、练习、AI 反馈、修改、提交。"),
        ("📦", "3 个可展示作品", "用作品证明自己学会了。"),
        ("⚙️", "个人 AI 学习工作流", "以后学新技能可以继续复用。"),
        ("💼", "自由职业服务包", "把技能包装成可报价、可交付服务。"),
        ("🧾", "升职/转岗/接单表达", "用于简历、面试、主页和客户沟通。"),
    ]
    st.markdown("<div class='card-grid'>" + "".join(html_card(*c) for c in outcomes) + "</div>", unsafe_allow_html=True)

    section("ARTIFACTS", "作品墙示例", "首页要让用户马上看到：学完不是听懂，而是能拿出东西。")
    artifacts = [
        ("销售", "客户画像 + 跟进话术 + 成交复盘"),
        ("运营", "活动方案 + 内容日历 + 数据复盘"),
        ("行政", "会议纪要 + 行动项表 + SOP"),
        ("IT / 测试", "需求理解 + 测试用例 + Bug 报告"),
        ("培训师", "课程设计 + 练习任务 + Q&A 脚本"),
        ("自由职业", "服务包 + 报价单 + 样品案例 + 交付 SOP"),
        ("求职转岗", "AI 化简历 + 岗位作品 + 面试表达稿"),
        ("小微老板", "客户调研 + 销售文案 + 流程清单"),
    ]
    st.markdown("<div class='artifact-wall'>" + "".join(f"<div class='artifact'><b>{a}</b><p>{b}</p></div>" for a, b in artifacts) + "</div>", unsafe_allow_html=True)

    section("PROGRAMS", "课程产品矩阵", "从体验课到自由职业变现营，再到企业内训，围绕同一个技能成长闭环。")
    st.markdown("<div class='program-grid'>" + "".join(f"<div class='program'><b>{a}</b><div class='price'>{b}</div><p>{c}</p></div>" for a, b, c in PROGRAM_ROWS) + "</div>", unsafe_allow_html=True)

    st.markdown(
        """
<div class='bottom-cta'>
  <h3>先用 2 小时，找到你的下一个技能增长点。</h3>
  <p>选择一个技能目标，现场完成一个微型任务和 AI 学习路径。后续可以进入 5 天技能成长营、自由职业技能变现营或企业内训。</p>
  <div class='cta-row'><span class='btn btn-primary'>预约体验课</span><span class='btn btn-secondary'>咨询课程方案</span></div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_paths(lang: str):
    st.markdown("## 成长路径")
    st.markdown("同一套 AI 学习方法，可以服务不同阶段的职场人和自由职业者。")
    st.dataframe(pd.DataFrame([{"场景": a, "目标": b, "训练重点": c} for a, b, c in MOTIVE_ROWS]), use_container_width=True, hide_index=True)


def render_skills(lang: str):
    st.markdown("## 技能训练")
    st.markdown("AI 的价值不是替你偷懒，而是把学习变成可训练闭环。")
    cols = st.columns(3)
    for i, (name, desc) in enumerate(SKILL_ROWS):
        with cols[i % 3]:
            st.markdown(html_card("🧠", name, desc), unsafe_allow_html=True)
    st.markdown("### 可训练岗位 / 变现技能")
    st.dataframe(pd.DataFrame([{"方向": a, "可训练技能": b} for a, b in ROLE_ROWS]), use_container_width=True, hide_index=True)


def render_portfolio(lang: str):
    st.markdown("## 作品集")
    st.markdown("升职、转岗、跳槽、接单时，最有说服力的不是一句“我会 AI”，而是可检查作品。")
    examples = [("销售", "客户画像 + 跟进话术 + 成交复盘"), ("运营", "活动方案 + 内容日历 + 数据复盘"), ("行政", "会议纪要 + 行动项表 + SOP"), ("IT / 测试", "需求理解 + 测试用例 + Bug 报告"), ("培训师", "课程设计 + 练习任务 + Q&A 脚本"), ("自由职业者", "服务包 + 报价单 + 样品案例 + 交付 SOP"), ("求职转岗", "AI 化简历 + 岗位作品 + 面试表达稿")]
    st.dataframe(pd.DataFrame([{"方向": a, "作品示例": b} for a, b in examples]), use_container_width=True, hide_index=True)


def render_freelance(lang: str):
    st.markdown("## 自由职业者：学新技能，赚更多钱")
    st.markdown("自由职业者的问题不是只缺技能，而是缺一整套从技能到收入的路径。")
    st.dataframe(pd.DataFrame([{"阶段": a, "训练内容": b} for a, b in FREELANCE_ROWS]), use_container_width=True, hide_index=True)
    st.markdown("<div class='dark'>技能学习 → 样品作品 → 服务包 → 报价单 → 获客话术 → 交付 SOP → 复盘提价</div>", unsafe_allow_html=True)


def render_company(lang: str):
    st.markdown("## 企业内训")
    st.markdown("企业需要的不只是 AI 讲座，而是新人上手、在岗提升和部门技能训练体系。")
    cols = st.columns(3)
    items = [("新人上手", "把学习路径、任务练习、AI 反馈和老师点评标准化。"), ("在岗提升", "把部门高频任务做成 AI 学习与工作流模板。"), ("转岗培养", "围绕新岗位能力做作品集和成果发表。")]
    for col, (title, body) in zip(cols, items):
        with col:
            st.markdown(html_card("🏢", title, body), unsafe_allow_html=True)
    st.markdown("<div class='warn'>企业数据必须脱敏；不上传商业秘密、客户隐私、合同原文、财务敏感数据。关键输出必须人工审核。</div>", unsafe_allow_html=True)


def render_pricing(lang: str):
    st.markdown("## 报价")
    st.dataframe(pd.DataFrame([{"产品": a, "价格": b, "交付": c} for a, b, c in PROGRAM_ROWS]), use_container_width=True, hide_index=True)
    st.markdown("不要按讲师小时数卖。按技能成长成果卖：学习路径、任务闭环、AI 反馈、作品集、服务包、升职/转岗/接单表达。")


def render_faq(lang: str):
    st.markdown("## FAQ")
    with st.expander("这是不是只适合新人？"):
        st.write("不是。新人、想升职的人、转岗的人、跳槽高薪的人、自由职业者、想带团队的人都适合。")
    with st.expander("自由职业者能学什么？"):
        st.write("学可出售技能，做样品，包装服务包，写报价，设计获客话术和交付 SOP。")
    with st.expander("这是不是 AI 办公提效课？"):
        st.write("不是。提效只是副产品，核心是学习新技能、提升技能，并做出可展示成果。")
    with st.expander("会不会承诺就业、涨薪、接单收入或证书？"):
        st.write("不承诺。平台交付技能路径、作品集、服务包和表达能力，不做官方职业资格或收入保证。")
    with st.expander("为什么不做 K12 或补习？"):
        st.write("K12 学科补习监管风险高，本项目只做成人职业技能成长、自由职业技能训练和企业内训。")


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
    st.sidebar.caption("AI Skill Growth Platform · visual landing v1.3")


if __name__ == "__main__":
    main()
