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
.nav{position:sticky;top:.45rem;z-index:999;margin-bottom:1rem}.nav-inner{display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:.75rem 1rem;border:1px solid #c7d2fe;border-radius:1.25rem;background:rgba(255,255,255,.95);box-shadow:0 14px 34px rgba(15,23,42,.08)}
.brand{display:flex;gap:.62rem;align-items:center;font-weight:950;color:#111827}.logo{width:36px;height:36px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,#4f46e5,#06b6d4);color:white}.brand small{display:block;color:#64748b;font-weight:800}.badges{display:flex;gap:.45rem;flex-wrap:wrap}
.badge,.pill,.status-chip{display:inline-block;border-radius:999px;padding:.28rem .62rem;font-weight:900;font-size:.82rem;background:#f8fafc;border:1px solid #e2e8f0;color:#475569}.badge.cta{background:linear-gradient(90deg,#4f46e5,#7c3aed);color:white;border:none}
.nav-panel{margin:.65rem 0 1.15rem;padding:.55rem;border:1px solid #e0e7ff;border-radius:1.2rem;background:#f8fafc}div[data-testid="stRadio"]>label{display:none}div[role="radiogroup"]{display:flex;flex-wrap:wrap;gap:.42rem}div[role="radiogroup"] label{border:1px solid #dbeafe!important;border-radius:999px!important;background:white!important;padding:.38rem .74rem!important}div[role="radiogroup"] label p{font-weight:900!important;color:#334155!important;font-size:.9rem!important}div[role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,#4f46e5,#06b6d4)!important}div[role="radiogroup"] label:has(input:checked) p{color:white!important}
.hero,.subhero{border:1px solid #c7d2fe;border-radius:1.45rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 46%,#fff);box-shadow:0 18px 44px rgba(15,23,42,.08);padding:1.45rem;margin:1.15rem 0}.hero{padding:2rem}.hero h1{font-size:2.65rem;line-height:1.05;margin:.55rem 0;color:#0f172a;font-weight:980}.hero h1 span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}.hero p,.subhero p{color:#475569;line-height:1.75}
.eyebrow,.label{display:inline-block;font-size:.78rem;letter-spacing:.12em;color:#3730a3;font-weight:950;background:white;border:1px solid #c7d2fe;border-radius:999px;padding:.3rem .65rem}.kicker{font-size:.78rem;font-weight:950;letter-spacing:.14em;color:#4f46e5;text-transform:uppercase;margin-top:1.6rem}.title{font-size:1.65rem;font-weight:950;color:#0f172a}.sub{color:#64748b;line-height:1.75;max-width:860px}
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:.95rem}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}.card,.offer,.state-card{border:1px solid #e2e8f0;border-radius:1.08rem;background:white;padding:1rem;box-shadow:0 8px 22px rgba(15,23,42,.045);min-height:105px}.card p,.offer p,.state-card p{color:#64748b;line-height:1.58}.green{background:#f0fdf4;border-color:#bbf7d0}.orange{background:#fff7ed;border-color:#fed7aa}.soft{background:#f8fafc;border-color:#dbeafe}
.flow{display:grid;grid-template-columns:repeat(6,1fr);gap:.55rem}.flow div{background:white;border:1px solid #c7d2fe;border-radius:1rem;padding:.85rem;text-align:center}.flow b{display:block;color:#4f46e5}.flow span{font-weight:850;color:#312e81;font-size:.82rem}.chip-green{background:#dcfce7;color:#166534}.chip-blue{background:#dbeafe;color:#1e40af}.chip-orange{background:#ffedd5;color:#9a3412}.chip-gray{background:#f1f5f9;color:#475569}.chip-red{background:#fee2e2;color:#991b1b}.summary{border-radius:1rem;background:#0f172a;color:#e2e8f0;padding:1rem;line-height:1.7;white-space:pre-wrap}
@media(max-width:960px){.nav{position:relative}.nav-inner{align-items:flex-start;flex-direction:column}.badges{display:none}.grid2,.grid3,.grid4{grid-template-columns:1fr}.flow{grid-template-columns:repeat(2,1fr)}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

NAV = {"home":"首页","workspace":"学习工作台","trial":"2小时体验课","sop":"跟进SOP","paths":"成长路径","skills":"技能训练","portfolio":"作品集","freelance":"自由职业","company":"企业内训","pricing":"报价","booking":"预约咨询","faq":"FAQ"}
STATUS_CHIP = {"未开始":"chip-gray","进行中":"chip-blue","已提交":"chip-orange","AI已反馈":"chip-blue","待老师点评":"chip-orange","已点评":"chip-green","已入作品集":"chip-green","风险":"chip-red","等待":"chip-gray"}

CREATE_TABLE_SQL = """create table if not exists public.courses (
  course_id text primary key,
  name text not null,
  audience text,
  promise text,
  is_active boolean default true,
  created_at timestamptz default now()
);

create table if not exists public.task_templates (
  task_key text primary key,
  course_id text not null references public.courses(course_id) on delete cascade,
  day text,
  title text not null,
  outcome text,
  prompt text,
  standard text,
  sort_order int default 0,
  created_at timestamptz default now()
);

create table if not exists public.enrollments (
  enrollment_id text primary key,
  student_name text not null,
  course_id text not null references public.courses(course_id),
  status text default '学习中',
  owner_email text,
  coach_email text,
  created_at timestamptz default now()
);

create table if not exists public.task_instances (
  instance_id text primary key,
  enrollment_id text not null references public.enrollments(enrollment_id) on delete cascade,
  student text not null,
  course_id text not null references public.courses(course_id),
  task_key text not null references public.task_templates(task_key),
  status text default '未开始',
  version text default '未提交',
  draft text default '',
  ai_feedback text default '',
  teacher_review text default '',
  score int default 0,
  portfolio boolean default false,
  risk text default '正常',
  updated_at timestamptz default now()
);

create table if not exists public.reviews (
  review_id text primary key,
  instance_id text not null references public.task_instances(instance_id) on delete cascade,
  reviewer text not null,
  score int default 0,
  conclusion text,
  review_text text,
  created_at timestamptz default now()
);"""

COURSE_SEED_SQL = """insert into public.courses(course_id, name, audience, promise, is_active) values
('growth_5d', '5 天 AI 技能成长营', '职场新人 / 在岗提升 / 升职准备 / 转岗跳槽', '3 个可展示作品 + AI 反馈记录 + 老师点评 + 30 天行动计划', true),
('freelance_5d', '5 天自由职业技能变现营', '自由职业 / 副业接单者', '1 个服务包 + 3 个样品案例 + 报价单 + 获客话术 + 交付 SOP', true),
('enterprise_dept', '企业部门 AI 训练营', '企业内训部门 / 新人培养 / 部门负责人', '部门任务模板 + 评分标准 + 员工练习包 + 培训复盘', true)
on conflict (course_id) do update set
name = excluded.name,
audience = excluded.audience,
promise = excluded.promise,
is_active = excluded.is_active;"""

TASK_TEMPLATE_SEED_SQL = """insert into public.task_templates(task_key, course_id, day, title, outcome, prompt, standard, sort_order) values
('g_day1','growth_5d','Day 1','定目标 + 拆任务','技能成长路线图','你是职业技能教练。请把我的目标拆成 5 天训练任务，并说明每天交付物。','目标明确；任务可执行；交付物可检查。',1),
('g_day2','growth_5d','Day 2','作品 1：基础任务作品','测试用例 + Bug 报告模板','你是严格的软件测试教练。请根据登录页面需求设计测试用例，并输出遗漏点和 Bug 报告模板。','覆盖正常、异常、边界、安全、权限；步骤可执行。',2),
('g_day3','growth_5d','Day 3','作品 2：复杂任务作品','复杂需求拆解 + 异常场景补全','请把复杂业务需求拆成流程、角色、输入输出、异常分支和测试点。','能解释流程；能发现异常；能说明遗漏信息。',3),
('g_day4','growth_5d','Day 4','作品 3：展示 / 发表作品','项目发表说明 + 成果表达稿','请把我的项目成果整理成 3 分钟发表稿，包含背景、任务、方法、结果和改进点。','表达清楚；能展示价值；能回答追问。',4),
('g_day5','growth_5d','Day 5','复盘 + 后续路径','30 天行动计划','请根据我的 3 个作品和老师点评，生成后续 30 天行动计划。','路径清楚；动作具体；能持续复盘。',5),
('f_day1','freelance_5d','Day 1','选择可售卖技能','服务方向定位','请帮我把一个技能转成可售卖服务方向，说明目标客户、痛点和交付物。','客户明确；痛点具体；交付边界清楚。',1),
('f_day2','freelance_5d','Day 2','样品案例 1','第一个可展示样品','请根据目标客户场景，帮我设计一个可展示样品案例。','样品能展示能力；客户能看懂价值。',2),
('e_1','enterprise_dept','模块 1','部门高频任务清单','AI 训练任务地图','请把部门高频任务整理成可训练任务清单，并标出可用 AI 辅助的环节。','任务真实；频率高；能训练。',1)
on conflict (task_key) do update set
course_id=excluded.course_id,
day=excluded.day,
title=excluded.title,
outcome=excluded.outcome,
prompt=excluded.prompt,
standard=excluded.standard,
sort_order=excluded.sort_order;"""

RLS_OFF_SQL = """alter table public.courses disable row level security;
alter table public.task_templates disable row level security;
alter table public.enrollments disable row level security;
alter table public.task_instances disable row level security;
alter table public.reviews disable row level security;"""

def get_secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return default

def configured(name: str) -> bool:
    value = get_secret(name)
    return bool(value and value.strip() and "YOUR_" not in value and "xxxx" not in value)

def db_ready() -> bool:
    return configured("SUPABASE_URL") and configured("SUPABASE_ANON_KEY")

def get_supabase_client():
    from supabase import create_client
    return create_client(get_secret("SUPABASE_URL"), get_secret("SUPABASE_ANON_KEY"))

def safe_id(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", text.strip()).strip("_") or "item"

def chip(status: Any) -> str:
    status_text = str(status or "")
    cls = STATUS_CHIP.get(status_text, "chip-gray")
    return f"<span class='status-chip {cls}'>{status_text}</span>"

def val(row: pd.Series, col: str, default: str = "") -> Any:
    try:
        item = row.get(col, default)
        if pd.isna(item):
            return default
        return item
    except Exception:
        return default

def section(kicker: str, title: str, sub: str = "") -> None:
    st.markdown(f"<div class='kicker'>{kicker}</div><div class='title'>{title}</div><div class='sub'>{sub}</div>", unsafe_allow_html=True)

def subhero(label: str, title: str, body: str) -> None:
    st.markdown(f"<div class='subhero'><span class='label'>{label}</span><h2>{title}</h2><p>{body}</p></div>", unsafe_allow_html=True)

def html_card(icon: str, title: str, body: str, cls: str = "card") -> str:
    return f"<div class='{cls}'><b>{icon} {title}</b><p>{body}</p></div>"

def db_select(table: str, columns: str = "*", limit: int = 500) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready():
        return False, "未配置 Supabase Secrets。", pd.DataFrame()
    try:
        res = get_supabase_client().table(table).select(columns).limit(limit).execute()
        data = res.data or []
        return True, f"读取 {table} 成功：{len(data)} 条。", pd.DataFrame(data)
    except Exception as exc:
        return False, f"读取 {table} 失败：{exc}", pd.DataFrame()

def db_tasks_for_course(course_id: str) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready():
        return False, "未配置 Supabase Secrets。", pd.DataFrame()
    try:
        res = get_supabase_client().table("task_templates").select("*").eq("course_id", course_id).order("sort_order").execute()
        data = res.data or []
        return True, f"读取任务模板成功：{len(data)} 条。", pd.DataFrame(data)
    except Exception as exc:
        return False, f"读取任务模板失败：{exc}", pd.DataFrame()

def db_task_instances(status: str | None = None, enrollment_id: str | None = None) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready():
        return False, "未配置 Supabase Secrets。", pd.DataFrame()
    try:
        query = get_supabase_client().table("task_instances").select("*").order("updated_at", desc=True).limit(500)
        if status:
            query = query.eq("status", status)
        if enrollment_id:
            query = query.eq("enrollment_id", enrollment_id)
        res = query.execute()
        data = res.data or []
        return True, f"读取 task_instances 成功：{len(data)} 条。", pd.DataFrame(data)
    except Exception as exc:
        return False, f"读取 task_instances 失败：{exc}", pd.DataFrame()

def db_update_task_instance(instance_id: str, updates: dict[str, Any]) -> tuple[bool, str]:
    if not db_ready():
        return False, "未配置 Supabase Secrets。"
    try:
        payload = dict(updates)
        payload["updated_at"] = datetime.now().isoformat()
        get_supabase_client().table("task_instances").update(payload).eq("instance_id", instance_id).execute()
        return True, f"已更新 task_instances：{instance_id}"
    except Exception as exc:
        return False, f"更新失败：{exc}"

def db_insert_review(instance_id: str, reviewer: str, score: int, conclusion: str, review_text: str) -> tuple[bool, str, str]:
    if not db_ready():
        return False, "未配置 Supabase Secrets。", ""
    try:
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        review_id = f"rev_{safe_id(instance_id)}_{stamp}"
        row = {"review_id": review_id, "instance_id": instance_id, "reviewer": reviewer.strip() or "老师", "score": int(score), "conclusion": conclusion, "review_text": review_text.strip()}
        get_supabase_client().table("reviews").insert(row).execute()
        return True, f"已写入 reviews：{review_id}", review_id
    except Exception as exc:
        return False, f"写入 reviews 失败：{exc}", ""

def db_submit_teacher_review(instance_id: str, reviewer: str, score: int, conclusion: str, review_text: str, portfolio: bool) -> tuple[bool, str]:
    ok, msg, review_id = db_insert_review(instance_id, reviewer, score, conclusion, review_text)
    if not ok:
        return False, msg
    new_status = "已入作品集" if portfolio else "已点评"
    updates = {"teacher_review": review_text.strip(), "score": int(score), "status": new_status, "risk": "已完成", "portfolio": bool(portfolio)}
    ok2, msg2 = db_update_task_instance(instance_id, updates)
    if not ok2:
        return False, f"{msg}；但回写任务失败：{msg2}"
    return True, f"{msg}；{msg2}"

def create_real_enrollment(student_name: str, course_id: str, owner_email: str = "", coach_email: str = "") -> tuple[bool, str, str]:
    student_name = student_name.strip()
    if not student_name:
        return False, "请先输入学员名。", ""
    if not db_ready():
        return False, "未配置 Supabase Secrets。", ""
    ok, msg, tasks = db_tasks_for_course(course_id)
    if not ok:
        return False, msg, ""
    if tasks.empty:
        return False, "该课程还没有 task_templates。请先运行 task_templates seed SQL。", ""
    try:
        client = get_supabase_client()
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        enrollment_id = f"enr_{safe_id(student_name)}_{course_id}_{stamp}"
        enrollment = {"enrollment_id": enrollment_id, "student_name": student_name, "course_id": course_id, "status": "学习中", "owner_email": owner_email.strip() or None, "coach_email": coach_email.strip() or None}
        client.table("enrollments").insert(enrollment).execute()
        rows: list[dict[str, Any]] = []
        for i, task in tasks.reset_index(drop=True).iterrows():
            status = "进行中" if i == 0 else "未开始"
            rows.append({"instance_id": f"ti_{safe_id(student_name)}_{task['task_key']}_{stamp}", "enrollment_id": enrollment_id, "student": student_name, "course_id": course_id, "task_key": task["task_key"], "status": status, "version": "未提交", "draft": "", "ai_feedback": "", "teacher_review": "", "score": 0, "portfolio": False, "risk": "正常" if status == "进行中" else "等待"})
        client.table("task_instances").insert(rows).execute()
        return True, f"已创建报名 {enrollment_id}，并生成 {len(rows)} 条任务实例。", enrollment_id
    except Exception as exc:
        return False, f"写入失败：{exc}", ""

def format_webhook_payload(lead: dict[str, Any], provider: str) -> dict[str, Any]:
    text = lead.get("summary", "")
    provider = (provider or "generic").lower().strip()
    if provider in {"feishu", "lark"}:
        return {"msg_type": "text", "content": {"text": text}}
    if provider in {"wecom", "wechat_work", "qywx", "enterprise_wechat"}:
        return {"msgtype": "text", "text": {"content": text}}
    return lead

def post_lead_to_webhook(lead: dict[str, Any]) -> tuple[bool, str]:
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

def merge_instances_with_templates(instances: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    if instances.empty or tasks.empty:
        return instances
    if not {"course_id", "task_key"}.issubset(tasks.columns):
        return instances
    keep = [c for c in ["course_id", "task_key", "day", "title", "outcome", "prompt", "standard", "sort_order"] if c in tasks.columns]
    return instances.merge(tasks[keep], on=["course_id", "task_key"], how="left")

def render_top_nav() -> str:
    st.markdown("""
    <div class='nav'><div class='nav-inner'>
    <div class='brand'><div class='logo'>AI</div><div>AI Skill Growth Platform<small>技能成长 · 真实老师点评 · v4.0</small></div></div>
    <div class='badges'><span class='badge'>学员提交</span><span class='badge'>AI反馈</span><span class='badge'>老师点评</span><span class='badge cta'>真实闭环</span></div>
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='nav-panel'>", unsafe_allow_html=True)
    page = st.radio("导航", list(NAV.keys()), horizontal=True, label_visibility="collapsed", format_func=lambda key: NAV[key], key="top_page_nav")
    st.markdown("</div>", unsafe_allow_html=True)
    return page

def render_home() -> None:
    st.markdown("""
    <div class='hero'>
    <span class='eyebrow'>AI Skill Growth Platform</span>
    <h1>AI 技能成长<br><span>教育平台</span></h1>
    <p><b>用 AI 更快学会新技能，并做出可展示、可交付、可变现的成果。</b><br>
    v4.0：真实老师点评端。学员提交草稿后，老师可以写入 reviews，并回写任务评分、点评、状态和作品集标记。</p>
    <span class='pill'>课程模板</span><span class='pill'>报名</span><span class='pill'>任务实例</span><span class='pill'>老师点评</span>
    </div>
    """, unsafe_allow_html=True)
    flow = [("01", "课程"), ("02", "报名"), ("03", "任务"), ("04", "提交"), ("05", "AI反馈"), ("06", "老师点评")]
    section("METHOD", "真实学习闭环已经成型", "当前先关闭 RLS 跑通原型，后续再加登录和权限。")
    st.markdown("<div class='flow'>" + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in flow) + "</div>", unsafe_allow_html=True)
    offers = [("2 小时体验课", "99 / 199 元", "完成一个微型任务，拿到 AI 路径和一版作品。"), ("5 天技能成长营", "3999 元建议", "形成 3 个可展示作品、反馈记录和老师点评。"), ("自由职业技能变现营", "4999 元建议", "形成服务包、样品、报价和交付 SOP。"), ("企业内训", "3 万元起", "把部门高频任务改造成可训练、可评分的 AI 工作流。")]
    st.markdown("<div class='grid4'>" + "".join(html_card("🚀", title + " · " + price, body, "offer") for title, price, body in offers) + "</div>", unsafe_allow_html=True)

def render_diagnostics() -> None:
    status = {"SUPABASE_URL": "已配置" if configured("SUPABASE_URL") else "未配置", "SUPABASE_ANON_KEY": "已配置" if configured("SUPABASE_ANON_KEY") else "未配置", "当前模式": "真实数据库" if db_ready() else "模拟模式"}
    cols = st.columns(3)
    for col, item in zip(cols, status.items()):
        name, value = item
        col.metric(name, value)

def render_real_loop() -> None:
    section("REAL LOOP", "创建报名与任务实例", "从 courses 和 task_templates 创建真实 enrollments / task_instances。")
    render_diagnostics()
    if not db_ready():
        st.info("请先配置 Streamlit Secrets。")
        return
    ok_c, msg_c, courses = db_select("courses")
    ok_t, msg_t, tasks = db_select("task_templates")
    st.success(msg_c) if ok_c else st.error(msg_c)
    st.success(msg_t) if ok_t else st.error(msg_t)
    left, right = st.columns(2)
    with left:
        st.markdown("### courses")
        st.dataframe(courses, use_container_width=True, hide_index=True)
    with right:
        st.markdown("### task_templates")
        if tasks.empty:
            st.warning("task_templates 表为空。请运行 seed SQL，或检查 RLS 是否关闭。")
        else:
            cols = [c for c in ["course_id", "task_key", "day", "title", "sort_order"] if c in tasks.columns]
            st.dataframe(tasks[cols], use_container_width=True, hide_index=True)
    if courses.empty:
        return
    st.markdown("### 创建真实学员")
    with st.form("create_enrollment_v40"):
        student_name = st.text_input("学员 / 小组名称", value="真实学员A")
        course_id = st.selectbox("选择课程", courses["course_id"].tolist())
        owner_email = st.text_input("学员邮箱，可空")
        coach_email = st.text_input("老师邮箱，可空")
        submitted = st.form_submit_button("创建报名并生成任务实例")
    if submitted:
        ok, msg, eid = create_real_enrollment(student_name, course_id, owner_email, coach_email)
        if ok:
            st.success(msg)
            st.session_state["last_enrollment_id"] = eid
        else:
            st.error(msg)
    eid_filter = st.text_input("按 enrollment_id 过滤，可空", value=st.session_state.get("last_enrollment_id", ""))
    ok_i, msg_i, instances = db_task_instances(enrollment_id=eid_filter.strip() or None)
    st.success(msg_i) if ok_i else st.error(msg_i)
    if not instances.empty:
        st.dataframe(instances, use_container_width=True, hide_index=True)

def render_real_student() -> None:
    section("REAL STUDENT", "真实学员端", "学员读取真实任务，提交草稿，生成模拟 AI 反馈，并提交老师点评。")
    render_diagnostics()
    if not db_ready():
        st.info("未配置 Supabase Secrets。")
        return
    ok_i, msg_i, instances = db_task_instances()
    ok_t, msg_t, tasks = db_select("task_templates")
    if not ok_i:
        st.error(msg_i)
        return
    if instances.empty:
        st.warning("task_instances 为空。先到“创建报名与任务实例”创建一个学员。")
        return
    merged = merge_instances_with_templates(instances, tasks if ok_t else pd.DataFrame())
    students = sorted(merged["student"].dropna().unique().tolist())
    student = st.selectbox("选择真实学员", students, key="student_select_v40")
    sdf = merged[merged["student"] == student].copy()
    status_rank = {"进行中": 0, "已提交": 1, "AI已反馈": 2, "待老师点评": 3, "未开始": 4, "已点评": 5, "已入作品集": 6}
    sdf["_rank"] = sdf["status"].map(status_rank).fillna(9)
    sdf = sdf.sort_values(["_rank", "updated_at" if "updated_at" in sdf.columns else "instance_id"], ascending=[True, False])
    st.dataframe(sdf.drop(columns=["_rank"], errors="ignore"), use_container_width=True, hide_index=True)
    labels = [f"{row['instance_id']}｜{val(row, 'status')}｜{val(row, 'day', '')}｜{val(row, 'title', row['task_key'])}" for _, row in sdf.iterrows()]
    selected_label = st.selectbox("选择要处理的任务", labels, key="task_select_student_v40")
    instance_id = selected_label.split("｜", 1)[0]
    row = sdf[sdf["instance_id"] == instance_id].iloc[0]
    st.markdown(f"<div class='state-card'><b>{val(row, 'day', '')}｜{val(row, 'title', row['task_key'])}</b><p>实例：{row['instance_id']}<br>课程：{row['course_id']}　任务：{row['task_key']}<br>状态：{chip(val(row, 'status'))}　版本：{val(row, 'version', '未提交')}</p><p><b>交付物：</b>{val(row, 'outcome', '')}</p><p><b>标准：</b>{val(row, 'standard', '')}</p></div>", unsafe_allow_html=True)
    if val(row, "prompt", ""):
        st.code(str(val(row, "prompt")), language="text")
    draft = st.text_area("作品草稿 draft", value=str(val(row, "draft", "")), height=220, key=f"draft_{instance_id}")
    if val(row, "ai_feedback", ""):
        st.info("AI反馈：\n" + str(val(row, "ai_feedback")))
    if val(row, "teacher_review", ""):
        st.success("老师点评：\n" + str(val(row, "teacher_review")))
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("保存草稿并标记已提交", type="primary", key=f"save_{instance_id}"):
        ok, msg = db_update_task_instance(instance_id, {"draft": draft, "status": "已提交", "version": "第一版", "risk": "等待AI反馈"})
        st.success(msg) if ok else st.error(msg)
        if ok:
            st.rerun()
    if c2.button("生成模拟AI反馈", key=f"ai_{instance_id}"):
        feedback = f"AI反馈：已检查任务 {row['task_key']}。请对照评分标准补充遗漏，把输出改成可执行格式，并保留修改前后版本。"
        ok, msg = db_update_task_instance(instance_id, {"ai_feedback": feedback, "status": "AI已反馈", "risk": "需按AI反馈修改"})
        st.success(msg) if ok else st.error(msg)
        if ok:
            st.rerun()
    if c3.button("提交老师点评", key=f"teacher_{instance_id}"):
        ok, msg = db_update_task_instance(instance_id, {"status": "待老师点评", "risk": "待人工判断"})
        st.success(msg) if ok else st.error(msg)
        if ok:
            st.rerun()
    if c4.button("标记进行中", key=f"progress_{instance_id}"):
        ok, msg = db_update_task_instance(instance_id, {"status": "进行中", "risk": "正常"})
        st.success(msg) if ok else st.error(msg)
        if ok:
            st.rerun()

def render_real_teacher() -> None:
    section("REAL TEACHER", "v4.0 真实老师点评端", "老师读取待点评任务，写入 reviews，并回写 task_instances。")
    render_diagnostics()
    if not db_ready():
        st.info("未配置 Supabase Secrets。")
        return
    status_filter = st.selectbox("筛选状态", ["待老师点评", "AI已反馈", "已提交", "已点评", "已入作品集", "全部"], index=0)
    selected_status = None if status_filter == "全部" else status_filter
    ok_i, msg_i, instances = db_task_instances(status=selected_status)
    ok_t, msg_t, tasks = db_select("task_templates")
    if not ok_i:
        st.error(msg_i)
        return
    st.success(msg_i)
    if instances.empty:
        st.warning("当前没有符合条件的任务。让学员端先提交草稿并点“提交老师点评”。")
        return
    merged = merge_instances_with_templates(instances, tasks if ok_t else pd.DataFrame())
    view_cols = [c for c in ["student", "course_id", "task_key", "day", "title", "status", "version", "score", "risk", "updated_at"] if c in merged.columns]
    st.dataframe(merged[view_cols], use_container_width=True, hide_index=True)
    labels = [f"{row['instance_id']}｜{val(row, 'student')}｜{val(row, 'status')}｜{val(row, 'title', row['task_key'])}" for _, row in merged.iterrows()]
    selected_label = st.selectbox("选择要点评的任务", labels, key="teacher_select_v40")
    instance_id = selected_label.split("｜", 1)[0]
    row = merged[merged["instance_id"] == instance_id].iloc[0]
    st.markdown(f"<div class='state-card'><b>{val(row, 'student')}｜{val(row, 'title', row['task_key'])}</b><p>实例：{row['instance_id']}<br>状态：{chip(val(row, 'status'))}<br>交付物：{val(row, 'outcome', '')}<br>标准：{val(row, 'standard', '')}</p></div>", unsafe_allow_html=True)
    st.markdown("#### 学员草稿")
    st.text_area("draft", value=str(val(row, "draft", "")), height=220, disabled=True, key=f"teacher_draft_{instance_id}")
    if val(row, "ai_feedback", ""):
        st.info("AI反馈：\n" + str(val(row, "ai_feedback")))
    with st.form(f"teacher_review_form_{instance_id}"):
        reviewer = st.text_input("点评老师", value="老师A")
        score = st.slider("评分", 0, 100, int(val(row, "score", 0) or 0))
        conclusion = st.selectbox("结论", ["通过", "需要修改", "退回重做", "收入作品集"])
        default_review = "优点：\n改进点：\n下一步："
        current_review = str(val(row, "teacher_review", "")) or default_review
        review_text = st.text_area("老师点评", value=current_review, height=180)
        portfolio = st.checkbox("收入作品集", value=bool(val(row, "portfolio", False)) or conclusion == "收入作品集")
        submitted = st.form_submit_button("写入 reviews，并回写任务状态")
    if submitted:
        if not review_text.strip():
            st.error("请先填写老师点评。")
            return
        ok, msg = db_submit_teacher_review(instance_id, reviewer, score, conclusion, review_text, portfolio)
        st.success(msg) if ok else st.error(msg)
        if ok:
            st.rerun()
    ok_r, msg_r, reviews = db_select("reviews")
    if ok_r and not reviews.empty and "instance_id" in reviews.columns:
        recent = reviews[reviews["instance_id"] == instance_id]
        if not recent.empty:
            st.markdown("#### 该任务历史点评")
            st.dataframe(recent, use_container_width=True, hide_index=True)

def render_real_ops() -> None:
    section("REAL OPS", "真实运营看板", "聚合 Supabase 的 task_instances，查看状态、风险和作品集。")
    if not db_ready():
        st.info("未配置 Supabase Secrets。")
        return
    ok, msg, df = db_task_instances()
    if not ok:
        st.error(msg)
        return
    st.success(msg)
    if df.empty:
        st.warning("暂无任务实例。")
        return
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("任务实例", len(df))
    c2.metric("待老师点评", int((df["status"] == "待老师点评").sum()) if "status" in df.columns else 0)
    c3.metric("已点评/作品集", int((df["status"].isin(["已点评", "已入作品集"])).sum()) if "status" in df.columns else 0)
    c4.metric("作品集", int(df["portfolio"].fillna(False).astype(bool).sum()) if "portfolio" in df.columns else 0)
    if "status" in df.columns:
        st.bar_chart(df["status"].value_counts())
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_sql_tools() -> None:
    section("SQL", "建表 / Seed / RLS 开关", "当前原型阶段建议先关闭 RLS。")
    tabs = st.tabs(["建表 SQL", "courses seed", "task_templates seed", "关闭 RLS"])
    with tabs[0]:
        st.code(CREATE_TABLE_SQL, language="sql")
    with tabs[1]:
        st.code(COURSE_SEED_SQL, language="sql")
    with tabs[2]:
        st.code(TASK_TEMPLATE_SEED_SQL, language="sql")
    with tabs[3]:
        st.code(RLS_OFF_SQL, language="sql")

def render_workspace() -> None:
    subhero("V4.0 REAL TEACHER REVIEW", "学习工作台：真实老师点评闭环版", "学员端提交草稿，老师端写入 reviews 并回写 task_instances，运营端查看真实状态。")
    tabs = st.tabs(["真实学员端", "真实老师点评端", "真实运营看板", "创建报名与任务实例", "SQL / Seed / RLS"])
    with tabs[0]:
        render_real_student()
    with tabs[1]:
        render_real_teacher()
    with tabs[2]:
        render_real_ops()
    with tabs[3]:
        render_real_loop()
    with tabs[4]:
        render_sql_tools()

def render_trial() -> None:
    subhero("2-HOUR TRIAL", "AI 技能成长 2 小时体验课", "低门槛入口产品。目标是在 2 小时内帮用户完成一个真实小任务。")
    cards = [("推荐价格", "99 / 199 元：降低决策门槛，用真实体验建立信任。"), ("适合谁", "职场新人、在岗提升、升职准备、转岗跳槽、自由职业、企业内训负责人。"), ("核心承诺", "2 小时内不空谈，必须完成一个微型任务。")]
    st.markdown("<div class='grid3'>" + "".join(html_card("✅", a, b, "card green") for a, b in cards) + "</div>", unsafe_allow_html=True)

def render_followup_sop() -> None:
    subhero("SALES SOP", "线索跟进 SOP", "飞书或下载线索后，销售按固定动作推进。")
    statuses = [("新线索", "5 分钟内响应"), ("已联系", "发送第一条回复"), ("已约时间", "确定体验课时间"), ("已付款", "确认体验课"), ("已上课", "进入课后转化"), ("已转化", "进入训练营或企业方案"), ("未转化", "记录原因，7 天后触达")]
    st.markdown("<div class='grid4'>" + "".join(html_card("📌", a, b, "card soft") for a, b in statuses) + "</div>", unsafe_allow_html=True)

def render_paths() -> None:
    subhero("GROWTH PATHS", "成长路径", "平台先帮用户选路径，再拆成任务。")
    rows = [("新人上手", "从不会到能做", "岗位基础技能，完成第一个可检查任务"), ("在岗提升", "从能做到价值更高", "把重复任务做成 AI 工作流"), ("升职准备", "从执行者到负责人", "分析、汇报、复盘和带新人"), ("转岗换工作", "从旧岗位到新岗位", "补齐技能并形成作品集"), ("自由职业增收", "从会技能到能接单", "服务包、报价和交付作品")]
    st.dataframe(pd.DataFrame(rows, columns=["场景", "目标", "训练重点"]), use_container_width=True, hide_index=True)

def render_skills() -> None:
    subhero("SKILL TRAINING", "技能训练", "AI 负责高频反馈，老师负责最终判断。")
    rows = [("学新技能", "AI 生成学习路径、解释概念、给例子"), ("做任务", "把学习目标变成真实工作任务"), ("被纠错", "AI 第一轮反馈遗漏、逻辑、格式、风险"), ("再修改", "根据反馈形成第二版、第三版成果"), ("做作品", "变成能给老板、客户或面试官看的作品"), ("会表达", "说明自己怎么学、怎么做、怎么提升结果")]
    st.markdown("<div class='grid3'>" + "".join(html_card("🧠", a, b) for a, b in rows) + "</div>", unsafe_allow_html=True)

def render_portfolio() -> None:
    subhero("PORTFOLIO", "作品集", "作品集来自已点评或已入作品集的真实 task_instances。")
    if not db_ready():
        st.info("配置 Supabase 后可查看真实作品集。")
        return
    ok, msg, df = db_task_instances()
    if not ok:
        st.error(msg)
        return
    if df.empty or "portfolio" not in df.columns:
        st.info("暂无作品集。")
        return
    pf = df[df["portfolio"].fillna(False).astype(bool)]
    if pf.empty:
        st.info("暂无收入作品集的任务。")
    else:
        st.dataframe(pf, use_container_width=True, hide_index=True)

def render_freelance() -> None:
    subhero("FREELANCE", "自由职业者：学新技能，赚更多钱", "不是保证收入，而是训练你把技能包装成可出售服务。")
    rows = [("选技能", "选择能变现的技能方向"), ("做样品", "完成 2-3 个可展示样品"), ("包装服务", "把技能变成清楚的服务包"), ("获客表达", "写主页简介、私信话术、报价说明"), ("交付流程", "需求确认、初稿、修改、验收、复盘 SOP"), ("提价路径", "从低价单到标准化服务，再到高价值项目")]
    st.markdown("<div class='grid3'>" + "".join(html_card("💼", a, b) for a, b in rows) + "</div>", unsafe_allow_html=True)

def render_company() -> None:
    subhero("COMPANY TRAINING", "企业内训", "企业需要的不只是 AI 讲座，而是新人上手和部门技能训练体系。")
    rows = [("新人上手", "学习路径、任务练习、AI 反馈和老师点评标准化。"), ("在岗提升", "把部门高频任务做成 AI 学习与工作流模板。"), ("部门模板", "沉淀日报、周报、会议纪要、客户回复、PPT、数据说明模板。"), ("合规边界", "企业数据脱敏，关键输出必须人工审核。")]
    st.markdown("<div class='grid4'>" + "".join(html_card("🏢", a, b) for a, b in rows) + "</div>", unsafe_allow_html=True)

def render_pricing() -> None:
    subhero("PRICING", "报价与产品入口", "价格不是按讲师小时数，而是按训练结果。")
    rows = [("2 小时体验课", "99 / 199 元"), ("5 天技能成长营", "3999 元建议"), ("自由职业技能变现营", "4999 元建议"), ("企业内训", "3 万元起")]
    st.markdown("<div class='grid4'>" + "".join(html_card("💰", a, b, "offer") for a, b in rows) + "</div>", unsafe_allow_html=True)

def render_booking() -> None:
    subhero("BOOKING", "预约体验课 / 咨询方案", "填写后可生成咨询摘要，也可自动发送到你配置的 Webhook。")
    configured_webhook = bool(get_secret("LEAD_WEBHOOK_URL"))
    status_cls = "green" if configured_webhook else "orange"
    status_text = "已配置：提交后会自动发送线索。" if configured_webhook else "未配置：线索不会自动保存，请下载 TXT/CSV。"
    st.markdown(f"<div class='card {status_cls}'><b>Webhook 状态</b><p>{status_text}</p></div>", unsafe_allow_html=True)
    with st.form("booking_form_v40"):
        name = st.text_input("姓名 / 称呼")
        contact = st.text_input("联系方式（微信 / 邮箱 / 手机，任选）")
        identity = st.selectbox("你现在属于哪类人？", ["职场新人", "在岗提升", "升职准备", "转岗 / 跳槽", "自由职业 / 副业接单", "企业培训负责人", "小微老板"])
        goal = st.selectbox("你最想解决什么？", ["学新技能", "提升现有技能", "做作品集", "升职表达", "换工作 / 高薪跳槽", "自由职业接单", "企业内训"])
        skill = st.text_input("想学习或提升的具体技能")
        note = st.text_area("补充说明")
        submitted = st.form_submit_button("生成并提交咨询摘要")
    if submitted:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = f"""【AI 技能成长咨询摘要】
提交时间：{timestamp}
姓名/称呼：{name or '未填写'}
联系方式：{contact or '未填写'}
当前身份：{identity}
主要目标：{goal}
目标技能：{skill or '未填写'}
补充说明：{note or '无'}"""
        lead = {"timestamp": timestamp, "name": name, "contact": contact, "identity": identity, "goal": goal, "skill": skill, "note": note, "summary": summary, "source": "streamlit_site"}
        ok, msg = post_lead_to_webhook(lead)
        st.success("咨询摘要已生成。")
        st.info(msg)
        st.markdown(f"<div class='summary'>{summary}</div>", unsafe_allow_html=True)
        df = pd.DataFrame([lead])
        st.download_button("下载 TXT 摘要", data=summary, file_name="ai_skill_growth_lead.txt", mime="text/plain")
        st.download_button("下载 CSV 线索", data=df.to_csv(index=False).encode("utf-8-sig"), file_name="ai_skill_growth_lead.csv", mime="text/csv")

def render_faq() -> None:
    subhero("FAQ", "常见问题", "把风险边界说清楚，比夸大承诺更能建立信任。")
    qs = [("这是不是只适合新人？", "不是。新人、想升职的人、转岗的人、自由职业者、想带团队的人都适合。"), ("这是不是 AI 办公提效课？", "不是。提效只是副产品，核心是学习新技能、提升技能，并做出可展示成果。"), ("会不会承诺就业、涨薪、接单收入或证书？", "不承诺。平台交付技能路径、作品集、服务包和表达能力，不做官方职业资格或收入保证。"), ("AI 会不会替代老师？", "不会。AI 做第一轮解释和反馈，老师负责任务设计、标准把关和关键点评。")]
    st.markdown("<div class='grid2'>" + "".join(html_card("❓", q, a) for q, a in qs) + "</div>", unsafe_allow_html=True)

def main() -> None:
    page = render_top_nav()
    if page == "home":
        render_home()
    elif page == "workspace":
        render_workspace()
    elif page == "trial":
        render_trial()
    elif page == "sop":
        render_followup_sop()
    elif page == "paths":
        render_paths()
    elif page == "skills":
        render_skills()
    elif page == "portfolio":
        render_portfolio()
    elif page == "freelance":
        render_freelance()
    elif page == "company":
        render_company()
    elif page == "pricing":
        render_pricing()
    elif page == "booking":
        render_booking()
    else:
        render_faq()
    st.caption("AI Skill Growth Platform · real teacher review loop prototype v4.0")

if __name__ == "__main__":
    main()
