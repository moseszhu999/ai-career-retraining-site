# v6.8 Static Prototype Design：双 MVP 静态原型页面设计

## 1. 本版目标

v6.7 已经定义两个 MVP 的原型规格。本版继续推进到静态原型页面设计。

本阶段仍然不写代码，只定义未来静态原型页面应该如何组织。

两个原型方向：

```text
A. AI Data Analysis Assistant Certificate
B. Cross-border Trade Documentation & Compliance Assistant Certificate
```

共同产品闭环：

```text
Landing
-> Learner Onboarding
-> Capability Path
-> Practice
-> Exam
-> Project Task
-> Agent Score
-> Evidence Package
-> Certificate
-> Claim Proof
-> Verifier Portal
```

---

## 2. 原型设计原则

```text
不要做完整学习平台。
不要做真实考试系统。
不要做真实钱包和链交易。
不要做真实数据库。
不要写运行代码。

只做可展示、可讲解、可销售验证的静态原型设计。
```

静态原型必须让人一眼看懂：

```text
这个证书证明什么能力？
学习者需要完成什么任务？
Agent 如何评分？
证据包里有什么？
Verifier 能验证什么？
链上 proof 有什么价值？
```

---

## 3. 信息架构

### 3.1 顶部导航

```text
Home
Certificates
AI Data Analysis
Trade Documentation
Verifier Portal
Proof Registry
Founder View
```

### 3.2 首页结构

首页不展示所有复杂能力，只讲一个核心句子：

```text
Issue verifiable AI-era skill certificates backed by tasks, evidence packages, agent scoring, and crypto proof.
```

中文：

```text
用任务、证据包、Agent 评分和链上证明，签发可验证的 AI 时代能力证书。
```

首页模块：

```text
Hero
Two MVP cards
How it works
Learner path
Verifier value
Proof credential explanation
Founder demo route
```

---

## 4. 页面清单总览

| 页面编号 | 页面名称 | 目的 |
| --- | --- | --- |
| P0 | Home / Product Overview | 解释平台总价值 |
| P1 | Certificate Catalog | 展示两个 MVP 证书 |
| P2A | AI Data Landing | 介绍 AI Data Analysis 证书 |
| P2B | Trade Landing | 介绍 Trade Documentation 证书 |
| P3 | Learner Onboarding | 学习者选择证书并创建画像 |
| P4A | AI Data Path Dashboard | 展示数据分析路径进度 |
| P4B | Trade Path Dashboard | 展示贸易单证路径进度 |
| P5 | Practice Page | 展示练习题和即时反馈 |
| P6 | Exam Page | 展示考试题、分数和通过线 |
| P7A | AI Data Project Task | 展示数据分析项目任务 |
| P7B | Trade Project Task | 展示贸易单证项目任务 |
| P8 | Agent Score Report | 展示 Agent 自动评分结果 |
| P9 | Evidence Package | 展示证据包组成 |
| P10 | Certificate Detail | 展示证书详情 |
| P11 | Claim Proof Credential | 展示绑定钱包和领取 proof 的流程 |
| P12 | Verifier Portal | 验证方输入证书链接 / QR |
| P13 | Verifier Result | 展示验证结果和授权摘要 |
| P14 | Founder Dashboard | Founder 视角展示全流程 |
| P15 | Proof Registry Mock | 展示链上 proof registry mock |

---

# Part A：AI Data Analysis 静态原型

## 5. P2A AI Data Landing

页面目的：

```text
让学习者和企业理解这个证书证明什么。
```

主标题：

```text
AI Data Analysis Assistant Certificate
```

副标题：

```text
Prove you can turn messy business data into clear insights with AI, evidence, and verifiable proof.
```

页面模块：

```text
1. 证书证明的能力
2. 谁适合报名
3. 任务和考试怎么评估
4. 证书如何被雇主验证
5. 示例项目：Sales Performance Mini BI Report
6. CTA: Start assessment
```

关键展示字段：

```text
5 capability modules
40 exam questions
1 project task
Agent-scored
Evidence-backed
Verifier-ready
```

## 6. P4A AI Data Path Dashboard

页面目的：

```text
展示学习者完成证书路径的进度。
```

卡片：

```text
Data Literacy                         80% complete
Spreadsheet Reasoning                 60% complete
AI-assisted Analysis                   40% complete
Chart & Insight Communication          20% complete
Data Quality & Risk                    40% complete
```

右侧状态：

```text
Practice completion: 72%
Exam readiness: Not ready
Project task: Locked
Certificate status: Not eligible
```

按钮：

```text
Continue Practice
Preview Exam
View Certificate Requirements
```

## 7. P7A AI Data Project Task

页面目的：

```text
展示项目任务材料和提交要求。
```

任务名称：

```text
Sales Performance Mini BI Report
```

左侧材料：

```text
sales_sample.csv
business_goal.txt
data_dictionary.md
privacy_notice.md
```

中间任务说明：

```text
You are asked to analyze 12 months of sales data and prepare a short business insight report.
```

提交清单：

```text
metric_definition.md
insight_summary.md
anomaly_notes.md
chart_recommendation.md
business_recommendation.md
data_risk_note.md
```

右侧评分 rubrics：

```text
Metric accuracy             20%
Anomaly detection           20%
Insight quality             20%
Chart recommendation        15%
Data risk awareness         15%
Communication clarity       10%
```

---

# Part B：Cross-border Trade 静态原型

## 8. P2B Trade Landing

页面目的：

```text
让外贸、物流、供应链、贸易金融相关用户理解证书价值。
```

主标题：

```text
AI Cross-border Trade Documentation & Compliance Assistant Certificate
```

副标题：

```text
Prove you can review trade documents, detect discrepancies, and prepare evidence packages with AI-assisted checks.
```

页面模块：

```text
1. 证书证明的能力
2. 适合谁：外贸助理、跨境电商、供应链、物流、贸易融资材料助理
3. 任务和单证材料
4. Agent 如何检查单证差异
5. Verifier 如何验证证书和项目证据
6. CTA: Start trade document assessment
```

关键展示字段：

```text
PO / Invoice / Packing List / BL matching
Document consistency check
Compliance awareness
Evidence package
Proof-ready certificate
```

## 9. P4B Trade Path Dashboard

页面目的：

```text
展示贸易单证证书路径进度。
```

卡片：

```text
Trade Document Literacy          80% complete
Document Consistency Check        50% complete
Compliance Awareness              40% complete
Supply Chain Evidence             30% complete
AI-assisted Document Review        20% complete
```

右侧状态：

```text
Practice completion: 68%
Exam readiness: Not ready
Project task: Locked
Certificate status: Not eligible
```

按钮：

```text
Continue Practice
Preview Exam
View Trade Project Task
```

## 10. P7B Trade Project Task

页面目的：

```text
展示贸易文件项目任务。
```

任务名称：

```text
Trade Document Consistency Review
```

左侧材料：

```text
purchase_order.md
commercial_invoice.md
packing_list.md
bill_of_lading_summary.md
supplier_certificate.md
inspection_note.md
review_policy.md
```

中间任务说明：

```text
You are asked to review a simulated cross-border trade document set, identify discrepancies, and prepare an evidence package summary.
```

提交清单：

```text
trade_document_summary.md
five_document_match_table.md
discrepancy_list.md
missing_document_list.md
manual_review_questions.md
evidence_package_summary.md
```

右侧评分 rubrics：

```text
Field extraction accuracy           20%
Consistency check coverage          25%
Discrepancy detection               25%
Compliance boundary awareness       15%
Evidence package completeness       15%
```

---

# 共用页面设计

## 11. P5 Practice Page

页面目的：

```text
展示练习题、即时反馈和补练建议。
```

页面区域：

```text
Question stem
Options / answer input
Submit answer
Instant feedback
Capability tag
Explanation
Next recommended question
```

字段：

```text
question_id
capability_id
question_type
answer
is_correct
score
feedback
recommended_next_action
```

## 12. P6 Exam Page

页面目的：

```text
展示考试流程和达标规则。
```

顶部状态：

```text
Exam: AI Data Analysis Assistant Exam
Questions: 40
Time limit: 75 min
Pass score: 70%
Attempts allowed: 2
```

考试结束展示：

```text
Overall score
Module score breakdown
Passed / Not passed
Project task unlocked / locked
Retry recommendation
```

## 13. P8 Agent Score Report

页面目的：

```text
让用户看到 Agent 如何评分，而不是黑盒打分。
```

展示模块：

```text
Overall score
Capability score breakdown
Rubric evaluation
Risk flags
Confidence
Evidence coverage
Recommended improvement
```

字段：

```text
agent_score_id
model_version
rubric_version
overall_score
confidence
rationale_hash
risk_flags
score_breakdown
```

## 14. P9 Evidence Package

页面目的：

```text
展示证书背后的证据，而不是只展示一个分数。
```

展示结构：

```text
Evidence Package ID
Learner
Credential Type
Exam Session
Project Submission
Agent Score
Files / outputs hash
Risk flags
Certificate readiness
```

状态：

```text
Complete
Incomplete
Needs retry
Critical risk detected
Ready for certificate
```

## 15. P10 Certificate Detail

页面目的：

```text
展示平台证书内容。
```

字段：

```text
certificate_id
certificate_name
issuer
learner_name / holder alias
issued_at
expires_at
overall_score_band
module_summary
project_task_summary
evidence_package_id
proof_status
revocation_status
```

按钮：

```text
Claim Proof Credential
Share with Verifier
Download Certificate PDF mock
View Evidence Package
```

## 16. P11 Claim Proof Credential

页面目的：

```text
展示普通用户如何从平台证书升级为 crypto native Proof Credential。
```

流程：

```text
Step 1: Review certificate
Step 2: Connect wallet / DID
Step 3: Generate claims hash
Step 4: Register proof hash
Step 5: Proof Credential ready
```

静态状态：

```text
Wallet: not connected / connected
Proof hash: generated
Chain registry: pending / registered
Verifier link: ready
```

说明文案：

```text
Only the proof hash and status are registered. Your raw answers, project files, and personal information are not stored on-chain.
```

## 17. P12 Verifier Portal

页面目的：

```text
给用人单位、客户方、企业、学校或项目方验证证书。
```

输入区：

```text
Paste proof link
Enter certificate ID
Scan QR code mock
```

验证按钮：

```text
Verify Credential
```

说明：

```text
Verifier can confirm certificate status, issuer, validity, revocation status, and authorized capability summary.
```

## 18. P13 Verifier Result

页面目的：

```text
展示验证结果。
```

默认展示：

```text
Credential valid / invalid
Issuer
Issued date
Expiration date
Revocation status
Credential type
Capability summary
Overall score band
Project task summary
Proof registry status
```

授权后展示：

```text
Evidence summary preview
Selected project outputs
Agent score summary
Verification receipt
```

禁止展示：

```text
完整原始考试答案
完整项目文件
个人敏感身份信息
未授权数据
```

## 19. P14 Founder Dashboard

页面目的：

```text
Founder 用于演示完整产品闭环。
```

指标卡：

```text
Certificates: 2 active MVPs
Questions: 20 sample questions
Project tasks: 2
Proof credentials: mock-ready
Verifier flow: ready
Code changes: none
```

演示路线：

```text
Route A: Data Analysis MVP
Route B: Trade Documentation MVP
Route C: Verifier Proof Demo
Route D: Founder Architecture Demo
```

## 20. P15 Proof Registry Mock

页面目的：

```text
用静态方式解释链上 proof registry 的价值。
```

表格字段：

```text
proof_hash
credential_type
issuer
issued_at
status
revocation_status
schema_version
```

示例状态：

```text
registered
revoked
expired
pending
```

---

## 21. 静态原型数据集

### 21.1 mock learners

```text
learner_001: Data certificate candidate
learner_002: Trade certificate candidate
```

### 21.2 mock verifier

```text
verifier_001: HR manager
verifier_002: Trade finance analyst
verifier_003: SMB owner
```

### 21.3 mock certificates

```text
cert_data_001: AI Data Analysis Assistant Certificate
cert_trade_001: AI Cross-border Trade Documentation & Compliance Assistant Certificate
```

### 21.4 mock proof records

```text
proof_data_001: registered
proof_trade_001: registered
```

---

## 22. 静态原型不做事项

```text
不接真实钱包。
不发真实链交易。
不保存真实用户数据。
不上传真实贸易文件。
不运行真实考试。
不调用真实 Agent。
不做真实自动评分。
不提供法律、贸易合规、金融、税务或投资意见。
```

---

## 23. 原型验收标准

```text
能讲清 Learner -> Evidence -> Certificate -> Proof -> Verifier 全流程。
两个 MVP 都有独立 landing、path、project task 和 verifier result。
所有证书都能追溯到 Evidence Package。
所有 ProofCredential 都只展示 hash / status / issuer / revocation。
Verifier 默认只看到最小披露信息。
授权后才看到 Evidence Summary。
Founder Dashboard 能支持 3-5 分钟演示。
静态原型不触碰真实代码、真实钱包、真实链和真实数据库。
```

---

## 24. 下一步

v6.9 建议进入：

```text
Static Prototype Content Pack
```

即为每个页面准备可直接放进 HTML / Streamlit 原型的具体文案和 mock 数据。

包括：

```text
Hero 文案
按钮文案
页面标题
mock learner 数据
mock question 数据
mock project task 数据
mock certificate 数据
mock verifier result 数据
mock proof registry 数据
```

v6.9 完成后，再决定是否进入真正静态原型实现。
