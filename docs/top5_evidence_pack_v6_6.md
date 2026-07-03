# v6.6 Top 5 Evidence Pack：五个垂直方向最小验证包

## 1. 本版目标

本版不再继续拍脑袋决定第一行业，而是对 v6.5 选出的 Top 5 做同规格最小验证包。

Top 5：

```text
1. AI Data Analysis / BI Assistant
2. AI Security & Cyber Awareness
3. AI Governance / Privacy / Risk Operations
4. AI Legal Operations / Contract Review Assistant
5. Cross-border Trade Documentation & Supply Chain Compliance Assistant
```

每个方向统一给出：

```text
证书名称
目标用户
Verifier
5 个能力模块
10 道样题方向
1 个项目任务
自动评分规则
Evidence Package
Verifier 页面描述
Landing Page 标题
主要风险边界
冷启动判断
```

---

## 2. 方向一：AI Data Analysis / BI Assistant

### 2.1 证书名称

```text
AI Data Analysis Assistant Certificate
```

中文：

```text
AI 数据分析助理能力证书
```

### 2.2 目标用户

```text
运营人员
行政 / 财务 / 销售支持人员
想转数据分析方向的成年人
中小企业员工
自由职业数据报告服务者
```

### 2.3 Verifier

```text
企业运营部门
数据团队
财务团队
销售管理团队
HR / 招聘方
中小企业老板
```

### 2.4 能力模块

| 模块 | 名称 | 说明 |
| --- | --- | --- |
| DA1 | Data Literacy | 理解字段、指标、口径、缺失值和异常值 |
| DA2 | Spreadsheet Reasoning | 处理 CSV / Excel，做排序、筛选、分组、汇总 |
| DA3 | AI-assisted Analysis | 使用 AI 辅助提出问题、生成分析思路和解释结果 |
| DA4 | Chart & Insight Communication | 选择图表、表达洞察、写业务摘要 |
| DA5 | Data Quality & Risk | 识别样本不足、口径错误、误导性结论和隐私风险 |

### 2.5 10 道样题方向

```text
1. 识别一张销售表中的关键字段和指标。
2. 判断某个增长率计算是否正确。
3. 从表格中找出异常月份。
4. 选择最适合展示趋势的图表。
5. 判断 AI 给出的数据结论是否过度推断。
6. 根据业务目标提出 3 个分析问题。
7. 识别缺失值、重复值、异常值。
8. 给一段 AI 生成的数据摘要打标签：正确 / 不完整 / 误导。
9. 将表格结果转成 5 句话业务汇报。
10. 判断哪些数据不应该上传到外部 AI 工具。
```

### 2.6 项目任务

```text
Sales Performance Mini BI Report
```

给学习者一份模拟销售 CSV，包括：

```text
日期
地区
渠道
产品
销售额
客户数
退货数
广告费用
```

要求输出：

```text
1. 指标口径说明
2. 3 个关键发现
3. 1 个异常点解释
4. 1 个图表建议
5. 1 段业务建议
6. 1 个数据风险提醒
```

### 2.7 自动评分规则

```text
客观题：AnswerKey 自动评分。
表格任务：预设 expected insight + acceptable variants。
摘要题：Rubric + AgentScore。
风险题：RiskLabelKey + AgentScore。
项目任务：完整性、准确性、洞察质量、风险意识、表达清晰度。
```

### 2.8 Evidence Package

```text
原始数据 hash
学习者分析问题
答案记录
AgentScore
ScoreBreakdown
项目报告文本 hash
图表建议
风险提醒
最终证书 hash
```

### 2.9 Verifier 页面描述

Verifier 可查看：

```text
证书状态
考试得分
能力模块得分
项目报告摘要
数据风险意识得分
是否通过链上 Proof 验证
```

### 2.10 Landing Page 标题

```text
Prove You Can Turn Data into Business Insight with AI
```

中文：

```text
证明你能用 AI 把数据变成业务洞察
```

### 2.11 主要风险边界

```text
不承诺成为专业数据科学家。
不做投资建议。
不处理真实敏感个人数据。
不要求上传真实企业数据。
```

### 2.12 冷启动判断

```text
冷启动难度：低
自动评分：强
证书解释性：强
Verifier 清晰度：强
建议：Top 1 候选
```

---

## 3. 方向二：AI Security & Cyber Awareness

### 3.1 证书名称

```text
AI Security & Cyber Awareness Certificate
```

中文：

```text
AI 安全与网络安全意识证书
```

### 3.2 目标用户

```text
普通企业员工
远程办公人员
SaaS 工具使用者
客服 / 销售 / 运营人员
初级 IT / 安全入门人员
```

### 3.3 Verifier

```text
企业 IT 部门
安全团队
HR / 培训部门
合规团队
中小企业老板
```

### 3.4 能力模块

| 模块 | 名称 | 说明 |
| --- | --- | --- |
| CS1 | Cyber Hygiene | 密码、MFA、钓鱼、设备安全、权限基础 |
| CS2 | AI Tool Safety | AI 工具使用中的数据泄露、账号、文件上传风险 |
| CS3 | Prompt Injection Awareness | 识别外部内容操控模型或工具的风险 |
| CS4 | Data Classification | 判断哪些数据可以处理，哪些不能上传或分享 |
| CS5 | Incident Reporting | 遇到可疑邮件、泄露、异常输出时知道如何升级处理 |

### 3.5 10 道样题方向

```text
1. 判断一封邮件是否存在钓鱼风险。
2. 识别哪些信息属于敏感数据。
3. 判断是否可以把客户名单上传给 AI。
4. 识别 prompt injection 文本。
5. 选择最安全的 MFA 使用方式。
6. 判断 AI 总结网页内容时可能被网页提示词操控的场景。
7. 对 SaaS 权限设置做风险判断。
8. 识别可疑附件和链接。
9. 判断 AI 生成代码或脚本是否有危险操作。
10. 遇到疑似泄露时选择正确上报流程。
```

### 3.6 项目任务

```text
AI Tool Safety Review Scenario
```

给学习者一个企业场景：员工想把客户邮件、销售表、合同片段和网页资料交给 AI 总结。

要求输出：

```text
1. 哪些材料可以上传
2. 哪些材料必须脱敏
3. 哪些材料不能上传
4. prompt injection 风险点
5. 安全替代方案
6. 事件上报建议
```

### 3.7 自动评分规则

```text
风险识别题：RiskLabelKey。
多选题：partial credit。
情景题：Rubric + AgentScore。
项目任务：敏感数据识别、风险覆盖、处理建议、升级流程、误判率。
```

### 3.8 Evidence Package

```text
风险判断记录
敏感数据分类答案
prompt injection 识别结果
项目安全审查报告 hash
AgentScore
风险覆盖率
证书 hash
```

### 3.9 Verifier 页面描述

Verifier 可查看：

```text
证书状态
安全意识总分
敏感数据识别得分
prompt injection awareness 得分
项目任务风险覆盖摘要
链上 Proof 状态
```

### 3.10 Landing Page 标题

```text
Prove Your Team Can Use AI Tools Safely
```

中文：

```text
证明你的团队能安全使用 AI 工具
```

### 3.11 主要风险边界

```text
不教授攻击技术。
不提供绕过安全系统的方法。
不做高级渗透测试证书。
不替代企业正式安全合规认证。
```

### 3.12 冷启动判断

```text
冷启动难度：低到中
自动评分：强
证书解释性：强
Verifier 清晰度：很强
建议：Top 2 候选，适合企业培训入口
```

---

## 4. 方向三：AI Governance / Privacy / Risk Operations

### 4.1 证书名称

```text
AI Governance & Privacy Operations Certificate
```

中文：

```text
AI 治理、隐私与风险运营证书
```

### 4.2 目标用户

```text
企业运营人员
合规助理
数据保护相关岗位
AI 产品 / 项目成员
HR / 培训部门
咨询助理
```

### 4.3 Verifier

```text
企业合规团队
数据保护团队
AI 项目负责人
咨询公司
HR / 用人单位
```

### 4.4 能力模块

| 模块 | 名称 | 说明 |
| --- | --- | --- |
| GR1 | AI Use Case Inventory | 记录组织内 AI 使用场景和数据流 |
| GR2 | Privacy & Data Handling | 识别个人数据、敏感数据、授权和最小化原则 |
| GR3 | Risk Classification | 按风险等级分类 AI 使用场景 |
| GR4 | Policy & Control Mapping | 将风险映射到控制措施和操作流程 |
| GR5 | Audit Evidence | 保留使用记录、审批、评估和整改证据 |

### 4.5 10 道样题方向

```text
1. 判断某 AI 使用场景是否涉及个人数据。
2. 为一个 AI 使用案例选择风险等级。
3. 判断哪些字段应脱敏。
4. 识别是否需要用户同意。
5. 将风险映射到控制措施。
6. 选择合适的审计证据。
7. 判断一段 AI policy 是否缺少关键内容。
8. 判断某流程是否违反最小披露原则。
9. 识别模型输出可能造成的歧视或不公平风险。
10. 判断哪些 AI 使用场景应该进入人工复核。
```

### 4.6 项目任务

```text
AI Use Case Risk Register
```

给学习者 5 个企业 AI 使用场景，例如：

```text
HR 简历筛选
客服聊天机器人
销售邮件生成
客户数据分析
内部知识库问答
```

要求输出：

```text
1. 使用场景清单
2. 涉及数据类型
3. 风险等级
4. 需要的控制措施
5. 审计证据清单
6. 人工复核节点
```

### 4.7 自动评分规则

```text
分类题：expected labels。
风险等级题：risk rubric。
项目任务：覆盖率、风险判断、控制措施匹配、审计证据完整度。
AgentScore 必须输出 confidence 和 rationale_hash。
```

### 4.8 Evidence Package

```text
AI use case register
risk classification table
privacy handling answers
control mapping
AuditEvidence checklist
AgentScore
证书 hash
```

### 4.9 Verifier 页面描述

Verifier 可查看：

```text
证书状态
风险识别能力得分
隐私处理能力得分
AI use case register 项目摘要
审计证据意识得分
Proof 状态
```

### 4.10 Landing Page 标题

```text
Prove You Can Operate AI Responsibly in an Organization
```

中文：

```text
证明你具备企业 AI 治理与风险运营能力
```

### 4.11 主要风险边界

```text
不提供法律意见。
不声称满足某国完整监管要求。
不替代 DPO、律师或正式合规审计。
只做操作层风险识别、流程执行和证据意识。
```

### 4.12 冷启动判断

```text
冷启动难度：中
自动评分：中强
证书解释性：强
Verifier 清晰度：强
建议：Top 3 候选，前瞻性强
```

---

## 5. 方向四：AI Legal Operations / Contract Review Assistant

### 5.1 证书名称

```text
AI Legal Operations & Contract Review Assistant Certificate
```

中文：

```text
AI 法务运营与合同审查助理证书
```

### 5.2 目标用户

```text
法务助理
合同管理员
行政 / 采购 / 销售支持人员
律师事务所支持人员
企业运营人员
```

### 5.3 Verifier

```text
企业法务部门
律师事务所
采购部门
销售运营团队
合同管理团队
HR / 招聘方
```

### 5.4 能力模块

| 模块 | 名称 | 说明 |
| --- | --- | --- |
| LO1 | Contract Structure Literacy | 识别合同结构、主体、期限、金额、义务和附件 |
| LO2 | Clause Extraction | 提取付款、交付、违约、保密、终止、争议解决等条款 |
| LO3 | Playbook-based Review | 按企业 playbook 标记偏离项，而不是给法律意见 |
| LO4 | Legal AI Citation Safety | 识别 AI 编造引用、错误法域、过度结论 |
| LO5 | Matter Workflow & Evidence | 保留审查过程、版本、标记、审批和证据 |

### 5.5 10 道样题方向

```text
1. 从合同片段中识别合同主体。
2. 提取付款期限和付款条件。
3. 判断某条款是否偏离 playbook。
4. 识别保密条款是否缺少期限。
5. 判断 AI 给出的法律结论是否越界。
6. 识别合同中的交付物和验收要求。
7. 判断争议解决条款属于哪个法域。
8. 识别 AI 编造案例引用的风险。
9. 判断合同审查记录应保留哪些证据。
10. 给合同摘要选择正确标签。
```

### 5.6 项目任务

```text
Contract Intake & Playbook Review
```

给学习者一份短合同和一份公司合同审查 playbook。

要求输出：

```text
1. 合同摘要
2. 关键条款提取表
3. 与 playbook 不一致的条款
4. 需要升级给律师的问题
5. 不能自行给法律意见的边界说明
6. 审查证据包
```

### 5.7 自动评分规则

```text
条款提取：expected spans / labels。
playbook 偏离：rule matching + AgentScore。
越界判断：red flag key。
项目任务：条款覆盖率、偏离识别准确率、升级边界、摘要质量。
```

### 5.8 Evidence Package

```text
contract hash
playbook version
extracted clause table
deviation flags
escalation questions
AgentScore
review summary hash
证书 hash
```

### 5.9 Verifier 页面描述

Verifier 可查看：

```text
证书状态
条款提取得分
playbook review 得分
legal boundary awareness 得分
项目审查摘要
Proof 状态
```

### 5.10 Landing Page 标题

```text
Prove You Can Support Contract Review with AI Safely
```

中文：

```text
证明你能安全地用 AI 辅助合同审查与法务运营
```

### 5.11 主要风险边界

```text
不提供法律意见。
不替代律师。
不声称可以独立审查高风险合同。
不做法域特定法律判断，除非未来引入专业版本和专家审核。
```

### 5.12 冷启动判断

```text
冷启动难度：中
自动评分：中强
证书解释性：强
Verifier 清晰度：强
建议：Top 4 候选，商业价值高但边界必须清楚
```

---

## 6. 方向五：Cross-border Trade Documentation & Supply Chain Compliance Assistant

### 6.1 证书名称

```text
AI Cross-border Trade Documentation & Compliance Assistant Certificate
```

中文：

```text
AI 跨境贸易单证与供应链合规助理证书
```

### 6.2 目标用户

```text
外贸助理
跨境电商运营
供应链专员
物流协调员
贸易融资材料助理
小微外贸企业员工
```

### 6.3 Verifier

```text
外贸企业
物流公司
供应链金融机构
采购方
出口商 / 进口商
跨境电商公司
HR / 招聘方
```

### 6.4 能力模块

| 模块 | 名称 | 说明 |
| --- | --- | --- |
| TR1 | Trade Document Literacy | 发票、装箱单、提单、合同、PO、CO 等单证理解 |
| TR2 | Document Consistency Check | 金额、数量、货描、日期、主体、币种一致性检查 |
| TR3 | Compliance Awareness | 制裁、HS code、原产地、许可证、贸易条款基础意识 |
| TR4 | Supply Chain Evidence | 供应商文件、质检、交付、物流、收款证据整理 |
| TR5 | AI-assisted Document Review | 使用 AI 辅助预审单证并生成风险清单 |

### 6.5 10 道样题方向

```text
1. 识别商业发票中的买方、卖方、金额和币种。
2. 判断 PO 与发票数量是否一致。
3. 识别装箱单和发票中的货描差异。
4. 判断贸易术语的责任边界。
5. 识别缺少原产地文件的风险。
6. 判断哪些单证适合进入贸易融资 Evidence Package。
7. 判断 AI 给出的 HS code 建议是否需要人工确认。
8. 找出提单日期与发票日期的异常。
9. 判断供应商文件缺失会影响什么流程。
10. 生成一份单证差异清单。
```

### 6.6 项目任务

```text
Trade Document Consistency Review
```

给学习者一组模拟贸易文件：

```text
Purchase Order
Commercial Invoice
Packing List
Bill of Lading summary
Supplier Certificate
Inspection Note
```

要求输出：

```text
1. 单证摘要
2. 五单匹配表
3. 差异和风险清单
4. 缺失文件清单
5. 需要人工确认的问题
6. Evidence Package 摘要
```

### 6.7 自动评分规则

```text
字段提取：expected fields。
一致性检查：rule-based comparison。
风险识别：risk label key。
项目任务：差异发现率、误报率、文件覆盖率、人工确认边界。
```

### 6.8 Evidence Package

```text
document hashes
field extraction table
consistency check result
risk flags
missing document list
manual review questions
AgentScore
证书 hash
```

### 6.9 Verifier 页面描述

Verifier 可查看：

```text
证书状态
单证识别能力得分
一致性检查得分
合规意识得分
项目任务差异清单摘要
Proof 状态
```

### 6.10 Landing Page 标题

```text
Prove You Can Review Trade Documents with AI and Evidence
```

中文：

```text
证明你能用 AI 和证据链预审跨境贸易单证
```

### 6.11 主要风险边界

```text
不替代报关员、律师、银行审单员或官方合规判断。
不提供最终 HS code 法律结论。
不处理真实敏感贸易文件。
只做单证预审、差异识别、证据整理和人工确认问题生成。
```

### 6.12 冷启动判断

```text
冷启动难度：中
自动评分：强
证书解释性：强
Verifier 清晰度：很强
Crypto Proof 价值：很强
建议：Top 5 中最贴合 ChainTrace / 供应链可信证明方向
```

---

## 7. 横向比较

| 方向 | 冷启动 | 自动评分 | Verifier | Crypto Proof | 合规风险 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| AI Data Analysis | 低 | 强 | 强 | 中 | 低 | 最适合快速做 C 端 / 职业转型验证 |
| AI Security Awareness | 低中 | 强 | 很强 | 中 | 中 | 最适合企业培训和组织采购 |
| AI Governance / Privacy | 中 | 中强 | 强 | 强 | 中 | 前瞻强，适合企业 AI 落地趋势 |
| AI Legal Ops | 中 | 中强 | 强 | 强 | 中高 | 商业价值高，但法律边界要硬 |
| Cross-border Trade Docs | 中 | 强 | 很强 | 很强 | 中 | 最贴合可信证据、供应链和区块链叙事 |

---

## 8. 当前建议

不要一次只押一个。

第一阶段做两个并行验证包：

```text
A. AI Data Analysis Assistant
B. Cross-border Trade Documentation & Compliance Assistant
```

原因：

```text
AI Data Analysis：最容易冷启动，市场最宽。
Cross-border Trade：最能体现 crypto proof / evidence chain / ChainTrace 延展价值。
```

第二梯队：

```text
AI Security & Cyber Awareness
AI Governance / Privacy / Risk Operations
AI Legal Operations / Contract Review Assistant
```

这些适合作为 B2B / 企业版或后续证书线。

---

## 9. 下一步

下一步进入：

```text
v6.7 Dual MVP Prototype Spec
```

建议同时设计两个 MVP 原型规格：

```text
1. AI Data Analysis Assistant Certificate
2. Cross-border Trade Documentation & Compliance Assistant Certificate
```

每个规格包含：

```text
页面清单
数据对象
10 道真实样题
项目任务材料包
Agent 自动评分字段
证书样张字段
Verifier 页面字段
Proof Credential 字段
```

这一步完成后，再决定是否进入原型页面设计。
