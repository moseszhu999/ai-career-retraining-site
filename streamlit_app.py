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
:root{--ink:#0f172a;--muted:#64748b;--brand:#4f46e5;--brand2:#06b6d4;--line:#e2e8f0}.main .block-container{max-width:1180px;padding-top:.7rem;padding-bottom:5rem}[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none}.nav{position:sticky;top:.45rem;z-index:999;margin-bottom:1rem}.nav-inner{display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:.72rem .95rem;border:1px solid #c7d2fe;border-radius:1.25rem;background:rgba(255,255,255,.94);box-shadow:0 14px 34px rgba(15,23,42,.08)}.brand{display:flex;gap:.62rem;align-items:center;font-weight:950;color:#111827}.logo{width:36px;height:36px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:white}.brand small{display:block;color:var(--muted);font-weight:800}.badges{display:flex;gap:.45rem;flex-wrap:wrap}.badge,.pill,.tag,.status-chip{display:inline-block;border-radius:999px;padding:.28rem .62rem;font-weight:900;font-size:.82rem}.badge,.pill,.tag{background:#f8fafc;border:1px solid var(--line);color:#475569}.badge.cta{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white;border:none}.nav-panel{margin:.65rem 0 1.15rem;padding:.55rem;border:1px solid #e0e7ff;border-radius:1.2rem;background:#f8fafc}div[data-testid="stRadio"]>label{display:none}div[role="radiogroup"]{display:flex;flex-wrap:wrap;gap:.42rem}div[role="radiogroup"] label{border:1px solid #dbeafe!important;border-radius:999px!important;background:white!important;padding:.38rem .74rem!important}div[role="radiogroup"] label p{font-weight:900!important;color:#334155!important;font-size:.9rem!important}div[role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,#4f46e5,#06b6d4)!important}div[role="radiogroup"] label:has(input:checked) p{color:white!important}.hero,.subhero,.workspace-hero{border:1px solid #c7d2fe;border-radius:1.45rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 46%,#fff);box-shadow:0 18px 44px rgba(15,23,42,.08);padding:1.35rem;margin:1.15rem 0}.hero{padding:2rem}.hero h1{font-size:2.7rem;line-height:1.05;margin:.55rem 0;color:var(--ink);font-weight:980}.hero h1 span{background:linear-gradient(90deg,var(--brand),var(--brand2));-webkit-background-clip:text;color:transparent}.hero p,.subhero p{color:#475569;line-height:1.75}.eyebrow,.label{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}.btn{display:inline-flex;border-radius:999px;padding:.78rem 1.08rem;font-weight:950;margin:.25rem}.primary{background:linear-gradient(90deg,var(--brand),#7c3aed);color:white}.secondary{background:white;color:#3730a3;border:1px solid #c7d2fe}.kicker{font-size:.78rem;font-weight:950;letter-spacing:.14em;color:var(--brand);text-transform:uppercase;margin-top:1.8rem}.title{font-size:1.65rem;font-weight:950;color:var(--ink)}.sub{color:var(--muted);line-height:1.75;max-width:850px}.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:.95rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card,.offer,.task-panel,.student-card,.portfolio-card,.review-card,.ops-card,.rubric-card,.state-card,.schema-card{border:1px solid var(--line);border-radius:1.08rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045);min-height:110px}.card p,.portfolio-card p,.review-card p,.ops-card p,.state-card p,.schema-card p{color:var(--muted);line-height:1.58}.soft{background:#f8fafc;border-color:#dbeafe}.green{background:#f0fdf4;border-color:#bbf7d0}.orange{background:#fff7ed;border-color:#fed7aa}.dark{background:#0f172a;color:#e2e8f0;border-radius:1rem;padding:1rem;white-space:pre-wrap}.flow{display:grid;grid-template-columns:repeat(6,1fr);gap:.55rem}.flow div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.flow b{display:block;color:var(--brand)}.flow span{font-weight:850;color:#312e81;font-size:.82rem}.offer{border-color:#dbeafe;min-height:210px}.offer.featured{border:2px solid #4f46e5}.price{font-size:1.35rem;font-weight:980;color:#16a34a}.chip-green{background:#dcfce7;color:#166534}.chip-blue{background:#dbeafe;color:#1e40af}.chip-orange{background:#ffedd5;color:#9a3412}.chip-gray{background:#f1f5f9;color:#475569}.chip-red{background:#fee2e2;color:#991b1b}.summary{border-radius:1rem;background:#0f172a;color:#e2e8f0;padding:1rem;line-height:1.7;white-space:pre-wrap}.mobile-sticky{display:none}@media(max-width:960px){.nav{position:relative}.nav-inner{align-items:flex-start;flex-direction:column}.badges{display:none}.grid2,.grid3,.grid4{grid-template-columns:1fr}.flow{grid-template-columns:repeat(2,1fr)}}
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
    "growth_5d": {"name":"5 天 AI 技能成长营","audience":"职场新人 / 在岗提升 / 升职准备 / 转岗跳槽","promise":"3 个可展示作品 + AI 反馈记录 + 老师点评 + 30 天行动计划","tasks":[{"task_key":"g_day1","day":"Day 1","title":"定目标 + 拆任务","outcome":"技能成长路线图","prompt":"你是职业技能教练。请把我的目标拆成 5 天训练任务，并说明每天交付物。","standard":"目标明确；任务可执行；交付物可检查。"},{"task_key":"g_day2","day":"Day 2","title":"作品 1：基础任务作品","outcome":"测试用例 + Bug 报告模板","prompt":"你是严格的软件测试教练。请根据登录页面需求设计测试用例，并输出遗漏点和 Bug 报告模板。","standard":"覆盖正常、异常、边界、安全、权限；步骤可执行。"},{"task_key":"g_day3","day":"Day 3","title":"作品 2：复杂任务作品","outcome":"复杂需求拆解 + 异常场景补全","prompt":"请把复杂业务需求拆成流程、角色、输入输出、异常分支和测试点。","standard":"能解释流程；能发现异常；能说明遗漏信息。"},{"task_key":"g_day4","day":"Day 4","title":"作品 3：展示 / 发表作品","outcome":"项目发表说明 + 成果表达稿","prompt":"请把我的项目成果整理成 3 分钟发表稿，包含背景、任务、方法、结果和改进点。","standard":"表达清楚；能展示价值；能回答追问。"},{"task_key":"g_day5","day":"Day 5","title":"复盘 + 后续路径","outcome":"30 天行动计划","prompt":"请根据我的 3 个作品和老师点评，生成后续 30 天行动计划。","standard":"路径清楚；动作具体；能持续复盘。"}]},
    "freelance_5d": {"name":"5 天自由职业技能变现营","audience":"自由职业 / 副业接单者","promise":"1 个服务包 + 3 个样品案例 + 报价单 + 获客话术 + 交付 SOP","tasks":[{"task_key":"f_day1","day":"Day 1","title":"选择可售卖技能","outcome":"服务方向定位","prompt":"请帮我把一个技能转成可售卖服务方向，说明目标客户、痛点和交付物。","standard":"客户明确；痛点具体；交付边界清楚。"},{"task_key":"f_day2","day":"Day 2","title":"样品案例 1","outcome":"第一个可展示样品","prompt":"请根据目标客户场景，帮我设计一个可展示样品案例。","standard":"样品能展示能力；客户能看懂价值。"}]},
    "enterprise_dept": {"name":"企业部门 AI 训练营","audience":"企业内训部门 / 新人培养 / 部门负责人","promise":"部门任务模板 + 评分标准 + 员工练习包 + 培训复盘","tasks":[{"task_key":"e_1","day":"模块 1","title":"部门高频任务清单","outcome":"AI 训练任务地图","prompt":"请把部门高频任务整理成可训练任务清单，并标出可用 AI 辅助的环节。","standard":"任务真实；频率高；能训练。"}]},
}
TABLE_SCHEMAS = {"courses":[("course_id","PK","课程模板 ID"),("name","text","课程名称"),("audience","text","适用人群"),("promise","text","交付承诺"),("is_active","bool","是否启用")],"task_templates":[("task_key","PK","任务模板 ID"),("course_id","FK","关联 courses.course_id"),("day","text","Day / 模块"),("title","text","任务标题"),("outcome","text","交付物"),("prompt","text","AI 提示词"),("standard","text","评分标准")],"enrollments":[("enrollment_id","PK","报名 / 班级实例 ID"),("student_name","text","学员或小组名称"),("course_id","FK","课程模板 ID"),("status","text","学习中 / 结营 / 退课"),("created_at","datetime","创建时间")],"task_instances":[("instance_id","PK","学员任务实例 ID"),("enrollment_id","FK","关联报名实例"),("student","text","学员"),("course_id","FK","课程模板"),("task_key","FK","任务模板"),("status","text","学习状态"),("draft","text","作品草稿"),("ai_feedback","text","AI 反馈"),("teacher_review","text","老师点评"),("score","int","评分"),("portfolio","bool","是否入作品集")],"reviews":[("review_id","PK","点评记录 ID"),("instance_id","FK","任务实例 ID"),("reviewer","text","点评老师"),("score","int","分数"),("conclusion","text","通过 / 修改 / 退回"),("review_text","text","点评正文"),("created_at","datetime","点评时间")]}
CREATE_TABLE_SQL = """create table if not exists public.courses (course_id text primary key, name text not null, audience text, promise text, is_active boolean default true, created_at timestamptz default now());
create table if not exists public.task_templates (task_key text primary key, course_id text not null references public.courses(course_id) on delete cascade, day text, title text not null, outcome text, prompt text, standard text, sort_order int default 0, created_at timestamptz default now());
create table if not exists public.enrollments (enrollment_id text primary key, student_name text not null, course_id text not null references public.courses(course_id), status text default '学习中', owner_email text, coach_email text, created_at timestamptz default now());
create table if not exists public.task_instances (instance_id text primary key, enrollment_id text not null references public.enrollments(enrollment_id) on delete cascade, student text not null, course_id text not null references public.courses(course_id), task_key text not null references public.task_templates(task_key), status text default '未开始', version text default '未提交', draft text default '', ai_feedback text default '', teacher_review text default '', score int default 0, portfolio boolean default false, risk text default '正常', updated_at timestamptz default now());
create table if not exists public.reviews (review_id text primary key, instance_id text not null references public.task_instances(instance_id) on delete cascade, reviewer text not null, score int default 0, conclusion text, review_text text, created_at timestamptz default now());"""
TASK_TEMPLATE_SEED_SQL = """insert into public.task_templates(task_key, course_id, day, title, outcome, prompt, standard, sort_order) values
('g_day1','growth_5d','Day 1','定目标 + 拆任务','技能成长路线图','你是职业技能教练。请把我的目标拆成 5 天训练任务，并说明每天交付物。','目标明确；任务可执行；交付物可检查。',1),
('g_day2','growth_5d','Day 2','作品 1：基础任务作品','测试用例 + Bug 报告模板','你是严格的软件测试教练。请根据登录页面需求设计测试用例，并输出遗漏点和 Bug 报告模板。','覆盖正常、异常、边界、安全、权限；步骤可执行。',2),
('g_day3','growth_5d','Day 3','作品 2：复杂任务作品','复杂需求拆解 + 异常场景补全','请把复杂业务需求拆成流程、角色、输入输出、异常分支和测试点。','能解释流程；能发现异常；能说明遗漏信息。',3),
('g_day4','growth_5d','Day 4','作品 3：展示 / 发表作品','项目发表说明 + 成果表达稿','请把我的项目成果整理成 3 分钟发表稿，包含背景、任务、方法、结果和改进点。','表达清楚；能展示价值；能回答追问。',4),
('g_day5','growth_5d','Day 5','复盘 + 后续路径','30 天行动计划','请根据我的 3 个作品和老师点评，生成后续 30 天行动计划。','路径清楚；动作具体；能持续复盘。',5),
('f_day1','freelance_5d','Day 1','选择可售卖技能','服务方向定位','请帮我把一个技能转成可售卖服务方向，说明目标客户、痛点和交付物。','客户明确；痛点具体；交付边界清楚。',1),
('f_day2','freelance_5d','Day 2','样品案例 1','第一个可展示样品','请根据目标客户场景，帮我设计一个可展示样品案例。','样品能展示能力；客户能看懂价值。',2),
('e_1','enterprise_dept','模块 1','部门高频任务清单','AI 训练任务地图','请把部门高频任务整理成可训练任务清单，并标出可用 AI 辅助的环节。','任务真实；频率高；能训练。',1)
on conflict (task_key) do update set course_id=excluded.course_id, day=excluded.day, title=excluded.title, outcome=excluded.outcome, prompt=excluded.prompt, standard=excluded.standard, sort_order=excluded.sort_order;"""
RLS_SQL = """-- v3.9 仍建议先不开 RLS。真实读写闭环跑通后，v4.0 再做登录与权限。
-- alter table public.courses enable row level security;
-- alter table public.task_templates enable row level security;"""

def get_secret(name: str, default: str = "") -> str:
    try: return str(st.secrets.get(name, default))
    except Exception: return default

def secret_is_configured(name: str) -> bool:
    value = get_secret(name, "")
    return bool(value and value.strip() and "YOUR_" not in value and "xxxx" not in value)

def supabase_config_status() -> dict:
    return {"SUPABASE_URL": secret_is_configured("SUPABASE_URL"), "SUPABASE_ANON_KEY": secret_is_configured("SUPABASE_ANON_KEY")}

def db_ready() -> bool: return all(supabase_config_status().values())

def get_supabase_client():
    from supabase import create_client
    return create_client(get_secret("SUPABASE_URL"), get_secret("SUPABASE_ANON_KEY"))

def db_select(table: str, columns: str = "*", limit: int = 300) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready(): return False, "未配置 Supabase，当前为模拟模式。", pd.DataFrame()
    try:
        res = get_supabase_client().table(table).select(columns).limit(limit).execute()
        return True, f"读取 {table} 成功：{len(res.data or [])} 条。", pd.DataFrame(res.data or [])
    except Exception as exc:
        return False, f"读取 {table} 失败：{exc}", pd.DataFrame()

def db_tasks_for_course(course_id: str) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready(): return False, "未配置 Supabase，当前为模拟模式。", pd.DataFrame()
    try:
        res = get_supabase_client().table("task_templates").select("*").eq("course_id", course_id).order("sort_order").execute()
        return True, f"读取任务模板成功：{len(res.data or [])} 条。", pd.DataFrame(res.data or [])
    except Exception as exc:
        return False, f"读取任务模板失败：{exc}", pd.DataFrame()

def db_task_instances(enrollment_id: str | None = None) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready(): return False, "未配置 Supabase，当前为模拟模式。", pd.DataFrame()
    try:
        query = get_supabase_client().table("task_instances").select("*").order("updated_at", desc=True).limit(300)
        if enrollment_id: query = query.eq("enrollment_id", enrollment_id)
        res = query.execute()
        return True, f"读取 task_instances 成功：{len(res.data or [])} 条。", pd.DataFrame(res.data or [])
    except Exception as exc:
        return False, f"读取 task_instances 失败：{exc}", pd.DataFrame()

def db_update_task_instance(instance_id: str, updates: dict) -> tuple[bool, str]:
    if not db_ready(): return False, "未配置 Supabase，无法写入真实数据库。"
    try:
        updates = {**updates, "updated_at": datetime.now().isoformat()}
        get_supabase_client().table("task_instances").update(updates).eq("instance_id", instance_id).execute()
        return True, f"已更新 task_instances：{instance_id}"
    except Exception as exc:
        return False, f"更新失败：{exc}"

def create_real_enrollment(student_name: str, course_id: str, owner_email: str = "", coach_email: str = "") -> tuple[bool, str, str]:
    student_name = student_name.strip()
    if not student_name: return False, "请先输入学员名。", ""
    if not db_ready(): return False, "未配置 Supabase，无法写入真实数据库。", ""
    ok, msg, tasks = db_tasks_for_course(course_id)
    if not ok: return False, msg, ""
    if tasks.empty: return False, "该课程还没有 task_templates。请先运行 task_templates seed SQL。", ""
    try:
        client = get_supabase_client(); stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        enrollment_id = f"enr_{safe_id(student_name)}_{course_id}_{stamp}"
        enrollment = {"enrollment_id": enrollment_id, "student_name": student_name, "course_id": course_id, "status": "学习中", "owner_email": owner_email.strip() or None, "coach_email": coach_email.strip() or None}
        client.table("enrollments").insert(enrollment).execute()
        rows = []
        for i, task in tasks.reset_index(drop=True).iterrows():
            status = "进行中" if i == 0 else "未开始"
            rows.append({"instance_id": f"ti_{safe_id(student_name)}_{task['task_key']}_{stamp}", "enrollment_id": enrollment_id, "student": student_name, "course_id": course_id, "task_key": task["task_key"], "status": status, "version": "未提交", "draft": "", "ai_feedback": "", "teacher_review": "", "score": 0, "portfolio": False, "risk": "正常" if status == "进行中" else "等待"})
        client.table("task_instances").insert(rows).execute()
        return True, f"已创建报名 {enrollment_id}，并生成 {len(rows)} 条任务实例。", enrollment_id
    except Exception as exc: return False, f"写入失败：{exc}", ""

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

def html_card(icon: str, title: str, body: str, cls: str = "card") -> str: return f"<div class='{cls}'><b>{icon} {title}</b><p>{body}</p></div>"
def safe_id(text: str) -> str: return re.sub(r"[^a-zA-Z0-9_]+", "_", text.strip()).strip("_") or "item"
def chip(status: str) -> str: return f"<span class='status-chip {STATUS_CHIP.get(status, 'chip-gray')}'>{status}</span>"
def v(row, col, default=""):
    try:
        val = row.get(col, default)
        return default if pd.isna(val) else val
    except Exception: return default

def template_task(course_id: str, task_key: str) -> dict:
    for task in COURSE_TEMPLATES[course_id]["tasks"]:
        if task["task_key"] == task_key: return task
    raise KeyError(task_key)

def build_instance(student: str, course_id: str, task_key: str, status: str = "未开始", **overrides) -> dict:
    course = COURSE_TEMPLATES[course_id]; task = template_task(course_id, task_key)
    item = {"id": f"{safe_id(student)}_{course_id}_{task_key}_{len(st.session_state.get('task_instances', []))}", "student": student, "course_id": course_id, "course": course["name"], "task_key": task_key, "enrollment_id": f"{safe_id(student)}_{course_id}", "day": task["day"], "title": task["title"], "desc": task["outcome"], "prompt": task["prompt"], "standard": task["standard"], "status": status, "version": "未提交", "score": 0, "risk": "正常" if status != "未开始" else "等待", "portfolio": False, "draft": "", "ai_feedback": "", "teacher_review": ""}
    item.update(overrides); return item

def init_workspace_state():
    if "task_instances" not in st.session_state:
        st.session_state["task_instances"] = [build_instance("张同学", "growth_5d", "g_day1", "已点评", version="第一版", score=22, teacher_review="目标清楚，可以进入 Day 2。"), build_instance("张同学", "growth_5d", "g_day2", "进行中"), build_instance("李同学", "growth_5d", "g_day3", "待老师点评", version="第二版", risk="表达不清", draft="已提交第二版复杂任务拆解。", ai_feedback="AI 已建议补充异常分支。"), build_instance("王同学", "freelance_5d", "f_day1", "已提交", version="第一版", risk="未看AI反馈", draft="我可以提供 AI PPT 美化服务。"), build_instance("企业A组", "enterprise_dept", "e_1", "AI已反馈", version="第一版", risk="待人工判断", draft="部门高频任务：周报、会议纪要、客户回复。", ai_feedback="AI反馈：任务频率清楚，但缺少评分标准。")]

def workspace_df() -> pd.DataFrame:
    init_workspace_state(); rows = []
    for it in st.session_state["task_instances"]: rows.append({"学员": it["student"], "课程": it["course"], "Day/模块": it["day"], "作品/任务": it["title"], "模板ID": it["course_id"] + "/" + it["task_key"], "版本": it["version"], "状态": it["status"], "评分": it["score"] or "-", "风险": it["risk"], "作品集": "是" if it["portfolio"] else "否"})
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

def make_zip(files: dict[str, str | bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            if isinstance(content, str): content = content.encode("utf-8")
            zf.writestr(name, content)
    return buffer.getvalue()

def merge_instances_with_templates(instances: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    if instances.empty: return instances
    if tasks.empty or not {"course_id","task_key"}.issubset(tasks.columns): return instances
    keep=[c for c in ["course_id","task_key","day","title","outcome","prompt","standard","sort_order"] if c in tasks.columns]
    return instances.merge(tasks[keep], on=["course_id","task_key"], how="left", suffixes=("","_tpl"))

def render_top_nav(lang: str):
    st.markdown("""<div class='nav'><div class='nav-inner'><div class='brand'><div class='logo'>AI</div><div>AI Skill Growth Platform<small>技能成长 · 真实学员端 · v3.9</small></div></div><div class='badges'><span class='badge'>真实任务</span><span class='badge'>草稿写回</span><span class='badge'>AI反馈</span><span class='badge cta'>预约体验课</span></div></div></div>""", unsafe_allow_html=True)
    nav_keys=["home","workspace","trial","sop","paths","skills","portfolio","freelance","company","pricing","booking","faq"]
    st.markdown("<div class='nav-panel'>", unsafe_allow_html=True)
    page=st.radio(TEXT[lang]["nav"], nav_keys, horizontal=True, label_visibility="collapsed", format_func=lambda key: TEXT[lang][key], key="top_page_nav")
    st.markdown("</div>", unsafe_allow_html=True); return page

def render_offer_section():
    section("PROGRAMS", "选择你的技能成长入口", "每个产品对应一个清晰目标和交付结果。")
    offers=[("低门槛开始","2 小时体验课","99 / 199 元","现场完成一个微型任务，拿到一版 AI 学习路径。"),("主推","5 天技能成长营","3999 元建议","形成 3 个可展示作品、反馈记录和表达稿。"),("自由职业","5 天技能变现营","4999 元建议","形成服务包、报价单、样品案例和交付 SOP。"),("企业版","企业 AI 技能内训","3 万元起","把部门高频任务改造成可训练、可评分的 AI 工作流。")]
    st.markdown("<div class='grid4'>"+"".join(f"<div class='offer {'featured' if tag=='主推' else ''}'><span class='tag'>{tag}</span><h3>{title}</h3><div class='price'>{price}</div><p>{body}</p></div>" for tag,title,price,body in offers)+"</div>", unsafe_allow_html=True)

def render_home(lang: str):
    st.markdown("""<div class='hero'><span class='eyebrow'>AI Skill Growth Platform</span><h1>AI 技能成长<br><span>教育平台</span></h1><p><b>用 AI 更快学会新技能，并做出可展示、可交付、可变现的成果。</b><br>v3.9：真实学员端。读取真实 task_instances，提交草稿，并写回 Supabase。</p><span class='btn primary'>🚀 预约 2 小时体验课</span><span class='btn secondary'>🧑‍💻 进入学习工作台</span><div><span class='pill'>真实任务读取</span><span class='pill'>草稿写回</span><span class='pill'>AI反馈写回</span><span class='pill'>待点评状态</span></div></div>""", unsafe_allow_html=True)
    flow=[("01","读取实例"),("02","选择学员"),("03","查看任务"),("04","提交草稿"),("05","AI反馈"),("06","待点评")]
    section("METHOD", "从真实数据到真实学习动作", "从 v3.8 的创建实例，推进到 v3.9 的学员任务读写。")
    st.markdown("<div class='flow'>"+"".join(f"<div><b>{n}</b><span>{t}</span></div>" for n,t in flow)+"</div>", unsafe_allow_html=True); render_offer_section()

def render_student_workspace():
    init_workspace_state(); item=st.session_state["task_instances"][1]
    st.markdown(f"<div class='workspace-hero'><span class='label'>模拟学员端</span><h2>张同学 · {item['course']}</h2><p>当前任务：{item['day']} / {item['title']} {chip(item['status'])}</p></div>", unsafe_allow_html=True)
    st.dataframe(workspace_df(), use_container_width=True, hide_index=True)
    draft=st.text_area("粘贴你的第一版作品", value=item["draft"], height=180)
    if st.button("保存到模拟任务实例草稿", type="primary"):
        item["draft"]=draft; set_item_status(item,"已提交"); st.success("已保存到当前会话。真实数据库写入请用“真实学员端”。")

def render_real_student_workspace():
    section("REAL STUDENT", "v3.9 真实学员端", "从 Supabase 读取真实 task_instances，并把草稿、AI反馈和状态写回数据库。")
    if not db_ready():
        st.info("未配置 Supabase Secrets。请先完成 v3.7 的连接配置。")
        return
    ok_i, msg_i, instances = db_task_instances()
    ok_t, msg_t, tasks = db_select("task_templates")
    if not ok_i: st.error(msg_i); return
    if instances.empty:
        st.warning("真实 task_instances 为空。请先在“后端准备 / 真实闭环”里创建报名并生成任务实例。")
        return
    merged = merge_instances_with_templates(instances, tasks if ok_t else pd.DataFrame())
    students = sorted([x for x in merged["student"].dropna().unique().tolist()]) if "student" in merged.columns else []
    student = st.selectbox("选择真实学员", students, key="real_student_select")
    sdf = merged[merged["student"] == student].copy()
    status_rank = {"进行中":0,"已提交":1,"AI已反馈":2,"待老师点评":3,"未开始":4,"已点评":5,"已入作品集":6}
    sdf["_rank"] = sdf["status"].map(status_rank).fillna(9)
    sdf = sdf.sort_values(["_rank", "updated_at" if "updated_at" in sdf.columns else "instance_id"], ascending=[True, False])
    st.dataframe(sdf.drop(columns=["_rank"], errors="ignore"), use_container_width=True, hide_index=True)
    labels=[]
    for _, row in sdf.iterrows():
        labels.append(f"{row['instance_id']}｜{v(row,'status')}｜{v(row,'day','')}｜{v(row,'title', row['task_key'])}")
    selected_label = st.selectbox("选择要处理的任务", labels, key="real_task_select")
    instance_id = selected_label.split("｜",1)[0]
    row = sdf[sdf["instance_id"] == instance_id].iloc[0]
    st.markdown(f"<div class='state-card'><b>{v(row,'day','')}｜{v(row,'title', row['task_key'])}</b><p>实例：{row['instance_id']}<br>课程：{row['course_id']}　任务：{row['task_key']}<br>状态：{chip(v(row,'status'))}　版本：{v(row,'version','未提交')}</p><p><b>交付物：</b>{v(row,'outcome','')}</p><p><b>标准：</b>{v(row,'standard','')}</p></div>", unsafe_allow_html=True)
    if v(row, "prompt", ""):
        st.code(v(row, "prompt"), language="text")
    draft = st.text_area("作品草稿 draft", value=str(v(row,"draft","")), height=220, key=f"real_draft_{instance_id}")
    ai_feedback = str(v(row,"ai_feedback",""))
    teacher_review = str(v(row,"teacher_review",""))
    if ai_feedback: st.info("AI反馈：\n" + ai_feedback)
    if teacher_review: st.success("老师点评：\n" + teacher_review)
    c1,c2,c3,c4=st.columns(4)
    if c1.button("保存草稿并标记已提交", type="primary", key=f"real_save_{instance_id}"):
        ok,msg=db_update_task_instance(instance_id,{"draft":draft,"status":"已提交","version":"第一版","risk":"等待AI反馈"})
        st.success(msg) if ok else st.error(msg)
        if ok: st.rerun()
    if c2.button("生成模拟AI反馈", key=f"real_ai_{instance_id}"):
        feedback=f"AI反馈：已检查任务 {v(row,'task_key')}。请对照标准补充遗漏，把输出改成可执行格式，并保留修改前后版本。"
        ok,msg=db_update_task_instance(instance_id,{"ai_feedback":feedback,"status":"AI已反馈","risk":"需按AI反馈修改"})
        st.success(msg) if ok else st.error(msg)
        if ok: st.rerun()
    if c3.button("提交老师点评", key=f"real_teacher_{instance_id}"):
        ok,msg=db_update_task_instance(instance_id,{"status":"待老师点评","risk":"待人工判断"})
        st.success(msg) if ok else st.error(msg)
        if ok: st.rerun()
    if c4.button("标记进行中", key=f"real_progress_{instance_id}"):
        ok,msg=db_update_task_instance(instance_id,{"status":"进行中","risk":"正常"})
        st.success(msg) if ok else st.error(msg)
        if ok: st.rerun()

def render_teacher_review_workspace():
    init_workspace_state(); section("TEACHER REVIEW", "老师点评端", "v3.9 仍是模拟点评端；真实老师点评写入放到 v4.0。")
    st.dataframe(workspace_df(), use_container_width=True, hide_index=True)

def render_ops_workspace():
    init_workspace_state(); section("OPERATIONS", "班主任 / 运营看板", "运营看任务实例状态。")
    df=workspace_df(); m1,m2,m3,m4=st.columns(4)
    m1.metric("任务实例",len(df)); m2.metric("进行中/未开始",int((df["状态"].isin(["进行中","未开始"])).sum())); m3.metric("待老师点评",int((df["状态"]=="待老师点评").sum())); m4.metric("风险项",int((df["风险"].isin(["风险","遗漏场景较多","未看AI反馈"])).sum()))
    st.dataframe(df,use_container_width=True,hide_index=True)

def template_df(course_id: str | None = None) -> pd.DataFrame:
    rows=[]
    for cid,course in COURSE_TEMPLATES.items():
        if course_id and cid!=course_id: continue
        for task in course["tasks"]: rows.append({"课程模板ID":cid,"课程名称":course["name"],"Day/模块":task["day"],"任务Key":task["task_key"],"任务标题":task["title"],"交付物":task["outcome"],"做到什么标准":task["standard"]})
    return pd.DataFrame(rows)

def render_template_engine():
    section("TEMPLATE ENGINE", "课程模板引擎", "本地模板用于模拟；真实模板来自 Supabase task_templates。")
    selected=st.selectbox("选择本地课程模板",list(COURSE_TEMPLATES.keys()),format_func=lambda cid:COURSE_TEMPLATES[cid]["name"])
    st.dataframe(template_df(selected),use_container_width=True,hide_index=True)

def render_real_data_loop():
    section("REAL LOOP", "v3.9 最小真实数据闭环", "读取真实课程和任务模板，创建报名，并批量生成任务实例。")
    status=supabase_config_status(); c1,c2,c3=st.columns(3)
    c1.metric("SUPABASE_URL", "已配置" if status["SUPABASE_URL"] else "未配置")
    c2.metric("SUPABASE_ANON_KEY", "已配置" if status["SUPABASE_ANON_KEY"] else "未配置")
    c3.metric("当前模式", "真实数据库" if db_ready() else "模拟模式")
    if not db_ready(): st.info("还没有配置 Supabase Secrets。当前只能看模拟数据。"); return
    ok_c, msg_c, courses = db_select("courses"); ok_t, msg_t, all_tasks = db_select("task_templates")
    st.success(msg_c) if ok_c else st.error(msg_c); st.success(msg_t) if ok_t else st.error(msg_t)
    left,right=st.columns([1,1])
    with left:
        st.markdown("### 1. 真实课程表 courses")
        st.dataframe(courses, use_container_width=True, hide_index=True) if not courses.empty else st.warning("courses 表为空。")
    with right:
        st.markdown("### 2. 真实任务模板 task_templates")
        if all_tasks.empty: st.warning("task_templates 表为空。请运行 seed SQL。")
        else: st.dataframe(all_tasks[[col for col in ["course_id","task_key","day","title","sort_order"] if col in all_tasks.columns]], use_container_width=True, hide_index=True)
    st.markdown("### 3. 创建真实报名 enrollment，并批量生成 task_instances")
    if courses.empty: return
    with st.form("real_enrollment_form_v39"):
        student_name = st.text_input("学员 / 小组名称", value="真实学员A")
        course_id = st.selectbox("选择课程", courses["course_id"].tolist())
        owner_email = st.text_input("学员邮箱，可空")
        coach_email = st.text_input("老师邮箱，可空")
        submitted = st.form_submit_button("写入 Supabase：创建报名并生成任务实例")
    if submitted:
        ok, msg, eid = create_real_enrollment(student_name, course_id, owner_email, coach_email)
        if ok: st.success(msg); st.session_state["last_enrollment_id"] = eid
        else: st.error(msg)
    st.markdown("### 4. 读取真实 task_instances")
    eid_filter = st.text_input("按 enrollment_id 过滤，可空", value=st.session_state.get("last_enrollment_id", ""))
    ok_i, msg_i, instances = db_task_instances(eid_filter.strip() or None)
    st.success(msg_i) if ok_i else st.error(msg_i)
    if not instances.empty: st.dataframe(instances, use_container_width=True, hide_index=True)

def render_backend_prep():
    subhero("V3.9 REAL STUDENT","真实数据库闭环：课程 → 报名 → 任务实例 → 学员提交","这一步确认真实任务实例可以被学员读取和更新。")
    tabs=st.tabs(["真实闭环", "Schema / SQL", "CSV 备份", "迁移顺序"])
    with tabs[0]: render_real_data_loop()
    with tabs[1]:
        section("SCHEMA", "数据库 SQL", "如果 task_templates 为空，运行任务模板 seed SQL。")
        st.code(CREATE_TABLE_SQL, language="sql"); st.download_button("下载 01_create_tables.sql", CREATE_TABLE_SQL, "01_create_tables.sql", "text/sql")
        st.code(TASK_TEMPLATE_SEED_SQL, language="sql"); st.download_button("下载 04_seed_task_templates.sql", TASK_TEMPLATE_SEED_SQL, "04_seed_task_templates.sql", "text/sql")
        st.code(RLS_SQL, language="sql")
    with tabs[2]:
        tables=normalized_tables(); name=st.selectbox("选择导出表", list(tables.keys()))
        st.dataframe(tables[name], use_container_width=True, hide_index=True)
        st.download_button("下载本地模拟 CSV ZIP", make_zip({f"{k}.csv": v.to_csv(index=False).encode("utf-8-sig") for k,v in tables.items()}), "ai_skill_growth_v39_local_tables.zip", "application/zip")
    with tabs[3]:
        st.code("""v3.9 当前目标：
1. 真实 task_instances 可读。
2. 可按学员筛选真实任务。
3. 学员可保存草稿到 task_instances.draft。
4. 可写入 AI 反馈和状态。
5. 可把任务状态改为待老师点评。

下一步 v4.0：
1. 真实老师点评端：写 reviews，并回写 task_instances.teacher_review/score/status。
2. 真实运营看板：聚合 Supabase 的 task_instances。
3. 再开始设计登录角色与 RLS。""", language="text")

def render_learning_workspace(lang: str):
    init_workspace_state(); subhero("V3.9 REAL STUDENT WORKSPACE","学习工作台：真实学员任务读写版","在 v3.8 创建真实任务实例基础上，加入真实学员端：读取、提交草稿、写AI反馈、提交老师点评。")
    tabs=st.tabs(["真实学员端", "模拟学员端", "老师点评端", "班主任 / 运营看板", "课程模板引擎", "后端准备 / 真实闭环"])
    with tabs[0]: render_real_student_workspace()
    with tabs[1]: render_student_workspace()
    with tabs[2]: render_teacher_review_workspace()
    with tabs[3]: render_ops_workspace()
    with tabs[4]: render_template_engine()
    with tabs[5]: render_backend_prep()

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
    configured=bool(get_secret("LEAD_WEBHOOK_URL")); st.markdown(f"<div class='card {'green' if configured else 'orange'}'><b>Webhook 状态</b><p>{'已配置：提交后会自动发送线索。' if configured else '未配置：线索不会自动保存，请下载 TXT/CSV。'}</p></div>",unsafe_allow_html=True)
    with st.form("booking_form"):
        name=st.text_input("姓名 / 称呼"); contact=st.text_input("联系方式（微信 / 邮箱 / 手机，任选）")
        identity=st.selectbox("你现在属于哪类人？",["职场新人","在岗提升","升职准备","转岗 / 跳槽","自由职业 / 副业接单","企业培训负责人","小微老板"])
        goal=st.selectbox("你最想解决什么？",["学新技能","提升现有技能","做作品集","升职表达","换工作 / 高薪跳槽","自由职业接单","企业内训"])
        skill=st.text_input("想学习或提升的具体技能",placeholder="例如：PPT汇报、销售话术、测试用例、Java项目、自由职业服务包")
        time_budget=st.selectbox("你愿意投入的时间",["2 小时体验","1 天入门","5 天训练营","4 周小班","企业内训待沟通"])
        note=st.text_area("补充说明"); submitted=st.form_submit_button("生成并提交咨询摘要")
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
        st.success("咨询摘要已生成。"); st.info(msg); st.markdown(f"<div class='summary'>{summary}</div>",unsafe_allow_html=True)
        df=pd.DataFrame([lead]); st.download_button("下载 TXT 摘要",data=summary,file_name="ai_skill_growth_lead.txt",mime="text/plain"); st.download_button("下载 CSV 线索",data=df.to_csv(index=False).encode("utf-8-sig"),file_name="ai_skill_growth_lead.csv",mime="text/csv")

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
    st.caption("AI Skill Growth Platform · real student task workspace prototype v3.9")

if __name__ == "__main__":
    main()
