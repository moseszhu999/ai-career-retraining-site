# v7.2 Frontend-only Evidence Credential Architecture

## 1. 核心结论

在当前产品边界下：

```text
No backend database.
No backend application server.
Frontend pages + smart contracts only.
```

因此，平台不是传统考试平台，也不是传统 LMS。

更准确的定位是：

```text
Frontend-only Evidence Credential
```

中文：

```text
纯前端证据型能力证书
```

它的可信基础不是“后台保存成绩”，而是：

```text
公开任务
本地生成证据包
钱包签名
hash 上链
Issuer / Evaluator 签发
Verifier 合约验证
```

---

## 2. 数据三分法

### 2.1 可以直接放前端的公共资源

这些可以放在静态 HTML / JS / JSON 文件里：

```text
练习题题面
开放式项目任务说明
模拟 CSV
模拟贸易文件
评分 rubric 的公开部分
证书 schema
Evidence Package schema
ProofCredential schema
智能合约 ABI
合约地址
前端 hash 规则
Verifier 页面逻辑
```

这些内容本质上是教材、任务包、前端资源，不需要保密。

### 2.2 用户本地生成的私有数据

这些不上链，也不进入后端数据库，因为没有后端：

```text
原始作答
项目提交文件
数据分析报告
贸易单证 review 结果
完整分项成绩
Agent / Evaluator 评分明细
Evidence Package 原文
```

它们可以存在于：

```text
浏览器内存
localStorage
IndexedDB
用户本地下载的 JSON evidence bundle
用户钱包签名的数据包
加密后的本地 evidence bundle
可选的加密 IPFS / Arweave 文件
```

### 2.3 智能合约保存的最小证明

合约只保存：

```text
credentialId
credentialType
issuer
holder
certificateHash
evidenceHash
scoreHash
schemaHash
overallScore or scoreBand
issuedAt
expiresAt
status
revocationStatus
```

不保存：

```text
原始答案
项目文件
贸易单据
CSV 明细
个人身份信息
企业敏感信息
完整评分解释
```

---

## 3. 为什么不能做传统闭卷考试

如果题库、答案和评分逻辑都在前端，那么任何用户都可以查看源码或网络资源。

所以当前架构不适合：

```text
传统闭卷考试
高风险资格认证
需要强防作弊的考试
依赖答案保密的测评
```

当前架构适合：

```text
开放题库
项目制评测
作品集评测
Evidence Package
Verifier 复核
Issuer / Evaluator 签发
链上 proof
```

一句话：

```text
不要靠题目保密建立可信度。
要靠证据、签名、hash、时间戳、Verifier 和 Issuer 信任建立可信度。
```

---

## 4. 前端 Evidence Bundle

前端应生成一个 Evidence Bundle。

示例：

```json
{
  "bundleType": "EvidenceBundle",
  "schemaVersion": "evidence-bundle-v1",
  "credentialType": "AI_DATA_ANALYSIS_ASSISTANT",
  "learnerDid": "did:example:holder-mia-chen",
  "assessmentId": "data-assessment-v1",
  "projectTaskId": "sales-mini-bi-report-v1",
  "outputs": {
    "metricDefinitionHash": "0x...",
    "insightSummaryHash": "0x...",
    "anomalyNotesHash": "0x...",
    "dataRiskNoteHash": "0x..."
  },
  "score": {
    "overallScore": 86,
    "scoreBand": "Strong",
    "moduleScores": {
      "DA1_Data_Literacy": 90,
      "DA2_Spreadsheet_Reasoning": 84,
      "DA3_AI_Assisted_Analysis": 88,
      "DA5_Data_Quality_Risk": 86
    },
    "rubricVersion": "data-rubric-v1"
  },
  "createdAt": "2026-07-03T00:00:00Z"
}
```

前端从它计算：

```text
evidenceHash = keccak256(canonical EvidenceBundle)
scoreHash = keccak256(canonical score object)
certificateHash = keccak256(canonical certificate object)
schemaHash = keccak256(schemaVersion + credentialType + rubricVersion)
```

---

## 5. Issuer / Evaluator 信任问题

纯前端有一个关键问题：

```text
如果学习者自己在浏览器里算分并自己上链，Verifier 只能看到这是 self-attested credential。
```

这可以作为低信任证书，但不能作为高信任证书。

因此需要分三种信任等级。

### 5.1 Level 1: Self-attested Credential

```text
学习者本地完成任务
学习者自己生成 Evidence Bundle
学习者自己注册 hash
issuer = learner wallet
```

适合：

```text
作品集
学习记录
低风险技能展示
自我证明
```

Verifier 看到：

```text
Self-attested
```

### 5.2 Level 2: Issuer-attested Credential

```text
学习者提交 Evidence Bundle 给 Issuer / Training Partner
Issuer 用自己的 wallet 审核并调用 registerCredentialProof
issuer = authorized issuer wallet
```

适合：

```text
培训机构证书
企业内部培训
合作方认证
付费证书
```

Verifier 看到：

```text
Issuer-attested by authorized issuer
```

### 5.3 Level 3: Evaluator-signed Credential

```text
Evidence Bundle 由一个或多个 evaluator 签名
合约记录 evaluator signature hash 或 evaluator address
issuer 汇总签发
```

适合：

```text
高价值项目制评测
企业招聘场景
B2B 认证
```

Verifier 看到：

```text
Issuer-attested + evaluator-signed
```

---

## 6. 无后端情况下如何有 Issuer

没有后端不等于没有 Issuer。

Issuer 可以是：

```text
平台官方钱包
培训机构钱包
企业 L&D 钱包
DAO / multisig 钱包
合作方机构钱包
人工评审员钱包
```

它们不需要后台数据库，只需要：

```text
前端页面
钱包
合约权限
本地或去中心化的 evidence bundle
```

Issuer 审核后直接通过钱包签发上链。

---

## 7. 真实版本的评分来源

如果没有后端，评分来源可以有几种：

| 模式 | 说明 | 信任等级 |
| --- | --- | --- |
| Deterministic frontend scoring | 选择题、字段匹配、规则评分在前端执行 | 低到中 |
| Learner self-attested score | 用户自己生成分数并上链 | 低 |
| Issuer-reviewed score | Issuer 通过前端审核 evidence 后签发 | 中高 |
| Evaluator-signed score | 多个评审员签名评分 | 高 |
| BYOK browser AI scoring | 用户在浏览器里调用自己的 AI key | 低到中，需要 issuer 复核 |
| Local model scoring | 本地模型评分 | 中，仍需签名与复核 |

第一版建议：

```text
公开任务 + 前端 mock scoring + Issuer-attested contract proof
```

也就是说，v7 原型先展示 Level 2，而不是声称完全自动可信。

---

## 8. 前端文件组织建议

未来静态资源可以这样组织：

```text
docs/prototypes/v7-static-founder-demo.html
public/credentials/data-analysis/questions.json
public/credentials/data-analysis/project-task.json
public/credentials/data-analysis/rubric.json
public/credentials/trade-docs/questions.json
public/credentials/trade-docs/project-task.json
public/credentials/trade-docs/rubric.json
public/contracts/ProofSkillCredentialRegistry.abi.json
public/contracts/deployment.json
```

第一版可以先单 HTML，后续再拆。

---

## 9. Verifier 的真实验证逻辑

Verifier 不是相信页面显示，而是相信：

```text
1. issuer 是否是可信地址
2. credentialId 是否存在
3. status 是否 active
4. revocationStatus 是否 not_revoked
5. expiresAt 是否未过期
6. certificateHash 是否匹配
7. evidenceHash 是否匹配
8. scoreHash 是否匹配
9. schemaHash 是否匹配
10. signer / issuer / evaluator 是否满足信任等级
```

如果学习者只给 hash，而不给 Evidence Bundle，Verifier 只能验证“某个 hash 上链存在”。

如果学习者授权展示 Evidence Summary 或提供加密 evidence bundle，Verifier 才能重新计算 hash 并核对。

---

## 10. 产品文案修改

应把平台描述为：

```text
Frontend-only evidence credential infrastructure.
```

而不是：

```text
Online exam platform.
```

应强调：

```text
Open tasks
Local evidence
Issuer wallet attestation
Smart contract proof registry
Verifier-side validation
```

---

## 11. v7 原型需要补充的页面信息

v7 HTML 原型需要继续补：

```text
Public task bundle lives in frontend
Private evidence bundle stays local
Issuer wallet signs proof registration
Self-attested vs issuer-attested badge
Verifier trust level display
```

---

## 12. 结论

当前正确架构是：

```text
前端：公开任务、练习题、rubric、schema、ABI、hash 逻辑
用户本地：作答、项目文件、成绩明细、Evidence Bundle
Issuer / Evaluator 钱包：签发或评审证明
智能合约：hash、状态、issuer、holder、scoreBand / overallScore
Verifier：读取合约并验证 hash / issuer / status
```

这不是传统后台考试系统。

这是：

```text
Frontend-only Evidence Credential + Smart Contract Proof Registry
```
