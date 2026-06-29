from __future__ import annotations

import pandas as pd

CLIENTS = pd.DataFrame(
    [
        {
            "client_id": "jhc",
            "client_name": "信华信日本业务部",
            "contact": "人材育成担当",
            "service_package": "Java新人研修 Proof Sprint",
            "contract_value": 78000,
            "currency": "CNY",
            "status": "进行中",
        },
        {
            "client_id": "bitkids",
            "client_name": "比特顽童教育",
            "contact": "校区负责人",
            "service_package": "少儿编程讲师训练包",
            "contract_value": 24000,
            "currency": "CNY",
            "status": "待跟进",
        },
    ]
)

COHORTS = pd.DataFrame(
    [
        {
            "cohort_id": "jhc-2026-java",
            "client_id": "jhc",
            "cohort_name": "2026 JHC Java新人训练营",
            "learner_count": 13,
            "start_date": "2026-06-01",
            "end_date": "2026-08-31",
            "trainer": "Zhu Moses",
            "status": "Week 4 进行中",
        },
        {
            "cohort_id": "bitkids-mentor-01",
            "client_id": "bitkids",
            "cohort_name": "讲师交付能力训练 Demo",
            "learner_count": 6,
            "start_date": "2026-07-08",
            "end_date": "2026-07-12",
            "trainer": "Zhu Moses",
            "status": "售前样板",
        },
    ]
)

LEARNERS = pd.DataFrame(
    [
        ["jhc-s01", "佐藤拓海", "jhc-2026-java", "学员", "A组", "进行中", 72, 3, 1],
        ["jhc-s02", "鈴木美咲", "jhc-2026-java", "学员", "A组", "待Review", 81, 4, 2],
        ["jhc-s03", "田中悠真", "jhc-2026-java", "学员", "B组", "需修改", 58, 2, 1],
        ["jhc-s04", "高橋葵", "jhc-2026-java", "学员", "B组", "进行中", 66, 3, 1],
        ["jhc-s05", "伊藤蓮", "jhc-2026-java", "学员", "C组", "待Review", 76, 4, 2],
        ["jhc-s06", "山本結衣", "jhc-2026-java", "学员", "C组", "已确认", 88, 5, 3],
    ],
    columns=["learner_id", "learner_name", "cohort_id", "role", "group", "status", "progress", "tasks_done", "proof_files"],
)

TASK_INSTANCES = pd.DataFrame(
    [
        {
            "task_id": "task-login-test-s01",
            "learner_id": "jhc-s01",
            "learner_name": "佐藤拓海",
            "cohort_id": "jhc-2026-java",
            "day": "Day 2",
            "proof_task": "登录功能测试用例",
            "business_context": "Spring Boot + Thymeleaf 登录画面测试",
            "required_output": "测试用例表 + Bug报告样例",
            "status": "进行中",
            "progress": 70,
            "draft": "已覆盖正常登录、错误密码、空用户名。待补充权限差异、安全输入、边界值。",
            "agent_review": "建议补充：1. 管理员/普通用户权限差异；2. 恶意输入；3. 超长用户名；4. Bug严重度。",
            "founder_decision": "未处理",
            "proof_score": 64,
        },
        {
            "task_id": "task-order-flow-s02",
            "learner_id": "jhc-s02",
            "learner_name": "鈴木美咲",
            "cohort_id": "jhc-2026-java",
            "day": "Day 3",
            "proof_task": "订单状态流转拆解",
            "business_context": "培训管理系统订单：未支付、已支付、退费、结转",
            "required_output": "业务流程图 + 异常分支说明",
            "status": "待Review",
            "progress": 85,
            "draft": "已完成主流程，包含未支付到已支付、退费、结转。异常分支待确认。",
            "agent_review": "结构较完整。建议补充：重复支付、退费后课耗回滚、跨校区结算影响。",
            "founder_decision": "待确认进入作品集",
            "proof_score": 81,
        },
        {
            "task_id": "task-qa-jp-s03",
            "learner_id": "jhc-s03",
            "learner_name": "田中悠真",
            "cohort_id": "jhc-2026-java",
            "day": "Day 4",
            "proof_task": "日语Q&A发表准备",
            "business_context": "结业发表会：对方公司领导提问",
            "required_output": "3分钟说明稿 + Q&A回答模板",
            "status": "需修改",
            "progress": 55,
            "draft": "准备了项目说明，但对无法回答的问题还没有自然的日语回复。",
            "agent_review": "建议加入：確認してから後ほど回答いたします、発表後のフォロー说明、被指名时的回答方式。",
            "founder_decision": "打回修改",
            "proof_score": 58,
        },
        {
            "task_id": "task-spring-error-s06",
            "learner_id": "jhc-s06",
            "learner_name": "山本結衣",
            "cohort_id": "jhc-2026-java",
            "day": "Day 5",
            "proof_task": "Spring Boot错误定位报告",
            "business_context": "Controller / Service / Mapper / MyBatis 调试",
            "required_output": "错误原因分析 + 修正前后截图 + 复盘",
            "status": "已确认",
            "progress": 100,
            "draft": "定位到 mapper XML 参数名不一致导致查询失败，已修复并补充测试。",
            "agent_review": "证据完整：错误日志、原因、修复、验证、复盘均具备。",
            "founder_decision": "确认进入作品集",
            "proof_score": 88,
        },
    ]
)

PROOF_FILES = pd.DataFrame(
    [
        ["proof-001", "山本結衣", "Spring Boot错误定位报告", "可展示", 88, "错误日志 + 修正截图 + 复盘", "适合结业发表和面试说明"],
        ["proof-002", "鈴木美咲", "订单状态流转拆解", "待Review", 81, "业务流程图 + 异常分支", "等待Founder确认"],
        ["proof-003", "佐藤拓海", "登录功能测试用例", "修改中", 64, "测试用例表 + Bug报告", "待补安全和边界"],
    ],
    columns=["proof_id", "learner_name", "title", "status", "score", "evidence", "note"],
)

CONSULT_LEADS = pd.DataFrame(
    [
        ["lead-001", "信华信日本业务部", "企业训练版", "Java新人训练标准包", "已预约", 78000, "希望把3个月讲师交付沉淀成可复用训练包"],
        ["lead-002", "比特顽童教育", "讲师训练版", "少儿编程讲师训练包", "新线索", 24000, "希望降低新讲师培养成本"],
    ],
    columns=["lead_id", "client_name", "package", "need", "status", "potential_value", "note"],
)

SERVICE_PACKAGES = pd.DataFrame(
    [
        ["pkg-java-newcomer", "Java新人研修 Proof Sprint", "企业新人", "5天任务样板 + 3个月扩展", 78000],
        ["pkg-testing", "软件测试 Proof Sprint", "转岗/新人", "测试用例、Bug报告、业务流程", 19800],
        ["pkg-trainer", "讲师交付能力产品化包", "培训讲师/小机构", "任务卡、点评标准、作品集模板", 36000],
    ],
    columns=["package_id", "package_name", "target", "deliverables", "price_cny"],
)


def get_business_metrics() -> dict[str, int]:
    return {
        "active_clients": int((CLIENTS["status"] == "进行中").sum()),
        "active_cohorts": int((COHORTS["status"].str.contains("进行中|售前", regex=True)).sum()),
        "learners": int(LEARNERS["learner_id"].nunique()),
        "pending_reviews": int((TASK_INSTANCES["status"] == "待Review").sum()),
        "proof_files": int(len(PROOF_FILES)),
        "lead_value": int(CONSULT_LEADS["potential_value"].sum()),
    }
