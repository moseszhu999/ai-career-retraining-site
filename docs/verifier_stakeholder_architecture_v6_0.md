# v6.0 Verifier Stakeholder 架构：用人单位 / 招生机构 / 录取方

## 1. 核心判断

本项目不是单边学习平台，而是双边能力证明网络。

```text
一边是能力证明供给侧：学习者 / 证书持有者。
另一边是能力验证需求侧：用人单位、招生机构、学校、企业 HR、项目方、客户方、招聘平台。
```

第二类用户非常重要。他们不是边缘用户，而是核心 stakeholder，也是潜在核心客户。

他们真正需要的是：

```text
在招聘、录取、晋升、转岗、项目合作之前，更低成本、更可信、更结构化地了解一个人的过往学习成绩、能力证据、项目作品和可信证书。
```

---

## 2. Stakeholder 定义

| Stakeholder | 角色含义 | 典型场景 |
| --- | --- | --- |
| 用人单位 | 需要招聘、选拔、晋升、转岗的人才需求方 | 招聘、晋升、内部人才盘点 |
| 企业 HR / 招聘团队 | 需要快速筛选候选人能力证据 | 初筛、复筛、面试前验证 |
| 业务部门负责人 | 需要判断候选人是否能做真实工作 | 项目岗位匹配、团队补位 |
| 招生机构 / 学校 | 需要了解申请者能力、项目经历和成长记录 | 招生、项目班录取、国际教育申请 |
| 项目方 / 客户方 | 需要判断自由职业者或服务方是否可靠 | 外包、接单、顾问合作 |
| 招聘平台 / 人才平台 | 需要提升简历和证书真实性 | 人才画像、证书验证、岗位匹配 |
| 家长 / 监护人 | 未成年人场景下需要了解成长结果 | AI 素养成长档案、项目学习成果 |

---

## 3. 为什么他们也是核心客户

传统招聘、录取和选拔存在几个问题：

```text
简历容易包装。
证书真假难辨。
项目经历缺少证据。
面试成本高。
第三方背调慢且贵。
候选人的真实能力和岗位要求难匹配。
学校或机构很难快速理解申请人的真实项目能力。
```

本平台可以提供一个更好的方式：

```text
候选人授权后，用人单位或招生机构可以查看被授权的能力证明、成绩记录、项目作品、Evidence Package 摘要和链上验证状态。
```

这就把平台价值从“学习者自我提升”扩展到：

```text
人才能力验证基础设施。
```

---

## 4. Verifier Customer 价值主张

| 客户 | 平台价值 |
| --- | --- |
| 用人单位 | 降低筛选成本，提高候选人能力判断质量 |
| 企业 HR | 快速验证证书真伪、过期状态、撤销状态和能力范围 |
| 业务负责人 | 查看与岗位相关的真实任务、项目作品和能力证据摘要 |
| 招生机构 / 学校 | 查看申请者的项目式学习成果、AI 素养成长和能力轨迹 |
| 项目方 / 客户方 | 判断自由职业者或服务方是否具备交付能力 |
| 招聘平台 | 为简历和证书增加可信验证层 |
| 家长 / 监护人 | 查看未成年人非应试方向的成长记录和项目成果 |

---

## 5. 产品能力：Verifier Portal

未来应设计一个专门面向验证方的门户：

```text
Verifier Portal
```

核心功能：

```text
输入证书编号 / QR Code / Proof Link
验证证书是否真实
验证证书是否过期
验证证书是否被撤销
查看签发方
查看签发时间
查看能力范围
查看候选人授权的成绩摘要
查看候选人授权的 Evidence Package 摘要
查看候选人授权的作品集
查看与岗位或招生要求的匹配度
生成验证记录和审计日志
```

---

## 6. 关键原则：候选人授权与最小披露

Verifier 不能无限制查看学习者全部数据。

必须遵守：

```text
候选人授权
最小披露
用途限定
可撤回授权
访问留痕
敏感数据隐藏
未成年人监护人控制
```

正确数据流：

```text
Verifier 发起验证请求
-> Holder / Guardian 授权
-> 系统生成可见范围
-> Verifier 查看被授权摘要
-> 链上验证证书状态
-> 系统记录 VerificationEvent
```

禁止做法：

```text
未经授权展示学习者完整数据。
把未成年人身份信息公开给第三方。
向用人单位出售完整学习隐私。
做黑名单、歧视性评分或不可解释的人才信用分。
把平台证书包装成国家资格、学历或监管认证。
```

---

## 7. Verifier 使用路径

### 7.1 招聘 / 跳槽场景

```text
候选人申请岗位
-> 候选人提交 Proof Credential Link
-> HR 打开 Verifier Portal
-> 验证证书状态
-> 查看被授权能力摘要和项目证据
-> 决定是否进入面试或下一轮
```

### 7.2 公司内部晋升 / 转岗场景

```text
员工完成训练和考试
-> 平台生成内部 Readiness Credential
-> 经理 / HR 查看团队能力证明
-> 对照岗位要求查看 Gap
-> 决定晋升、转岗或补训计划
```

### 7.3 招生 / 录取场景

```text
申请人提交成长档案或项目证明
-> 招生机构查看项目作品和能力证明
-> 验证 Proof 状态
-> 查看项目式学习证据摘要
-> 辅助录取或分班决策
```

### 7.4 自由职业 / 项目合作场景

```text
服务方提交能力 Proof
-> 客户验证证书和作品
-> 查看交付场景相关证据
-> 判断是否合作
```

---

## 8. Verifier 数据对象

| 数据对象 | 含义 |
| --- | --- |
| VerifierProfile | 验证方资料，如企业、学校、项目方、HR、客户 |
| VerificationRequest | 验证请求 |
| ConsentGrant | 候选人或监护人的授权记录 |
| DisclosurePolicy | 可见范围策略 |
| VerificationView | 给验证方展示的最小披露视图 |
| VerificationEvent | 验证事件 |
| RoleRequirement | 岗位或招生要求 |
| MatchSummary | 能力证明与岗位 / 招生要求的匹配摘要 |
| AccessAuditEvent | 访问审计事件 |

---

## 9. 与 Crypto Native 的关系

Verifier 是 crypto native 架构的核心使用者。

```text
如果证书只在平台内可见，Verifier 必须相信平台数据库。
如果证书是 crypto native，Verifier 可以独立验证证书状态、签发方和撤销记录。
```

链上只应该给 Verifier 提供：

```text
Proof hash
issuer
issued_at
status
revocation status
network / tx reference
```

不应该上链：

```text
完整成绩单
原始作品
未成年人身份信息
面试记录
个人隐私
```

---

## 10. 与 Agent Native 的关系

Verifier 侧也需要 Agent。

可设计：

| Agent | 作用 |
| --- | --- |
| Requirement Agent | 帮用人单位或招生机构结构化岗位 / 招生要求 |
| Match Agent | 将候选人授权 Proof 与岗位要求做匹配摘要 |
| Risk Agent | 提示证书过期、撤销、证据不足或能力范围不匹配 |
| Interview Prep Agent | 基于候选人授权证据生成面试问题建议 |
| Admission Review Agent | 基于项目证据生成招生评审摘要 |

边界：

```text
Agent 可以辅助筛选和摘要。
Agent 不能替代最终录用、录取或晋升决策。
Agent 输出必须可解释、可审计、可被人工复核。
```

---

## 11. 商业模式

Verifier 侧可以形成 B 端收入：

```text
企业验证席位
HR 验证套餐
招聘平台 API
学校 / 项目班招生验证工具
企业内部 Readiness Dashboard
候选人授权能力报告
证书验证 API
```

注意：

```text
不能把学习者隐私卖给用人单位。
收入应来自验证工具、组织账号、API、报告和流程效率提升，而不是出售未经授权的个人数据。
```

---

## 12. 原型页面建议

新增页面：

```text
Verifier Portal
Verifier Organization
Verification Request
Consent Grant
Credential Verify
Evidence Summary View
Role Requirement
Match Summary
Verification Audit
Verifier API Keys
```

这些页面应与现有：

```text
Certificate
Proof Credential
Chain Proof Registry
Evidence Package
Readiness Reports
```

形成闭环。

---

## 13. 验收标准

```text
Verifier 被定义为核心 stakeholder，而不是附属角色。
用人单位、招生机构、学校、HR、项目方、客户方都有明确价值主张。
Verifier Portal 能验证证书真伪、状态、过期、撤销和签发方。
候选人授权和最小披露是基本原则。
未成年人数据必须经过监护人控制。
Verifier 侧 Agent 只能辅助摘要和匹配，不能替代最终录用或录取决策。
商业模式来自验证工具、组织账号和 API，而不是出售隐私数据。
```
