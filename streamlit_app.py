from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from urllib.parse import quote

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI 技能成长教育平台", page_icon="🚀", layout="wide")

CSS = """
<style>
:root{--ink:#0f172a;--muted:#64748b;--brand:#4f46e5;--brand2:#06b6d4;--line:#e2e8f0}
.main .block-container{max-width:1180px;padding-top:.7rem;padding-bottom:5.5rem}
[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none}
.nav{position:sticky;top:.45rem;z-index:999;margin-bottom:1rem}.nav-inner{display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:.72rem .95rem;border:1px solid #c7d2fe;border-radius:1.25rem;background:rgba(255,255,255,.93);box-shadow:0 14px 34px rgba(15,23,42,.08)}.brand{display:flex;gap:.62rem;align-items:center;font-weight:950;color:#111827}.logo{width:36px;height:36px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:white}.brand small{display:block;color:var(--muted);font-weight:800}.badges{display:flex;gap:.45rem;flex-wrap:wrap}.badge{padding:.36rem .7rem;border-radius:999px;background:#f8fafc;border:1px solid var(--line);font-weight:900;color:#475569;font-size:.82rem}.badge.cta{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white;border:none}
.nav-panel{margin:.65rem 0 1.15rem;padding:.55rem;border:1px solid #e0e7ff;border-radius:1.2rem;background:#f8fafc;box-shadow:0 10px 26px rgba(15,23,42,.05)}
div[data-testid="stRadio"]>label{display:none}div[role="radiogroup"]{display:flex;flex-wrap:wrap;gap:.42rem}div[role="radiogroup"] label{border:1px solid #dbeafe!important;border-radius:999px!important;background:white!important;padding:.38rem .74rem!important}div[role="radiogroup"] label p{font-weight:900!important;color:#334155!important;font-size:.9rem!important}div[role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,#4f46e5,#06b6d4)!important}div[role="radiogroup"] label:has(input:checked) p{color:white!important}
.hero,.subhero,.workspace-hero{border:1px solid #c7d2fe;border-radius:1.45rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 46%,#fff);box-shadow:0 18px 44px rgba(15,23,42,.08);padding:1.35rem;margin:1.15rem 0}.hero{padding:2.1rem}.hero h1{font-size:3rem;line-height:1.05;margin:.55rem 0;color:var(--ink);font-weight:980}.hero h1 span{background:linear-gradient(90deg,var(--brand),var(--brand2));-webkit-background-clip:text;color:transparent}.hero p,.subhero p{color:#475569;line-height:1.75}.eyebrow,.label{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}.btn{display:inline-flex;border-radius:999px;padding:.78rem 1.08rem;font-weight:950;margin:.25rem}.primary{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white}.secondary{background:white;color:#3730a3;border:1px solid #c7d2fe}.pill{display:inline-block;border-radius:999px;background:white;color:#3730a3;border:1px solid #c7d2fe;padding:.28rem .62rem;margin:.15rem;font-weight:850;font-size:.83rem}
.kicker{font-size:.78rem;font-weight:950;letter-spacing:.14em;color:var(--brand);text-transform:uppercase;margin-top:1.8rem}.title{font-size:1.65rem;font-weight:950;color:var(--ink)}.sub{color:var(--muted);line-height:1.75;max-width:850px}.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:.95rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card,.offer,.task-panel,.student-card,.portfolio-card,.review-card,.ops-card,.rubric-card{border:1px solid var(--line);border-radius:1.08rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045);min-height:120px}.card p,.portfolio-card p,.review-card p,.ops-card p{color:var(--muted);line-height:1.58}.soft{background:#f8fafc;border-color:#dbeafe}.green{background:#f0fdf4;border-color:#bbf7d0}.orange{background:#fff7ed;border-color:#fed7aa}.dark{background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;white-space:pre-wrap}.flow{display:grid;grid-template-columns:repeat(6,1fr);gap:.55rem}.flow div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.flow b{display:block;color:var(--brand)}.flow span{font-weight:850;color:#312e81;font-size:.82rem}
.offer{position:relative;border-color:#dbeafe;min-height:270px}.offer.featured{border:2px solid #4f46e5}.tag,.status-chip{display:inline-block;border-radius:999px;padding:.24rem .58rem;font-size:.76rem;font-weight:950}.tag{background:#eef2ff;color:#3730a3;border:1px solid #c7d2fe}.price{font-size:1.35rem;font-weight:980;color:#16a34a}.offer-btn{position:absolute;left:1rem;right:1rem;bottom:1rem;text-align:center;border-radius:999px;padding:.62rem;background:#0f172a;color:white;font-weight:950}.form-card,.diagnosis{border:1px solid #dbeafe;background:white;border-radius:1.25rem;padding:1.15rem;box-shadow:0 14px 34px rgba(15,23,42,.07)}.summary{border-radius:1rem;background:#0f172a;color:#e2e8f0;padding:1rem;line-height:1.7;white-space:pre-wrap}.lead-note,.ai-feedback{border:1px solid #bbf7d0;background:#f0fdf4;color:#14532d;border-radius:1rem;padding:1rem;margin-top:1rem;font-weight:850}.mail-link{display:inline-block;border-radius:999px;background:linear-gradient(90deg,#4f46e5,#06b6d4);color:white!important;text-decoration:none;padding:.7rem 1rem;font-weight:950;margin-top:.7rem}.mobile-sticky{display:none}
.workspace-head{display:flex;justify-content:space-between;gap:1rem;align-items:flex-start}.day-card{border:1px solid #dbeafe;border-radius:1.05rem;background:white;padding:.92rem;min-height:118px;box-shadow:0 8px 18px rgba(15,23,42,.045)}.day-card.active{border:2px solid #4f46e5;background:#eef2ff}.day-card.done{background:#f0fdf4;border-color:#bbf7d0}.chip-green{background:#dcfce7;color:#166534}.chip-blue{background:#dbeafe;color:#1e40af}.chip-orange{background:#ffedd5;color:#9a3412}.chip-gray{background:#f1f5f9;color:#475569}.chip-red{background:#fee2e2;color:#991b1b}.teacher-box{border:1px solid #fed7aa;background:#fff7ed;color:#7c2d12;border-radius:1rem;padding:1rem;font-weight:850}.copy-note{font-size:.82rem;color:#64748b;font-weight:850;margin:.25rem 0 .5rem}.progress-wrap{height:10px;background:#e2e8f0;border-radius:999px;overflow:hidden}.progress-bar{height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4)}
@media(max-width:960px){.nav{position:relative}.nav-inner,.workspace-head{align-items:flex-start;flex-direction:column}.badges{display:none}.grid2,.grid3,.grid4{grid-template-columns:1fr}.flow{grid-template-columns:repeat(2,1fr)}}@media(max-width:640px){.main .block-container{padding-left:.75rem;padding-right:.75rem;padding-bottom:6.2rem}.nav-panel{overflow-x:auto}.nav-panel div[role="radiogroup"]{flex-wrap:nowrap;overflow-x:auto}.hero h1{font-size:2rem}.mobile-sticky{display:flex;position:fixed;left:.7rem;right:.7rem;bottom:.7rem;z-index:1000;gap:.5rem;background:rgba(15,23,42,.92);border-radius:1rem;padding:.55rem}.mobile-sticky span{flex:1;text-align:center;border-radius:.8rem;padding:.68rem .5rem;color:white;font-weight:950}.mobile-sticky .m1{background:linear-gradient(90deg,#4f46e5,#06b6d4)}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

TEXT = {"zh": {"nav": "导航", "home": "首页", "workspace": "学习工作台", "trial": "2小时体验课", "sop": "跟进SOP", "paths": "成长路径", "skills": "技能训练", "portfolio": "作品集", "freelance": "自由职业", "company": "企业内训", "pricing": "报价", "booking": "预约咨询", "faq": "FAQ"}}
MOTIVE_ROWS = [("新人上手", "从不会到能做", "学习岗位基础技能，完成第一个可检查任务"), ("在岗提升", "从能做到价值更高", "把重复任务做成 AI 工作流，提升交付质量"), ("升职准备", "从执行者到负责人", "学会分析、汇报、复盘和带新人"), ("转岗换工作", "从旧岗位到新岗位", "补齐新岗位技能，形成可展示作品集"), ("自由职业增收", "从会技能到能接单", "形成服务包、报价和交付作品")]
ROLE_ROWS = [("行政 / 人事", "会议纪要、制度、SOP、招聘沟通、数据说明"), ("销售 / 商务", "客户画像、跟进话术、方案初稿、报价说明、成交复盘"), ("运营 / 市场", "活动方案、内容日历、数据复盘、转化话术"), ("IT / 项目人员", "需求理解、测试用例、Bug 报告、日报周报、发表说明"), ("自由职业者", "服务包设计、报价单、交付 SOP、客户沟通、案例展示"), ("小微老板", "市场调研、文案、报价、客户沟通、流程清单")]
SKILL_ROWS = [("学新技能", "用 AI 生成学习路径、解释概念、给例子、拆练习"), ("做任务", "把学习目标变成真实工作任务，而不是只看教程"), ("被纠错", "让 AI 做第一轮反馈：遗漏、逻辑、格式、表达、风险"), ("再修改", "根据反馈修改，形成第二版、第三版成果"), ("做作品", "把练习变成能给老板、客户或面试官看的作品"), ("会表达", "能说明自己怎么学、怎么做、怎么用 AI 提升结果")]
FREELANCE_ROWS = [("选技能", "选择能变现的技能方向"), ("做样品", "用 AI 辅助完成 2-3 个可展示样品"), ("包装服务", "把技能变成清楚的服务包"), ("获客表达", "写主页简介、私信话术、报价说明"), ("交付流程", "形成需求确认、初稿、修改、验收、复盘 SOP"), ("提价路径", "从低价单到标准化服务，再到高价值项目")]


def get_secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return default


def format_webhook_payload(lead: dict, provider: str) -> dict:
    text = lead.get("summary", "")
    provider = (provider or "generic").lower().strip()
    if provider in {"feishu", "lark"}:
        return {"msg_type": "text", "content": {"text": text}}
    if provider in {"wecom", "wechat_work", "qywx", "enterprise_wechat"}:
        return {"msgtype": "text", "text": {"content": text}}
    return lead


def post_lead_to_webhook(lead: dict) -> tuple[bool, str]:
    url = get_secret("LEAD_WEBHOOK_URL")
    provider = get_secret("WEBHOOK_PROVIDER", "generic")
    if not url:
        return False, "未配置 LEAD_WEBHOOK_URL，线索仅在本页生成，可下载后手动跟进。"
    try:
        data = json.dumps(format_webhook_payload(lead, provider), ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
        with urllib.request.urlopen(req, timeout=8) as resp:
            return 200 <= resp.status < 300, f"已按 {provider} 格式发送，Webhook 返回状态：{resp.status}"
    except Exception as exc:
        return False, f"Webhook 发送失败：{exc}"


def section(kicker: str, title: str, sub: str = ""):
    st.markdown(f"<div class='kicker'>{kicker}</div><div class='title'>{title}</div><div class='sub'>{sub}</div>", unsafe_allow_html=True)


def subhero(label: str, title: str, body: str):
    st.markdown(f"<div class='subhero'><span class='label'>{label}</span><h2>{title}</h2><p>{body}</p></div>", unsafe_allow_html=True)


def html_card(icon: str, title: str, body: str, cls: str = "card") -> str:
    return f"<div class='{cls}'><b>{icon} {title}</b><p>{body}</p></div>"


def render_top_nav(lang: str):
    st.markdown("""<div class='nav'><div class='nav-inner'><div class='brand'><div class='logo'>AI</div><div>AI Skill Growth Platform<small>技能成长 · 作品交付 · 学习工作台</small></div></div><div class='badges'><span class='badge'>职场成长</span><span class='badge'>学习任务</span><span class='badge'>作品集</span><span class='badge cta'>预约体验课</span></div></div></div>""", unsafe_allow_html=True)
    nav_keys = ["home", "workspace", "trial", "sop", "paths", "skills", "portfolio", "freelance", "company", "pricing", "booking", "faq"]
    st.markdown("<div class='nav-panel'>", unsafe_allow_html=True)
    page = st.radio(TEXT[lang]["nav"], nav_keys, horizontal=True, label_visibility="collapsed", format_func=lambda key: TEXT[lang][key], key="top_page_nav")
    st.markdown("</div>", unsafe_allow_html=True)
    return page


def render_offer_section():
    section("PROGRAMS", "选择你的技能成长入口", "每个产品对应一个清晰目标和交付结果。")
    offers = [("低门槛开始", "2 小时体验课", "99 / 199 元", "现场完成一个微型任务，拿到一版 AI 学习路径。"), ("主推", "5 天技能成长营", "3999 元建议", "形成 3 个可展示作品、反馈记录和表达稿。"), ("自由职业", "5 天技能变现营", "4999 元建议", "形成服务包、报价单、样品案例和交付 SOP。"), ("企业版", "企业 AI 技能内训", "3 万元起", "把部门高频任务改造成可训练、可评分的 AI 工作流。")]
    html = "<div class='grid4'>"
    for tag, title, price, body in offers:
        cls = "offer featured" if tag == "主推" else "offer"
        html += f"<div class='{cls}'><span class='tag'>{tag}</span><h3>{title}</h3><div class='price'>{price}</div><p>{body}</p><div class='offer-btn'>查看方案</div></div>"
    st.markdown(html + "</div>", unsafe_allow_html=True)


def render_home(lang: str):
    st.markdown("""<div class='hero'><span class='eyebrow'>AI Skill Growth Platform</span><h1>AI 技能成长<br><span>教育平台</span></h1><p><b>用 AI 更快学会新技能，并做出可展示、可交付、可变现的成果。</b><br>面向职场新人、在岗提升者、升职准备者、转岗/跳槽者、自由职业者、小微老板和企业内训部门。</p><span class='btn primary'>🚀 预约 2 小时体验课</span><span class='btn secondary'>🧑‍💻 进入学习工作台</span><div><span class='pill'>今天学什么</span><span class='pill'>今天做什么</span><span class='pill'>AI 如何反馈</span><span class='pill'>老师如何点评</span><span class='pill'>作品集沉淀</span></div></div>""", unsafe_allow_html=True)
    section("METHOD", "AI 技能成长闭环", "把学习从“看资料”变成“有目标、有任务、有反馈、有作品、有价值”的训练流程。")
    flow = [("01", "定目标"), ("02", "学技能"), ("03", "做任务"), ("04", "AI 反馈"), ("05", "出作品"), ("06", "老师点评")]
    st.markdown("<div class='flow'>" + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in flow) + "</div>", unsafe_allow_html=True)
    section("ARTIFACTS", "作品墙示例", "学完不是听懂，而是能拿出东西。")
    artifacts = [("销售", "客户画像 + 跟进话术 + 成交复盘"), ("运营", "活动方案 + 内容日历 + 数据复盘"), ("行政", "会议纪要 + 行动项表 + SOP"), ("IT / 测试", "需求理解 + 测试用例 + Bug 报告"), ("自由职业", "服务包 + 报价单 + 样品案例"), ("企业内训", "任务包 + 评分标准 + 成果发表")]
    st.markdown("<div class='grid3'>" + "".join(f"<div class='card soft'><b>{a}</b><p>{b}</p></div>" for a, b in artifacts) + "</div>", unsafe_allow_html=True)
    render_offer_section()


def render_student_workspace():
    st.markdown("""<div class='workspace-hero'><div class='workspace-head'><div><span class='label'>模拟学员账号</span><h2>张同学 · Day 2 / 5</h2><p>当前课程：5 天 AI 技能成长营。学习目标：用 AI 完成测试用例、Bug 报告和项目发表作品。当前状态：作品 1 进行中。</p></div><div class='student-card'><b>学习完成度</b><p>整体进度：40%</p><div class='progress-wrap'><div class='progress-bar' style='width:40%'></div></div><p><span class='status-chip chip-blue'>作品 1 进行中</span> <span class='status-chip chip-orange'>老师点评：待提交</span></p></div></div></div>""", unsafe_allow_html=True)
    section("STUDENT", "学员信息卡", "平台要让用户马上看到当前课程、当前阶段、学习目标和下一步动作。")
    c = st.columns(4)
    c[0].metric("学员", "张同学")
    c[1].metric("当前课程", "5 天成长营")
    c[2].metric("当前阶段", "Day 2 / 5")
    c[3].metric("状态", "作品 1 进行中")
    section("PATH", "5 天学习路径", "每一天都对应一个可交付结果，而不是普通课程目录。")
    days = [("Day 1", "定目标 + 拆任务", "已完成", "done"), ("Day 2", "作品 1：基础任务", "进行中", "active"), ("Day 3", "作品 2：复杂任务", "未开始", ""), ("Day 4", "作品 3：展示任务", "未开始", ""), ("Day 5", "复盘 + 后续路径", "未开始", "")]
    st.markdown("<div class='grid3'>" + "".join(f"<div class='day-card {cls}'><b>{d}</b><p>{t}</p><span class='status-chip chip-gray'>{s}</span></div>" for d, t, s, cls in days) + "</div>", unsafe_allow_html=True)
    left, right = st.columns([1.05, .95])
    with left:
        section("TODAY", "今日任务", "今日任务：完成作品 1：基础任务作品。")
        st.markdown("""<div class='task-panel'><h3>完成作品 1：基础任务作品</h3><ol><li>阅读任务说明</li><li>查看优秀示例</li><li>使用 AI 提示词生成第一版</li><li>粘贴你的第一版作品</li><li>查看 AI 反馈</li><li>修改成第二版</li><li>提交给老师点评</li></ol></div>""", unsafe_allow_html=True)
        section("STANDARD", "做到什么标准", "先给标准，再让学员做，避免只生成一堆空话。")
        st.markdown("""<div class='task-panel'><ul><li><b>目标清楚：</b>能看出测试对象、功能范围和提交结果。</li><li><b>结构完整：</b>覆盖正常流程、异常流程、边界输入、安全与权限。</li><li><b>可执行：</b>测试步骤、输入数据、预期结果能被别人照着执行。</li><li><b>有遗漏检查：</b>主动说明还需要补充哪些信息。</li><li><b>有 Bug 报告模板：</b>包含标题、环境、步骤、实际结果、预期结果、严重程度。</li></ul></div>""", unsafe_allow_html=True)
    with right:
        section("PROMPT", "AI 提示词区", "给学员一个可复制提示词，先让 AI 做第一轮高频反馈。")
        prompt_text = """你是一个严格的软件测试教练。
请根据以下登录页面需求，设计测试用例。
要求覆盖正常登录、错误密码、空字段、输入格式、权限与安全、异常提示。
同时输出遗漏点和 Bug 报告模板。
需求如下：
【粘贴需求】"""
        st.markdown("<div class='copy-note'>复制下面提示词，到你常用的 AI 工具里使用。</div>", unsafe_allow_html=True)
        st.code(prompt_text, language="text")
        section("TEACHER", "老师点评状态", "AI 负责高频反馈，老师负责最终判断。")
        teacher_status = st.selectbox("老师点评", ["待提交", "待点评", "已点评"], index=0, key="teacher_status_student")
        chip = "chip-orange" if teacher_status == "待提交" else "chip-blue" if teacher_status == "待点评" else "chip-green"
        st.markdown(f"<div class='teacher-box'>老师点评：<span class='status-chip {chip}'>{teacher_status}</span><br>提交第二版后，老师根据任务标准给最终点评。</div>", unsafe_allow_html=True)
    section("SUBMIT", "作品提交框", "先用文本框模拟提交。后续可以接入数据库、文件上传、老师点评后台和真实 AI API。")
    draft = st.text_area("粘贴你的第一版作品", height=220, placeholder="例如：登录页面测试用例列表、Bug 报告模板、遗漏点检查……", key="student_first_draft")
    if st.button("查看模拟 AI 反馈", type="primary"):
        if draft.strip():
            st.markdown("""<div class='ai-feedback'><b>模拟 AI 反馈</b><br>✅ 目标基本清楚：你已经围绕登录页面展开。<br>⚠️ 结构还需要更完整：建议把测试用例分成正常登录、异常输入、权限安全、提示文案、兼容性五类。<br>⚠️ 有遗漏：目前缺少账号锁定、验证码、连续错误密码、SQL 注入/脚本输入、不同角色权限等场景。<br>⚠️ 空话较多：把“检查是否正常”改成具体步骤、输入数据和预期结果。<br>➡️ 下一版修改：用表格输出「编号 / 场景 / 前置条件 / 步骤 / 测试数据 / 预期结果 / 优先级」，并补 1 个 Bug 报告示例。</div>""", unsafe_allow_html=True)
        else:
            st.warning("请先粘贴第一版作品，再查看模拟 AI 反馈。")
    section("PORTFOLIO", "作品集进度", "学习结果最终要沉淀为可展示作品。")
    items = [("作品 1：基础任务作品", "测试用例 + Bug 报告模板", "进行中", "chip-blue"), ("作品 2：复杂任务作品", "复杂需求拆解 + 异常场景补全", "未开始", "chip-gray"), ("作品 3：展示 / 发表作品", "项目发表说明 + 成果表达稿", "未开始", "chip-gray")]
    st.markdown("<div class='grid3'>" + "".join(f"<div class='portfolio-card'><h4>{t}</h4><p>{d}</p><span class='status-chip {cls}'>{s}</span></div>" for t, d, s, cls in items) + "</div>", unsafe_allow_html=True)


def render_teacher_review_workspace():
    section("TEACHER REVIEW", "老师点评端", "老师不负责高频陪聊，老师负责最终判断：是否达到作品标准、是否可以进入作品集、下一版怎么改。")
    review_queue = pd.DataFrame([
        {"学员": "张同学", "课程": "5 天成长营", "作品": "作品 1：基础任务", "提交版本": "第一版", "AI反馈": "已反馈", "老师状态": "待点评", "风险": "遗漏场景较多"},
        {"学员": "李同学", "课程": "5 天成长营", "作品": "作品 2：复杂任务", "提交版本": "第二版", "AI反馈": "已反馈", "老师状态": "待点评", "风险": "表达不清"},
        {"学员": "王同学", "课程": "自由职业营", "作品": "服务包", "提交版本": "第一版", "AI反馈": "未查看", "老师状态": "暂不点评", "风险": "等待AI反馈"},
    ])
    st.dataframe(review_queue, use_container_width=True, hide_index=True)
    left, right = st.columns([1.05, .95])
    with left:
        section("SUBMISSION", "学员作品预览", "模拟老师看到的提交内容。")
        selected = st.selectbox("选择待点评作品", review_queue["学员"] + " / " + review_queue["作品"], key="review_select")
        st.markdown(f"<div class='review-card'><b>当前点评对象：</b>{selected}<p>提交摘要：登录页面测试用例已覆盖正常登录、错误密码、空字段，但缺少账号锁定、验证码、安全输入和权限边界。Bug 报告模板有字段，但严重程度和复现环境不够明确。</p></div>", unsafe_allow_html=True)
        st.text_area("老师可编辑点评", value="整体方向正确，但第一版还不能进入作品集。请补充安全、权限、边界输入和异常提示场景，并把每条测试用例改成可执行格式。", height=160, key="teacher_review_text")
    with right:
        section("RUBRIC", "评分标准", "先标准化，再个性化点评。")
        clarity = st.slider("目标清楚", 1, 5, 4)
        structure = st.slider("结构完整", 1, 5, 3)
        executable = st.slider("可执行程度", 1, 5, 3)
        omissions = st.slider("遗漏检查", 1, 5, 2)
        expression = st.slider("表达清楚", 1, 5, 3)
        score = clarity + structure + executable + omissions + expression
        st.markdown(f"<div class='rubric-card'><b>模拟总分：{score} / 25</b><p>建议：低于 18 分先退回修改；18-22 分可进入第二版；23 分以上可进入作品集候选。</p></div>", unsafe_allow_html=True)
    if st.button("生成模拟老师点评记录", type="primary"):
        st.markdown("""<div class='ai-feedback'><b>老师点评记录</b><br>结论：暂不通过，进入第二版修改。<br>优点：目标方向明确，已经能围绕登录页面设计测试。<br>主要问题：异常场景和安全场景不足，测试步骤不够可执行，Bug 报告缺少复现环境和严重程度判断。<br>下一步：补 8-10 条遗漏测试用例，统一表格格式，再提交第二版。</div>""", unsafe_allow_html=True)
    section("TEMPLATE", "点评记录模板", "后续可以保存到数据库，或推送到学员端。")
    st.code("""【老师点评记录】
学员：
课程：
作品：
版本：
评分：
结论：通过 / 修改后通过 / 退回重做
优点：
主要问题：
必须修改：
可选优化：
是否进入作品集：是 / 否
下一步任务：""", language="text")


def render_ops_workspace():
    section("OPERATIONS", "班主任 / 运营看板", "运营不是看销售线索，而是看学习交付有没有卡住：谁没提交、谁待点评、谁要催改、谁可以进入作品集。")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("本期学员", "12")
    m2.metric("今日应提交", "9")
    m3.metric("待老师点评", "5")
    m4.metric("风险学员", "3")
    progress = pd.DataFrame([
        {"学员": "张同学", "Day": "Day 2", "当前任务": "作品1第二版", "完成度": "40%", "状态": "需提交第二版", "运营动作": "今晚提醒"},
        {"学员": "李同学", "Day": "Day 3", "当前任务": "作品2", "完成度": "60%", "状态": "待老师点评", "运营动作": "催老师点评"},
        {"学员": "王同学", "Day": "Day 1", "当前任务": "目标拆解", "完成度": "20%", "状态": "未提交", "运营动作": "私信确认卡点"},
        {"学员": "赵同学", "Day": "Day 4", "当前任务": "发表作品", "完成度": "80%", "状态": "已点评", "运营动作": "提醒准备发表"},
    ])
    st.dataframe(progress, use_container_width=True, hide_index=True)
    section("QUEUE", "今日运营动作队列", "每个状态都要有下一步动作，不能只展示数据。")
    st.markdown("""<div class='grid3'><div class='ops-card orange'><b>未提交</b><p>发送提醒：你今天的作品还没有提交。先提交第一版，哪怕不完美，也可以先拿 AI 反馈。</p></div><div class='ops-card soft'><b>待点评</b><p>提醒老师：有作品等待最终判断。24 小时内完成点评，避免学员进度断掉。</p></div><div class='ops-card green'><b>已点评</b><p>提醒学员：根据老师点评改第二版，符合标准后进入作品集。</p></div></div>""", unsafe_allow_html=True)
    section("SOP", "班主任日常 SOP", "先把人工运营流程跑通，后面再接自动化。")
    st.code("""每天固定动作：
1. 上午检查昨日未提交学员。
2. 中午检查待老师点评列表。
3. 下午提醒学员根据点评修改第二版。
4. 晚上统计每人作品状态：未开始 / 进行中 / 已提交 / 已点评 / 已入作品集。
5. Day 5 前确认每人至少 3 个作品和 1 份表达稿。
6. 风险学员单独私信，确认是不会做、没时间，还是目标不清。""", language="text")


def render_learning_workspace(lang: str):
    subhero("V3.2 WORKSPACE", "学习工作台：学员端 + 老师点评端 + 班主任看板", "从单个学员页面升级为交付闭环原型。先不做真实登录、不接真实 OpenAI API、不做复杂后端，先跑通学习任务、AI 反馈、老师点评、运营跟进。")
    tab_student, tab_teacher, tab_ops = st.tabs(["学员端", "老师点评端", "班主任 / 运营看板"])
    with tab_student:
        render_student_workspace()
    with tab_teacher:
        render_teacher_review_workspace()
    with tab_ops:
        render_ops_workspace()


def render_trial(lang: str):
    subhero("2-HOUR TRIAL", "AI 技能成长 2 小时体验课", "低门槛入口产品。目标不是讲很多理论，而是在 2 小时内帮用户完成一个真实小任务，拿到一个小作品和后续学习路径。")
    cards = [("推荐价格", "99 / 199 元：降低决策门槛，用真实体验建立信任。"), ("适合谁", "想学新技能、升职表达、转岗跳槽、做作品集、自由职业接单、企业内训负责人。"), ("核心承诺", "2 小时内不空谈，必须完成一个微型任务，并形成可继续打磨的成果。")]
    st.markdown("<div class='grid3'>" + "".join(html_card("✅", a, b, "card green") for a, b in cards) + "</div>", unsafe_allow_html=True)
    section("FLOW", "2 小时体验课流程", "目标诊断 → 任务拆解 → AI 辅助第一版 → AI 反馈修改 → 作品定稿 → 后续路径。")


def render_followup_sop(lang: str):
    subhero("SALES SOP", "飞书线索跟进 SOP / 成交话术", "飞书收到线索只是开始。这个页面指导销售如何跟进、邀约、收款、转化和复盘。")
    statuses = [("新线索", "5 分钟内响应"), ("已联系", "发送第一条回复"), ("已约时间", "确定体验课时间"), ("已付款", "确认 99/199 体验课"), ("已上课", "进入课后转化"), ("已转化", "进入 5 天营/企业方案"), ("未转化", "记录原因，7 天后触达")]
    st.markdown("<div class='grid4'>" + "".join(f"<div class='card soft'><b>{a}</b><p>{b}</p></div>" for a, b in statuses) + "</div>", unsafe_allow_html=True)
    section("RECORD", "飞书跟进记录模板", "每条线索至少记录这些字段，后面才能复盘。")
    st.markdown("""<div class='dark'>【线索跟进记录】
姓名/称呼：
联系方式：
身份：新人 / 在岗 / 升职 / 跳槽 / 自由职业 / 企业
目标技能：
推荐产品：2小时体验课 / 5天成长营 / 自由职业营 / 企业内训
跟进状态：新线索 / 已联系 / 已约时间 / 已付款 / 已上课 / 已转化 / 未转化
下次动作：
备注：</div>""", unsafe_allow_html=True)


def render_paths(lang: str):
    subhero("GROWTH PATHS", "成长路径", "平台先帮你选路径，再把路径拆成任务。")
    st.dataframe(pd.DataFrame([{"场景": a, "目标": b, "训练重点": c} for a, b, c in MOTIVE_ROWS]), use_container_width=True, hide_index=True)


def render_skills(lang: str):
    subhero("SKILL TRAINING", "技能训练", "AI 把学习过程变成训练闭环：定目标、学概念、做任务、收反馈、改作品、能表达。")
    steps = [("01", "定技能目标"), ("02", "生成学习路径"), ("03", "拆真实任务"), ("04", "AI 先纠错"), ("05", "老师再点评"), ("06", "提交作品")]
    st.markdown("<div class='flow'>" + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in steps) + "</div>", unsafe_allow_html=True)
    st.markdown("<div class='grid3'>" + "".join(html_card("🧠", a, b) for a, b in SKILL_ROWS) + "</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{"方向": a, "可训练技能": b} for a, b in ROLE_ROWS]), use_container_width=True, hide_index=True)


def render_portfolio(lang: str):
    subhero("PORTFOLIO", "作品集", "升职、转岗、跳槽、接单时，最有说服力的是能被检查的作品。")
    showcase = [("销售作品包", "客户画像 / 跟进话术 / 方案初稿 / 成交复盘"), ("运营作品包", "活动方案 / 内容日历 / 数据复盘 / 转化话术"), ("IT / 测试作品包", "需求理解 / 测试用例 / Bug 报告 / 发表说明"), ("自由职业作品包", "服务包 / 报价单 / 样品案例 / 交付 SOP")]
    st.markdown("<div class='grid2'>" + "".join(html_card("📦", a, b, "card soft") for a, b in showcase) + "</div><div class='card green'><b>作品集的作用</b><p>把“我学过”变成“我能交付”。</p></div>", unsafe_allow_html=True)


def render_freelance(lang: str):
    subhero("FREELANCE", "自由职业者：学新技能，赚更多钱", "不是保证收入，而是训练你把技能包装成可出售服务。")
    st.markdown("<div class='grid3'>" + "".join(html_card("💼", a, b) for a, b in FREELANCE_ROWS) + "</div>", unsafe_allow_html=True)
    st.markdown("<div class='dark'>技能学习 → 样品作品 → 服务包 → 报价单 → 获客话术 → 交付 SOP → 复盘提价</div>", unsafe_allow_html=True)


def render_company(lang: str):
    subhero("COMPANY TRAINING", "企业内训", "企业需要的不只是 AI 讲座，而是新人上手、在岗提升和部门技能训练体系。")
    items = [("新人上手", "学习路径、任务练习、AI 反馈和老师点评标准化。"), ("在岗提升", "把部门高频任务做成 AI 学习与工作流模板。"), ("部门模板", "沉淀日报、周报、会议纪要、客户回复、PPT、数据说明模板。"), ("合规边界", "企业数据脱敏，关键输出必须人工审核。")]
    st.markdown("<div class='grid4'>" + "".join(html_card("🏢", a, b) for a, b in items) + "</div><div class='card orange'><b>数据安全</b><p>企业数据必须脱敏；不上传商业秘密、客户隐私、合同原文、财务敏感数据。</p></div>", unsafe_allow_html=True)


def render_pricing(lang: str):
    subhero("PRICING", "报价与产品入口", "价格不是按讲师小时数，而是按训练结果：路径、任务、反馈、作品、服务包、表达能力。")
    render_offer_section()


def render_booking(lang: str):
    subhero("BOOKING", "预约体验课 / 咨询方案", "填写后可生成咨询摘要，也可自动发送到你配置的 Webhook。")
    provider = get_secret("WEBHOOK_PROVIDER", "未配置")
    configured = bool(get_secret("LEAD_WEBHOOK_URL"))
    status_class = "green" if configured else "orange"
    status_text = f"已配置：提交后会按 {provider} 格式自动发送线索。" if configured else "未配置：线索不会自动保存，请下载 TXT/CSV 或用邮件发送。"
    st.markdown(f"<div class='card {status_class}'><b>Webhook 状态</b><p>{status_text}</p></div>", unsafe_allow_html=True)
    left, right = st.columns([1.05, .95])
    with left:
        with st.form("booking_form"):
            name = st.text_input("姓名 / 称呼")
            contact = st.text_input("联系方式（微信 / 邮箱 / 手机，任选）")
            identity = st.selectbox("你现在属于哪类人？", ["职场新人", "在岗提升", "升职准备", "转岗 / 跳槽", "自由职业 / 副业接单", "企业培训负责人", "小微老板"])
            goal = st.selectbox("你最想解决什么？", ["学新技能", "提升现有技能", "做作品集", "升职表达", "换工作 / 高薪跳槽", "自由职业接单", "企业内训"])
            skill = st.text_input("想学习或提升的具体技能", placeholder="例如：PPT汇报、销售话术、测试用例、Java项目、自由职业服务包")
            time_budget = st.selectbox("你愿意投入的时间", ["2 小时体验", "1 天入门", "5 天训练营", "4 周小班", "企业内训待沟通"])
            note = st.text_area("补充说明")
            submitted = st.form_submit_button("生成并提交咨询摘要")
    with right:
        st.markdown("<div class='diagnosis'><h3>大陆优先推荐</h3><ul><li>飞书机器人：WEBHOOK_PROVIDER = feishu</li><li>企业微信机器人：WEBHOOK_PROVIDER = wecom</li><li>腾讯云函数 / 阿里云函数 / 自建接口：WEBHOOK_PROVIDER = generic</li></ul></div>", unsafe_allow_html=True)
    if submitted:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lead = {"timestamp": timestamp, "name": name, "contact": contact, "identity": identity, "goal": goal, "skill": skill, "time_budget": time_budget, "note": note, "source": "streamlit_site"}
        summary = f"""【AI 技能成长咨询摘要】
提交时间：{timestamp}
姓名/称呼：{name or '未填写'}
联系方式：{contact or '未填写'}
当前身份：{identity}
主要目标：{goal}
目标技能：{skill or '未填写'}
时间投入：{time_budget}
补充说明：{note or '无'}

初步建议：
1. 先把“{skill or goal}”拆成 1 个微型任务。
2. 体验课中完成一次 AI 辅助学习、练习和反馈。
3. 之后根据结果选择 5 天技能成长营、自由职业技能变现营或企业内训。"""
        lead["summary"] = summary
        st.session_state.setdefault("leads", []).append(lead)
        ok, msg = post_lead_to_webhook(lead)
        st.success("咨询摘要已生成。")
        st.info(msg)
        if ok:
            st.success("线索已发送到 Webhook。")
        st.markdown(f"<div class='summary'>{summary}</div>", unsafe_allow_html=True)
        df = pd.DataFrame([lead])
        st.download_button("下载 TXT 摘要", data=summary, file_name="ai_skill_growth_lead.txt", mime="text/plain")
        st.download_button("下载 CSV 线索", data=df.to_csv(index=False).encode("utf-8-sig"), file_name="ai_skill_growth_lead.csv", mime="text/csv")
        owner_email = get_secret("OWNER_EMAIL")
        mailto = f"mailto:{owner_email}?subject=" + quote("AI技能成长咨询摘要") + "&body=" + quote(summary)
        st.markdown(f"<a class='mail-link' href='{mailto}'>用邮件发送摘要</a>", unsafe_allow_html=True)
    if st.session_state.get("leads"):
        section("SESSION LEADS", "本次会话线索", "这些线索保存在当前浏览会话中；关闭或重启后可能消失。")
        leads_df = pd.DataFrame(st.session_state["leads"])
        st.dataframe(leads_df.drop(columns=["summary"], errors="ignore"), use_container_width=True, hide_index=True)
    section("WEBHOOK CONFIG", "大陆可用配置示例", "在 Streamlit Cloud 的 App settings / Secrets 中加入以下配置。")
    st.code("""LEAD_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
WEBHOOK_PROVIDER = "feishu"
OWNER_EMAIL = "your-email@example.com"

# 或企业微信机器人
# LEAD_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"
# WEBHOOK_PROVIDER = "wecom"

# 或腾讯云函数 / 阿里云函数 / 自建后端
# WEBHOOK_PROVIDER = "generic" """, language="toml")


def render_faq(lang: str):
    subhero("FAQ", "常见问题", "把风险边界说清楚，比夸大承诺更能建立信任。")
    qs = [("这是不是只适合新人？", "不是。新人、想升职的人、转岗的人、跳槽高薪的人、自由职业者、想带团队的人都适合。"), ("这是不是 AI 办公提效课？", "不是。提效只是副产品，核心是学习新技能、提升技能，并做出可展示成果。"), ("会不会承诺就业、涨薪、接单收入或证书？", "不承诺。平台交付技能路径、作品集、服务包和表达能力，不做官方职业资格或收入保证。"), ("AI 会不会替代老师？", "不会。AI 做第一轮解释和反馈，老师负责任务设计、标准把关和关键点评。")]
    st.markdown("<div class='grid2'>" + "".join(html_card("❓", q, a) for q, a in qs) + "</div>", unsafe_allow_html=True)


def main():
    lang = st.radio("语言", ["zh"], horizontal=True, label_visibility="collapsed", format_func=lambda x: "中文", key="lang_nav")
    page = render_top_nav(lang)
    if page == "home":
        render_home(lang)
    elif page == "workspace":
        render_learning_workspace(lang)
    elif page == "trial":
        render_trial(lang)
    elif page == "sop":
        render_followup_sop(lang)
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
    elif page == "booking":
        render_booking(lang)
    else:
        render_faq(lang)
    st.markdown("<div class='mobile-sticky'><span class='m1'>预约体验课</span><span>学习工作台</span></div>", unsafe_allow_html=True)
    st.caption("AI Skill Growth Platform · learner workspace operations prototype v3.2")


if __name__ == "__main__":
    main()
