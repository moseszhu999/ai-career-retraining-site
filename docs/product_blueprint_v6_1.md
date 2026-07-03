# v6.1 Product Blueprint：AI 能力证明 MVP

## 1. 本版决策

本版本根据当前讨论，先固定第一版 MVP 的产品选择。

```text
MVP 市场：海外成年人能力证明 + Verifier Portal
证书签发：平台先签发，未来支持企业 / 训练营 / 学校联合签发
登录方式：先邮箱登录，领取 Proof Credential 时再绑定 Wallet / DID
第一张证书：AI Office Productivity Certificate
评分方式：第一版默认全自动评分
Verifier 展示：默认验证证书真伪 + 能力摘要；学习者授权后可展示作品摘要或 Evidence Package 摘要
```

## 2. 一句话定位

```text
面向 AI 时代成年人能力提升的 crypto native + agent native 可信证书平台。
```

第一版不做泛教育平台，而是先验证一个最清晰闭环：

```text
学习者完成 AI 办公能力训练和考试
-> Agent 自动评分
-> 平台自动生成证书
-> 用户绑定钱包领取 Proof Credential
-> 用人单位 / HR / 客户通过 Verifier Portal 验证
```

## 3. 双边用户模型

| 侧 | 用户 | 核心价值 |
| --- | --- | --- |
| Learner Side | 海外成年人、职场人、跳槽者、自由职业者 | 提升 AI 办公能力，并获得可验证能力证书 |
| Verifier Side | 用人单位、HR、项目方、客户方 | 快速验证候选人的证书真伪、能力范围和授权摘要 |

## 4. 第一张证书

```text
AI Office Productivity Certificate
```

证明学习者具备基础 AI 办公生产力能力。

能力范围：

```text
AI 文档处理
AI 邮件写作
AI 会议纪要整理
AI 报告摘要
AI 信息检索与判断
AI 表格 / 数据初步分析
AI 演示文稿大纲生成
AI 工作流基本安全意识
```

证书不证明：

```text
国家职业资格
学历
保证就业
保证晋升
保证薪资
监管行业资质
```

## 5. MVP 用户旅程

### 5.1 Learner Journey

```text
注册邮箱账号
-> 完成能力自评
-> 进入 AI Office Productivity 路径
-> 完成练习题
-> 完成考试题
-> 完成一个小型办公场景任务
-> Agent 自动评分
-> 达到证书规则
-> 自动生成 Certificate
-> 绑定 Wallet / DID
-> Claim Proof Credential
-> 分享给 Verifier
```

### 5.2 Verifier Journey

```text
收到候选人 Proof Link / QR Code
-> 打开 Verifier Portal
-> 验证证书状态
-> 查看证书范围
-> 查看能力摘要
-> 如候选人授权，查看作品摘要或 Evidence Package 摘要
-> 记录 VerificationEvent
```

## 6. 为什么第一版要全自动评分

当前是一人公司，不能依赖人工评审作为核心流程。

因此第一版评分原则是：

```text
默认全自动评分。
优先选择可自动判分题型。
主观题也必须有明确 rubric，由 Agent 自动评分。
证书签发由规则自动触发。
异常只记录风险，不阻断主流程。
```

后续可以扩展：

```text
企业版人工确认
高价值证书人工复核
第三方 Issuer 复核
抽检机制
```

但这些不是第一版 MVP 的依赖项。

## 7. 练习题与考试题的核心设计

你提出的关键点是对的：练习题和考试题必须进入核心数据结构。

方向还没完全定时，不能把题目结构写死在某一个课程里。正确设计是：

```text
底层是通用 Assessment Item 引擎。
练习题和考试题是不同使用模式。
题目必须绑定能力点、场景、评分规则和证书规则。
```

### 7.1 练习题 vs 考试题

| 类型 | 目的 | 是否影响证书 | 设计原则 |
| --- | --- | --- | --- |
| 练习题 Practice Question | 帮学习者掌握能力点 | 默认不直接决定证书，但影响学习进度 | 多反馈、可重做、低压力 |
| 考试题 Exam Question | 判断是否达标 | 直接影响证书签发 | 有时间、次数、达标线、完整性检查 |
| 项目任务 Project Task | 模拟真实工作场景 | 可作为证书证据 | 输出作品、过程记录和 Evidence Package |

### 7.2 第一版题型

优先做容易自动评分的题型：

```text
单选题
多选题
判断题
排序题
匹配题
填空题
短答案题
结构化输出题
小型项目任务
```

暂不优先做：

```text
长论文式主观题
需要复杂人工审美判断的作品
完全开放式大项目
难以解释评分依据的题型
```

### 7.3 题目和能力的关系

每道题不只是内容，而是能力测量单元。

```text
QuestionItem
-> CapabilityNode
-> ScenarioTag
-> DifficultyLevel
-> Rubric
-> ScoringRule
-> CertificateRequirement
```

这样未来无论方向变成 AI Office、AI 写作、AI 数据分析、青少年 AI 素养，底层都不用推倒重来。

## 8. 数据结构建议

### 8.1 核心题库对象

| 数据对象 | 含义 |
| --- | --- |
| QuestionItem | 通用题目对象，练习题和考试题共用底层结构 |
| PracticeSet | 练习题集合，用于学习和训练 |
| ExamPaper | 考试卷，用于证书达标判断 |
| ProjectTask | 项目任务，用于真实工作场景证据 |
| CapabilityNode | 能力点 |
| ScenarioTag | 使用场景标签 |
| AnswerKey | 标准答案或参考答案 |
| Rubric | 主观题 / 项目题评分规则 |
| ScoringRule | 自动评分规则 |
| CertificateRequirement | 证书达标规则 |

### 8.2 学习者作答对象

| 数据对象 | 含义 |
| --- | --- |
| PracticeAttempt | 练习作答记录 |
| ExamSession | 考试会话 |
| ExamAttempt | 考试作答记录 |
| ProjectSubmission | 项目任务提交 |
| AgentScore | Agent 自动评分结果 |
| ScoreBreakdown | 分项得分 |
| FeedbackAdvice | 自动反馈建议 |
| EvidencePackage | 证据包 |

### 8.3 证书对象

| 数据对象 | 含义 |
| --- | --- |
| CertificateCandidate | 达标后自动生成的证书候选 |
| Certificate | 平台签发证书 |
| ProofCredential | 可验证凭证 |
| ProofChainRecord | 链上证明登记 |
| VerificationEvent | Verifier 验证事件 |

## 9. 自动评分策略

### 9.1 客观题

```text
单选 / 多选 / 判断 / 匹配 / 排序 / 填空
-> AnswerKey 自动判分
-> 即时反馈
```

### 9.2 短答案题

```text
短答案
-> keyword / semantic match
-> Agent 解释评分
-> 输出 score + rationale_hash
```

### 9.3 结构化输出题

例如：

```text
用 AI 把会议记录整理成 action list。
用 AI 把客户邮件改写成专业英文回复。
用 AI 把一段资料总结成报告摘要。
```

评分方式：

```text
Rubric 分项评分
-> 完整性
-> 准确性
-> 清晰度
-> 可执行性
-> 风险意识
```

### 9.4 项目任务

项目任务不追求人工精细打分，第一版只做结构化自动评估：

```text
是否提交完整
是否符合格式
是否覆盖要求
是否体现 AI 使用过程
是否有最终交付物
是否存在明显风险
```

## 10. Certificate 签发规则

第一版 AI Office Productivity Certificate 的达标逻辑：

```text
完成必要 PracticeSet
完成 ExamPaper
考试达到最低分
完成一个 ProjectTask
AgentRiskFlag 未超过阈值
自动生成 CertificateCandidate
自动签发 Certificate
生成 ProofCredential
登记 ProofChainRecord
```

建议第一版规则：

```text
Practice completion >= 80%
Exam score >= 70%
ProjectTask status = completed
Critical risk = false
```

## 11. 产品页面清单

### 11.1 Learner Side

```text
Learner Dashboard
Capability Assessment
Learning Path
Practice Set
Exam Paper
Project Task
Submission Result
Certificate
Claim Proof Credential
Wallet Connect
```

### 11.2 Verifier Side

```text
Verifier Portal
Credential Verify
Capability Summary
Evidence Summary
Verification Event
```

### 11.3 Founder / Admin Side

```text
Question Bank
Practice Set Builder
Exam Paper Builder
Project Task Builder
Capability Map
Scoring Rule
Certificate Rule
Proof Registry Monitor
Audit Log
```

## 12. 第一版不做什么

第一版 MVP 不做：

```text
未成年人正式商业化
国内未成年人市场
复杂人工评审流程
第三方 Issuer 入驻
多证书体系
招聘平台 API
企业复杂组织架构
高风险监管职业证书
```

第一版先验证：

```text
一个人可以完成 AI Office 能力训练。
系统可以全自动评分。
系统可以自动签发平台证书。
证书可以链上验证。
Verifier 可以看懂并验证。
```

## 13. 后续路线图

| 阶段 | 目标 |
| --- | --- |
| v6.1 | 产品蓝图和数据结构定稿 |
| v6.2 | 原型页面清单和用户旅程细化 |
| v6.3 | Question Bank / Exam / Scoring / Certificate 数据字典 |
| v6.4 | MVP 原型设计 |
| v6.5 | 才开始代码实现 |

## 14. 下一步需要确认的问题

目前还需要确认三个问题：

```text
1. AI Office Productivity Certificate 里，第一版到底包含哪些能力模块？
2. 考试题数量和练习题数量大概多少？
3. 证书是否设置有效期，例如 1 年或 2 年？
```

建议默认：

```text
能力模块：文档、邮件、会议纪要、信息检索、报告摘要、表格分析、PPT 大纲、安全意识
练习题：每个能力模块 5-10 题
考试题：总共 30-40 题 + 1 个项目任务
证书有效期：2 年
```
