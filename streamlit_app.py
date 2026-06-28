from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from urllib.parse import quote

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI 技能成长教育平台", page_icon="🚀", layout="wide")

st.markdown(
    """
<style>
:root{--ink:#0f172a;--muted:#64748b;--brand:#4f46e5;--brand2:#06b6d4;--green:#16a34a;--line:#e2e8f0}
.main .block-container{max-width:1180px;padding-top:.7rem;padding-bottom:5rem}[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none}
section{margin:2.2rem 0 .95rem}.kicker{font-size:.78rem;font-weight:950;letter-spacing:.14em;color:var(--brand);text-transform:uppercase}.title{font-size:1.72rem;font-weight:950;color:var(--ink);line-height:1.22}.sub{color:var(--muted);line-height:1.75;max-width:850px}
.nav{position:sticky;top:.45rem;z-index:999;margin-bottom:1rem}.nav-inner{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:.72rem .95rem;border:1px solid #c7d2fe;border-radius:1.25rem;background:rgba(255,255,255,.88);backdrop-filter:blur(18px);box-shadow:0 14px 34px rgba(15,23,42,.08)}.brand{display:flex;gap:.62rem;align-items:center;font-weight:950;color:#111827}.logo{width:36px;height:36px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:white}.brand small{display:block;color:var(--muted);font-weight:800}.badges{display:flex;gap:.45rem;flex-wrap:wrap}.badge{padding:.36rem .7rem;border-radius:999px;background:#f8fafc;border:1px solid var(--line);font-weight:900;color:#475569;font-size:.82rem}.badge.cta{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white;border:none}
.nav-panel{margin:.65rem 0 1.15rem;padding:.55rem;border:1px solid #e0e7ff;border-radius:1.2rem;background:#f8fafc;box-shadow:0 10px 26px rgba(15,23,42,.05)}div[data-testid="stRadio"]>label{display:none}div[role="radiogroup"]{display:flex;flex-wrap:wrap;gap:.42rem}div[role="radiogroup"] label{border:1px solid #dbeafe!important;border-radius:999px!important;background:white!important;padding:.38rem .74rem!important;box-shadow:0 4px 12px rgba(15,23,42,.035)}div[role="radiogroup"] label p{font-weight:900!important;color:#334155!important;font-size:.9rem!important}div[role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,#4f46e5,#06b6d4)!important;border-color:#4f46e5!important}div[role="radiogroup"] label:has(input:checked) p{color:white!important}
.hero{position:relative;padding:2.25rem;border:1px solid #c7d2fe;border-radius:1.65rem;background:radial-gradient(circle at 86% 12%,#cffafe 0,#eef2ff 32%,#f8fafc 72%);box-shadow:0 24px 70px rgba(15,23,42,.10);overflow:hidden}.hero-grid{display:grid;grid-template-columns:1.02fr .98fr;gap:1.8rem;align-items:center}.eyebrow{display:inline-block;font-size:.78rem;letter-spacing:.13em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.32rem .65rem}.hero h1{margin:.7rem 0 .8rem;font-size:3.15rem;line-height:1.02;color:var(--ink);font-weight:980}.hero h1 span{background:linear-gradient(90deg,var(--brand),var(--brand2));-webkit-background-clip:text;color:transparent}.hero p{font-size:1.12rem;color:#475569;line-height:1.78}.hero b{color:#312e81}.btn-row{display:flex;gap:.75rem;flex-wrap:wrap;margin-top:1.1rem}.btn{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:.78rem 1.08rem;font-weight:950}.primary{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white;box-shadow:0 12px 25px rgba(79,70,229,.28)}.secondary{background:white;color:#3730a3;border:1px solid #c7d2fe}.pill{display:inline-block;border-radius:999px;background:white;color:#3730a3;border:1px solid #c7d2fe;padding:.28rem .62rem;margin:.15rem;font-weight:850;font-size:.83rem}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem;margin-top:1.08rem}.stat{background:white;border:1px solid #e0e7ff;border-radius:1rem;padding:.78rem;text-align:center}.stat b{display:block;font-size:1.48rem;color:var(--brand)}.stat span{font-size:.82rem;color:var(--muted);font-weight:850}
.visual{position:relative;min-height:455px;border:1px solid #dbeafe;border-radius:1.45rem;background:linear-gradient(160deg,#fff,#eef2ff 54%,#ecfeff);overflow:hidden;box-shadow:0 18px 36px rgba(30,41,59,.08)}.dash{position:absolute;left:30px;right:30px;top:28px;bottom:28px;border-radius:1.2rem;background:rgba(255,255,255,.75);border:1px solid #dbeafe;box-shadow:0 18px 40px rgba(15,23,42,.12);padding:1rem}.dash-head{display:flex;justify-content:space-between;align-items:center;font-weight:950}.avatar{width:38px;height:38px;border-radius:14px;display:inline-grid;place-items:center;background:linear-gradient(135deg,var(--brand),var(--brand2));color:white;margin-right:.55rem}.live{padding:.28rem .55rem;border-radius:999px;background:#dcfce7;color:#166534;font-size:.78rem}.journey{display:grid;grid-template-columns:repeat(5,1fr);gap:.42rem;margin:.8rem 0}.journey div{border:1px solid #c7d2fe;background:white;border-radius:.85rem;padding:.55rem .3rem;text-align:center}.journey b{display:block;color:var(--brand);font-size:.82rem}.journey span{font-size:.72rem;font-weight:900;color:#312e81}.ai-box{margin-top:.85rem;background:#0f172a;border-radius:1rem;color:#e2e8f0;padding:.95rem}.ai-box b{color:#93c5fd}.prompt{border:1px solid #334155;background:#111827;border-radius:.8rem;padding:.72rem;color:#cbd5e1;line-height:1.55}.mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:.55rem;margin-top:.75rem}.mini{background:white;border:1px solid #e0e7ff;border-radius:.9rem;padding:.7rem;font-weight:930;color:#111827}.mini small{display:block;color:#64748b;font-weight:750;margin-top:.22rem}.progress{position:absolute;left:22px;right:22px;bottom:20px;background:linear-gradient(90deg,#312e81,#0369a1);color:white;border-radius:1rem;padding:.8rem}.bar{height:9px;background:rgba(255,255,255,.25);border-radius:999px;margin-top:.55rem;overflow:hidden}.bar span{display:block;width:72%;height:100%;background:linear-gradient(90deg,#86efac,#67e8f9)}
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:.95rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card{border:1px solid var(--line);border-radius:1.08rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045);min-height:132px}.card b{color:var(--ink)}.card p{color:var(--muted);line-height:1.58}.soft{background:linear-gradient(180deg,#fff,#f8fafc);border-color:#dbeafe}.orange{background:#fff7ed;border-color:#fed7aa;color:#7c2d12}.green{background:#f0fdf4;border-color:#bbf7d0}.dark{background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;white-space:pre-wrap}.strip{display:grid;grid-template-columns:repeat(4,1fr);gap:.85rem;margin:1rem 0 1.2rem}.metric{border:1px solid #e0e7ff;background:white;border-radius:1.05rem;padding:1rem;box-shadow:0 10px 24px rgba(15,23,42,.05)}.metric b{display:block;font-size:1.6rem;color:var(--brand)}.metric span{color:#64748b;font-weight:850;font-size:.86rem}.flow{display:grid;grid-template-columns:repeat(6,1fr);gap:.55rem}.flow div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.flow b{display:block;color:var(--brand)}.flow span{font-weight:850;color:#312e81;font-size:.82rem}
.offer-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}.offer{position:relative;border:1px solid #dbeafe;border-radius:1.25rem;background:white;padding:1.15rem;box-shadow:0 14px 34px rgba(15,23,42,.07);min-height:292px}.offer.featured{border:2px solid #4f46e5;box-shadow:0 22px 44px rgba(79,70,229,.16);transform:translateY(-4px)}.offer:before{content:"";position:absolute;left:0;top:0;right:0;height:5px;background:linear-gradient(90deg,var(--brand),var(--brand2))}.tag{display:inline-block;border-radius:999px;background:#eef2ff;color:#3730a3;border:1px solid #c7d2fe;padding:.24rem .55rem;font-size:.76rem;font-weight:950}.offer.featured .tag{background:#4f46e5;color:white}.price{font-size:1.45rem;font-weight:980;color:#16a34a}.offer ul{margin:.45rem 0 3.2rem 1rem;color:#475569;line-height:1.7}.offer-btn{position:absolute;left:1.15rem;right:1.15rem;bottom:1.05rem;text-align:center;border-radius:999px;padding:.68rem .8rem;font-weight:950;background:#0f172a;color:white}.offer.featured .offer-btn{background:linear-gradient(90deg,var(--brand),#7c3aed)}
.subhero{border:1px solid #c7d2fe;border-radius:1.35rem;padding:1.35rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 46%,#fff);box-shadow:0 16px 36px rgba(15,23,42,.07);margin:1.2rem 0}.subhero h2{margin:.2rem 0 .5rem;color:var(--ink);font-size:2rem}.subhero p{color:#475569;line-height:1.75}.label{display:inline-block;border-radius:999px;background:white;border:1px solid #c7d2fe;color:#3730a3;font-weight:950;padding:.25rem .6rem;font-size:.78rem}.form-shell{display:grid;grid-template-columns:1fr .85fr;gap:1rem;align-items:start}.form-card,.diagnosis{border:1px solid #dbeafe;background:white;border-radius:1.25rem;padding:1.15rem;box-shadow:0 14px 34px rgba(15,23,42,.07)}.diagnosis{background:linear-gradient(180deg,#fff,#eef2ff);border-color:#c7d2fe}.summary{border-radius:1rem;background:#0f172a;color:#e2e8f0;padding:1rem;line-height:1.7;white-space:pre-wrap}.lead-note{border:1px solid #bbf7d0;background:#f0fdf4;color:#14532d;border-radius:1rem;padding:1rem;margin-top:1rem;font-weight:850}.mail-link{display:inline-block;border-radius:999px;background:linear-gradient(90deg,#4f46e5,#06b6d4);color:white!important;text-decoration:none;padding:.7rem 1rem;font-weight:950;margin-top:.7rem}.mobile-sticky{display:none}
@media(max-width:960px){.nav{position:relative}.nav-inner{align-items:flex-start;flex-direction:column}.badges{display:none}.hero-grid,.grid2,.grid3,.grid4,.strip,.offer-grid,.form-shell{grid-template-columns:1fr}.flow{grid-template-columns:repeat(2,1fr)}.visual{min-height:450px}.offer.featured{transform:none}.stats{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.main .block-container{padding-left:.75rem;padding-right:.75rem;padding-bottom:6.2rem}.nav-panel{overflow-x:auto}.nav-panel div[role="radiogroup"]{flex-wrap:nowrap;overflow-x:auto}.nav-panel div[role="radiogroup"] label{white-space:nowrap}.hero{padding:1.1rem;border-radius:1.2rem}.hero h1{font-size:2rem}.hero p{font-size:1rem}.btn-row{display:grid;grid-template-columns:1fr}.btn{width:100%}.dash{left:14px;right:14px;top:14px;bottom:54px;padding:.75rem}.journey{gap:.25rem}.journey span{font-size:.62rem}.mini-grid{grid-template-columns:1fr}.progress{left:14px;right:14px;bottom:12px}.offer{min-height:0}.offer ul{margin-bottom:1rem}.offer-btn{position:static;margin-top:.75rem}.mobile-sticky{display:flex;position:fixed;left:.7rem;right:.7rem;bottom:.7rem;z-index:1000;gap:.5rem;background:rgba(15,23,42,.92);backdrop-filter:blur(16px);border-radius:1rem;padding:.55rem;box-shadow:0 18px 44px rgba(15,23,42,.35)}.mobile-sticky span{flex:1;text-align:center;border-radius:.8rem;padding:.68rem .5rem;color:white;font-weight:950}.mobile-sticky .m1{background:linear-gradient(90deg,#4f46e5,#06b6d4)}.mobile-sticky .m2{background:rgba(255,255,255,.12)}}
</style>
""", unsafe_allow_html=True)

TEXT = {"zh":{"nav":"导航","home":"首页","paths":"成长路径","skills":"技能训练","portfolio":"作品集","freelance":"自由职业","company":"企业内训","pricing":"报价","booking":"预约咨询","faq":"FAQ"}}
MOTIVE_ROWS=[("新人上手","从不会到能做","学习岗位基础技能，完成第一个可检查任务"),("在岗提升","从能做到账户价值更高","把重复任务做成 AI 工作流，提升交付质量"),("升职准备","从执行者到负责人","学会分析、汇报、复盘和带新人"),("转岗换工作","从旧岗位到新岗位","补齐新岗位技能，形成可展示作品集"),("跳槽高薪","从会说到有证据","用作品、流程和表达证明能力"),("自由职业增收","从会技能到能接单赚钱","学习可出售技能，形成服务包、报价和交付作品"),("小团队管理","从自己干到带团队","把团队高频任务标准化、模板化")]
ROLE_ROWS=[("行政 / 人事","会议纪要、制度、SOP、招聘沟通、数据说明"),("销售 / 商务","客户画像、跟进话术、方案初稿、报价说明、成交复盘"),("客服 / 售后","问题分类、回复模板、知识库、满意度复盘"),("运营 / 市场","活动方案、内容日历、数据复盘、转化话术"),("老师 / 培训师","课程设计、练习设计、反馈、发表会、教学复盘"),("IT / 项目人员","需求理解、测试用例、Bug 报告、日报周报、发表说明"),("自由职业者","获客定位、服务包设计、报价单、交付 SOP、客户沟通、案例展示"),("小微老板","市场调研、文案、报价、客户沟通、流程清单")]
SKILL_ROWS=[("学新技能","用 AI 生成学习路径、解释概念、给例子、拆练习"),("做任务","把学习目标变成真实工作任务，而不是只看教程"),("被纠错","让 AI 做第一轮反馈：遗漏、逻辑、格式、表达、风险"),("再修改","根据反馈修改，形成第二版、第三版成果"),("做作品","把练习变成能给老板、客户或面试官看的作品"),("变服务","把技能包装成自由职业服务包、报价和交付流程"),("会表达","能说明自己怎么学、怎么做、怎么用 AI 提升结果")]
FREELANCE_ROWS=[("选技能","选择能变现的技能方向：文案、PPT、运营、自动化、课程设计、数据说明等"),("做样品","用 AI 辅助完成 2-3 个可展示样品，而不是只写能力介绍"),("包装服务","把技能变成清楚的服务包：交付内容、周期、边界、价格"),("获客表达","写主页简介、私信话术、报价说明、案例说明"),("交付流程","形成需求确认、初稿、修改、验收、复盘的 SOP"),("提价路径","从低价单到标准化服务，再到高价值项目")]


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
        payload = format_webhook_payload(lead, provider)
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
        with urllib.request.urlopen(req, timeout=8) as resp:
            return 200 <= resp.status < 300, f"已按 {provider} 格式发送，Webhook 返回状态：{resp.status}"
    except Exception as exc:
        return False, f"Webhook 发送失败：{exc}"


def section(kicker: str, title: str, sub: str = ""):
    st.markdown(f"<section><div class='kicker'>{kicker}</div><div class='title'>{title}</div><div class='sub'>{sub}</div></section>", unsafe_allow_html=True)


def subhero(label: str, title: str, body: str):
    st.markdown(f"<div class='subhero'><span class='label'>{label}</span><h2>{title}</h2><p>{body}</p></div>", unsafe_allow_html=True)


def html_card(icon: str, title: str, body: str, cls: str = "card") -> str:
    return f"<div class='{cls}'><b>{icon} {title}</b><p>{body}</p></div>"


def render_top_nav(lang: str):
    st.markdown("""<div class='nav'><div class='nav-inner'><div class='brand'><div class='logo'>AI</div><div>AI Skill Growth Platform<small>技能成长 · 作品交付 · 自由职业变现</small></div></div><div class='badges'><span class='badge'>职场成长</span><span class='badge'>自由职业</span><span class='badge'>企业内训</span><span class='badge cta'>预约体验课</span></div></div></div>""", unsafe_allow_html=True)
    nav_keys=["home","paths","skills","portfolio","freelance","company","pricing","booking","faq"]
    st.markdown("<div class='nav-panel'>", unsafe_allow_html=True)
    page=st.radio(TEXT[lang]["nav"], nav_keys, horizontal=True, label_visibility="collapsed", format_func=lambda key:TEXT[lang][key], key="top_page_nav")
    st.markdown("</div>", unsafe_allow_html=True)
    return page


def render_hero():
    st.markdown("""<div class='hero'><div class='hero-grid'><div><div class='eyebrow'>AI Skill Growth Platform</div><h1>AI 技能成长<br><span>教育平台</span></h1><p><b>用 AI 更快学会新技能，并做出可展示、可交付、可变现的成果。</b><br>面向职场人和自由职业者：新人上手、在岗提升、升职、转岗、跳槽高薪、自由职业增收，都可以用 AI 建立学习-练习-纠错-作品-变现闭环。</p><div class='btn-row'><span class='btn primary'>🚀 预约 2 小时体验课</span><span class='btn secondary'>📚 查看课程产品</span></div><div><span class='pill'>新人上手</span><span class='pill'>在岗提升</span><span class='pill'>升职跳槽</span><span class='pill'>自由职业接单</span><span class='pill'>企业内训</span></div><div class='stats'><div class='stat'><b>5</b><span>步成长闭环</span></div><div class='stat'><b>3+</b><span>可展示作品</span></div><div class='stat'><b>2h</b><span>低门槛体验</span></div><div class='stat'><b>B/C</b><span>个人+企业</span></div></div></div><div class='visual'><div class='dash'><div class='dash-head'><div><span class='avatar'>AI</span>Skill Growth Dashboard</div><span class='live'>Live Coach</span></div><div class='journey'><div><b>01</b><span>定目标</span></div><div><b>02</b><span>学技能</span></div><div><b>03</b><span>做任务</span></div><div><b>04</b><span>出作品</span></div><div><b>05</b><span>变价值</span></div></div><div class='ai-box'><b>AI Skill Coach</b><div class='prompt'><strong>今日任务：</strong>把“想学 PPT 汇报”拆成 3 个练习任务，并生成可提交作品标准。</div></div><div class='mini-grid'><div class='mini'>📦 作品集<small>能展示，不空谈</small></div><div class='mini'>💼 服务包<small>能报价，能交付</small></div><div class='mini'>🎤 表达稿<small>升职 / 面试 / 接单</small></div><div class='mini'>✅ 反馈记录<small>AI 纠错 + 人工点评</small></div></div></div><div class='progress'><div style='display:flex;justify-content:space-between;font-weight:950'><span>Skill Growth Progress</span><span>72%</span></div><div class='bar'><span></span></div></div></div></div></div>""", unsafe_allow_html=True)


def render_offer_section():
    section("PROGRAMS","选择你的技能成长入口","每个产品对应一个清晰目标和交付结果。")
    offers=[("低门槛开始","2 小时体验课","99 元建议","适合还没想清楚学什么的人",["现场选择一个技能目标","完成一个微型任务","拿到一版 AI 学习路径"],"预约体验"),("主推","5 天技能成长营","3999 元建议","适合想升职、转岗、跳槽的人",["1 套技能成长路线图","3 个可展示作品","1 份升职/面试表达稿"],"进入主课"),("自由职业","5 天技能变现营","4999 元建议","适合想接单、副业、涨价的人",["1 个可报价服务包","3 个样品案例","获客话术 + 交付 SOP"],"学会接单"),("进阶小班","4 周技能跃迁小班","8000–20000 元","适合目标明确、需要深度打磨的人",["围绕一个方向深度训练","完善作品集和表达","形成后续 30 天行动计划"],"申请小班"),("企业版","企业 AI 技能内训","3 万元起","适合企业新人培养和部门提升",["部门技能地图","任务练习模板","AI 工作流与点评标准"],"咨询企业方案"),("入门营","1 天技能入门营","699 元建议","适合先体验完整学习闭环的人",["拆解一个真实任务","完成一次 AI 反馈修改","形成一个可提交结果"],"参加入门营")]
    html="<div class='offer-grid'>"
    for tag,title,price,fit,bullets,button in offers:
        cls="offer featured" if tag=="主推" else "offer"
        html+=f"<div class='{cls}'><span class='tag'>{tag}</span><h3>{title}</h3><div class='price'>{price}</div><p style='color:#64748b;font-weight:850'>{fit}</p><ul>"+"".join(f"<li>{b}</li>" for b in bullets)+f"</ul><div class='offer-btn'>{button}</div></div>"
    html+="</div>"
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("""<div class='grid2' style='margin-top:1rem'><div class='card green'><b>为什么这个产品更容易被购买？</b><p>它不是卖“AI 很厉害”，而是卖明确结果：学会一个技能、完成真实任务、获得 AI 反馈、形成作品集、用于升职/转岗/跳槽/接单。</p></div><div class='card orange'><b>合规边界</b><p>不承诺就业、不承诺涨薪、不承诺接单收入、不做官方证书。平台只交付训练过程、作品成果、服务包和表达能力。</p></div></div><div class='bottom-cta card' style='background:#0f172a;color:white;margin-top:1rem'><h3>先用 2 小时，找到你的下一个技能增长点。</h3><p style='color:#dbeafe'>选择一个技能目标，现场完成一个微型任务和 AI 学习路径。</p><div class='btn-row'><span class='btn primary'>🚀 预约体验课</span><span class='btn secondary'>📩 咨询课程方案</span></div></div>""", unsafe_allow_html=True)


def render_home(lang: str):
    render_hero()
    st.markdown("""<div class='strip'><div class='metric'><b>4</b><span>主路径：新人、升职、跳槽、自由职业</span></div><div class='metric'><b>6</b><span>训练闭环：目标、学习、任务、反馈、作品、价值</span></div><div class='metric'><b>3+</b><span>每期沉淀可展示作品</span></div><div class='metric'><b>1</b><span>个人技能增长与变现路径</span></div></div>""", unsafe_allow_html=True)
    section("TRACKS","四条主路径","先让用户找到自己属于哪一类。")
    tracks=[("01","职场新人 / 转岗","快速补齐岗位基础技能，完成第一个可检查任务。"),("02","在岗提升 / 升职","把日常工作升级成 AI 工作流，形成汇报和复盘能力。"),("03","跳槽高薪 / 作品集","把能力做成证据：作品、流程、表达稿。"),("04","自由职业 / 接单","学可变现技能，做服务包、报价单和交付 SOP。")]
    st.markdown("<div class='grid4'>"+"".join(f"<div class='card soft'><b>{n} {t}</b><p>{b}</p></div>" for n,t,b in tracks)+"</div>", unsafe_allow_html=True)
    section("WHO","谁会需要这个平台","凡是需要学习新技能、提升技能、证明能力或把技能变现的人，都有使用场景。")
    who=[("🌱","新人上手","从不会到能做，完成第一个可检查任务。"),("📈","在岗提升","把重复任务变成 AI 工作流，提升交付质量。"),("🧗","升职准备","从执行者升级为能分析、汇报、复盘的人。"),("🔁","转岗跳槽","补齐新岗位技能，用作品证明能力。"),("💼","自由职业增收","把技能包装成服务包、报价和交付 SOP。"),("🏢","企业内训","把新人培养和在岗提升做成标准化体系。")]
    st.markdown("<div class='grid3'>"+"".join(html_card(*c) for c in who)+"</div>", unsafe_allow_html=True)
    section("BEFORE / AFTER","从“学过”变成“能交付”","不是多听课，而是能产出作品、服务包和表达证据。")
    st.markdown("""<div class='grid2'><div class='card orange'><b>普通学习方式</b><p>看很多教程，但没有真实任务；不知道自己错在哪里；学完没有作品。</p></div><div class='card green'><b>AI 技能成长方式</b><p>先定技能目标，再拆成任务；AI 做第一轮纠错，老师做关键点评；每个阶段都有可展示作品。</p></div></div>""", unsafe_allow_html=True)
    section("METHOD","AI 技能成长闭环","把学习从“看资料”变成“有目标、有任务、有反馈、有作品、有价值”的训练流程。")
    flow=[("01","定目标"),("02","学技能"),("03","做任务"),("04","AI 反馈"),("05","出作品"),("06","变价值")]
    st.markdown("<div class='flow'>"+"".join(f"<div><b>{n}</b><span>{t}</span></div>" for n,t in flow)+"</div>", unsafe_allow_html=True)
    section("ARTIFACTS","作品墙示例","学完不是听懂，而是能拿出东西。")
    artifacts=[("销售","客户画像 + 跟进话术 + 成交复盘"),("运营","活动方案 + 内容日历 + 数据复盘"),("行政","会议纪要 + 行动项表 + SOP"),("IT / 测试","需求理解 + 测试用例 + Bug 报告"),("培训师","课程设计 + 练习任务 + Q&A 脚本"),("自由职业","服务包 + 报价单 + 样品案例 + 交付 SOP"),("求职转岗","AI 化简历 + 岗位作品 + 面试表达稿"),("小微老板","客户调研 + 销售文案 + 流程清单")]
    st.markdown("<div class='grid4'>"+"".join(f"<div class='card soft'><b>{a}</b><p>{b}</p></div>" for a,b in artifacts)+"</div>", unsafe_allow_html=True)
    render_offer_section()


def render_paths(lang: str):
    subhero("GROWTH PATHS","成长路径","平台先帮你选路径，再把路径拆成任务。")
    cards=[("🌱","新人上手","先做出第一个可检查成果。"),("📈","在岗提升","把高频工作变成 AI 工作流。"),("🧗","升职准备","训练分析、汇报、复盘、带新人。"),("🔁","转岗跳槽","用作品集证明能力。"),("💼","自由职业","把技能转成服务包和交付流程。"),("🏢","企业培养","把培训做成可复制体系。")]
    st.markdown("<div class='grid3'>"+"".join(html_card(*c) for c in cards)+"</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{"场景":a,"目标":b,"训练重点":c} for a,b,c in MOTIVE_ROWS]), use_container_width=True, hide_index=True)


def render_skills(lang: str):
    subhero("SKILL TRAINING","技能训练","AI 把学习过程变成训练闭环：定目标、学概念、做任务、收反馈、改作品、能表达。")
    steps=[("01","定技能目标"),("02","生成学习路径"),("03","拆真实任务"),("04","AI 先纠错"),("05","老师再点评"),("06","提交作品")]
    st.markdown("<div class='flow'>"+"".join(f"<div><b>{n}</b><span>{t}</span></div>" for n,t in steps)+"</div>", unsafe_allow_html=True)
    st.markdown("<div class='grid3'>"+"".join(html_card("🧠",a,b) for a,b in SKILL_ROWS)+"</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{"方向":a,"可训练技能":b} for a,b in ROLE_ROWS]), use_container_width=True, hide_index=True)


def render_portfolio(lang: str):
    subhero("PORTFOLIO","作品集","升职、转岗、跳槽、接单时，最有说服力的是能被检查的作品。")
    showcase=[("销售作品包","客户画像 / 跟进话术 / 方案初稿 / 成交复盘"),("运营作品包","活动方案 / 内容日历 / 数据复盘 / 转化话术"),("IT / 测试作品包","需求理解 / 测试用例 / Bug 报告 / 发表说明"),("自由职业作品包","服务包 / 报价单 / 样品案例 / 交付 SOP")]
    st.markdown("<div class='grid2'>"+"".join(html_card("📦",a,b,"card soft") for a,b in showcase)+"</div><div class='card green'><b>作品集的作用</b><p>把“我学过”变成“我能交付”。</p></div>", unsafe_allow_html=True)


def render_freelance(lang: str):
    subhero("FREELANCE","自由职业者：学新技能，赚更多钱","不是保证收入，而是训练你把技能包装成可出售服务。")
    st.markdown("<div class='grid3'>"+"".join(html_card("💼",a,b) for a,b in FREELANCE_ROWS)+"</div>", unsafe_allow_html=True)
    st.markdown("<div class='dark'>技能学习 → 样品作品 → 服务包 → 报价单 → 获客话术 → 交付 SOP → 复盘提价</div>", unsafe_allow_html=True)


def render_company(lang: str):
    subhero("COMPANY TRAINING","企业内训","企业需要的不只是 AI 讲座，而是新人上手、在岗提升和部门技能训练体系。")
    items=[("新人上手","学习路径、任务练习、AI 反馈和老师点评标准化。"),("在岗提升","把部门高频任务做成 AI 学习与工作流模板。"),("转岗培养","围绕新岗位能力做作品集和成果发表。"),("部门模板","沉淀日报、周报、会议纪要、客户回复、PPT、数据说明模板。"),("评价标准","让主管能判断员工是否真的能交付。"),("合规边界","企业数据脱敏，关键输出必须人工审核。")]
    st.markdown("<div class='grid3'>"+"".join(html_card("🏢",a,b) for a,b in items)+"</div><div class='card orange'><b>数据安全</b><p>企业数据必须脱敏；不上传商业秘密、客户隐私、合同原文、财务敏感数据。关键输出必须人工审核。</p></div>", unsafe_allow_html=True)


def render_pricing(lang: str):
    subhero("PRICING","报价与产品入口","价格不是按讲师小时数，而是按训练结果：路径、任务、反馈、作品、服务包、表达能力。")
    render_offer_section()


def render_booking(lang: str):
    subhero("BOOKING","预约体验课 / 咨询方案","大陆场景优先支持飞书、企业微信、腾讯云函数、阿里云函数、自建后端。填写后可生成咨询摘要，也可自动发送到你配置的 Webhook。")
    provider = get_secret("WEBHOOK_PROVIDER", "未配置")
    webhook_configured = bool(get_secret("LEAD_WEBHOOK_URL"))
    status_class = "green" if webhook_configured else "orange"
    status_text = f"已配置：提交后会按 {provider} 格式自动发送线索。" if webhook_configured else "未配置：线索不会自动保存，请下载 TXT/CSV 或用邮件发送。"
    st.markdown(f"<div class='card {status_class}'><b>Webhook 状态</b><p>{status_text}</p></div>", unsafe_allow_html=True)
    left, right = st.columns([1.05,.95])
    with left:
        st.markdown("<div class='form-card'><h3>预约信息</h3><p style='color:#64748b;line-height:1.7'>支持下载 TXT/CSV、邮件发送；配置 LEAD_WEBHOOK_URL 后，可提交到飞书机器人、企业微信机器人或普通后端接口。</p></div>", unsafe_allow_html=True)
        with st.form("booking_form"):
            name=st.text_input("姓名 / 称呼")
            contact=st.text_input("联系方式（微信 / 邮箱 / 手机，任选）")
            identity=st.selectbox("你现在属于哪类人？",["职场新人","在岗提升","升职准备","转岗 / 跳槽","自由职业 / 副业接单","企业培训负责人","小微老板"])
            goal=st.selectbox("你最想解决什么？",["学新技能","提升现有技能","做作品集","升职表达","换工作 / 高薪跳槽","自由职业接单","企业内训"])
            skill=st.text_input("想学习或提升的具体技能",placeholder="例如：PPT汇报、销售话术、测试用例、Java项目、自由职业服务包")
            time_budget=st.selectbox("你愿意投入的时间",["2 小时体验","1 天入门","5 天训练营","4 周小班","企业内训待沟通"])
            note=st.text_area("补充说明",placeholder="你的背景、现在卡在哪里、希望最终拿到什么成果")
            submitted=st.form_submit_button("生成并提交咨询摘要")
    with right:
        st.markdown("<div class='diagnosis'><h3>大陆优先推荐</h3><ul><li>飞书机器人：WEBHOOK_PROVIDER = feishu</li><li>企业微信机器人：WEBHOOK_PROVIDER = wecom</li><li>腾讯云函数 / 阿里云函数 / 自建接口：WEBHOOK_PROVIDER = generic</li><li>腾讯文档、金山表单：可先用 CSV 导入</li></ul></div>", unsafe_allow_html=True)
        st.markdown("<div class='lead-note'>建议从 2 小时体验课开始：先完成一个微型任务，再决定是否进入完整训练营。</div>", unsafe_allow_html=True)

    if submitted:
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lead={"timestamp":timestamp,"name":name,"contact":contact,"identity":identity,"goal":goal,"skill":skill,"time_budget":time_budget,"note":note,"source":"streamlit_site"}
        summary=f"""【AI 技能成长咨询摘要】
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
        lead["summary"]=summary
        if "leads" not in st.session_state:
            st.session_state["leads"]=[]
        st.session_state["leads"].append(lead)
        ok,msg=post_lead_to_webhook(lead)
        st.success("咨询摘要已生成。")
        st.info(msg)
        if ok:
            st.success("线索已发送到 Webhook。")
        st.markdown(f"<div class='summary'>{summary}</div>", unsafe_allow_html=True)
        csv_df=pd.DataFrame([lead])
        col1,col2=st.columns(2)
        with col1:
            st.download_button("下载 TXT 摘要",data=summary,file_name="ai_skill_growth_lead.txt",mime="text/plain")
        with col2:
            st.download_button("下载 CSV 线索",data=csv_df.to_csv(index=False).encode("utf-8-sig"),file_name="ai_skill_growth_lead.csv",mime="text/csv")
        owner_email=get_secret("OWNER_EMAIL")
        mailto=f"mailto:{owner_email}?subject="+quote("AI技能成长咨询摘要")+"&body="+quote(summary)
        st.markdown(f"<a class='mail-link' href='{mailto}'>用邮件发送摘要</a>", unsafe_allow_html=True)

    if st.session_state.get("leads"):
        section("SESSION LEADS","本次会话线索","这些线索保存在当前浏览会话中；关闭或重启后可能消失。正式保存请配置大陆可用 Webhook。")
        leads_df=pd.DataFrame(st.session_state["leads"])
        st.dataframe(leads_df.drop(columns=["summary"], errors="ignore"), use_container_width=True, hide_index=True)
        st.download_button("下载本次会话全部线索 CSV", data=leads_df.to_csv(index=False).encode("utf-8-sig"), file_name="ai_skill_growth_session_leads.csv", mime="text/csv")

    section("WEBHOOK CONFIG","大陆可用配置示例","在 Streamlit Cloud 的 App settings / Secrets 中加入以下配置。")
    st.code('LEAD_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"\nWEBHOOK_PROVIDER = "feishu"\nOWNER_EMAIL = "your-email@example.com"\n\n# 或企业微信机器人\n# LEAD_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"\n# WEBHOOK_PROVIDER = "wecom"\n\n# 或腾讯云函数 / 阿里云函数 / 自建后端\n# WEBHOOK_PROVIDER = "generic"', language="toml")


def render_faq(lang: str):
    subhero("FAQ","常见问题","把风险边界说清楚，比夸大承诺更能建立信任。")
    qs=[("这是不是只适合新人？","不是。新人、想升职的人、转岗的人、跳槽高薪的人、自由职业者、想带团队的人都适合。"),("自由职业者能学什么？","学可出售技能，做样品，包装服务包，写报价，设计获客话术和交付 SOP。"),("这是不是 AI 办公提效课？","不是。提效只是副产品，核心是学习新技能、提升技能，并做出可展示成果。"),("会不会承诺就业、涨薪、接单收入或证书？","不承诺。平台交付技能路径、作品集、服务包和表达能力，不做官方职业资格或收入保证。"),("为什么不做 K12 或补习？","K12 学科补习监管风险高，本项目只做成人职业技能成长、自由职业技能训练和企业内训。"),("AI 会不会替代老师？","不会。AI 做第一轮解释和反馈，老师负责任务设计、标准把关和关键点评。")]
    st.markdown("<div class='grid2'>"+"".join(html_card("❓",q,a) for q,a in qs)+"</div>", unsafe_allow_html=True)


def main():
    lang=st.radio("语言",["zh"],horizontal=True,label_visibility="collapsed",format_func=lambda x:"中文",key="lang_nav")
    page=render_top_nav(lang)
    if page=="home": render_home(lang)
    elif page=="paths": render_paths(lang)
    elif page=="skills": render_skills(lang)
    elif page=="portfolio": render_portfolio(lang)
    elif page=="freelance": render_freelance(lang)
    elif page=="company": render_company(lang)
    elif page=="pricing": render_pricing(lang)
    elif page=="booking": render_booking(lang)
    else: render_faq(lang)
    st.markdown("<div class='mobile-sticky'><span class='m1'>预约体验课</span><span class='m2'>咨询方案</span></div>", unsafe_allow_html=True)
    st.caption("AI Skill Growth Platform · mainland webhooks v2.3")


if __name__=="__main__":
    main()
