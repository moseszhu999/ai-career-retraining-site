# v6.10 Static Prototype Implementation Gate：静态原型实现前门禁

## 1. 本版目标

v6.9 已经准备好静态原型内容包。本版用于决定是否进入真正静态原型实现，以及如何实现。

本文件不是代码实现文档，而是实现前的门禁判断。

需要回答：

```text
1. 先实现什么形式？
2. 先实现几个 MVP？
3. 原型服务谁看？
4. 技术栈怎么选？
5. 哪些边界不能越过？
6. 什么条件满足才允许开始写代码？
```

---

## 2. 当前阶段判断

当前项目已经完成：

```text
v6.0 总体瀑布式交付方案
v6.0 Credential Architecture
v6.0 Verifier Stakeholder Architecture
v6.1 Product Blueprint
v6.2 Assessment & Question Bank Architecture
v6.3 Vertical Market Selection
v6.4 Vertical Market Research
v6.5 Broad Vertical Universe Scan
v6.6 Top 5 Evidence Pack
v6.7 Dual MVP Prototype Spec
v6.8 Static Prototype Design
v6.9 Static Prototype Content Pack
```

因此，理论上可以进入静态原型实现。

但进入实现前必须明确：

```text
第一版原型只服务销售验证和产品方向验证。
不是生产系统。
不是考试系统。
不是证书签发系统。
不是钱包系统。
不是链上系统。
不是 AI Agent 真实评分系统。
```

---

## 3. 推荐实现路线

推荐第一版静态原型采用：

```text
Single-page static HTML
+
Bootstrap 5
+
vanilla JavaScript
+
embedded mock data
```

原因：

```text
最快。
最容易部署到 GitHub Pages / Vercel / Netlify。
不需要后端。
不需要数据库。
不需要账号。
方便投资人、客户、合作方直接打开。
方便后续拆成真实前端页面。
```

暂不推荐第一版用 Streamlit：

```text
Streamlit 适合内部 demo，但外部销售展示质感有限。
Streamlit 容易让人误以为是数据工具，而不是证书平台。
```

暂不推荐第一版直接用 React / Next.js：

```text
会过早进入工程复杂度。
当前核心仍是验证产品方向，不是搭建正式系统。
```

---

## 4. 第一版原型范围

第一版原型名称：

```text
v7.0 Static Founder Demo Prototype
```

定位：

```text
一个可点击的 Founder / Sales Demo 原型。
```

目标观众：

```text
潜在客户
潜在合作方
培训机构
企业 HR / L&D
供应链 / 贸易场景合作方
投资人 / 顾问
早期学习者
```

核心演示目标：

```text
让观众理解平台不是普通课程平台，而是可验证能力证书平台。
让观众理解证书不是 PDF，而是 Evidence Package + Agent Score + Proof Credential。
让观众理解 Verifier 是核心客户，不是附属角色。
让观众理解 Data 和 Trade 是两个垂直 MVP 方向。
```

---

## 5. 第一版是否保留双 MVP

推荐：

```text
保留双 MVP，但主线展示 AI Data，Trade 作为差异化扩展线。
```

页面优先级：

```text
Primary route: AI Data Analysis Assistant
Secondary route: Cross-border Trade Documentation
Common route: Verifier + Proof Registry
Founder route: Architecture / Roadmap
```

原因：

```text
AI Data 方向更容易被普通观众理解。
Trade 方向更能体现 Evidence Package、Verifier 和 crypto proof 的独特性。
双路线能证明平台不是单一课程，而是可扩展证书基础设施。
```

---

## 6. 第一版页面范围

v7.0 只实现以下页面区块，不做完整页面系统。

```text
1. Hero / Product Overview
2. Certificate Catalog
3. AI Data MVP Route
4. Trade MVP Route
5. Practice / Exam Mock
6. Project Task Mock
7. Agent Score Report
8. Evidence Package
9. Certificate Detail
10. Claim Proof Credential Mock
11. Verifier Portal
12. Verifier Result
13. Proof Registry Mock
14. Founder Dashboard
15. Static Boundary Footer
```

这些可以在一个 HTML 文件中通过 tabs / anchors / section navigation 实现。

---

## 7. 不做事项

第一版静态原型明确不做：

```text
不做真实登录。
不做真实用户注册。
不做真实考试。
不做真实自动评分。
不调用 OpenAI / LLM API。
不接真实钱包。
不发真实链交易。
不部署智能合约。
不保存任何数据。
不上传文件。
不处理真实贸易单据。
不处理真实企业数据。
不处理真实个人数据。
不提供法律、贸易合规、金融、税务、医疗或投资意见。
```

---

## 8. 技术选择门禁

### 8.1 推荐技术

```text
HTML
Bootstrap 5
vanilla JavaScript
static JSON-like mock data
no build step
```

### 8.2 文件建议

```text
docs/prototypes/v7-static-founder-demo.html
```

可选拆分：

```text
docs/prototypes/v7-static-founder-demo.css
docs/prototypes/v7-static-founder-demo.js
```

但第一版建议单文件，减少路径和部署复杂度。

### 8.3 样式原则

```text
B2B SaaS 质感。
证书和 proof 区域要可信、稳重。
不要做过于儿童化或课程平台化。
不要像在线题库。
要像“可信能力基础设施 + 企业验证门户”。
```

---

## 9. 原型信息架构

推荐首页顶部：

```text
Brand: ProofSkill AI / AI Career Credential OS / 待定
Nav: Overview | Certificates | Data MVP | Trade MVP | Verifier | Proof Registry | Founder View
CTA: Verify Credential
```

主视觉：

```text
Prove real work skills, not just course completion.
```

副标题：

```text
Verifiable AI-era skill certificates backed by tasks, evidence packages, agent scoring, and crypto proof.
```

三个价值卡片：

```text
Task-based assessment
Agent-scored evidence
Verifier-ready proof
```

---

## 10. v7.0 Demo Route

### 10.1 3-minute route

```text
1. Hero: platform positioning.
2. Certificate Catalog: show two MVPs.
3. Data MVP: show path + project task.
4. Agent Score + Evidence Package.
5. Certificate + Claim Proof.
6. Verifier Result.
```

### 10.2 5-minute route

```text
1. Explain why not a course platform.
2. Walk through AI Data MVP.
3. Show Trade MVP as second vertical.
4. Show Proof Registry.
5. Show Founder Dashboard and roadmap.
```

### 10.3 8-minute route

```text
1. Market research and vertical universe logic.
2. Top 5 evidence pack.
3. Dual MVP choice.
4. AI Data route.
5. Trade route.
6. Verifier customer logic.
7. Crypto native proof boundary.
8. Roadmap to real product.
```

---

## 11. 页面内容来源

v7.0 实现必须只使用以下文档内容：

```text
docs/static_prototype_design_v6_8.md
docs/static_prototype_content_pack_v6_9.md
docs/dual_mvp_prototype_spec_v6_7.md
docs/credential_architecture_v6_0.md
docs/verifier_stakeholder_architecture_v6_0.md
```

不得临时创造新的业务方向。
不得新增未确认高风险能力声明。
不得把 mock 证书包装成真实证书。

---

## 12. Copy 边界

页面必须明确展示：

```text
Static prototype only.
No real wallet connection.
No real chain transaction.
No real database.
No real exam.
No real agent scoring.
No legal, trade compliance, financial, tax, medical, or investment advice.
```

中文：

```text
仅静态原型。
不连接真实钱包。
不发真实链交易。
不使用真实数据库。
不运行真实考试。
不调用真实 Agent 评分。
不提供法律、贸易合规、金融、税务、医疗或投资意见。
```

---

## 13. 多语言判断

第一版建议：

```text
先英文。
界面可预留 language selector。
暂不做完整多语言。
```

原因：

```text
MVP 市场目前偏海外。
英文更适合验证国际市场和 B2B 观感。
中文可在后续 v7.1 增加。
```

如果用户要求多语言，建议只做：

```text
English / 简体中文
```

不建议第一版做 5 种语言。

---

## 14. 品牌命名暂定

当前项目名称仍可保留：

```text
AI Career Retraining Site
```

但静态原型视觉品牌可以暂用：

```text
ProofSkill AI
```

候选品牌：

```text
ProofSkill AI
SkillProof AI
CredentialOS
ProofPath AI
VeriSkill AI
```

暂定建议：

```text
ProofSkill AI
```

原因：

```text
短。
容易理解。
突出 proof + skill。
不局限某一个垂直行业。
```

---

## 15. 进入实现的 Go / No-Go

### Go 条件

```text
v6.8 页面设计已完成。
v6.9 内容包已完成。
静态原型边界已明确。
第一版技术选择已明确。
第一版不接真实钱包 / 链 / Agent / DB。
用户同意进入静态原型实现。
```

### No-Go 条件

```text
用户还想继续扩展行业研究。
用户还未确认双 MVP 是否保留。
用户要求先做更多文档。
用户要求换技术路线。
用户要求真实功能而非静态原型。
```

---

## 16. 推荐下一步

建议下一步进入：

```text
v7.0 Static Founder Demo Prototype
```

实施文件：

```text
docs/prototypes/v7-static-founder-demo.html
```

第一版验收标准：

```text
单文件可打开。
Bootstrap 5 风格。
包含 Data 和 Trade 双 MVP。
包含 Verifier Portal mock。
包含 Proof Registry mock。
包含 Founder Dashboard。
包含静态原型边界声明。
不调用任何外部 API。
不写真实业务逻辑。
```

---

## 17. 结论

当前已经可以开始 v7.0 静态原型实现。

但实现必须遵守：

```text
先演示价值，不做系统。
先 Founder / Sales Demo，不做生产产品。
先静态 mock，不做真实链上和 Agent。
先验证双 MVP 方向，不做完整平台。
```
