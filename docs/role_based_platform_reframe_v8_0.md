# v8.0 Role-based Platform Reframe：从展示页改为真正平台

## 1. 本版目标

v7 系列把产品做成了 Founder / Sales Demo 展示页。这个方向不够，因为用户目标不是“展示页”，而是一个真正的平台。

正确方向应改为：

```text
Role-based frontend platform
+
Smart contract proof registry
+
No backend database
+
No backend application server
```

也就是说：

```text
不是所有人看同一个展示页。
而是不同角色进入后看到不同工作台、不同任务、不同合约操作。
```

---

## 2. 平台角色

第一版至少应包含 5 类角色。

### 2.1 Learner / Candidate

学习者 / 候选人。

能看到：

```text
我的证书路径
我的练习题
我的项目任务
我的本地 Evidence Bundle
我的分数
我的 proof 状态
我的钱包地址
我分享给 Verifier 的链接
```

能操作：

```text
选择证书路径
完成练习
完成项目任务
本地生成 Evidence Bundle
本地生成 certificateHash / evidenceHash / scoreHash
申请 Issuer 签发
自证明上链，低信任模式
分享验证链接
```

### 2.2 Issuer / Training Partner

签发方 / 培训机构 / 平台官方。

能看到：

```text
待审核 Evidence Bundle
学习者提交摘要
成绩和 rubric 结果
hash 预览
Issuer wallet 状态
待签发证书
已签发证书
被撤销证书
```

能操作：

```text
审核 Evidence Bundle
签发 issuer-attested credential
调用 registerIssuerAttestedProof
撤销 credential
查看签发历史
```

### 2.3 Evaluator / Reviewer

评审员 / 项目审核员。

能看到：

```text
待评审项目
项目提交摘要
评分 rubric
风险提示
评分草稿
evaluator signature preview
```

能操作：

```text
评分
添加评审意见
生成 evaluator signature
提交给 Issuer
形成 evaluatorSetHash
```

### 2.4 Verifier / Employer / Client

验证方 / 雇主 / 客户 / 学校 / 贸易金融方。

能看到：

```text
证书是否存在
合约状态
是否被撤销
是否过期
issuer 是否可信
attestation level
scoreHash 是否匹配
evidenceHash 是否匹配
授权后的 evidence summary
```

能操作：

```text
输入 credentialId / proof link
读取合约 proof record
查看 trust level
查看授权证据摘要
生成 verification receipt
```

### 2.5 Admin / Contract Owner

合约管理员 / 平台治理角色。

能看到：

```text
authorized issuers
deployed contract address
contract status
registry stats
revocation events
schema versions
```

能操作：

```text
授权 issuer wallet
移除 issuer wallet
查看合约事件
管理 schema/rubric version
```

---

## 3. 角色入口

平台首页不应是展示页，而应是角色入口：

```text
Choose your role

Learner / Candidate
Issuer / Training Partner
Evaluator / Reviewer
Verifier / Employer
Admin / Contract Owner
```

每个角色进入不同 dashboard。

---

## 4. 角色视图差异

### Learner Dashboard

```text
My Credential Paths
My Tasks
Local Evidence Bundle
Score Preview
Proof Status
Share Link
```

### Issuer Dashboard

```text
Review Queue
Pending Evidence Bundles
Issue Credential
Revoke Credential
Issuer Wallet
Contract Events
```

### Evaluator Dashboard

```text
Review Assignments
Rubric Scoring
Evaluator Signature
EvaluatorSetHash Preview
Submit Review
```

### Verifier Dashboard

```text
Verify Credential
Contract Proof Record
Trust Level
Hash Match
Evidence Summary
Verification Receipt
```

### Admin Dashboard

```text
Issuer Registry
Contract Configuration
Schema Versions
Rubric Versions
Event Monitor
```

---

## 5. 无后端架构下的角色状态

因为没有后端数据库，角色状态不能来自服务器 session。

第一版可以使用：

```text
前端 role selector
wallet address mock
localStorage role state
contract read state
static mock data
```

真实版本中：

```text
角色权限 = wallet address + contract authorization
```

例如：

```text
Learner: any connected wallet
Issuer: authorizedIssuers[address] == true
Evaluator: evaluator list or signature authority
Verifier: anyone can read proof record
Admin: contract owner / multisig
```

---

## 6. 平台页面结构

第一版 role-based 静态原型建议文件：

```text
docs/prototypes/v8-role-based-platform.html
```

页面区块：

```text
1. Role Select / Login Mock
2. Learner Dashboard
3. Issuer Dashboard
4. Evaluator Dashboard
5. Verifier Dashboard
6. Admin Dashboard
7. Smart Contract Registry
8. Static Boundary
```

---

## 7. 每个角色的主流程

### Learner flow

```text
Select credential path
Open project task
Generate local evidence bundle
Preview score
Compute hashes
Request issuer attestation
or self-attest to contract
Share proof link
```

### Issuer flow

```text
Open review queue
Inspect evidence summary
Confirm certificateHash / evidenceHash / scoreHash
Register issuer-attested proof
or register evaluator-signed proof
```

### Evaluator flow

```text
Open assigned project
Score with rubric
Sign evaluation
Generate evaluatorSetHash contribution
Submit to issuer
```

### Verifier flow

```text
Enter credentialId
Read contract
Check status / revocation / expiration
Check trust level
Check hash match
View authorized evidence summary
```

### Admin flow

```text
View authorized issuers
Authorize new issuer
Remove issuer
View contract events
View schema versions
```

---

## 8. 不能再做成营销页

后续原型原则：

```text
不要 Hero 大展示页优先。
不要所有内容堆成 sales landing。
不要把 Verifier 和 Proof 只是展示模块。
不要只讲价值主张。
```

应优先做：

```text
角色入口
角色 dashboard
角色操作按钮
角色可见数据差异
合约调用 mock
本地 evidence bundle mock
```

---

## 9. v8 原型验收标准

```text
打开页面后首先看到 Role Select。
选择不同角色后，主内容变化。
Learner 能看到自己的任务和本地 evidence。
Issuer 能看到待审核队列和签发按钮。
Evaluator 能看到评分任务和 evaluator signature。
Verifier 能看到合约验证结果。
Admin 能看到 issuer registry。
Smart Contract Registry 作为底层共享组件，而不是营销展示模块。
页面仍然无后端、无真实 API、无真实链交易。
```

---

## 10. 结论

v7 是 Founder/Sales Demo。

v8 必须升级为：

```text
Role-based frontend platform prototype
```

核心不是“展示我们有什么”，而是：

```text
不同角色进入平台后，各自完成自己的任务。
```
