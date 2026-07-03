# v6.0 可信证书架构：Crypto Native + Agent Native

## 1. 核心判断

证书 / Proof Credential 是本项目最重要的产品能力之一，不是普通报表，也不是普通 PDF。

本平台要解决的是：

```text
学习者完成学习、考试、任务、项目和作品之后，如何低成本、自动化、可信地获得一个可验证能力证明。
```

这个证明可以用于：

```text
成年人跳槽
公司内部晋升
岗位转型
自由职业接单
企业团队培训验收
未成年人 AI 素养成长档案
项目式学习成果展示
```

## 2. 为什么现有证明不够

现有证明通常有三个问题：

```text
1. 不可验证
   证书只是 PDF、图片、纸质文件或平台内记录，离开平台后可信度下降。

2. 流程繁琐
   证明往往依赖人工审核、第三方机构、线下流程或复杂查询。

3. 证据断裂
   证书和真实学习过程、考试结果、任务作品、评审记录之间没有稳定证据链。
```

本平台的机会是：

```text
用 Agent 自动完成能力评测、证据汇总和证书候选生成。
用区块链或可信账本完成证书状态、哈希和撤销记录验证。
用 Proof Credential 取代低效率、低透明度的中间证明流程。
```

注意：本平台证书不是国家职业资格、学校学历或监管资格证书；它是平台基于学习、任务、考试、作品和评审签发的能力证明。

## 3. 产品定位

```text
Crypto Native Certificate Platform
+
Agent Native Learning & Assessment OS
```

中文可以表达为：

```text
加密原生的能力证明平台
+
Agent 原生的学习评测系统
```

含义：

```text
crypto native：证书从一开始就设计为可签名、可携带、可验证、可撤销。
agent native：诊断、路径、任务、评分、证据汇总、证书候选生成都由 Agent 原生参与。
```

## 4. 证书生命周期

```text
能力诊断
-> 学习路径
-> 任务训练 / 考试 / 项目作品
-> Evidence Package
-> Agent 自动评分
-> Agent 证据汇总
-> Agent 风险提示
-> 人类确认 / 策略批准
-> Certificate / Proof File 生成
-> Proof Credential 签发
-> 链上 Proof Registry 登记
-> Holder 钱包保存
-> Verifier 验证
-> 续期 / 撤销 / 重新评测
```

## 5. 角色模型

| 角色 | 含义 | 本平台对应 |
| --- | --- | --- |
| Issuer | 证书签发方 | 平台、训练营、企业、授权 Reviewer、未来合作机构 |
| Holder | 证书持有者 | 成年学习者；未成年人场景下可由监护人代持 |
| Subject | 证书主体 | 完成学习、考试、任务或项目的人 |
| Verifier | 验证方 | 雇主、上级、客户、企业 HR、项目方、监护人、学校或社群 |
| Registry | 可验证登记层 | 链上 Proof Registry、撤销注册表、签发方 DID / key 注册表 |

## 6. 证书类型

| 证书类型 | 适用场景 | 示例 |
| --- | --- | --- |
| Skill Certificate | 单项能力证明 | AI 文档处理能力、AI 数据分析能力、AI 写作能力 |
| Workflow Certificate | 工作流能力证明 | AI 辅助销售方案生成、AI 辅助需求分析、AI 辅助项目交付 |
| Project Proof | 项目作品证明 | 完成一个作品、案例、原型或交付物 |
| Readiness Credential | 岗位就绪证明 | AI Office Readiness、AI Product Assistant Readiness |
| Team Readiness Report | 团队能力报告 | 某企业团队 AI 应用能力分布和提升建议 |
| Youth AI Literacy Proof | 青少年 AI 素养成长证明 | 创造力项目、数字素养、表达能力、计算思维 |

## 7. Crypto Native 设计原则

Crypto native 不是把所有数据都放到链上。

正确原则是：

```text
用户拥有自己的证明。
证书可以离开平台被验证。
链上只放哈希、时间戳、签发方、状态和撤销信息。
原始学习内容不上链。
个人隐私不上链。
未成年人身份信息不上链。
Proof File 内容由用户或监护人控制可见范围。
Verifier 不需要登录平台数据库，也能验证证书状态。
```

推荐结构：

```text
前端应用
-> Wallet / DID
-> Proof Credential
-> 用户控制的加密存储
-> Chain Proof Registry
-> Verifier Portal
```

## 8. Agent Native 设计原则

Agent native 不是页面里加一个聊天机器人。

正确原则是：

```text
Agent 负责能力诊断。
Agent 负责生成个性化路径。
Agent 负责生成任务、考试和项目练习。
Agent 负责初步评分和反馈。
Agent 负责汇总 Evidence Package。
Agent 负责识别证书候选。
Agent 负责标记风险和证据缺口。
Agent 不能单独最终签发高价值证书。
高价值证书需要人类确认或策略批准。
```

Agent 角色：

| Agent | 职责 | 输出 |
| --- | --- | --- |
| Diagnosis Agent | 能力诊断、目标分析、Gap 分析 | CapabilityAssessment |
| Path Agent | 生成学习路径和训练计划 | LearningPath / TrainingPlan |
| Task Agent | 生成任务、考试、项目练习 | TaskTemplate / AssessmentExam |
| Review Agent | 自动评分、反馈、证据汇总 | AgentScore / AgentReviewTrace |
| Risk Agent | 检查异常、证据缺口、低可信度结果 | AgentRiskFlag |
| Credential Agent | 生成证书候选和 Proof Credential 草稿 | CertificateCandidate / ProofCredential draft |
| Verification Agent | 辅助验证证书状态和证据摘要 | VerificationEvent |

## 9. 人类与 Agent 的边界

```text
低风险证书：可以策略自动签发，但必须可审计、可撤销。
中风险证书：Agent 生成候选，人类抽检或批量确认。
高价值证书：必须人类确认后签发。
企业团队证书：需要企业管理员或授权 Reviewer 确认。
未成年人证明：必须有监护人可见性规则和隐私保护。
异常证据：必须进入 Review Queue。
```

## 10. 数据对象

| 数据对象 | 含义 |
| --- | --- |
| LearnerProfile | 学习者画像 |
| CapabilityAssessment | 能力诊断结果 |
| LearningPath | 学习路径 |
| AssessmentExam | 考试 / 测评 |
| TaskTemplate | 任务模板 |
| Submission | 学习者提交 |
| EvidencePackage | 证据包 |
| AgentScore | Agent 评分 |
| AgentReviewTrace | Agent 证据汇总轨迹 |
| AgentRiskFlag | Agent 风险提示 |
| CertificateCandidate | 证书候选 |
| IssuancePolicy | 证书签发规则 |
| Certificate | 平台证书 |
| ProofCredential | 可验证能力凭证 |
| ProofChainRecord | 链上证明记录 |
| VerificationEvent | 外部验证记录 |
| CredentialLifecycleEvent | 证书撤销、续期、过期、重新评测事件 |
| AuditEvent | 审计事件 |

## 11. 关键数据链路

```text
LearnerProfile
-> CapabilityAssessment
-> LearningPath
-> AssessmentExam / TaskTemplate
-> Submission
-> EvidencePackage
-> AgentScore / AgentReviewTrace / AgentRiskFlag
-> CertificateCandidate
-> HumanReview / IssuancePolicy
-> Certificate
-> ProofCredential
-> ProofChainRecord
-> VerificationEvent
```

## 12. 去中介化价值

本平台不是在所有场景中取代官方机构，也不是取代国家资格或学历体系。

它要取代的是大量低效率的中间证明流程：

```text
人工开证明
平台内截图
无法验证的 PDF
第三方背书查询
低可信作品包装
重复提交材料
雇主或客户手工核验证书
```

在非监管资格场景下，本平台可以通过：

```text
任务证据
考试结果
作品记录
Agent 评测
人类确认
链上哈希
撤销状态
Verifier Portal
```

形成自动化、低成本、可验证的能力证明基础设施。

## 13. 国内与海外路线

| 路线 | 市场 | 技术选择 | 说明 |
| --- | --- | --- | --- |
| Phase 1 | 海外成年人 | Frontend + Wallet/DID + Chain Proof Registry | 最适合验证 crypto native 证书差异化 |
| Phase 2 | 海外青少年 | 增加监护人控制和儿童隐私保护 | 只做 AI 素养与项目成长，不做学科补课 |
| Phase 3 | 国内成年人 | 普通 Web 或联盟链 / 许可链 | 避免公链、Token、虚拟币叙事 |
| Phase 4 | 国内未成年人 | 合规确认后再进入 | 必须避开学科补课、应试提分和高压训练 |

## 14. MVP 建议

第一版不要做大而全，先做一个最能体现差异化的闭环：

```text
能力诊断
-> 任务 / 考试
-> 提交作品
-> Agent 评分
-> 人类确认
-> 生成 Certificate
-> 生成 ProofCredential
-> 链上登记 hash
-> Verifier 页面验证
```

MVP 页面：

```text
Learner Profile
Capability Assessment
Task / Exam
Submission
Evidence Package
Agent Review
Human Review Queue
Certificate
Proof Credential
Chain Proof Registry
Verifier Portal
Audit Log
```

## 15. 验收标准

```text
证书价值清楚：用于跳槽、晋升、接单、团队验收、成长档案和外部验证。
证书边界清楚：平台证书不是国家职业资格、学校学历或监管证书。
crypto native 清楚：证书可离开平台验证，链上只放哈希、状态、签发方和撤销信息。
agent native 清楚：Agent 原生参与诊断、路径、任务、评分、证据汇总、风险提示和证书候选生成。
去中介化清楚：在非监管资格场景下，用证据链和链上证明降低第三方中介验证依赖。
人类边界清楚：高价值证书必须人类确认或策略批准，不能让 Agent 无边界签发。
未成年人边界清楚：只做 AI 素养、创造力和项目式成长，不做学科补课和应试提分。
数据链路清楚：ProofCredential 必须能追溯到 EvidencePackage、Certificate 和 ProofChainRecord。
```
