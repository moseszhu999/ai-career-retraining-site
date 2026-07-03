# v6.7 Dual MVP Prototype Spec：双 MVP 原型规格

## 1. 本版目标

v6.6 建议不立即押一个方向，而是先并行验证两个最有代表性的方向：

```text
A. AI Data Analysis Assistant Certificate
B. Cross-border Trade Documentation & Compliance Assistant Certificate
```

本文件把两个方向推进到原型规格层，但仍然不写代码。

本阶段只定义：

```text
页面清单
用户旅程
数据对象
样题结构
项目任务材料包
Agent 自动评分字段
证书字段
Verifier 字段
Proof Credential 字段
风险边界
验收标准
```

---

## 2. 为什么是双 MVP

两个方向分别代表两种市场逻辑。

| 方向 | 市场逻辑 | 验证重点 |
| --- | --- | --- |
| AI Data Analysis Assistant | 市场宽、冷启动快、题库容易做 | C 端 / 成人转型 / 企业员工培训 |
| Cross-border Trade Documentation | 证据链强、Verifier 清晰、crypto proof 价值高 | 供应链 / 单证 / 合规 / 可信证明 |

双 MVP 的目的不是同时开发两个完整产品，而是用同一底层证书平台验证两个不同垂直方向。

---

## 3. 共用平台骨架

两个 MVP 共用同一套底层结构。

```text
Learner
-> Capability Path
-> Practice Questions
-> Exam Questions
-> Project Task
-> Agent Score
-> Evidence Package
-> Certificate
-> Proof Credential
-> Chain Proof Record
-> Verifier Portal
```

共用核心对象：

```text
LearnerProfile
CapabilityNode
QuestionItem
PracticeSet
ExamPaper
ProjectTask
PracticeAttempt
ExamSession
ExamAttempt
ProjectSubmission
AgentScore
ScoreBreakdown
EvidencePackage
Certificate
ProofCredential
ProofChainRecord
VerificationEvent
```

---

# Part A：AI Data Analysis Assistant Certificate

## 4. A 方向定位

证书名称：

```text
AI Data Analysis Assistant Certificate
```

中文：

```text
AI 数据分析助理能力证书
```

一句话：

```text
证明学习者能使用 AI 辅助理解表格数据、发现异常、生成业务洞察，并形成可验证的数据分析证据包。
```

## 5. A 用户旅程

```text
注册 / 登录
-> 选择 AI Data Analysis Assistant 路径
-> 完成能力自评
-> 完成练习题
-> 完成考试题
-> 完成 Sales Performance Mini BI Report 项目任务
-> Agent 自动评分
-> 生成 Evidence Package
-> 达标后生成 Certificate
-> 绑定 Wallet / DID 领取 Proof Credential
-> 分享给 Verifier
```

## 6. A 页面清单

### 6.1 Learner 页面

```text
A1 Data Certificate Landing
A2 Learner Profile
A3 Data Capability Self-assessment
A4 Data Learning Path
A5 Practice Set: Data Literacy
A6 Practice Set: Spreadsheet Reasoning
A7 Practice Set: AI-assisted Analysis
A8 Exam Paper
A9 Project Task: Sales Performance Mini BI Report
A10 Submission Result
A11 Certificate Detail
A12 Claim Proof Credential
A13 Share Proof Link
```

### 6.2 Verifier 页面

```text
A14 Verify Credential
A15 Capability Summary
A16 Project Evidence Summary
A17 Verification Event Receipt
```

### 6.3 Admin / Founder 页面

```text
A18 Data Question Bank
A19 Data Exam Builder
A20 Data Project Task Builder
A21 Data Scoring Rule
A22 Data Certificate Rule
A23 Proof Registry Monitor
```

## 7. A 能力模块

| 模块 | 名称 | 说明 |
| --- | --- | --- |
| DA1 | Data Literacy | 字段、指标、口径、缺失值、异常值 |
| DA2 | Spreadsheet Reasoning | 排序、筛选、分组、汇总、简单公式 |
| DA3 | AI-assisted Analysis | 用 AI 生成分析问题、解释结果、提出假设 |
| DA4 | Chart & Insight Communication | 图表选择、业务摘要、洞察表达 |
| DA5 | Data Quality & Risk | 数据质量、隐私、误导性结论、过度推断 |

## 8. A 样题 10 道

### A-Q1 单选题：字段识别

```text
题目：销售表中包含 order_date, region, product, revenue, customer_count。哪个字段最适合用于按地区比较销售表现？
A. order_date
B. region
C. product
D. customer_count
答案：B
能力点：DA1
```

### A-Q2 单选题：增长率

```text
题目：上月销售额 10000，本月销售额 12000。增长率是多少？
A. 10%
B. 20%
C. 120%
D. 2000%
答案：B
能力点：DA2
```

### A-Q3 多选题：异常值识别

```text
题目：以下哪些情况可能是数据异常？
A. 某地区销售额为负数
B. 某天 customer_count 为空
C. 某产品名称拼写出现两个版本
D. 所有月份销售额完全相同
答案：A, B, C, D
能力点：DA5
```

### A-Q4 单选题：图表选择

```text
题目：如果要展示 12 个月销售额变化趋势，最合适的图表是？
A. 饼图
B. 折线图
C. 地图
D. 组织架构图
答案：B
能力点：DA4
```

### A-Q5 判断题：AI 结论风险

```text
题目：AI 根据 3 天数据判断“全年销售趋势将持续上升”，这个结论可靠。
答案：False
能力点：DA5
```

### A-Q6 短答案题：分析问题生成

```text
题目：给定销售表字段 region, channel, revenue, ad_spend，请提出 3 个有业务价值的分析问题。
评分：Rubric + AgentScore
能力点：DA3
```

### A-Q7 多选题：隐私风险

```text
题目：以下哪些字段不应直接上传到外部 AI 工具？
A. customer_email
B. passport_number
C. anonymized_region
D. credit_card_number
答案：A, B, D
能力点：DA5
```

### A-Q8 排序题：分析流程

```text
题目：将数据分析步骤排序。
选项：理解业务问题、检查数据质量、计算指标、解释结果、提出建议
正确顺序：理解业务问题 -> 检查数据质量 -> 计算指标 -> 解释结果 -> 提出建议
能力点：DA1, DA3
```

### A-Q9 情景题：AI 摘要校验

```text
题目：AI 输出“北区表现最好”，但表格中南区 revenue 最高。学习者应如何处理？
答案要点：回查原始数据、指出 AI 错误、修正结论、说明校验依据。
评分：Rubric + AgentScore
能力点：DA4, DA5
```

### A-Q10 结构化输出题：业务摘要

```text
题目：根据给定小表格，写出 3 条业务发现和 1 条风险提醒。
评分：完整性、准确性、清晰度、风险意识。
能力点：DA3, DA4, DA5
```

## 9. A 项目任务材料包

项目名称：

```text
Sales Performance Mini BI Report
```

材料包：

```text
sales_sample.csv
business_goal.txt
data_dictionary.md
privacy_notice.md
```

### 9.1 sales_sample.csv 字段

```text
order_date
region
channel
product_category
revenue
customer_count
refund_count
ad_spend
```

### 9.2 business_goal.txt

```text
公司希望了解最近 12 个月不同地区和渠道的销售表现，找出增长机会、异常风险和广告投入效率问题。
```

### 9.3 学习者提交物

```text
metric_definition.md
insight_summary.md
anomaly_notes.md
chart_recommendation.md
business_recommendation.md
data_risk_note.md
```

## 10. A Agent 自动评分字段

```text
data_field_understanding_score
metric_calculation_score
anomaly_detection_score
insight_quality_score
chart_recommendation_score
privacy_risk_score
final_project_score
confidence
rationale_hash
risk_flags
```

## 11. A 证书字段

```text
certificate_id
credential_type = AI_DATA_ANALYSIS_ASSISTANT
learner_id
issued_at
expires_at
overall_score
module_scores
project_task_id
project_score
evidence_package_id
proof_credential_id
status
```

## 12. A Verifier 字段

默认展示：

```text
certificate_status
overall_score_band
module_score_summary
project_summary
issued_at
expires_at
issuer
proof_status
```

学习者授权后展示：

```text
insight_summary_preview
anomaly_notes_preview
chart_recommendation_preview
data_risk_note_preview
```

---

# Part B：Cross-border Trade Documentation & Compliance Assistant Certificate

## 13. B 方向定位

证书名称：

```text
AI Cross-border Trade Documentation & Compliance Assistant Certificate
```

中文：

```text
AI 跨境贸易单证与供应链合规助理证书
```

一句话：

```text
证明学习者能使用 AI 辅助预审跨境贸易单证、识别单据差异、整理供应链证据，并生成可验证 Evidence Package。
```

## 14. B 用户旅程

```text
注册 / 登录
-> 选择 Cross-border Trade Documentation 路径
-> 完成贸易单证能力自评
-> 完成练习题
-> 完成考试题
-> 完成 Trade Document Consistency Review 项目任务
-> Agent 自动评分
-> 生成 Evidence Package
-> 达标后生成 Certificate
-> 绑定 Wallet / DID 领取 Proof Credential
-> 分享给 Verifier
```

## 15. B 页面清单

### 15.1 Learner 页面

```text
B1 Trade Certificate Landing
B2 Learner Profile
B3 Trade Capability Self-assessment
B4 Trade Learning Path
B5 Practice Set: Trade Document Literacy
B6 Practice Set: Consistency Check
B7 Practice Set: Compliance Awareness
B8 Exam Paper
B9 Project Task: Trade Document Consistency Review
B10 Submission Result
B11 Certificate Detail
B12 Claim Proof Credential
B13 Share Proof Link
```

### 15.2 Verifier 页面

```text
B14 Verify Credential
B15 Trade Capability Summary
B16 Trade Evidence Summary
B17 Verification Event Receipt
```

### 15.3 Admin / Founder 页面

```text
B18 Trade Question Bank
B19 Trade Exam Builder
B20 Trade Project Task Builder
B21 Trade Scoring Rule
B22 Trade Certificate Rule
B23 Proof Registry Monitor
```

## 16. B 能力模块

| 模块 | 名称 | 说明 |
| --- | --- | --- |
| TR1 | Trade Document Literacy | 发票、装箱单、提单、合同、PO、CO 等单证理解 |
| TR2 | Document Consistency Check | 金额、数量、货描、日期、主体、币种一致性检查 |
| TR3 | Compliance Awareness | 制裁、HS code、原产地、许可证、贸易条款基础意识 |
| TR4 | Supply Chain Evidence | 供应商文件、质检、交付、物流、收款证据整理 |
| TR5 | AI-assisted Document Review | 用 AI 辅助预审单证并生成风险清单 |

## 17. B 样题 10 道

### B-Q1 单选题：单证识别

```text
题目：Commercial Invoice 的主要作用是什么？
A. 记录商品价格、买卖双方和交易金额
B. 证明货物已经装船
C. 证明员工培训完成
D. 记录仓库温度
答案：A
能力点：TR1
```

### B-Q2 单选题：装箱单

```text
题目：Packing List 通常最关注哪些信息？
A. 付款银行利率
B. 包装、数量、重量、箱数
C. 员工工资
D. 网站访问量
答案：B
能力点：TR1
```

### B-Q3 多选题：一致性检查

```text
题目：以下哪些字段应在 PO、Invoice、Packing List 中重点核对？
A. 商品描述
B. 数量
C. 币种和金额
D. 随机天气
答案：A, B, C
能力点：TR2
```

### B-Q4 判断题：HS code

```text
题目：AI 给出的 HS code 可以直接作为最终申报结论，无需人工确认。
答案：False
能力点：TR3
```

### B-Q5 单选题：原产地证

```text
题目：Certificate of Origin 主要用于说明什么？
A. 货物原产地
B. 员工学历
C. 仓库租金
D. 客户满意度
答案：A
能力点：TR3
```

### B-Q6 情景题：数量差异

```text
题目：PO 数量为 1000，Invoice 数量为 1000，Packing List 数量为 980。学习者应如何处理？
答案要点：标记差异、说明影响、要求人工确认、进入风险清单。
评分：Rubric + AgentScore
能力点：TR2, TR5
```

### B-Q7 多选题：Evidence Package

```text
题目：哪些文件适合进入贸易 Evidence Package？
A. PO
B. Commercial Invoice
C. Packing List
D. Bill of Lading summary
E. Inspection Note
答案：A, B, C, D, E
能力点：TR4
```

### B-Q8 判断题：AI 审单边界

```text
题目：AI 审单结果可以替代银行、海关、律师或专业审单人员的最终判断。
答案：False
能力点：TR3, TR5
```

### B-Q9 结构化输出题：差异清单

```text
题目：根据给定 PO 和 Invoice 摘要，输出字段差异清单。
评分：字段覆盖、差异准确性、格式清晰度。
能力点：TR2
```

### B-Q10 情景题：人工确认问题

```text
题目：发现货描、数量和交货日期三处不一致时，生成 3 个需要人工确认的问题。
评分：问题清晰度、风险覆盖、人工确认边界。
能力点：TR5
```

## 18. B 项目任务材料包

项目名称：

```text
Trade Document Consistency Review
```

材料包：

```text
purchase_order.md
commercial_invoice.md
packing_list.md
bill_of_lading_summary.md
supplier_certificate.md
inspection_note.md
review_policy.md
```

### 18.1 学习者提交物

```text
trade_document_summary.md
five_document_match_table.md
discrepancy_list.md
missing_document_list.md
manual_review_questions.md
evidence_package_summary.md
```

## 19. B Agent 自动评分字段

```text
field_extraction_score
consistency_check_score
discrepancy_detection_score
compliance_awareness_score
manual_review_boundary_score
evidence_package_completeness_score
final_project_score
confidence
rationale_hash
risk_flags
```

## 20. B 证书字段

```text
certificate_id
credential_type = AI_TRADE_DOCUMENTATION_COMPLIANCE_ASSISTANT
learner_id
issued_at
expires_at
overall_score
module_scores
project_task_id
project_score
evidence_package_id
proof_credential_id
status
```

## 21. B Verifier 字段

默认展示：

```text
certificate_status
overall_score_band
module_score_summary
project_summary
issued_at
expires_at
issuer
proof_status
```

学习者授权后展示：

```text
trade_document_summary_preview
five_document_match_table_preview
discrepancy_list_preview
manual_review_questions_preview
evidence_package_summary_preview
```

---

## 22. 共用 Proof Credential 字段

两个 MVP 共用 ProofCredential schema：

```text
proof_credential_id
credential_type
issuer_did
holder_did
subject_id_hash
certificate_id
claims_hash
evidence_package_hash
issued_at
expires_at
status
revocation_status
proof_chain_record_id
schema_version
```

链上只登记：

```text
proof_hash
issuer
issued_at
status
revocation_status
schema_version
```

不上链：

```text
原始数据
原始贸易文件
个人身份信息
企业敏感文件
完整作答内容
```

---

## 23. 共用证书达标规则

建议第一版：

```text
Practice completion >= 80%
Exam score >= 70%
Project score >= 70%
Critical risk flag = false
Evidence Package generated = true
```

未通过时：

```text
生成补练建议
允许重新练习
允许重新考试
不生成公开证书
保留内部 attempt record
```

---

## 24. 双 MVP 横向验证指标

| 指标 | AI Data | Cross-border Trade |
| --- | --- | --- |
| Landing Page 是否容易解释 | 待验证 | 待验证 |
| 10 道样题是否容易做 | 待验证 | 待验证 |
| 项目任务是否能自动评分 | 待验证 | 待验证 |
| Verifier 是否看得懂 | 待验证 | 待验证 |
| 用户是否愿意付费 | 待验证 | 待验证 |
| Crypto Proof 是否有感知价值 | 待验证 | 待验证 |
| 是否适合一人公司冷启动 | 待验证 | 待验证 |

---

## 25. 原型前门禁

进入原型页面设计之前，需要完成：

```text
1. 两个方向各自 10 道样题的最终题面。
2. 两个方向各自项目任务材料包的模拟数据。
3. AgentScore 字段和 rubric 版本。
4. Certificate schema 和 ProofCredential schema。
5. Verifier 默认视图和授权后视图。
6. Landing Page 文案。
7. 不做事项和风险边界。
```

---

## 26. 当前结论

当前最稳妥的推进方式：

```text
不是先写代码。
不是马上选唯一方向。
而是把 AI Data 和 Cross-border Trade 两个方向同时推进到可展示的静态原型规格。
```

如果只能先做一个静态原型：

```text
优先 AI Data，因为冷启动最快。
```

如果要体现平台最大差异化：

```text
优先 Cross-border Trade，因为它最能体现 Evidence Package + Proof Credential + Verifier + Chain Proof。
```
