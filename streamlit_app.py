from __future__ import annotations

import io
import json
import re
import urllib.request
import zipfile
from datetime import datetime
from urllib.parse import quote

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI 技能成长教育平台", page_icon="🚀", layout="wide")

CSS = """
<style>
:root{--ink:#0f172a;--muted:#64748b;--brand:#4f46e5;--brand2:#06b6d4;--line:#e2e8f0}.main .block-container{max-width:1180px;padding-top:.7rem;padding-bottom:5rem}[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none}.nav{position:sticky;top:.45rem;z-index:999;margin-bottom:1rem}.nav-inner{display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:.72rem .95rem;border:1px solid #c7d2fe;border-radius:1.25rem;background:rgba(255,255,255,.94);box-shadow:0 14px 34px rgba(15,23,42,.08)}.brand{display:flex;gap:.62rem;align-items:center;font-weight:950;color:#111827}.logo{width:36px;height:36px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:white}.brand small{display:block;color:var(--muted);font-weight:800}.badges{display:flex;gap:.45rem;flex-wrap:wrap}.badge,.pill,.tag,.status-chip{display:inline-block;border-radius:999px;padding:.28rem .62rem;font-weight:900;font-size:.82rem}.badge,.pill,.tag{background:#f8fafc;border:1px solid var(--line);color:#475569}.badge.cta{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white;border:none}.nav-panel{margin:.65rem 0 1.15rem;padding:.55rem;border:1px solid #e0e7ff;border-radius:1.2rem;background:#f8fafc}div[data-testid="stRadio"]>label{display:none}div[role="radiogroup"]{display:flex;flex-wrap:wrap;gap:.42rem}div[role="radiogroup"] label{border:1px solid #dbeafe!important;border-radius:999px!important;background:white!important;padding:.38rem .74rem!important}div[role="radiogroup"] label p{font-weight:900!important;color:#334155!important;font-size:.9rem!important}div[role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,#4f46e5,#06b6d4)!important}div[role="radiogroup"] label:has(input:checked) p{color:white!important}.hero,.subhero,.workspace-hero{border:1px solid #c7d2fe;border-radius:1.45rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 46%,#fff);box-shadow:0 18px 44px rgba(15,23,42,.08);padding:1.35rem;margin:1.15rem 0}.hero{padding:2rem}.hero h1{font-size:2.7rem;line-height:1.05;margin:.55rem 0;color:var(--ink);font-weight:980}.hero h1 span{background:linear-gradient(90deg,var(--brand),var(--brand2));-webkit-background-clip:text;color:transparent}.hero p,.subhero p{color:#475569;line-height:1.75}.eyebrow,.label{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}.btn{display:inline-flex;border-radius:999px;padding:.78rem 1.08rem;font-weight:950;margin:.25rem}.primary{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white}.secondary{background:white;color:#3730a3;border:1px solid #c7d2fe}.kicker{font-size:.78rem;font-weight:950;letter-spacing:.14em;color:var(--brand);text-transform:uppercase;margin-top:1.8rem}.title{font-size:1.65rem;font-weight:950;color:var(--ink)}.sub{color:var(--muted);line-height:1.75;max-width:850px}.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:.95rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card,.offer,.task-panel,.student-card,.portfolio-card,.review-card,.ops-card,.rubric-card,.state-card,.schema-card{border:1px solid var(--line);border-radius:1.08rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045);min-height:110px}.card p,.portfolio-card p,.review-card p,.ops-card p,.state-card p,.schema-card p{color:var(--muted);line-height:1.58}.soft{background:#f8fafc;border-color:#dbeafe}.green{background:#f0fdf4;border-color:#bbf7d0}.orange{background:#fff7ed;border-color:#fed7aa}.dark{background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;white-space:pre-wrap}.flow{display:grid;grid-template-columns:repeat(6,1fr);gap:.55rem}.flow div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.flow b{display:block;color:var(--brand)}.flow span{font-weight:850;color:#312e81;font-size:.82rem}.offer{position:relative;border-color:#dbeafe;min-height:235px}.offer.featured{border:2px solid #4f46e5}.price{font-size:1.35rem;font-weight:980;color:#16a34a}.chip-green{background:#dcfce7;color:#166534}.chip-blue{background:#dbeafe;color:#1e40af}.chip-orange{background:#ffedd5;color:#9a3412}.chip-gray{background:#f1f5f9;color:#475569}.chip-red{background:#fee2e2;color:#991b1b}.teacher-box{border:1px solid #fed7aa;background:#fff7ed;color:#7c2d12;border-radius:1rem;padding:1rem;font-weight:850}.progress-wrap{height:10px;background:#e2e8f0;border-radius:999px;overflow:hidden}.progress-bar{height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4)}.state-line{display:flex;gap:.35rem;flex-wrap:wrap;margin:.8rem 0}.state-step{border:1px solid #dbeafe;border-radius:999px;background:#f8fafc;color:#475569;padding:.3rem .55rem;font-size:.8rem;font-weight:900}.state-step.on{background:#eef2ff;color:#3730a3;border-color:#818cf8}.state-step.done{background:#dcfce7;color:#166534;border-color:#86efac}.summary{border-radius:1rem;background:#0f172a;color:#e2e8f0;padding:1rem;line-height:1.7;white-space:pre-wrap}.mail-link{display:inline-block;border-radius:999px;background:linear-gradient(90deg,#4f46e5,#06b6d4);color:white!important;text-decoration:none;padding:.7rem 1rem;font-weight:950;margin-top:.7rem}.mobile-sticky{display:none}@media(max-width:960px){.nav{position:relative}.nav-inner{align-items:flex-start;flex-direction:column}.badges{display:none}.grid2,.grid3,.grid4{grid-template-columns:1fr}.flow{grid-template-columns:repeat(2,1fr)}}@media(max-width:640px){.hero h1{font-size:2rem}.nav-panel{overflow-x:auto}.nav-panel div[role="radiogroup"]{flex-wrap:nowrap;overflow-x:auto}.mobile-sticky{display:flex;position:fixed;left:.7rem;right:.7rem;bottom:.7rem;z-index:1000;gap:.5rem;background:rgba(15,23,42,.92);border-radius:1rem;padding:.55rem}.mobile-sticky span{flex:1;text-align:center;border-radius:.8rem;padding:.68rem .5rem;color:white;font-weight:950}.mobile-sticky .m1{background:linear-gradient(90deg,#4f46e5,#06b6d4)}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

TEXT = {"zh": {"nav":"导航","home":"首页","workspace":"学习工作台","trial":"2小时体验课","sop":"跟进SOP","paths":"成长路径","skills":"技能训练","portfolio":"作品集","freelance":"自由职业","company":"企业内训","pricing":"报价","booking":"预约咨询","faq":"FAQ"}}
STATUS_ORDER = ["未开始","进行中","已提交","AI已反馈","待老师点评","已点评","已入作品集"]
STATUS_CHIP = {"未开始":"chip-gray","进行中":"chip-blue","已提交":"chip-orange","AI已反馈":"chip-blue","待老师点评":"chip-orange","已点评":"chip-green","已入作品集":"chip-green","风险":"chip-red","等待":"chip-gray"}
MOTIVE_ROWS = [("新人上手","从不会到能做","学习岗位基础技能，完成第一个可检查任务"),("在岗提升","从能做到价值更高","把重复任务做成 AI 工作流，提升交付质量"),("升职准备","从执行者到负责人","学会分析、汇报、复盘和带新人"),("转岗换工作","从旧岗位到新岗位","补齐新岗位技能，形成可展示作品集"),("自由职业增收","从会技能到能接单","形成服务包、报价和交付作品")]
ROLE_ROWS = [("行政 / 人事","会议纪要、制度、SOP、招聘沟通、数据说明"),("销售 / 商务","客户画像、跟进话术、方案初稿、成交复盘"),("运营 / 市场","活动方案、内容日历、数据复盘、转化话术"),("IT / 项目人员","需求理解、测试用例、Bug 报告、日报周报、发表说明"),("自由职业者","服务包设计、报价单、交付 SOP、客户沟通、案例展示"),("小微老板","市场调研、文案、报价、客户沟通、流程清单")]
SKILL_ROWS = [("学新技能","用 AI 生成学习路径、解释概念、给例子、拆练习"),("做任务","把学习目标变成真实工作任务，而不是只看教程"),("被纠错","让 AI 做第一轮反馈：遗漏、逻辑、格式、表达、风险"),("再修改","根据反馈修改，形成第二版、第三版成果"),("做作品","把练习变成能给老板、客户或面试官看的作品"),("会表达","能说明自己怎么学、怎么做、怎么用 AI 提升结果")]
FREELANCE_ROWS = [("选技能","选择能变现的技能方向"),("做样品","用 AI 辅助完成 2-3 个可展示样品"),("包装服务","把技能变成清楚的服务包"),("获客表达","写主页简介、私信话术、报价说明"),("交付流程","形成需求确认、初稿、修改、验收、复盘 SOP"),("提价路径","从低价单到标准化服务，再到高价值项目")]

COURSE_TEMPLATES = {
    "growth_5d": {"name":"5 天 AI 技能成长营","audience":"职场新人 / 在岗提升 / 升职准备 / 转岗跳槽","promise":"3 个可展示作品 + AI 反馈记录 + 老师点评 + 30 天行动计划","tasks":[
        {"task_key":"g_day1","day":"Day 1","title":"定目标 + 拆任务","outcome":"技能成长路线图","prompt":"你是职业技能教练。请把我的目标拆成 5 天训练任务，并说明每天交付物。","standard":"目标明确；任务可执行；交付物可检查。"},
        {"task_key":"g_day2","day":"Day 2","title":"作品 1：基础任务作品","outcome":"测试用例 + Bug 报告模板","prompt":"你是严格的软件测试教练。请根据登录页面需求设计测试用例，并输出遗漏点和 Bug 报告模板。","standard":"覆盖正常、异常、边界、安全、权限；步骤可执行。"},
        {"task_key":"g_day3","day":"Day 3","title":"作品 2：复杂任务作品","outcome":"复杂需求拆解 + 异常场景补全","prompt":"请把复杂业务需求拆成流程、角色、输入输出、异常分支和测试点。","standard":"能解释流程；能发现异常；能说明遗漏信息。"},
        {"task_key":"g_day4","day":"Day 4","title":"作品 3：展示 / 发表作品","outcome":"项目发表说明 + 成果表达稿","prompt":"请把我的项目成果整理成 3 分钟发表稿，包含背景、任务、方法、结果和改进点。","standard":"表达清楚；能展示价值；能回答追问。"},
        {"task_key":"g_day5","day":"Day 5","title":"复盘 + 后续路径","outcome":"30 天行动计划","prompt":"请根据我的 3 个作品和老师点评，生成后续 30 天行动计划。","standard":"路径清楚；动作具体；能持续复盘。"}]},
    "freelance_5d": {"name":"5 天自由职业技能变现营","audience":"自由职业 / 副业接单者","promise":"1 个服务包 + 3 个样品案例 + 报价单 + 获客话术 + 交付 SOP","tasks":[
        {"task_key":"f_day1","day":"Day 1","title":"选择可售卖技能","outcome":"服务方向定位","prompt":"请帮我把一个技能转成可售卖服务方向，说明目标客户、痛点和交付物。","standard":"客户明确；痛点具体；交付边界清楚。"},
        {"task_key":"f_day2","day":"Day 2","title":"样品案例 1","outcome":"第一个可展示样品","prompt":"请根据目标客户场景，帮我设计一个可展示样品案例。","standard":"样品能展示能力；客户能看懂价值。"},
        {"task_key":"f_day3","day":"Day 3","title":"服务包 + 报价单","outcome":"可报价服务包","prompt":"请把我的技能包装成 3 档服务包，包含交付内容、周期、修改次数和价格边界。","standard":"价格边界明确；交付流程清楚；不承诺不可控结果。"},
        {"task_key":"f_day4","day":"Day 4","title":"获客私信 + 主页介绍","outcome":"获客表达素材","prompt":"请帮我写一版自由职业主页介绍和 3 条获客私信。","standard":"不夸大；有案例；能引导客户回复。"},
        {"task_key":"f_day5","day":"Day 5","title":"交付 SOP + 提价路径","outcome":"客户交付流程","prompt":"请生成从需求确认到验收复盘的交付 SOP，并设计提价路径。","standard":"流程完整；风险可控；提价有依据。"}]},
    "enterprise_dept": {"name":"企业部门 AI 训练营","audience":"企业内训部门 / 新人培养 / 部门负责人","promise":"部门任务模板 + 评分标准 + 员工练习包 + 培训复盘","tasks":[
        {"task_key":"e_1","day":"模块 1","title":"部门高频任务清单","outcome":"AI 训练任务地图","prompt":"请把部门高频任务整理成可训练任务清单，并标出可用 AI 辅助的环节。","standard":"任务真实；频率高；能训练。"},
        {"task_key":"e_2","day":"模块 2","title":"任务模板 + 示例","outcome":"部门任务模板","prompt":"请把一个部门任务改造成员工练习模板，包含输入、步骤、输出和评分标准。","standard":"可复制；可评分；可用于新人训练。"},
        {"task_key":"e_3","day":"模块 3","title":"成果发表 + 复盘","outcome":"培训复盘报告","prompt":"请生成部门 AI 训练营成果发表结构和复盘报告模板。","standard":"能展示成果；能发现共性问题；能给出后续训练建议。"}]},
}

TABLE_SCHEMAS = {
    "courses": [("course_id","PK","课程模板 ID"),("name","text","课程名称"),("audience","text","适用人群"),("promise","text","交付承诺"),("is_active","bool","是否启用")],
    "task_templates": [("task_key","PK","任务模板 ID"),("course_id","FK","关联 courses.course_id"),("day","text","Day / 模块"),("title","text","任务标题"),("outcome","text","交付物"),("prompt","text","AI 提示词"),("standard","text","评分标准")],
    "enrollments": [("enrollment_id","PK","报名 / 班级实例 ID"),("student_name","text","学员或小组名称"),("course_id","FK","课程模板 ID"),("status","text","学习中 / 结营 / 退课"),("created_at","datetime","创建时间")],
    "task_instances": [("instance_id","PK","学员任务实例 ID"),("enrollment_id","FK","关联报名实例"),("student","text","学员"),("course_id","FK","课程模板"),("task_key","FK","任务模板"),("status","text","学习状态"),("draft","text","作品草稿"),("ai_feedback","text","AI 反馈"),("teacher_review","text","老师点评"),("score","int","评分"),("portfolio","bool","是否入作品集")],
    "reviews": [("review_id","PK","点评记录 ID"),("instance_id","FK","任务实例 ID"),("reviewer","text","点评老师"),("score","int","分数"),("conclusion","text","通过 / 修改 / 退回"),("review_text","text","点评正文"),("created_at","datetime","点评时间")],
}

def get_secret(name: str, default: str = "") -> str:
    try: return str(st.secrets.get(name, default))
    except Exception: return default

def format_webhook_payload(lead: dict, provider: str) -> dict:
    text = lead.get("summary", ""); provider = (provider or "generic").lower().strip()
    if provider in {"feishu", "lark"}: return {"msg_type":"text","content":{"text":text}}
    if provider in {"wecom", "wechat_work", "qywx", "enterprise_wechat"}: return {"msgtype":"text","text":{"content":text}}
    return lead

def post_lead_to_webhook(lead: dict) -> tuple[bool, str]:
    url = get_secret("LEAD_WEBHOOK_URL"); provider = get_secret("WEBHOOK_PROVIDER", "generic")
    if not url: return False, "未配置 LEAD_WEBHOOK_URL，线索仅在本页生成，可下载后手动跟进。"
    try:
        data = json.dumps(format_webhook_payload(lead, provider), ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json; charset=utf-8"}, method="POST")
        with urllib.request.urlopen(req, timeout=8) as resp: return 200 <= resp.status < 300, f"已按 {provider} 格式发送，Webhook 返回状态：{resp.status}"
    except Exception as exc: return False, f"Webhook 发送失败：{exc}"

def section(kicker: str, title: str, sub: str = ""):
    st.markdown(f"<div class='kicker'>{kicker}</div><div class='title'>{title}</div><div class='sub'>{sub}</div>", unsafe_allow_html=True)

def subhero(label: str, title: str, body: str):
    st.markdown(f"<div class='subhero'><span class='label'>{label}</span><h2>{title}</h2><p>{body}</p></div>", unsafe_allow_html=True)

def html_card(icon: str, title: str, body: str, cls: str = "card") -> str:
    return f"<div class='{cls}'><b>{icon} {title}</b><p>{body}</p></div>"

def safe_id(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", text.strip()).strip("_") or "item"

def chip(status: str) -> str:
    return f"<span class='status-chip {STATUS_CHIP.get(status, 'chip-gray')}'>{status}</span>"

def template_task(course_id: str, task_key: str) -> dict:
    for task in COURSE_TEMPLATES[course_id]["tasks"]:
        if task["task_key"] == task_key: return task
    raise KeyError(task_key)

def build_instance(student: str, course_id: str, task_key: str, status: str = "未开始", **overrides) -> dict:
    course = COURSE_TEMPLATES[course_id]; task = template_task(course_id, task_key)
    item = {"id": f"{safe_id(student)}_{course_id}_{task_key}_{len(st.session_state.get('task_instances', []))}", "student": student, "course_id": course_id, "course": course["name"], "task_key": task_key, "enrollment_id": f"{safe_id(student)}_{course_id}", "day": task["day"], "title": task["title"], "desc": task["outcome"], "prompt": task["prompt"], "standard": task["standard"], "status": status, "version": "未提交", "score": 0, "risk": "正常" if status != "未开始" else "等待", "portfolio": False, "draft": "", "ai_feedback": "", "teacher_review": ""}
    item.update(overrides); return item

def init_workspace_state():
    st.session_state.setdefault("course_templates", COURSE_TEMPLATES)
    if "task_instances" not in st.session_state:
        st.session_state["task_instances"] = [
            build_instance("张同学", "growth_5d", "g_day1", "已点评", version="第一版", score=22, teacher_review="目标清楚，可以进入 Day 2。"),
            build_instance("张同学", "growth_5d", "g_day2", "进行中"), build_instance("张同学", "growth_5d", "g_day3", "未开始"), build_instance("张同学", "growth_5d", "g_day4", "未开始"), build_instance("张同学", "growth_5d", "g_day5", "未开始"),
            build_instance("李同学", "growth_5d", "g_day3", "待老师点评", version="第二版", risk="表达不清", draft="已提交第二版复杂任务拆解。", ai_feedback="AI 已建议补充异常分支。"),
            build_instance("王同学", "freelance_5d", "f_day1", "已提交", version="第一版", risk="未看AI反馈", draft="我可以提供 AI PPT 美化服务。"),
            build_instance("企业A组", "enterprise_dept", "e_1", "AI已反馈", version="第一版", risk="待人工判断", draft="部门高频任务：周报、会议纪要、客户回复。", ai_feedback="AI反馈：任务频率清楚，但缺少评分标准。"),
        ]

def get_item(item_id: str) -> dict:
    init_workspace_state()
    for item in st.session_state["task_instances"]:
        if item["id"] == item_id: return item
    raise KeyError(item_id)

def set_item_status(item: dict, status: str):
    item["status"] = status
    if status == "已入作品集": item["portfolio"] = True
    if status in {"已提交","AI已反馈","待老师点评","已点评","已入作品集"} and item["version"] == "未提交": item["version"] = "第一版"

def status_flow_html(status: str) -> str:
    current = STATUS_ORDER.index(status) if status in STATUS_ORDER else 0
    html = "<div class='state-line'>"
    for i, step in enumerate(STATUS_ORDER):
        cls = "done" if i < current else "on" if i == current else ""
        html += f"<span class='state-step {cls}'>{step}</span>"
    return html + "</div>"

def workspace_df() -> pd.DataFrame:
    init_workspace_state(); rows = []
    for it in st.session_state["task_instances"]:
        rows.append({"学员": it["student"], "课程": it["course"], "Day/模块": it["day"], "作品/任务": it["title"], "模板ID": it["course_id"] + "/" + it["task_key"], "版本": it["version"], "状态": it["status"], "评分": it["score"] or "-", "风险": it["risk"], "作品集": "是" if it["portfolio"] else "否"})
    return pd.DataFrame(rows)

def normalized_tables() -> dict[str, pd.DataFrame]:
    init_workspace_state(); courses=[]; tasks=[]; instances=[]; enrollments={}; reviews=[]; now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for cid, course in COURSE_TEMPLATES.items():
        courses.append({"course_id": cid, "name": course["name"], "audience": course["audience"], "promise": course["promise"], "is_active": True})
        for task in course["tasks"]: tasks.append({"task_key": task["task_key"], "course_id": cid, "day": task["day"], "title": task["title"], "outcome": task["outcome"], "prompt": task["prompt"], "standard": task["standard"]})
    for it in st.session_state["task_instances"]:
        eid = it.get("enrollment_id") or f"{safe_id(it['student'])}_{it['course_id']}"; enrollments[eid] = {"enrollment_id": eid, "student_name": it["student"], "course_id": it["course_id"], "status": "学习中", "created_at": now}
        instances.append({"instance_id": it["id"], "enrollment_id": eid, "student": it["student"], "course_id": it["course_id"], "task_key": it["task_key"], "status": it["status"], "version": it["version"], "draft": it["draft"], "ai_feedback": it["ai_feedback"], "teacher_review": it["teacher_review"], "score": it["score"], "portfolio": it["portfolio"], "risk": it["risk"]})
        if it.get("teacher_review"): reviews.append({"review_id": f"review_{it['id']}", "instance_id": it["id"], "reviewer": "模拟老师", "score": it["score"], "conclusion": "已入作品集" if it.get("portfolio") else it["status"], "review_text": it["teacher_review"], "created_at": now})
    return {"courses": pd.DataFrame(courses), "task_templates": pd.DataFrame(tasks), "enrollments": pd.DataFrame(list(enrollments.values())), "task_instances": pd.DataFrame(instances), "reviews": pd.DataFrame(reviews)}

def make_csv_zip(tables: dict[str, pd.DataFrame]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, df in tables.items(): zf.writestr(f"{name}.csv", df.to_csv(index=False).encode("utf-8-sig"))
    return buffer.getvalue()

def render_top_nav(lang: str):
    st.markdown("""<div class='nav'><div class='nav-inner'><div class='brand'><div class='logo'>AI</div><div>AI Skill Growth Platform<small>技能成长 · 模板引擎 · 数据持久化准备</small></div></div><div class='badges'><span class='badge'>课程模板</span><span class='badge'>任务实例</span><span class='badge'>CSV持久化</span><span class='badge cta'>预约体验课</span></div></div></div>""", unsafe_allow_html=True)
    nav_keys=["home","workspace","trial","sop","paths","skills","portfolio","freelance","company","pricing","booking","faq"]
    st.markdown("<div class='nav-panel'>", unsafe_allow_html=True)
    page=st.radio(TEXT[lang]["nav"], nav_keys, horizontal=True, label_visibility="collapsed", format_func=lambda key: TEXT[lang][key], key="top_page_nav")
    st.markdown("</div>", unsafe_allow_html=True); return page

def render_offer_section():
    section("PROGRAMS", "选择你的技能成长入口", "每个产品对应一个清晰目标和交付结果。")
    offers=[("低门槛开始","2 小时体验课","99 / 199 元","现场完成一个微型任务，拿到一版 AI 学习路径。"),("主推","5 天技能成长营","3999 元建议","形成 3 个可展示作品、反馈记录和表达稿。"),("自由职业","5 天技能变现营","4999 元建议","形成服务包、报价单、样品案例和交付 SOP。"),("企业版","企业 AI 技能内训","3 万元起","把部门高频任务改造成可训练、可评分的 AI 工作流。")]
    html="<div class='grid4'>"
    for tag,title,price,body in offers:
        html+=f"<div class='offer {'featured' if tag=='主推' else ''}'><span class='tag'>{tag}</span><h3>{title}</h3><div class='price'>{price}</div><p>{body}</p></div>"
    st.markdown(html+"</div>", unsafe_allow_html=True)

def render_home(lang: str):
    st.markdown("""<div class='hero'><span class='eyebrow'>AI Skill Growth Platform</span><h1>AI 技能成长<br><span>教育平台</span></h1><p><b>用 AI 更快学会新技能，并做出可展示、可交付、可变现的成果。</b><br>v3.5：真实后端准备版，先用五张表和 CSV 导入导出模拟持久化。</p><span class='btn primary'>🚀 预约 2 小时体验课</span><span class='btn secondary'>🧑‍💻 进入学习工作台</span><div><span class='pill'>课程表</span><span class='pill'>任务模板表</span><span class='pill'>报名表</span><span class='pill'>任务实例表</span><span class='pill'>点评表</span></div></div>""", unsafe_allow_html=True)
    flow=[("01","课程模板"),("02","任务模板"),("03","报名实例"),("04","任务实例"),("05","老师点评"),("06","CSV持久化")]
    section("METHOD", "从原型到后端的过渡", "现在先用 Streamlit session_state + CSV 模拟，下一步可以接 Supabase / SQLite / PostgreSQL。")
    st.markdown("<div class='flow'>"+"".join(f"<div><b>{n}</b><span>{t}</span></div>" for n,t in flow)+"</div>", unsafe_allow_html=True); render_offer_section()

def current_student_items(student: str = "张同学") -> list[dict]:
    init_workspace_state(); return [it for it in st.session_state["task_instances"] if it["student"] == student and it["course_id"] == "growth_5d"]

def current_item() -> dict:
    items=current_student_items("张同学")
    for status in ["进行中","已提交","AI已反馈","待老师点评","已点评"]:
        for item in items:
            if item["status"] == status: return item
    return items[0]

def render_state_flow(item: dict):
    section("STATE FLOW", "v3.5 任务实例状态流", "状态流作用在学员任务实例上，实例未来对应数据库 task_instances 表。")
    st.markdown(f"<div class='state-card'><b>{item['day']}｜{item['title']}</b><p>实例ID：{item['id']}<br>模板：{item['course_id']} / {item['task_key']}<br>交付物：{item['desc']}</p>{status_flow_html(item['status'])}<p>当前状态：{chip(item['status'])}　版本：{item['version']}　评分：{item['score'] or '-'}</p></div>", unsafe_allow_html=True)
    cols=st.columns(5)
    if cols[0].button("提交第一版", key=f"flow_submit_{item['id']}"): set_item_status(item,"已提交"); item["version"]="第一版"; item["draft"]=st.session_state.get("student_first_draft","") or f"模拟第一版作品：{item['desc']}"; item["risk"]="等待AI反馈"; st.rerun()
    if cols[1].button("生成 AI 反馈", key=f"flow_ai_{item['id']}"): set_item_status(item,"AI已反馈"); item["ai_feedback"]=f"AI反馈：已根据模板标准检查。当前作品需要对照“{item['standard']}”补充遗漏，并把内容改成可执行格式。"; item["risk"]="遗漏场景较多"; st.rerun()
    if cols[2].button("提交老师点评", key=f"flow_teacher_{item['id']}"): set_item_status(item,"待老师点评"); item["risk"]="待人工判断"; st.rerun()
    if cols[3].button("老师已点评", key=f"flow_reviewed_{item['id']}"): set_item_status(item,"已点评"); item["score"]=21; item["teacher_review"]="老师点评：可以进入第二版修改。补齐关键遗漏后，可进入作品集候选。"; item["risk"]="需二版修改"; st.rerun()
    if cols[4].button("收入作品集", key=f"flow_portfolio_{item['id']}"): set_item_status(item,"已入作品集"); item["score"]=max(int(item["score"] or 0),23); item["teacher_review"]=item["teacher_review"] or "老师点评：达到作品集展示标准。"; item["risk"]="正常"; st.rerun()

def render_student_workspace():
    item=current_item(); user_items=current_student_items("张同学")
    completed=sum(1 for it in user_items if it["status"] in {"已点评","已入作品集"}); progress=min(20+completed*15+(10 if item["status"] in {"已提交","AI已反馈","待老师点评"} else 0),95)
    st.markdown(f"<div class='workspace-hero'><div class='workspace-head'><div><span class='label'>模拟学员账号</span><h2>张同学 · {item['course']}</h2><p>当前任务实例：{item['day']} / {item['title']} {chip(item['status'])}</p></div><div class='student-card'><b>学习完成度</b><p>整体进度：{progress}%</p><div class='progress-wrap'><div class='progress-bar' style='width:{progress}%'></div></div></div></div></div>", unsafe_allow_html=True)
    render_state_flow(item); section("PATH", "从课程模板生成的 5 天任务实例", "每一行都是一个学员任务实例。")
    cards=""
    for it in user_items:
        cls="active" if it["id"]==item["id"] else "done" if it["status"] in ["已点评","已入作品集"] else ""
        cards += f"<div class='day-card {cls}'><b>{it['day']}</b><p>{it['title']}</p>{chip(it['status'])}</div>"
    st.markdown("<div class='grid3'>"+cards+"</div>", unsafe_allow_html=True)
    left,right=st.columns([1.05,.95])
    with left:
        section("TODAY", "今日任务", f"今日任务：完成 {item['title']}。")
        st.markdown(f"<div class='task-panel'><h3>{item['title']}</h3><p><b>交付物：</b>{item['desc']}</p><p><b>做到什么标准：</b>{item['standard']}</p></div>", unsafe_allow_html=True)
    with right:
        section("PROMPT", "模板提示词", "提示词来自课程任务模板。")
        st.code(item["prompt"], language="text")
        st.markdown(f"<div class='teacher-box'><b>AI反馈：</b><br>{item['ai_feedback'] or '暂无。'}<br><br><b>老师点评：</b><br>{item['teacher_review'] or '暂无。'}</div>", unsafe_allow_html=True)
    draft=st.text_area("粘贴你的第一版作品", value=item["draft"], height=200, placeholder=f"请提交：{item['desc']}", key="student_first_draft")
    if st.button("保存到当前任务实例草稿", type="primary"): item["draft"]=draft; set_item_status(item,"进行中") if item["status"]=="未开始" else None; st.success("已保存到当前会话。")

def render_teacher_review_workspace():
    init_workspace_state(); section("TEACHER REVIEW", "老师点评端", "点评未来对应 reviews 表，同时回写 task_instances。")
    df=workspace_df(); st.dataframe(df[df["状态"].isin(["待老师点评","AI已反馈","已提交","已点评","已入作品集"])], use_container_width=True, hide_index=True)
    options=[f"{it['id']}｜{it['student']}｜{it['title']}｜{it['status']}" for it in st.session_state["task_instances"] if it["status"] in ["待老师点评","AI已反馈","已提交","已点评","已入作品集"]]
    if not options: st.info("暂无待点评作品。"); return
    item=get_item(st.selectbox("选择待点评作品", options, key="review_select_v35").split("｜",1)[0])
    left,right=st.columns([1.05,.95])
    with left:
        st.markdown(f"<div class='review-card'><b>当前点评对象：</b>{item['student']} / {item['title']} {chip(item['status'])}<p><b>模板标准：</b>{item['standard']}</p><p><b>草稿：</b>{item['draft'] or '暂无草稿'}</p><p><b>AI反馈：</b>{item['ai_feedback'] or '暂无AI反馈'}</p></div>", unsafe_allow_html=True)
        review_text=st.text_area("老师可编辑点评", value=item["teacher_review"] or "请根据模板标准补充遗漏，并把输出改成可执行格式。", height=160, key=f"teacher_review_text_{item['id']}")
    with right:
        section("RUBRIC", "评分标准", "先标准化，再个性化点评。")
        score=sum([st.slider("目标清楚",1,5,4,key=f"clarity_{item['id']}"),st.slider("结构完整",1,5,3,key=f"structure_{item['id']}"),st.slider("可执行程度",1,5,3,key=f"executable_{item['id']}"),st.slider("遗漏检查",1,5,2,key=f"omissions_{item['id']}"),st.slider("表达清楚",1,5,3,key=f"expression_{item['id']}")])
        st.markdown(f"<div class='rubric-card'><b>模拟总分：{score} / 25</b><p>23 分以上可进入作品集候选。</p></div>", unsafe_allow_html=True)
    a,b,c=st.columns(3)
    if a.button("保存老师点评", key=f"save_review_{item['id']}"): item["teacher_review"]=review_text; item["score"]=score; set_item_status(item,"已点评"); item["risk"]="需修改" if score<23 else "可入作品集"; st.rerun()
    if b.button("退回修改", key=f"return_review_{item['id']}"): item["teacher_review"]=review_text+"\n结论：退回修改。"; item["score"]=score; set_item_status(item,"已点评"); item["risk"]="风险"; st.rerun()
    if c.button("收入作品集", key=f"portfolio_review_{item['id']}"): item["teacher_review"]=review_text+"\n结论：达到展示标准，收入作品集。"; item["score"]=max(score,23); set_item_status(item,"已入作品集"); item["risk"]="正常"; st.rerun()

def render_ops_workspace():
    init_workspace_state(); section("OPERATIONS", "班主任 / 运营看板", "运营看的是任务实例状态。")
    df=workspace_df(); m1,m2,m3,m4=st.columns(4)
    m1.metric("任务实例",len(df)); m2.metric("今日应提交",int((df["状态"].isin(["进行中","未开始"])).sum())); m3.metric("待老师点评",int((df["状态"]=="待老师点评").sum())); m4.metric("风险项",int((df["风险"].isin(["风险","遗漏场景较多","未看AI反馈"])).sum()))
    st.dataframe(df,use_container_width=True,hide_index=True)
    not_submitted=df[df["状态"].isin(["未开始","进行中"])] ; waiting=df[df["状态"]=="待老师点评"] ; reviewed=df[df["状态"].isin(["已点评","已入作品集"])]
    st.markdown(f"<div class='grid3'><div class='ops-card orange'><b>未提交/进行中：{len(not_submitted)}</b><p>提醒学员先提交第一版。</p></div><div class='ops-card soft'><b>待点评：{len(waiting)}</b><p>提醒老师 24 小时内点评。</p></div><div class='ops-card green'><b>已点评/入作品集：{len(reviewed)}</b><p>提醒学员改第二版。</p></div></div>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    if c1.button("模拟一键提醒未提交学员"): st.success("已生成模拟提醒：请今晚 21:00 前提交第一版作品。")
    if c2.button("重置 v3.5 模拟数据"): st.session_state.pop("task_instances",None); init_workspace_state(); st.rerun()

def template_df(course_id: str | None = None) -> pd.DataFrame:
    rows=[]
    for cid,course in COURSE_TEMPLATES.items():
        if course_id and cid!=course_id: continue
        for task in course["tasks"]: rows.append({"课程模板ID":cid,"课程名称":course["name"],"Day/模块":task["day"],"任务Key":task["task_key"],"任务标题":task["title"],"交付物":task["outcome"],"做到什么标准":task["standard"]})
    return pd.DataFrame(rows)

def render_template_engine():
    init_workspace_state(); section("TEMPLATE ENGINE", "课程模板引擎", "课程模板定义路径，任务实例记录每个学员状态。")
    st.markdown("<div class='grid3'><div class='schema-card green'><b>1. 课程任务模板</b><p>定义 Day、任务标题、交付物、提示词、评分标准。</p></div><div class='schema-card soft'><b>2. 学员任务实例</b><p>从模板生成，保存状态、草稿、AI 反馈、老师点评和评分。</p></div><div class='schema-card orange'><b>3. CSV 持久化</b><p>先用 CSV 模拟数据库。</p></div></div>", unsafe_allow_html=True)
    course_options=list(COURSE_TEMPLATES.keys()); selected=st.selectbox("选择课程模板",course_options,format_func=lambda cid:COURSE_TEMPLATES[cid]["name"],key="template_course_select")
    course=COURSE_TEMPLATES[selected]; st.markdown(f"<div class='state-card'><b>{course['name']}</b><p>适用对象：{course['audience']}<br>交付承诺：{course['promise']}</p></div>",unsafe_allow_html=True)
    st.dataframe(template_df(selected),use_container_width=True,hide_index=True)
    left,right=st.columns([1,1])
    with left:
        new_student=st.text_input("学员 / 小组名称",value="新学员",key="new_student_name")
        if st.button("为该学员生成整套任务实例",type="primary"):
            existing=len(st.session_state["task_instances"])
            for task in course["tasks"]: st.session_state["task_instances"].append(build_instance(new_student,selected,task["task_key"],"进行中" if task==course["tasks"][0] else "未开始"))
            st.success(f"已生成 {len(course['tasks'])} 个任务实例。当前实例总数：{existing} → {len(st.session_state['task_instances'])}")
    with right: st.code("CourseTemplate -> TaskTemplate -> Enrollment -> TaskInstance -> Review",language="text")
    st.dataframe(workspace_df(),use_container_width=True,hide_index=True)

def render_backend_prep():
    init_workspace_state(); subhero("V3.5 BACKEND PREP","真实后端准备：五张表 + CSV 导出/上传","先不接数据库。用规范化表结构和 CSV 文件模拟持久化，为后续 Supabase / PostgreSQL / SQLite 迁移做准备。")
    tables=normalized_tables(); section("SCHEMA","五张核心表","这个数据模型已经能覆盖课程、任务、报名、学员作品、老师点评。")
    st.markdown("<div class='grid3'>"+"".join(f"<div class='schema-card'><b>{name}</b><p>{len(fields)} fields</p></div>" for name,fields in TABLE_SCHEMAS.items())+"</div>", unsafe_allow_html=True)
    schema_name=st.selectbox("查看表字段",list(TABLE_SCHEMAS.keys()),key="schema_table_select")
    st.dataframe(pd.DataFrame(TABLE_SCHEMAS[schema_name],columns=["字段","类型","说明"]),use_container_width=True,hide_index=True)
    section("EXPORT","CSV 导出","可下载单表 CSV，也可下载全部五张表 ZIP。")
    table_name=st.selectbox("选择导出表",list(tables.keys()),key="export_table_select")
    st.dataframe(tables[table_name],use_container_width=True,hide_index=True)
    st.download_button(f"下载 {table_name}.csv",data=tables[table_name].to_csv(index=False).encode("utf-8-sig"),file_name=f"{table_name}.csv",mime="text/csv")
    st.download_button("下载全部五张表 ZIP",data=make_csv_zip(tables),file_name="ai_skill_growth_v35_tables.zip",mime="application/zip")
    section("IMPORT","CSV 上传模拟恢复","目前先支持上传 task_instances.csv，恢复任务状态、草稿、AI反馈、老师点评和作品集标记。")
    uploaded=st.file_uploader("上传 task_instances.csv",type=["csv"],key="upload_task_instances")
    if uploaded is not None:
        try:
            df=pd.read_csv(uploaded).fillna(""); required={"instance_id","student","course_id","task_key","status"}
            if not required.issubset(set(df.columns)): st.error("CSV 缺少必要字段：instance_id, student, course_id, task_key, status")
            elif st.button("用上传 CSV 恢复 task_instances"):
                restored=[]
                for _,row in df.iterrows():
                    cid,tk=str(row["course_id"]),str(row["task_key"])
                    if cid in COURSE_TEMPLATES and any(t["task_key"]==tk for t in COURSE_TEMPLATES[cid]["tasks"]):
                        restored.append(build_instance(str(row["student"]),cid,tk,str(row["status"]),id=str(row["instance_id"]),enrollment_id=str(row.get("enrollment_id","")),version=str(row.get("version","未提交")),draft=str(row.get("draft","")),ai_feedback=str(row.get("ai_feedback","")),teacher_review=str(row.get("teacher_review","")),score=int(row.get("score",0) or 0),portfolio=str(row.get("portfolio","False")).lower() in {"true","1","yes","是"},risk=str(row.get("risk","正常"))))
                st.session_state["task_instances"]=restored; st.success(f"已恢复 {len(restored)} 条任务实例。"); st.rerun()
        except Exception as exc: st.error(f"读取 CSV 失败：{exc}")
    section("MIGRATION","迁移到真实后端的建议","下一步可选 Supabase / PostgreSQL。Streamlit 只保留前端和管理操作。")
    st.code("""建议迁移顺序：
1. 先建 courses 和 task_templates 两张静态表。
2. 再建 enrollments，记录学员选择了哪套课程。
3. 创建报名时自动批量生成 task_instances。
4. 学员提交作品时更新 task_instances.draft/status。
5. AI 反馈写入 task_instances.ai_feedback。
6. 老师点评写入 reviews，并回写 task_instances.score/status/portfolio。
7. 班主任看板只读 task_instances + reviews 聚合结果。""",language="text")

def render_learning_workspace(lang: str):
    init_workspace_state(); subhero("V3.5 BACKEND READY","学习工作台：后端准备版","在 v3.4 模板引擎基础上，加入五张表设计、CSV 导出、task_instances 上传恢复。")
    tabs=st.tabs(["学员端","老师点评端","班主任 / 运营看板","课程模板引擎","后端准备 / CSV"])
    with tabs[0]: render_student_workspace()
    with tabs[1]: render_teacher_review_workspace()
    with tabs[2]: render_ops_workspace()
    with tabs[3]: render_template_engine()
    with tabs[4]: render_backend_prep()

def render_trial(lang: str):
    subhero("2-HOUR TRIAL","AI 技能成长 2 小时体验课","低门槛入口产品。目标不是讲很多理论，而是在 2 小时内帮用户完成一个真实小任务。")
    cards=[("推荐价格","99 / 199 元：降低决策门槛，用真实体验建立信任。"),("适合谁","想学新技能、升职表达、转岗跳槽、做作品集、自由职业接单、企业内训负责人。"),("核心承诺","2 小时内不空谈，必须完成一个微型任务。")]
    st.markdown("<div class='grid3'>"+"".join(html_card("✅",a,b,"card green") for a,b in cards)+"</div>",unsafe_allow_html=True)

def render_followup_sop(lang: str):
    subhero("SALES SOP","飞书线索跟进 SOP / 成交话术","飞书收到线索只是开始。这个页面指导销售如何跟进、邀约、收款、转化和复盘。")
    statuses=[("新线索","5 分钟内响应"),("已联系","发送第一条回复"),("已约时间","确定体验课时间"),("已付款","确认 99/199 体验课"),("已上课","进入课后转化"),("已转化","进入 5 天营/企业方案"),("未转化","记录原因，7 天后触达")]
    st.markdown("<div class='grid4'>"+"".join(f"<div class='card soft'><b>{a}</b><p>{b}</p></div>" for a,b in statuses)+"</div>",unsafe_allow_html=True)

def render_paths(lang: str):
    subhero("GROWTH PATHS","成长路径","平台先帮你选路径，再把路径拆成任务。")
    st.dataframe(pd.DataFrame([{"场景":a,"目标":b,"训练重点":c} for a,b,c in MOTIVE_ROWS]),use_container_width=True,hide_index=True)

def render_skills(lang: str):
    subhero("SKILL TRAINING","技能训练","AI 把学习过程变成训练闭环。")
    steps=[("01","定技能目标"),("02","选择课程模板"),("03","生成任务实例"),("04","AI 先纠错"),("05","老师再点评"),("06","提交作品")]
    st.markdown("<div class='flow'>"+"".join(f"<div><b>{n}</b><span>{t}</span></div>" for n,t in steps)+"</div>",unsafe_allow_html=True)
    st.markdown("<div class='grid3'>"+"".join(html_card("🧠",a,b) for a,b in SKILL_ROWS)+"</div>",unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{"方向":a,"可训练技能":b} for a,b in ROLE_ROWS]),use_container_width=True,hide_index=True)

def render_portfolio(lang: str):
    subhero("PORTFOLIO","作品集","升职、转岗、跳槽、接单时，最有说服力的是能被检查的作品。")
    init_workspace_state(); items=[it for it in st.session_state["task_instances"] if it.get("portfolio")]
    if items: st.markdown("<div class='grid3'>"+"".join(f"<div class='portfolio-card'><h4>{it['student']} / {it['title']}</h4><p>{it['desc']}</p>{chip('已入作品集')}</div>" for it in items)+"</div>",unsafe_allow_html=True)
    else: st.info("当前会话还没有收入作品集的作品。")

def render_freelance(lang: str):
    subhero("FREELANCE","自由职业者：学新技能，赚更多钱","不是保证收入，而是训练你把技能包装成可出售服务。")
    st.markdown("<div class='grid3'>"+"".join(html_card("💼",a,b) for a,b in FREELANCE_ROWS)+"</div>",unsafe_allow_html=True)

def render_company(lang: str):
    subhero("COMPANY TRAINING","企业内训","企业需要的不只是 AI 讲座，而是新人上手、在岗提升和部门技能训练体系。")
    items=[("新人上手","学习路径、任务练习、AI 反馈和老师点评标准化。"),("在岗提升","把部门高频任务做成 AI 学习与工作流模板。"),("部门模板","沉淀日报、周报、会议纪要、客户回复、PPT、数据说明模板。"),("合规边界","企业数据脱敏，关键输出必须人工审核。")]
    st.markdown("<div class='grid4'>"+"".join(html_card("🏢",a,b) for a,b in items)+"</div><div class='card orange'><b>数据安全</b><p>企业数据必须脱敏；不上传商业秘密、客户隐私、合同原文、财务敏感数据。</p></div>",unsafe_allow_html=True)

def render_pricing(lang: str):
    subhero("PRICING","报价与产品入口","价格不是按讲师小时数，而是按训练结果。")
    render_offer_section()

def render_booking(lang: str):
    subhero("BOOKING","预约体验课 / 咨询方案","填写后可生成咨询摘要，也可自动发送到你配置的 Webhook。")
    provider=get_secret("WEBHOOK_PROVIDER","未配置"); configured=bool(get_secret("LEAD_WEBHOOK_URL"))
    status_class = "green" if configured else "orange"
    status_text = "已配置：提交后会按 " + provider + " 格式自动发送线索。" if configured else "未配置：线索不会自动保存，请下载 TXT/CSV 或用邮件发送。"
    st.markdown(f"<div class='card {status_class}'><b>Webhook 状态</b><p>{status_text}</p></div>",unsafe_allow_html=True)
    left,right=st.columns([1.05,.95])
    with left:
        with st.form("booking_form"):
            name=st.text_input("姓名 / 称呼"); contact=st.text_input("联系方式（微信 / 邮箱 / 手机，任选）")
            identity=st.selectbox("你现在属于哪类人？",["职场新人","在岗提升","升职准备","转岗 / 跳槽","自由职业 / 副业接单","企业培训负责人","小微老板"])
            goal=st.selectbox("你最想解决什么？",["学新技能","提升现有技能","做作品集","升职表达","换工作 / 高薪跳槽","自由职业接单","企业内训"])
            skill=st.text_input("想学习或提升的具体技能",placeholder="例如：PPT汇报、销售话术、测试用例、Java项目、自由职业服务包")
            time_budget=st.selectbox("你愿意投入的时间",["2 小时体验","1 天入门","5 天训练营","4 周小班","企业内训待沟通"])
            note=st.text_area("补充说明"); submitted=st.form_submit_button("生成并提交咨询摘要")
    with right: st.markdown("<div class='card soft'><b>大陆优先推荐</b><p>飞书机器人 / 企业微信机器人 / 腾讯云函数 / 阿里云函数 / 自建接口。</p></div>",unsafe_allow_html=True)
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
补充说明：{note or '无'}"""
        lead["summary"]=summary; st.session_state.setdefault("leads",[]).append(lead); ok,msg=post_lead_to_webhook(lead)
        st.success("咨询摘要已生成。"); st.info(msg)
        if ok: st.success("线索已发送到 Webhook。")
        st.markdown(f"<div class='summary'>{summary}</div>",unsafe_allow_html=True)
        df=pd.DataFrame([lead]); st.download_button("下载 TXT 摘要",data=summary,file_name="ai_skill_growth_lead.txt",mime="text/plain")
        st.download_button("下载 CSV 线索",data=df.to_csv(index=False).encode("utf-8-sig"),file_name="ai_skill_growth_lead.csv",mime="text/csv")
        mailto=f"mailto:{get_secret('OWNER_EMAIL')}?subject="+quote("AI技能成长咨询摘要")+"&body="+quote(summary)
        st.markdown(f"<a class='mail-link' href='{mailto}'>用邮件发送摘要</a>",unsafe_allow_html=True)
    section("WEBHOOK CONFIG","大陆可用配置示例","在 Streamlit Cloud 的 App settings / Secrets 中加入以下配置。")
    st.code('LEAD_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"\nWEBHOOK_PROVIDER = "feishu"\nOWNER_EMAIL = "your-email@example.com"',language="toml")

def render_faq(lang: str):
    subhero("FAQ","常见问题","把风险边界说清楚，比夸大承诺更能建立信任。")
    qs=[("这是不是只适合新人？","不是。新人、想升职的人、转岗的人、跳槽高薪的人、自由职业者、想带团队的人都适合。"),("这是不是 AI 办公提效课？","不是。提效只是副产品，核心是学习新技能、提升技能，并做出可展示成果。"),("会不会承诺就业、涨薪、接单收入或证书？","不承诺。平台交付技能路径、作品集、服务包和表达能力，不做官方职业资格或收入保证。"),("AI 会不会替代老师？","不会。AI 做第一轮解释和反馈，老师负责任务设计、标准把关和关键点评。")]
    st.markdown("<div class='grid2'>"+"".join(html_card("❓",q,a) for q,a in qs)+"</div>",unsafe_allow_html=True)

def main():
    lang=st.radio("语言",["zh"],horizontal=True,label_visibility="collapsed",format_func=lambda x:"中文",key="lang_nav")
    page=render_top_nav(lang)
    if page=="home": render_home(lang)
    elif page=="workspace": render_learning_workspace(lang)
    elif page=="trial": render_trial(lang)
    elif page=="sop": render_followup_sop(lang)
    elif page=="paths": render_paths(lang)
    elif page=="skills": render_skills(lang)
    elif page=="portfolio": render_portfolio(lang)
    elif page=="freelance": render_freelance(lang)
    elif page=="company": render_company(lang)
    elif page=="pricing": render_pricing(lang)
    elif page=="booking": render_booking(lang)
    else: render_faq(lang)
    st.markdown("<div class='mobile-sticky'><span class='m1'>预约体验课</span><span>学习工作台</span></div>", unsafe_allow_html=True)
    st.caption("AI Skill Growth Platform · backend prep with CSV persistence prototype v3.5")

if __name__ == "__main__":
    main()
