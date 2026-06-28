from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Founder Agent Console", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.main .block-container{max-width:1160px;padding-top:1rem;padding-bottom:4rem}
.hero{border:1px solid #c7d2fe;border-radius:1.25rem;background:radial-gradient(circle at right,#ecfeff,#eef2ff 48%,#fff);padding:1.4rem;margin:1rem 0;box-shadow:0 14px 34px rgba(15,23,42,.08)}
.hero h1{font-size:2.35rem;line-height:1.08;margin:.3rem 0}.hero span{background:linear-gradient(90deg,#4f46e5,#06b6d4);-webkit-background-clip:text;color:transparent}
.card{border:1px solid #e2e8f0;border-radius:1rem;background:white;padding:1rem;box-shadow:0 6px 18px rgba(15,23,42,.04)}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem}.pill{display:inline-block;border-radius:999px;background:#eef2ff;color:#3730a3;font-weight:900;padding:.25rem .6rem;margin-right:.3rem}.warn{background:#fff7ed;border-color:#fed7aa}.good{background:#f0fdf4;border-color:#bbf7d0}.bad{background:#fef2f2;border-color:#fecaca}
@media(max-width:900px){.grid3{grid-template-columns:1fr}}
</style>
""", unsafe_allow_html=True)


def get_secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return default


def db_ready() -> bool:
    return bool(get_secret("SUPABASE_URL") and get_secret("SUPABASE_ANON_KEY"))


def client():
    from supabase import create_client
    return create_client(get_secret("SUPABASE_URL"), get_secret("SUPABASE_ANON_KEY"))


def read_table(name: str, limit: int = 500) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready():
        return False, "Supabase 未配置", pd.DataFrame()
    try:
        res = client().table(name).select("*").limit(limit).execute()
        rows = res.data or []
        return True, f"读取 {name}：{len(rows)} 条", pd.DataFrame(rows)
    except Exception as exc:
        return False, f"读取 {name} 失败：{exc}", pd.DataFrame()


def read_instances(status: str | None = None) -> tuple[bool, str, pd.DataFrame]:
    if not db_ready():
        return False, "Supabase 未配置", pd.DataFrame()
    try:
        query = client().table("task_instances").select("*").order("updated_at", desc=True).limit(500)
        if status:
            query = query.eq("status", status)
        res = query.execute()
        rows = res.data or []
        return True, f"读取 task_instances：{len(rows)} 条", pd.DataFrame(rows)
    except Exception as exc:
        return False, f"读取 task_instances 失败：{exc}", pd.DataFrame()


def update_instance(instance_id: str, updates: dict[str, Any]) -> tuple[bool, str]:
    try:
        payload = dict(updates)
        payload["updated_at"] = datetime.now().isoformat()
        client().table("task_instances").update(payload).eq("instance_id", instance_id).execute()
        return True, "任务已更新"
    except Exception as exc:
        return False, f"更新失败：{exc}"


def insert_review(instance_id: str, reviewer: str, score: int, conclusion: str, text: str) -> tuple[bool, str]:
    try:
        review_id = f"rev_{instance_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"[:120]
        row = {
            "review_id": review_id,
            "instance_id": instance_id,
            "reviewer": reviewer,
            "score": int(score),
            "conclusion": conclusion,
            "review_text": text,
        }
        client().table("reviews").insert(row).execute()
        return True, "评价已写入"
    except Exception as exc:
        return False, f"写入评价失败：{exc}"


def agent_score(row: pd.Series) -> dict[str, Any]:
    draft = str(row.get("draft", "") or "").strip()
    score = 0
    if draft:
        score += 20
    score += min(40, len(draft) // 10)
    for token in ["目标", "步骤", "问题", "方案", "风险", "结论", "测试", "改进"]:
        if token in draft:
            score += 5
    score = max(0, min(100, score))
    if score >= 82:
        conclusion = "通过"
        status = "已入作品集"
        portfolio = True
    elif score >= 60:
        conclusion = "需要修改"
        status = "Agent已点评"
        portfolio = False
    else:
        conclusion = "需重训"
        status = "需重训"
        portfolio = False
    text = f"""【Agent 自动点评】
自动评分：{score}/100
结论：{conclusion}

优点：已提交第一版，可继续迭代。
主要问题：结构、证据、标准对应关系需要继续增强。
下一步：按“目标 → 步骤 → 输出物 → 检查标准 → 风险/遗漏”重新整理。

说明：本点评由 Agent 自动生成，用于一人公司规模化交付。"""
    return {"score": score, "conclusion": conclusion, "status": status, "portfolio": portfolio, "text": text}


def quality_check(row: pd.Series) -> dict[str, Any]:
    score = int(row.get("score", 0) or 0)
    review = str(row.get("teacher_review", "") or "")
    draft = str(row.get("draft", "") or "")
    flags: list[str] = []
    if score < 60:
        flags.append("低分任务")
    if len(draft.strip()) < 80:
        flags.append("草稿过短")
    if len(review.strip()) < 100:
        flags.append("点评过短")
    passed = not flags
    text = "【Agent 质检】\n" + ("质检通过。" if passed else "需要重训：" + "、".join(flags))
    return {"passed": passed, "score": max(0, score - len(flags) * 10), "text": text}


def metric_row(df: pd.DataFrame) -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("任务总数", len(df))
    c2.metric("待Agent点评", int((df.get("status") == "待Agent点评").sum()) if not df.empty and "status" in df else 0)
    c3.metric("需重训", int((df.get("status") == "需重训").sum()) if not df.empty and "status" in df else 0)
    c4.metric("作品集", int(df.get("portfolio", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not df.empty else 0)


def run_agent_review_batch(df: pd.DataFrame) -> tuple[int, list[str]]:
    count = 0
    messages: list[str] = []
    for _, row in df.iterrows():
        instance_id = str(row.get("instance_id"))
        result = agent_score(row)
        ok1, msg1 = insert_review(instance_id, "Agent Review", int(result["score"]), str(result["conclusion"]), str(result["text"]))
        if not ok1:
            messages.append(msg1)
            continue
        ok2, msg2 = update_instance(instance_id, {
            "teacher_review": result["text"],
            "score": int(result["score"]),
            "status": result["status"],
            "portfolio": bool(result["portfolio"]),
            "risk": "Agent已处理",
        })
        if ok2:
            count += 1
        else:
            messages.append(msg2)
    return count, messages


def run_quality_batch(df: pd.DataFrame) -> tuple[int, list[str]]:
    count = 0
    messages: list[str] = []
    for _, row in df.iterrows():
        instance_id = str(row.get("instance_id"))
        result = quality_check(row)
        status = "Agent质检通过" if result["passed"] else "需重训"
        ok1, msg1 = insert_review(instance_id, "Agent Quality", int(result["score"]), status, str(result["text"]))
        if not ok1:
            messages.append(msg1)
            continue
        ok2, msg2 = update_instance(instance_id, {
            "teacher_review": str(row.get("teacher_review", "") or "") + "\n\n" + str(result["text"]),
            "score": int(result["score"]),
            "status": status,
            "risk": "质检完成",
        })
        if ok2:
            count += 1
        else:
            messages.append(msg2)
    return count, messages


st.markdown("""
<div class='hero'>
<h1>Founder <span>Agent Console</span></h1>
<p><b>一人公司控制台。</b>你只做方向、产品判断和异常处理；Agent 负责点评、质检、作品集建议和运营日报。</p>
<span class='pill'>Agent Review</span><span class='pill'>Agent Quality</span><span class='pill'>Founder Daily</span>
</div>
""", unsafe_allow_html=True)

if not db_ready():
    st.warning("请先配置 Streamlit Secrets：SUPABASE_URL / SUPABASE_ANON_KEY。")
    st.stop()

ok, msg, tasks = read_instances()
st.success(msg) if ok else st.error(msg)
if not ok:
    st.stop()

if tasks.empty:
    st.info("暂无任务实例。先回主应用创建学员和任务。")
    st.stop()

metric_row(tasks)

st.markdown("### 今日 Agent Command Center")
col1, col2, col3 = st.columns(3)

pending_review = tasks[tasks["status"].isin(["待Agent点评", "AI已反馈", "已提交"])] if "status" in tasks.columns else pd.DataFrame()
pending_quality = tasks[tasks["status"].isin(["Agent已点评", "已入作品集"])] if "status" in tasks.columns else pd.DataFrame()
stalled = tasks[tasks["status"].isin(["未开始", "进行中", "需重训"])] if "status" in tasks.columns else pd.DataFrame()

with col1:
    st.markdown("<div class='card good'><b>运行今日 Agent 点评</b><p>处理已提交、已反馈、待点评任务。</p></div>", unsafe_allow_html=True)
    st.metric("待点评", len(pending_review))
    if st.button("一键运行 Agent 点评", type="primary"):
        count, errors = run_agent_review_batch(pending_review)
        st.success(f"Agent 点评完成：{count} 条")
        for e in errors[:5]:
            st.error(e)
        st.rerun()

with col2:
    st.markdown("<div class='card soft'><b>运行今日 Agent 质检</b><p>复核已点评任务，判断通过或重训。</p></div>", unsafe_allow_html=True)
    st.metric("待质检", len(pending_quality))
    if st.button("一键运行 Agent 质检"):
        count, errors = run_quality_batch(pending_quality)
        st.success(f"Agent 质检完成：{count} 条")
        for e in errors[:5]:
            st.error(e)
        st.rerun()

with col3:
    st.markdown("<div class='card warn'><b>生成今日运营日报</b><p>给你一个 Founder 视角的处理清单。</p></div>", unsafe_allow_html=True)
    st.metric("需关注", len(stalled))
    if st.button("生成日报"):
        report = f"""【Founder Daily】
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
任务总数：{len(tasks)}
待Agent点评：{len(pending_review)}
待Agent质检：{len(pending_quality)}
需关注/重训：{len(stalled)}

今日建议：
1. 先运行 Agent 点评。
2. 再运行 Agent 质检。
3. 查看需重训任务，优化任务模板或提示词。
4. 把高分作品整理成案例和销售素材。
"""
        st.text_area("运营日报", value=report, height=260)

st.markdown("### 待 Agent 点评")
st.dataframe(pending_review, use_container_width=True, hide_index=True)

st.markdown("### 待 Agent 质检")
st.dataframe(pending_quality, use_container_width=True, hide_index=True)

st.markdown("### 全部任务")
st.dataframe(tasks, use_container_width=True, hide_index=True)
