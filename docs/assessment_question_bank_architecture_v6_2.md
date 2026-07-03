# v6.2 Assessment & Question Bank Architecture

## 1. 核心纠偏

AI Office Productivity Certificate 不能只证明传统办公能力。

如果能力模块只停留在：

```text
文档
邮件
会议纪要
报告摘要
PPT 大纲
表格分析
```

那它很快会落伍。

正确方向是：

```text
从 Office worker 能力，升级为 AI-native worker / Agent-native operator 能力。
```

也就是说，第一张证书虽然以办公生产力为入口，但底层能力必须面向最前沿的大模型、工具调用、多模态、Agent 编排、自动化工作流和安全校验。

## 2. 设计原则

```text
不要围绕某个工具设计能力。
不要只围绕传统 Office 场景设计能力。
不要把题库写死成课程题。

要围绕“AI 时代完成真实工作的能力”设计能力点、练习题、考试题和证书规则。
```

因此，底层模型是：

```text
CapabilityNode
-> QuestionItem
-> PracticeSet
-> ExamPaper
-> ProjectTask
-> ScoringRule
-> CertificateRequirement
```

方向以后可以变，但这套测评引擎不变。

## 3. 前沿 AI 能力趋势

本证书需要跟随以下趋势设计：

```text
大模型不只是聊天，而是在向 Agent runtime 发展。
Agent 会使用工具、调用外部系统、维护上下文、执行多步骤任务。
MCP 等协议正在把模型与文件、数据库、搜索、日历、设计工具、业务系统连接起来。
多模态模型可以处理文本、图片、音频、视频和文档。
AI 工作能力不再只是 prompt writing，而是任务拆解、上下文管理、工具选择、结果校验和风险控制。
```

所以第一版能力模块必须稍微超前，而不是做成传统办公软件培训。

---

## 4. AI Office Productivity Certificate：能力模块 v1

### 4.1 一级能力模块

| 模块 | 名称 | 定位 |
| --- | --- | --- |
| M1 | AI Model Literacy | 理解大模型能力边界、幻觉、上下文、推理和多模态能力 |
| M2 | Prompt & Context Engineering | 能把任务、资料、约束、格式和评价标准组织成有效上下文 |
| M3 | AI Work Product Generation | 用 AI 生成文档、邮件、报告、纪要、PPT 大纲等工作产物 |
| M4 | Multimodal Information Processing | 处理文档、图片、表格、截图、音频/视频摘要等多模态资料 |
| M5 | Agentic Workflow Design | 能拆解任务、设计多步骤 Agent 工作流和人机协作节点 |
| M6 | Tool Use & External System Thinking | 理解工具调用、API、MCP、文件、搜索、表格、日历等外部系统连接 |
| M7 | AI Output Verification | 能检查 AI 输出的事实、逻辑、来源、格式、风险和可执行性 |
| M8 | AI Data & Spreadsheet Reasoning | 用 AI 辅助表格分析、数据摘要、异常发现和业务解释 |
| M9 | AI Collaboration & Delegation | 能把 AI 当作协作者、研究员、编辑、分析师、助理或 Agent 团队使用 |
| M10 | AI Safety, Privacy & Governance | 理解隐私、版权、数据泄露、prompt injection、过度依赖和合规边界 |
| M11 | Proof & Evidence Awareness | 知道如何保留任务过程、证据、版本、评分和可验证证明 |
| M12 | Future-ready Learning Ability | 能持续跟踪新模型、新 Agent、新工具，并迁移到新场景 |

### 4.2 为什么这些模块不会过时太快

传统能力模块：

```text
会写邮件
会做 PPT
会整理会议纪要
```

容易被工具自动化替代。

更稳定的能力模块是：

```text
会定义任务
会组织上下文
会选择模型和工具
会设计 Agent 流程
会检查输出
会识别风险
会沉淀证据
会把 AI 工作变成可交付成果
```

这些能力即使模型继续升级，也仍然有价值。

---

## 5. 二级能力点

### M1 AI Model Literacy

| 能力点 | 说明 |
| --- | --- |
| M1.1 模型能力边界 | 知道模型擅长什么、不擅长什么 |
| M1.2 幻觉识别 | 能识别不确定、编造、过度自信输出 |
| M1.3 上下文窗口意识 | 知道上下文长度、信息丢失和摘要风险 |
| M1.4 多模态意识 | 知道文本、图片、音频、视频、文档输入的差异 |
| M1.5 推理与工具区别 | 知道模型推理和真实工具调用不是一回事 |

### M2 Prompt & Context Engineering

| 能力点 | 说明 |
| --- | --- |
| M2.1 任务定义 | 把模糊需求改成明确任务 |
| M2.2 背景资料组织 | 提供必要上下文、资料和约束 |
| M2.3 输出格式控制 | 要求结构化输出、表格、JSON、报告格式等 |
| M2.4 评价标准注入 | 把 rubric 和质量标准写进任务 |
| M2.5 迭代改写 | 根据结果继续追问、修正和优化 |

### M3 AI Work Product Generation

| 能力点 | 说明 |
| --- | --- |
| M3.1 专业邮件 | 生成、改写、压缩、翻译邮件 |
| M3.2 商务文档 | 生成方案、摘要、说明、FAQ、SOP |
| M3.3 会议纪要 | 从记录中提取决定、行动项、负责人和截止日期 |
| M3.4 报告摘要 | 把长材料整理成高管摘要、风险点和建议 |
| M3.5 PPT 大纲 | 生成演示结构、叙事线和页面草稿 |

### M4 Multimodal Information Processing

| 能力点 | 说明 |
| --- | --- |
| M4.1 文档理解 | 处理 PDF、Word、长文档和混合资料 |
| M4.2 图片 / 截图理解 | 从截图、图表、页面中提取信息 |
| M4.3 表格理解 | 理解表格字段、行列含义、异常点 |
| M4.4 音视频摘要 | 把会议、课程、访谈转为摘要和行动项 |
| M4.5 跨格式整合 | 把多个格式资料整合成统一输出 |

### M5 Agentic Workflow Design

| 能力点 | 说明 |
| --- | --- |
| M5.1 任务拆解 | 把复杂任务拆成多步子任务 |
| M5.2 Agent 角色设计 | 定义研究员、编辑、审查员、执行员等 Agent 角色 |
| M5.3 Handoff 设计 | 知道何时把任务从一个 Agent 交给另一个 Agent |
| M5.4 人类检查点 | 设计需要人类确认的节点 |
| M5.5 失败恢复 | 识别失败步骤并重新规划 |

### M6 Tool Use & External System Thinking

| 能力点 | 说明 |
| --- | --- |
| M6.1 工具选择 | 判断什么时候需要搜索、计算、文件、表格、日历、浏览器等工具 |
| M6.2 MCP / Connector 思维 | 理解 AI 应用如何连接外部系统 |
| M6.3 API / 自动化意识 | 知道 AI 可以调用 API 或自动化工作流 |
| M6.4 权限意识 | 知道工具调用需要权限和边界 |
| M6.5 工具结果校验 | 不盲信工具结果，能检查来源和合理性 |

### M7 AI Output Verification

| 能力点 | 说明 |
| --- | --- |
| M7.1 事实核查 | 检查关键事实和来源 |
| M7.2 逻辑检查 | 检查论证、步骤和结论是否一致 |
| M7.3 格式检查 | 检查输出是否符合格式要求 |
| M7.4 风险检查 | 识别法律、隐私、商业、伦理风险 |
| M7.5 可执行性检查 | 判断输出是否能真正执行 |

### M8 AI Data & Spreadsheet Reasoning

| 能力点 | 说明 |
| --- | --- |
| M8.1 表格摘要 | 总结表格重点 |
| M8.2 指标解释 | 解释趋势、异常、变化和原因 |
| M8.3 简单公式 | 理解基础计算、比例、增长率、排序、筛选 |
| M8.4 图表建议 | 判断适合的图表和表达方式 |
| M8.5 数据风险 | 识别样本不足、缺失值、口径不一致 |

### M9 AI Collaboration & Delegation

| 能力点 | 说明 |
| --- | --- |
| M9.1 AI 角色分配 | 把 AI 作为研究员、助理、编辑、审查员使用 |
| M9.2 多轮协作 | 通过多轮交互改进结果 |
| M9.3 批判性协作 | 不把 AI 当权威，而是当协作对象 |
| M9.4 任务委派 | 能把工作委派给 AI 并验收结果 |
| M9.5 协作记录 | 保留关键输入、输出和修改过程 |

### M10 AI Safety, Privacy & Governance

| 能力点 | 说明 |
| --- | --- |
| M10.1 隐私保护 | 不上传敏感个人信息、公司机密和未授权数据 |
| M10.2 Prompt Injection 意识 | 知道外部内容可能操控模型或工具 |
| M10.3 版权意识 | 理解生成内容和引用材料的版权风险 |
| M10.4 自动化边界 | 知道什么任务不能完全交给 AI |
| M10.5 审计意识 | 重要任务要保留过程和决策记录 |

### M11 Proof & Evidence Awareness

| 能力点 | 说明 |
| --- | --- |
| M11.1 证据包意识 | 知道证书需要任务、考试、作品和评分证据 |
| M11.2 版本意识 | 保留初稿、修改稿和最终稿 |
| M11.3 可验证证明 | 理解 Proof Credential 和链上验证的基本含义 |
| M11.4 授权披露 | 知道向 Verifier 展示什么，不展示什么 |
| M11.5 作品包装 | 把学习成果包装成可信作品摘要 |

### M12 Future-ready Learning Ability

| 能力点 | 说明 |
| --- | --- |
| M12.1 新工具迁移 | 能把旧能力迁移到新模型和新工具 |
| M12.2 模型比较 | 知道不同模型适合不同任务 |
| M12.3 学习路线更新 | 能根据新技术调整学习路径 |
| M12.4 前沿意识 | 关注 Agent、多模态、工具调用、自动化趋势 |
| M12.5 自我评估 | 能定期重新评估自己的 AI 能力 |

---

## 6. 题型设计

### 6.1 客观题

| 题型 | 适合测什么 | 自动评分 |
| --- | --- | --- |
| 单选题 | 概念、边界、最佳选项 | AnswerKey |
| 多选题 | 风险识别、多因素判断 | AnswerKey + partial credit |
| 判断题 | 基础规则和红线 | AnswerKey |
| 排序题 | 工作流步骤、Agent 流程 | OrderedAnswerKey |
| 匹配题 | 工具选择、能力点匹配 | MatchingKey |

### 6.2 半结构化题

| 题型 | 适合测什么 | 自动评分 |
| --- | --- | --- |
| Prompt 改写题 | Context engineering | Rubric + AgentScore |
| 输出修正题 | AI output verification | Rubric + diff check |
| 风险标注题 | Safety / governance | RiskLabelKey |
| 工具选择题 | Tool use thinking | ToolSelectionRule |
| Agent 流程设计题 | Agentic workflow | WorkflowRubric |

### 6.3 项目任务

| 任务 | 目标 | 证据 |
| --- | --- | --- |
| 邮件改写任务 | 生成专业邮件 | Prompt、初稿、终稿、评分 |
| 会议纪要任务 | 提取行动项 | 原始记录、输出、Action list |
| 报告摘要任务 | 生成 executive summary | 输入资料、摘要、风险点 |
| 表格分析任务 | 找出趋势和异常 | 表格、分析结论、图表建议 |
| Agent 工作流设计任务 | 设计多步骤 AI workflow | 流程图、角色、检查点 |
| 安全审查任务 | 识别隐私和注入风险 | 风险清单、修正建议 |

---

## 7. 考试结构建议

第一版考试不要太重，但必须覆盖未来能力。

```text
总题量：40 题 + 1 个项目任务
考试时间：60-90 分钟
通过线：70%
证书有效期：建议 2 年
```

题目分布：

| 模块 | 题量 |
| --- | --- |
| AI Model Literacy | 4 |
| Prompt & Context Engineering | 5 |
| AI Work Product Generation | 5 |
| Multimodal Information Processing | 4 |
| Agentic Workflow Design | 5 |
| Tool Use & External System Thinking | 4 |
| AI Output Verification | 5 |
| AI Data & Spreadsheet Reasoning | 4 |
| AI Safety, Privacy & Governance | 4 |
| Project Task | 1 |

M9、M11、M12 不一定单独出很多题，可以嵌入项目任务和情景题中。

---

## 8. 练习题结构建议

每个模块 5-10 道练习题。

```text
M1-M10 每个模块第一版 6 题
总练习题：约 60 题
考试题：40 题
项目任务：1 个
```

练习题特点：

```text
允许重复做
立即反馈
解释为什么错
推荐补练能力点
不直接决定证书
```

考试题特点：

```text
限制次数
计入证书达标
记录 ExamSession
生成 EvidencePackage
进入 Proof Credential 证据链
```

---

## 9. 数据结构

### 9.1 题库对象

| 数据对象 | 字段建议 |
| --- | --- |
| QuestionItem | question_id, item_type, stem, options, answer_key, capability_ids, scenario_tags, difficulty, rubric_id, scoring_rule_id |
| PracticeSet | practice_set_id, title, capability_ids, question_ids, retry_policy |
| ExamPaper | exam_id, title, credential_type, question_ids, project_task_id, pass_rule, time_limit |
| ProjectTask | project_task_id, title, scenario, input_material, deliverable_format, rubric_id |
| Rubric | rubric_id, criteria, levels, weights, red_flags |
| ScoringRule | scoring_rule_id, method, auto_score_type, pass_threshold, partial_credit_policy |
| CertificateRequirement | requirement_id, credential_type, practice_required, exam_score_min, project_required, critical_risk_policy |

### 9.2 作答对象

| 数据对象 | 字段建议 |
| --- | --- |
| PracticeAttempt | attempt_id, learner_id, question_id, answer, score, feedback, timestamp |
| ExamSession | session_id, learner_id, exam_id, started_at, submitted_at, status |
| ExamAttempt | attempt_id, session_id, question_id, answer, score, rationale_hash |
| ProjectSubmission | submission_id, learner_id, project_task_id, file_hash, output_text, submitted_at |
| AgentScore | agent_score_id, target_type, target_id, score, confidence, feedback_hash |
| ScoreBreakdown | breakdown_id, agent_score_id, criterion, score, comment_hash |
| EvidencePackage | evidence_package_id, learner_id, exam_session_id, project_submission_id, final_score, status |

---

## 10. 自动评分原则

第一版默认全自动评分。

```text
客观题：AnswerKey 自动判分。
排序 / 匹配：结构化答案自动判分。
Prompt 改写题：Rubric + AgentScore。
风险标注题：RiskLabelKey + AgentScore。
项目任务：Rubric + AgentScore + red flag 检查。
```

AgentScore 必须保留：

```text
score
confidence
rationale_hash
rubric_version
model_version
risk_flags
```

这不是为了人工审核，而是为了未来审计、复测、升级模型和证书可信度。

---

## 11. 证书达标规则

第一版建议：

```text
Practice completion >= 80%
Exam score >= 70%
ProjectTask completed = true
Critical risk = false
Proof package generated = true
```

如果不满足：

```text
返回补练能力点
推荐 PracticeSet
允许重新考试
保留失败记录但不进入公开证书
```

---

## 12. 第一版项目任务建议

项目任务名称：

```text
AI Office Work Simulation
```

任务描述：

```text
给学习者一组混合材料：一封客户邮件、一段会议记录、一张简单表格、一个截图说明。
要求学习者使用 AI 完成：
1. 客户邮件回复草稿
2. 会议行动项列表
3. 表格异常摘要
4. 一页报告大纲
5. 风险与隐私检查清单
6. 简单 Agent 工作流设计
```

评分维度：

```text
完整性
准确性
结构化程度
AI 使用过程合理性
输出可执行性
风险意识
证据完整性
```

这个任务能同时覆盖传统 Office 能力和未来 Agent-native 能力。

---

## 13. 后续扩展

这套题库架构未来可以扩展到：

```text
AI Research Certificate
AI Data Analysis Assistant Certificate
AI Business Proposal Certificate
AI Workflow Operator Certificate
AI Agent Coordinator Certificate
Youth AI Literacy Certificate
```

扩展方式不是重写系统，而是新增：

```text
CapabilityNode
QuestionItem
PracticeSet
ExamPaper
ProjectTask
CertificateRequirement
```

---

## 14. 验收标准

```text
能力模块不只覆盖文档、邮件、PPT，而是覆盖 AI-native worker 能力。
模块必须包含 Agentic Workflow、Tool Use、MCP/Connector 思维、多模态、验证、安全和证据意识。
练习题和考试题都进入核心数据结构。
题库底层必须是通用 Assessment Item 引擎。
第一版默认全自动评分。
主观题和项目题必须通过 Rubric + AgentScore 自动评分。
题目必须绑定 CapabilityNode、ScenarioTag、Rubric、ScoringRule 和 CertificateRequirement。
证书必须能追溯到 ExamSession、ProjectSubmission、AgentScore 和 EvidencePackage。
```
