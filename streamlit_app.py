from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI 技能成长教育平台", page_icon="🚀", layout="wide")

CSS = """
<style>
.main .block-container{max-width:1180px;padding-top:.7rem;padding-bottom:4rem}
[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none}
.nav{position:sticky;top:.45rem;z-index:999;margin-bottom:1rem}.nav-inner{display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:.75rem 1rem;border:1px solid #c7d2fe;border-radius:1.25rem;background:rgba(255,255,255,.96);box-shadow:0 14px 34px rgba(15,23,42,.08)}
.brand{display:flex;gap:.62rem;align-items:center;font-weight:950;color:#111827}.logo{width:36px;height:36px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,#4f46e5,#06b6d4);color:white}.brand small{display:block;color:#64748b;font-weight:800}.badges{display:flex;gap:.45rem;flex-wrap:wrap}
.badge,.pill,.status-chip{display:inline-block;border-radius:999px;padding:.28rem .62rem;font-weight:900;font-size:.82rem;background:#f8fafc;border:1px solid #e2e8f0;color:#475569}.badge.cta{background:linear-gradient(90deg,#4f46e5,#7c3aed);color:white;border:none}
.nav-panel{margin:.65rem 0 1.15rem;padding:.55rem;border:1px solid #e0e7ff;border-radius:1.2rem;background:#f8fafc}div[data-testid="stRadio"]>label{display:none}div[role="radiogroup"]{display:flex;flex-wrap:wrap;gap:.42rem}div[role="radiogroup"] label{border:1px solid #dbeafe!important;border-radius:999px!important;background:white!important;padding:.38rem .74rem!important}div[role="radiogroup"] label p{font-weight:900!important;color:#334155!important;font-size:.9rem!important}div[role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,#4f46e5,#06b6d4)!important}div[role="radiogroup"] label:has(input:checked) p{color:white!important}
.hero,.subhero{border:1px solid #c7d2fe;border-radius:1.45rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 46%,#fff);box-shadow:0 18px 44px rgba(15,23,42,.08);padding:1.45rem;margin:1.15rem 0}.hero{padding:2rem}.hero h1{font-size:2.65rem;line-height:1.05;margin:.55rem 0;color:#0f172a;font-weight:980}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p,.subhero p{color:#475569;line-height:1.75}
.eyebrow,.label{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}.kicker{font-size:.78rem;font-weight:950;letter-spacing:.14em;color:#4f46e5;text-transform:uppercase;margin-top:1.4rem}.title{font-size:1.65rem;font-weight:950;color:#0f172a}.sub{color:#64748b;line-height:1.75;max-width:860px}
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:.95rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card,.offer,.state-card{border:1px solid #e2e8f0;border-radius:1.08rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045);min-height:105px}.card p,.offer p,.state-card p{color:#64748b;line-height:1.58}.green{background:#f0fdf4;border-color:#bbf7d0}.orange,.warn{background:#fff7ed;border-color:#fed7aa}.soft{background:#f8fafc;border-color:#dbeafe}
.flow{display:grid;grid-template-columns:repeat(6,1fr);gap:.55rem}.flow div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.flow b{display:block;color:#4f46e5}.flow span{font-weight:850;color:#312e81;font-size:.82rem}.chip-green{background:#dcfce7;color:#166534}.chip-blue{background:#dbeafe;color:#1e40af}.chip-orange{background:#ffedd5;color:#9a3412}.chip-gray{background:#f1f5f9;color:#475569}.chip-red{background:#fee2e2;color:#991b1b}.summary{border-radius:1rem;background:#0f172a;color:#e2e8f0;padding:1rem;line-height:1.7;white-space:pre-wrap}
@media(max-width:960px){.nav{position:relative}.nav-inner{align-items:flex-start;flex-direction:column}.badges{display:none}.grid2,.grid3,.grid4{grid-template-columns:1fr}.flow{grid-template-columns:repeat(2,1fr)}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

NAV = {"home":"首页","workspace":"学习工作台","founder":"Founder Console","trial":"2小时体验课","sop":"跟进SOP","paths":"成长路径","skills":"技能训练","portfolio":"作品集","freelance":"自由职业","company":"企业内训","pricing":"报价","booking":"预约咨询","faq":"FAQ"}
STATUS_CHIP = {"未开始":"chip-gray","进行中":"chip-blue","已提交":"chip-orange","AI已反馈":"chip-blue","待Agent点评":"chip-orange","待老师点评":"chip-orange","Agent已点评":"chip-green","Agent质检通过":"chip-green","已点评":"chip-green","已入作品集":"chip-green","需重训":"chip-red","风险":"chip-red","等待":"chip-gray"}
AGENT_REVIEW_QUEUE = ["待Agent点评", "待老师点评", "AI已反馈", "已提交"]

CREATE_TABLE_SQL = """create table if not exists public.courses (course_id text primary key, name text not null, audience text, promise text, is_active boolean default true, created_at timestamptz default now());
create table if not exists public.task_templates (task_key text primary key, course_id text not null references public.courses(course_id) on delete cascade, day text, title text not null, outcome text, prompt text, standard text, sort_order int default 0, created_at timestamptz default now());
create table if not exists public.enrollments (enrollment_id text primary key, student_name text not null, course_id text not null references public.courses(course_id), status text default '学习中', owner_email text, coach_email text, created_at timestamptz default now());
create table if not exists public.task_instances (instance_id text primary key, enrollment_id text not null references public.enrollments(enrollment_id) on delete cascade, student text not null, course_id text not null references public.courses(course_id), task_key text not null references public.task_templates(task_key), status text default '未开始', version text default '未提交', draft text default '', ai_feedback text default '', teacher_review text default '', score int default 0, portfolio boolean default false, risk text default '正常', updated_at timestamptz default now());
create table if not exists public.reviews (review_id text primary key, instance_id text not null references public.task_instances(instance_id) on delete cascade, reviewer text not null, score int default 0, conclusion text, review_text text, created_at timestamptz default now());"""
COURSE_SEED_SQL = """insert into public.courses(course_id, name, audience, promise, is_active) values
('growth_5d','5 天 AI 技能成长营','职场新人 / 在岗提升 / 升职准备 / 转岗跳槽','3 个可展示作品 + AI 反馈记录 + Agent 点评 + 30 天行动计划',true),
('freelance_5d','5 天自由职业技能变现营','自由职业 / 副业接单者','1 个服务包 + 3 个样品案例 + 报价单 + 获客话术 + 交付 SOP',true),
('enterprise_dept','企业部门 AI 训练营','企业内训部门 / 新人培养 / 部门负责人','部门任务模板 + 评分标准 + 员工练习包 + 培训复盘',true)
on conflict (course_id) do update set name=excluded.name, audience=excluded.audience, promise=excluded.promise, is_active=excluded.is_active;"""
TASK_TEMPLATE_SEED_SQL = """insert into public.task_templates(task_key, course_id, day, title, outcome, prompt, standard, sort_order) values
('g_day1','growth_5d','Day 1','定目标 + 拆任务','技能成长路线图','请把我的目标拆成 5 天训练任务，并说明每天交付物。','目标明确；任务可执行；交付物可检查。',1),
('g_day2','growth_5d','Day 2','作品 1：基础任务作品','测试用例 + Bug 报告模板','请根据登录页面需求设计测试用例，并输出遗漏点和 Bug 报告模板。','覆盖正常、异常、边界、安全、权限；步骤可执行。',2),
('g_day3','growth_5d','Day 3','作品 2：复杂任务作品','复杂需求拆解 + 异常场景补全','请把复杂业务需求拆成流程、角色、输入输出、异常分支和测试点。','能解释流程；能发现异常；能说明遗漏信息。',3),
('g_day4','growth_5d','Day 4','作品 3：展示 / 发表作品','项目发表说明 + 成果表达稿','请把我的项目成果整理成 3 分钟发表稿，包含背景、任务、方法、结果和改进点。','表达清楚；能展示价值；能回答追问。',4),
('g_day5','growth_5d','Day 5','复盘 + 后续路径','30 天行动计划','请根据我的 3 个作品和老师点评，生成后续 30 天行动计划。','路径清楚；动作具体；能持续复盘。',5),
('f_day1','freelance_5d','Day 1','选择可售卖技能','服务方向定位','请帮我把一个技能转成可售卖服务方向，说明目标客户、痛点和交付物。','客户明确；痛点具体；交付边界清楚。',1),
('f_day2','freelance_5d','Day 2','样品案例 1','第一个可展示样品','请根据目标客户场景，帮我设计一个可展示样品案例。','样品能展示能力；客户能看懂价值。',2),
('e_1','enterprise_dept','模块 1','部门高频任务清单','AI 训练任务地图','请把部门高频任务整理成可训练任务清单，并标出可用 AI 辅助的环节。','任务真实；频率高；能训练。',1)
on conflict (task_key) do update set course_id=excluded.course_id, day=excluded.day, title=excluded.title, outcome=excluded.outcome, prompt=excluded.prompt, standard=excluded.standard, sort_order=excluded.sort_order;"""
RLS_OFF_SQL = """alter table public.courses disable row level security;
alter table public.task_templates disable row level security;
alter table public.enrollments disable row level security;
alter table public.task_instances disable row level security;
alter table public.reviews disable row level security;"""

def get_secret(name: str, default: str = "") -> str:
    try: return str(st.secrets.get(name, default))
    except Exception: return default

def configured(name: str) -> bool:
    value = get_secret(name)
    return bool(value and value.strip() and "YOUR_" not in value and "xxxx" not in value)

def db_ready() -> bool: return configured("SUPABASE_URL") and configured("SUPABASE_ANON_KEY")

def get_supabase_client():
    from supabase import create_client
    return create_client(get_secret("SUPABASE_URL"), get_secret("SUPABASE_ANON_KEY"))

def safe_id(text: str) -> str: return re.sub(r"[^a-zA-Z0-9_]+", "_", text.strip()).strip("_") or "item"
def chip(status: Any) -> str: return f"<span class='status-chip {STATUS_CHIP.get(str(status or ''), 'chip-gray')}'>{str(status or '')}</span>"

def val(row: pd.Series, col: str, default: str = "") -> Any:
    try:
        item = row.get(col, default)
        return default if pd.isna(item) else item
    except Exception: return default

def section(kicker: str, title: str, sub: str = "") -> None:
    st.markdown(f"<div class='kicker'>{kicker}</div><div class='title'>{title}</div><div class='sub'>{sub}</div>", unsafe_allow_html=True)

def subhero(label: str, title: str, body: str) -> None:
    st.markdown(f"<div class='subhero'><span class='label'>{label}</span><h2>{title}</h2><p>{body}</p></div>", unsafe_allow_html=True)

def html_card(icon: str, title: str, body: str, cls: str = "card") -> str:
    return f"<div class='{cls}'><b>{icon} {title}</b><p>{body}</p></div>"

def db_select(table: str, columns: str = "*", limit: int = 500) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready(): return False, "未配置 Supabase Secrets。", pd.DataFrame()
    try:
        res = get_supabase_client().table(table).select(columns).limit(limit).execute()
        rows = res.data or []
        return True, f"读取 {table} 成功：{len(rows)} 条。", pd.DataFrame(rows)
    except Exception as exc: return False, f"读取 {table} 失败：{exc}", pd.DataFrame()

def db_tasks_for_course(course_id: str) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready(): return False, "未配置 Supabase Secrets。", pd.DataFrame()
    try:
        res = get_supabase_client().table("task_templates").select("*").eq("course_id", course_id).order("sort_order").execute()
        rows = res.data or []
        return True, f"读取任务模板成功：{len(rows)} 条。", pd.DataFrame(rows)
    except Exception as exc: return False, f"读取任务模板失败：{exc}", pd.DataFrame()

def db_task_instances(status: str | None = None, enrollment_id: str | None = None) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready(): return False, "未配置 Supabase Secrets。", pd.DataFrame()
    try:
        query = get_supabase_client().table("task_instances").select("*").order("updated_at", desc=True).limit(500)
        if status: query = query.eq("status", status)
        if enrollment_id: query = query.eq("enrollment_id", enrollment_id)
        res = query.execute(); rows = res.data or []
        return True, f"读取 task_instances 成功：{len(rows)} 条。", pd.DataFrame(rows)
    except Exception as exc: return False, f"读取 task_instances 失败：{exc}", pd.DataFrame()

def db_update_task_instance(instance_id: str, updates: dict[str, Any]) -> tuple[bool, str]:
    if not db_ready(): return False, "未配置 Supabase Secrets。"
    try:
        payload = dict(updates); payload["updated_at"] = datetime.now().isoformat()
        get_supabase_client().table("task_instances").update(payload).eq("instance_id", instance_id).execute()
        return True, f"已更新 task_instances：{instance_id}"
    except Exception as exc: return False, f"更新失败：{exc}"

def db_insert_review(instance_id: str, reviewer: str, score: int, conclusion: str, review_text: str) -> tuple[bool, str, str]:
    if not db_ready(): return False, "未配置 Supabase Secrets。", ""
    try:
        review_id = f"rev_{safe_id(instance_id)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        row = {"review_id": review_id, "instance_id": instance_id, "reviewer": reviewer.strip() or "Agent老师", "score": int(score), "conclusion": conclusion, "review_text": review_text.strip()}
        get_supabase_client().table("reviews").insert(row).execute()
        return True, f"已写入 reviews：{review_id}", review_id
    except Exception as exc: return False, f"写入 reviews 失败：{exc}", ""

def db_submit_review(instance_id: str, reviewer: str, score: int, conclusion: str, review_text: str, portfolio: bool, agent: bool = False) -> tuple[bool, str]:
    ok, msg, _ = db_insert_review(instance_id, reviewer, score, conclusion, review_text)
    if not ok: return False, msg
    new_status = "已入作品集" if portfolio else ("Agent已点评" if agent else "已点评")
    ok2, msg2 = db_update_task_instance(instance_id, {"teacher_review": review_text.strip(), "score": int(score), "status": new_status, "risk": "已完成", "portfolio": bool(portfolio)})
    return (ok2, f"{msg}；{msg2}" if ok2 else f"{msg}；但回写任务失败：{msg2}")

def merge_instances_with_templates(instances: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    if instances.empty or tasks.empty or not {"course_id", "task_key"}.issubset(tasks.columns): return instances
    keep = [c for c in ["course_id","task_key","day","title","outcome","prompt","standard","sort_order"] if c in tasks.columns]
    return instances.merge(tasks[keep], on=["course_id", "task_key"], how="left")

def load_merged_instances() -> tuple[bool, str, pd.DataFrame]:
    ok_i, msg_i, instances = db_task_instances(); ok_t, _, tasks = db_select("task_templates")
    if not ok_i: return False, msg_i, pd.DataFrame()
    return True, msg_i, merge_instances_with_templates(instances, tasks if ok_t else pd.DataFrame())

def create_real_enrollment(student_name: str, course_id: str, owner_email: str = "", coach_email: str = "") -> tuple[bool, str, str]:
    student_name = student_name.strip()
    if not student_name: return False, "请先输入学员名。", ""
    ok, msg, tasks = db_tasks_for_course(course_id)
    if not ok or tasks.empty: return False, msg if not ok else "该课程还没有 task_templates。请先运行 seed SQL。", ""
    try:
        client = get_supabase_client(); stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        enrollment_id = f"enr_{safe_id(student_name)}_{course_id}_{stamp}"
        client.table("enrollments").insert({"enrollment_id": enrollment_id, "student_name": student_name, "course_id": course_id, "status": "学习中", "owner_email": owner_email.strip() or None, "coach_email": coach_email.strip() or None}).execute()
        rows = []
        for i, task in tasks.reset_index(drop=True).iterrows():
            status = "进行中" if i == 0 else "未开始"
            rows.append({"instance_id": f"ti_{safe_id(student_name)}_{task['task_key']}_{stamp}", "enrollment_id": enrollment_id, "student": student_name, "course_id": course_id, "task_key": task["task_key"], "status": status, "version": "未提交", "draft": "", "ai_feedback": "", "teacher_review": "", "score": 0, "portfolio": False, "risk": "正常" if status == "进行中" else "等待"})
        client.table("task_instances").insert(rows).execute()
        return True, f"已创建报名 {enrollment_id}，并生成 {len(rows)} 条任务实例。", enrollment_id
    except Exception as exc: return False, f"写入失败：{exc}", ""

def agent_review(row: pd.Series) -> dict[str, Any]:
    draft = str(val(row, "draft", "")).strip(); standard = str(val(row, "standard", "")).strip(); title = str(val(row, "title", val(row, "task_key", "任务")))
    points = [p.strip() for p in re.split(r"[；;、，,。\n]", standard) if p.strip()]
    score = min(100, (10 if draft else 0) + min(35, len(draft)//12) + min(25, sum(4 for m in ["1","一","步骤","目标","问题","改进","结论","方案","测试","风险"] if m in draft)) + min(30, sum(10 for p in points if p[:2] and p[:2] in draft)))
    if not draft: conclusion, advice, portfolio = "退回重做", "当前没有提交有效草稿，请先完成第一版作品。", False
    elif score >= 82: conclusion, advice, portfolio = "通过", "作品结构和完成度较好，可以进入下一任务；建议进一步压缩表达并补充可验证结果。", True
    elif score >= 65: conclusion, advice, portfolio = "需要修改", "作品已有雏形，但还需要补充评分标准中的遗漏点。", False
    else: conclusion, advice, portfolio = "退回重做", "请按目标、步骤、输出物、检查标准、风险/遗漏重写。", False
    text = f"""【AI Agent 老师点评】
任务：{title}
自动评分：{score}/100
结论：{conclusion}

优点：已提交可被检查的第一版内容。
主要问题：与评分标准的逐项对应还不够清晰。
下一步：{advice}

Agent 说明：本点评由规则型 Agent 自动生成，用于一审与高频反馈。"""
    return {"score": score, "conclusion": conclusion, "review_text": text, "portfolio": portfolio}

def render_top_nav() -> str:
    st.markdown("""<div class='nav'><div class='nav-inner'><div class='brand'><div class='logo'>AI</div><div>AI Skill Growth Platform<small>一人公司 · Agent OS · v4.3.2</small></div></div><div class='badges'><span class='badge'>学员提交</span><span class='badge'>Agent一审</span><span class='badge'>Agent质检</span><span class='badge cta'>Founder Console</span></div></div></div>""", unsafe_allow_html=True)
    st.markdown("<div class='nav-panel'>", unsafe_allow_html=True)
    page = st.radio("导航", list(NAV.keys()), horizontal=True, label_visibility="collapsed", format_func=lambda key: NAV[key], key="top_page_nav")
    st.markdown("</div>", unsafe_allow_html=True)
    return page

def render_diagnostics() -> None:
    items = {"SUPABASE_URL":"已配置" if configured("SUPABASE_URL") else "未配置", "SUPABASE_ANON_KEY":"已配置" if configured("SUPABASE_ANON_KEY") else "未配置", "OWNER_PASSCODE":"已配置" if configured("OWNER_PASSCODE") else "未配置", "模式":"真实数据库" if db_ready() else "模拟模式"}
    for col, (name, value) in zip(st.columns(4), items.items()): col.metric(name, value)

def render_founder_console_link() -> None:
    st.markdown("<div class='card warn'><b>🤖 Founder Agent Console</b><p>老板专用后台：批量运行 Agent 点评、Agent 质检、生成 Founder Daily。进入后会再次要求 OWNER_PASSCODE。</p></div>", unsafe_allow_html=True)
    page_link = getattr(st, "page_link", None)
    if page_link: st.page_link("pages/99_Founder_Agent_Console.py", label="打开 Founder Agent Console", icon="🤖")
    else: st.info("当前 Streamlit 版本不支持 st.page_link。请升级 Streamlit，或直接打开 Founder_Agent_Console 页面。")

def render_home() -> None:
    st.markdown("""<div class='hero'><span class='eyebrow'>AI Skill Growth Platform</span><h1>AI 技能成长<br><span>一人公司 Agent OS</span></h1><p><b>从“真人老师点评型 LMS”跃迁到“Agent 驱动型技能训练平台”。</b><br>v4.3.2：Founder Console 接入主导航与首页入口；Agent 承担点评、质检、作品集建议和运营日报。</p><span class='pill'>课程模板</span><span class='pill'>报名</span><span class='pill'>任务实例</span><span class='pill'>Agent 老师</span><span class='pill'>Founder Console</span></div>""", unsafe_allow_html=True)
    flow = [("01","课程"),("02","报名"),("03","任务"),("04","提交"),("05","Agent点评"),("06","Founder质检")]
    section("METHOD", "不是请老师，而是把日常交付交给 Agent", "你本人保留方向、产品判断、销售、客服、异常处理和系统迭代。")
    st.markdown("<div class='flow'>" + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n,t in flow) + "</div>", unsafe_allow_html=True)
    st.markdown("<div class='grid3'>" + "".join(html_card("🤖", a, b, "card green") for a,b in [("Agent 老师","自动读取任务、草稿和评分标准，生成结构化点评。"),("Agent 质检","复核点评质量，标记通过、重训或老板关注。"),("Founder Console","每天只看异常、日报和关键运营指标。")]) + "</div>", unsafe_allow_html=True)
    render_founder_console_link()

def render_create_enrollment() -> None:
    section("REAL LOOP", "创建报名与任务实例", "从 courses 和 task_templates 创建真实 enrollments / task_instances。")
    render_diagnostics()
    if not db_ready(): st.info("请先配置 Streamlit Secrets。"); return
    ok_c, msg_c, courses = db_select("courses"); ok_t, msg_t, tasks = db_select("task_templates")
    st.success(msg_c) if ok_c else st.error(msg_c); st.success(msg_t) if ok_t else st.error(msg_t)
    l, r = st.columns(2)
    with l: st.markdown("### courses"); st.dataframe(courses, use_container_width=True, hide_index=True)
    with r: st.markdown("### task_templates"); st.dataframe(tasks[[c for c in ["course_id","task_key","day","title","sort_order"] if c in tasks.columns]] if not tasks.empty else tasks, use_container_width=True, hide_index=True)
    if courses.empty: return
    with st.form("create_enrollment_v432"):
        student_name = st.text_input("学员 / 小组名称", value="真实学员A"); course_id = st.selectbox("选择课程", courses["course_id"].tolist()); owner_email = st.text_input("学员邮箱，可空"); coach_email = st.text_input("Agent / 老师邮箱，可空")
        submitted = st.form_submit_button("创建报名并生成任务实例")
    if submitted:
        ok, msg, eid = create_real_enrollment(student_name, course_id, owner_email, coach_email)
        st.success(msg) if ok else st.error(msg)
        if ok: st.session_state["last_enrollment_id"] = eid
    ok_i, msg_i, instances = db_task_instances(enrollment_id=st.text_input("按 enrollment_id 过滤，可空", value=st.session_state.get("last_enrollment_id", "")).strip() or None)
    st.success(msg_i) if ok_i else st.error(msg_i)
    if not instances.empty: st.dataframe(instances, use_container_width=True, hide_index=True)

def render_student() -> None:
    section("REAL STUDENT", "真实学员端", "学员提交草稿后进入 Agent 点评队列。")
    if not db_ready(): st.info("未配置 Supabase Secrets。"); return
    ok, msg, merged = load_merged_instances()
    if not ok: st.error(msg); return
    if merged.empty: st.warning("task_instances 为空。先创建一个学员。"); return
    student = st.selectbox("选择真实学员", sorted(merged["student"].dropna().unique().tolist()), key="student_select_v432")
    sdf = merged[merged["student"] == student].copy(); st.dataframe(sdf, use_container_width=True, hide_index=True)
    labels = [f"{row['instance_id']}｜{val(row,'status')}｜{val(row,'title',row['task_key'])}" for _, row in sdf.iterrows()]
    instance_id = st.selectbox("选择要处理的任务", labels, key="task_select_student_v432").split("｜",1)[0]
    row = sdf[sdf["instance_id"] == instance_id].iloc[0]
    st.markdown(f"<div class='state-card'><b>{val(row,'title',row['task_key'])}</b><p>状态：{chip(val(row,'status'))}<br>标准：{val(row,'standard','')}</p></div>", unsafe_allow_html=True)
    draft = st.text_area("作品草稿 draft", value=str(val(row,"draft","")), height=220, key=f"draft_{instance_id}")
    c1,c2,c3,c4 = st.columns(4)
    if c1.button("保存草稿并标记已提交", type="primary", key=f"save_{instance_id}"):
        ok,msg=db_update_task_instance(instance_id,{"draft":draft,"status":"已提交","version":"第一版","risk":"等待AI反馈"}); st.success(msg) if ok else st.error(msg); st.rerun() if ok else None
    if c2.button("生成模拟AI反馈", key=f"ai_{instance_id}"):
        feedback=f"AI反馈：已检查任务 {row['task_key']}。请对照评分标准补充遗漏，把输出改成可执行格式，并保留修改前后版本。"; ok,msg=db_update_task_instance(instance_id,{"ai_feedback":feedback,"status":"AI已反馈","risk":"需按AI反馈修改"}); st.success(msg) if ok else st.error(msg); st.rerun() if ok else None
    if c3.button("提交给Agent老师", key=f"agent_queue_{instance_id}"):
        ok,msg=db_update_task_instance(instance_id,{"status":"待Agent点评","risk":"等待Agent点评"}); st.success(msg) if ok else st.error(msg); st.rerun() if ok else None
    if c4.button("标记进行中", key=f"progress_{instance_id}"):
        ok,msg=db_update_task_instance(instance_id,{"status":"进行中","risk":"正常"}); st.success(msg) if ok else st.error(msg); st.rerun() if ok else None
    if val(row,"ai_feedback",""): st.info("AI反馈：\n" + str(val(row,"ai_feedback")))
    if val(row,"teacher_review",""): st.success("Agent点评：\n" + str(val(row,"teacher_review")))

def render_agent_teacher() -> None:
    section("AGENT TEACHER", "Agent 老师端", "自动评分、生成结构化点评、写入 reviews 并回写 task_instances。")
    if not db_ready(): st.info("未配置 Supabase Secrets。"); return
    ok, msg, merged = load_merged_instances()
    if not ok: st.error(msg); return
    status_filter = st.selectbox("筛选状态", AGENT_REVIEW_QUEUE + ["进行中","Agent已点评","已入作品集","全部"], index=0)
    if status_filter != "全部": merged = merged[merged["status"] == status_filter]
    st.success(f"{msg} 当前视图：{len(merged)} 条。")
    if merged.empty: st.warning("当前没有符合条件的任务。"); return
    st.dataframe(merged[[c for c in ["student","course_id","task_key","title","status","score","risk","updated_at"] if c in merged.columns]], use_container_width=True, hide_index=True)
    instance_id = st.selectbox("选择 Agent 要点评的任务", [f"{row['instance_id']}｜{val(row,'student')}｜{val(row,'status')}｜{val(row,'title',row['task_key'])}" for _, row in merged.iterrows()], key="agent_select_v432").split("｜",1)[0]
    row = merged[merged["instance_id"] == instance_id].iloc[0]
    st.text_area("draft", value=str(val(row,"draft","")), height=180, disabled=True, key=f"agent_draft_{instance_id}")
    review = agent_review(row); c1,c2,c3 = st.columns(3); c1.metric("Agent评分", review["score"]); c2.metric("结论", review["conclusion"]); c3.metric("作品集建议", "收入" if review["portfolio"] else "暂不收入")
    editable = st.text_area("Agent 点评内容，可人工微调后写入", value=review["review_text"], height=240, key=f"agent_review_text_{instance_id}")
    if st.button("Agent 一键写入 reviews + 回写任务", type="primary", key=f"agent_submit_{instance_id}"):
        ok,msg=db_submit_review(instance_id,"AI Agent 老师",int(review["score"]),str(review["conclusion"]),editable,bool(review["portfolio"]),agent=True); st.success(msg) if ok else st.error(msg); st.rerun() if ok else None

def render_ops() -> None:
    section("REAL OPS", "真实运营看板", "聚合 task_instances，查看 Agent 结果。")
    if not db_ready(): st.info("未配置 Supabase Secrets。"); return
    ok,msg,df=db_task_instances(); st.success(msg) if ok else st.error(msg)
    if not ok or df.empty: return
    pending=int(df["status"].isin(AGENT_REVIEW_QUEUE).sum()) if "status" in df.columns else 0
    c1,c2,c3,c4=st.columns(4); c1.metric("任务实例",len(df)); c2.metric("待Agent点评",pending); c3.metric("Agent已点评",int((df["status"]=="Agent已点评").sum()) if "status" in df.columns else 0); c4.metric("作品集",int(df["portfolio"].fillna(False).astype(bool).sum()) if "portfolio" in df.columns else 0)
    if "status" in df.columns: st.bar_chart(df["status"].value_counts())
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_sql_tools() -> None:
    section("SQL", "建表 / Seed / RLS 开关", "当前原型阶段建议先关闭 RLS。")
    tabs=st.tabs(["建表 SQL","courses seed","task_templates seed","关闭 RLS"])
    with tabs[0]: st.code(CREATE_TABLE_SQL, language="sql")
    with tabs[1]: st.code(COURSE_SEED_SQL, language="sql")
    with tabs[2]: st.code(TASK_TEMPLATE_SEED_SQL, language="sql")
    with tabs[3]: st.code(RLS_OFF_SQL, language="sql")

def render_workspace() -> None:
    subhero("V4.3.2 AGENT TEACHER LOOP", "学习工作台：Agent 老师闭环版", "Agent 取代真人老师高频点评，自动写 reviews 并回写 task_instances。")
    tabs=st.tabs(["真实学员端","Agent老师端","真实运营看板","创建报名与任务实例","SQL / Seed / RLS"])
    with tabs[0]: render_student()
    with tabs[1]: render_agent_teacher()
    with tabs[2]: render_ops()
    with tabs[3]: render_create_enrollment()
    with tabs[4]: render_sql_tools()

def render_founder() -> None:
    subhero("V4.3.2 FOUNDER AGENT CONSOLE", "Founder Console 入口", "主导航入口已经接入。真正的批处理后台保留 OWNER_PASSCODE 二次门禁。")
    render_diagnostics()
    st.markdown("<div class='grid3'>" + "".join([html_card("🔐","OWNER_PASSCODE","Founder Console 仍然使用 OWNER_PASSCODE 门禁，避免普通学员误入。","card warn"), html_card("🤖","一键点评","批量处理待 Agent 点评、AI 已反馈、已提交任务。","card green"), html_card("✅","一键质检","复核 Agent 点评结果，生成 Founder Daily。","card soft")]) + "</div>", unsafe_allow_html=True)
    render_founder_console_link()

def simple_page(label: str, title: str, body: str, rows: list[tuple[str,str]], icon: str = "✅") -> None:
    subhero(label, title, body)
    st.markdown("<div class='grid3'>" + "".join(html_card(icon,a,b) for a,b in rows) + "</div>", unsafe_allow_html=True)

def format_webhook_payload(lead: dict[str, Any], provider: str) -> dict[str, Any]:
    text=lead.get("summary",""); provider=(provider or "generic").lower().strip()
    if provider in {"feishu","lark"}: return {"msg_type":"text","content":{"text":text}}
    if provider in {"wecom","wechat_work","qywx","enterprise_wechat"}: return {"msgtype":"text","text":{"content":text}}
    return lead

def post_lead_to_webhook(lead: dict[str, Any]) -> tuple[bool, str]:
    url=get_secret("LEAD_WEBHOOK_URL"); provider=get_secret("WEBHOOK_PROVIDER","generic")
    if not url: return False, "未配置 LEAD_WEBHOOK_URL，线索仅在本页生成，可下载后手动跟进。"
    try:
        data=json.dumps(format_webhook_payload(lead,provider),ensure_ascii=False).encode("utf-8"); req=urllib.request.Request(url,data=data,headers={"Content-Type":"application/json; charset=utf-8"},method="POST")
        with urllib.request.urlopen(req, timeout=8) as resp: return 200 <= resp.status < 300, f"已按 {provider} 格式发送，Webhook 返回状态：{resp.status}"
    except Exception as exc: return False, f"Webhook 发送失败：{exc}"

def render_booking() -> None:
    subhero("BOOKING", "预约体验课 / 咨询方案", "填写后可生成咨询摘要，也可自动发送到你配置的 Webhook。")
    with st.form("booking_form_v432"):
        name=st.text_input("姓名 / 称呼"); contact=st.text_input("联系方式"); identity=st.selectbox("你现在属于哪类人？", ["职场新人","在岗提升","升职准备","转岗 / 跳槽","自由职业 / 副业接单","企业培训负责人","小微老板"]); goal=st.selectbox("你最想解决什么？", ["学新技能","提升现有技能","做作品集","升职表达","换工作 / 高薪跳槽","自由职业接单","企业内训"]); skill=st.text_input("想学习或提升的具体技能"); note=st.text_area("补充说明"); submitted=st.form_submit_button("生成并提交咨询摘要")
    if submitted:
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"); summary=f"""【AI 技能成长咨询摘要】
提交时间：{timestamp}
姓名/称呼：{name or '未填写'}
联系方式：{contact or '未填写'}
当前身份：{identity}
主要目标：{goal}
目标技能：{skill or '未填写'}
补充说明：{note or '无'}"""; lead={"timestamp":timestamp,"name":name,"contact":contact,"identity":identity,"goal":goal,"skill":skill,"note":note,"summary":summary,"source":"streamlit_site"}
        ok,msg=post_lead_to_webhook(lead); st.success("咨询摘要已生成。"); st.info(msg); st.markdown(f"<div class='summary'>{summary}</div>", unsafe_allow_html=True); df=pd.DataFrame([lead]); st.download_button("下载 TXT 摘要", data=summary, file_name="ai_skill_growth_lead.txt", mime="text/plain"); st.download_button("下载 CSV 线索", data=df.to_csv(index=False).encode("utf-8-sig"), file_name="ai_skill_growth_lead.csv", mime="text/csv")

def main() -> None:
    page=render_top_nav()
    if page=="home": render_home()
    elif page=="workspace": render_workspace()
    elif page=="founder": render_founder()
    elif page=="trial": simple_page("2-HOUR TRIAL","AI 技能成长 2 小时体验课","低门槛入口产品。",[("推荐价格","99 / 199 元"),("适合谁","职场新人、转岗、自由职业、企业负责人"),("核心承诺","2 小时内完成一个微型任务")])
    elif page=="sop": simple_page("SALES SOP","线索跟进 SOP","销售按固定动作推进。",[("新线索","5 分钟内响应"),("已约时间","确定体验课时间"),("未转化","记录原因，7 天后触达")],"📌")
    elif page=="paths": simple_page("GROWTH PATHS","成长路径","平台先帮用户选路径，再拆成任务。",[("新人上手","岗位基础技能"),("在岗提升","把重复任务做成 AI 工作流"),("自由职业增收","服务包、报价和交付作品")],"🧭")
    elif page=="skills": simple_page("SKILL TRAINING","技能训练","AI Agent 负责高频反馈。",[("学新技能","AI 生成学习路径"),("Agent一审","自动评分、指出遗漏"),("做作品","变成能展示的作品")],"🧠")
    elif page=="portfolio": render_ops()
    elif page=="freelance": simple_page("FREELANCE","自由职业者：学新技能，赚更多钱","不保证收入，只训练服务化能力。",[("选技能","选择可变现方向"),("做样品","完成可展示样品"),("包装服务","报价和交付 SOP")],"💼")
    elif page=="company": simple_page("COMPANY TRAINING","企业内训","不是 AI 讲座，而是训练体系。",[("新人上手","任务练习和点评标准化"),("部门模板","沉淀高频工作模板"),("合规边界","企业数据脱敏")],"🏢")
    elif page=="pricing": simple_page("PRICING","报价与产品入口","按训练结果和 Agent 训练规模定价。",[("2 小时体验课","99 / 199 元"),("5 天技能成长营","3999 元建议"),("企业 Agent 内训","3 万元起")],"💰")
    elif page=="booking": render_booking()
    else: simple_page("FAQ","常见问题","把风险边界说清楚。",[("没有真人老师了吗？","高频一审由 Agent 完成，真人只做抽检。"),("Agent 点评可靠吗？","当前是规则型 Agent，用于跑通闭环。"),("承诺就业涨薪吗？","不承诺，交付技能路径、作品集和表达能力。")],"❓")
    st.caption("AI Skill Growth Platform · One-person Agent OS prototype v4.3.2")

if __name__ == "__main__": main()
