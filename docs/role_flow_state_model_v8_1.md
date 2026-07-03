# v8.1 Role Flow and State Model：把角色平台做成有状态流程

## 1. 本版目标

v8.0 已经把产品从展示页纠正为：

```text
Role-based frontend platform
+
Smart contract proof registry
+
No backend database
+
No backend application server
```

但 v8.0 仍然偏“角色仪表盘静态切换”。下一步要让平台更像真实产品：

```text
每个角色有自己的子菜单。
每个角色有自己的状态。
按钮点击后流程状态变化。
不同角色之间通过 mock state 产生联动。
```

目标不是做后端，而是做：

```text
frontend state machine prototype
```

---

## 2. 核心状态对象

第一版前端状态可以使用 localStorage / in-memory mock。

建议状态：

```json
{
  "currentRole": "learner",
  "wallet": {
    "connected": true,
    "address": "0xLearnerMock"
  },
  "evidenceBundle": {
    "status": "not_generated",
    "evidenceHash": null,
    "scoreHash": null,
    "certificateHash": null
  },
  "issuerReview": {
    "status": "not_requested"
  },
  "evaluatorReview": {
    "status": "not_assigned",
    "evaluatorSetHash": null
  },
  "contractProof": {
    "status": "not_registered",
    "attestationLevel": null,
    "credentialId": null,
    "txHash": null
  }
}
```

---

## 3. 平台状态机

### 3.1 Learner flow

```text
not_started
-> task_opened
-> evidence_generated
-> hashes_computed
-> issuer_requested
-> proof_registered
-> shared_to_verifier
```

Learner 操作：

```text
Open Task
Generate Evidence Bundle
Compute Hashes
Request Issuer Attestation
Self-attest Low Trust
Share Proof Link
```

### 3.2 Issuer flow

```text
no_request
-> review_pending
-> evidence_reviewed
-> proof_issued
-> revoked
```

Issuer 操作：

```text
Open Review
Approve Evidence
Issue IssuerAttested Proof
Issue EvaluatorSigned Proof
Revoke Credential
```

### 3.3 Evaluator flow

```text
not_assigned
-> review_assigned
-> scoring_in_progress
-> evaluation_signed
-> evaluator_set_ready
```

Evaluator 操作：

```text
Open Assignment
Score with Rubric
Sign Evaluation
Submit Signature to Issuer
```

### 3.4 Verifier flow

```text
empty
-> credential_entered
-> contract_read
-> proof_valid
-> proof_invalid
-> receipt_generated
```

Verifier 操作：

```text
Enter Credential ID
Read Contract
Check Hash Match
View Trust Level
Generate Verification Receipt
```

### 3.5 Admin flow

```text
contract_ready
-> issuer_added
-> issuer_removed
-> schema_updated
```

Admin 操作：

```text
Authorize Issuer
Remove Issuer
Publish Schema Version
View Events
```

---

## 4. 角色联动

平台感的关键不是单角色页面，而是角色之间联动。

### 4.1 Learner -> Issuer

```text
Learner clicks Request Issuer Attestation
-> issuerReview.status = review_pending
-> Issuer dashboard queue count +1
```

### 4.2 Evaluator -> Issuer

```text
Evaluator clicks Sign Evaluation
-> evaluatorReview.status = evaluator_set_ready
-> evaluatorSetHash generated
-> Issuer can issue EvaluatorSigned proof
```

### 4.3 Issuer -> Contract -> Verifier

```text
Issuer clicks Issue Proof
-> contractProof.status = active
-> credentialId generated
-> Verifier can read valid proof
```

### 4.4 Admin -> Issuer

```text
Admin authorizes issuer
-> issuer wallet becomes valid issuer
-> Issuer can issue proofs
```

---

## 5. v8.1 原型文件

建议新增：

```text
docs/prototypes/v8-role-based-platform-stateful.html
```

它应该比 v8.0 多：

```text
role-specific subnavigation
local mock state
state badges
buttons that mutate state
cross-role mock linkage
activity log
```

---

## 6. 不做事项

v8.1 仍然不做：

```text
真实后端
真实数据库
真实钱包连接
真实 RPC
真实链交易
真实考试评分
真实 AI Agent
```

但要模拟真实流程：

```text
按钮推动状态
状态改变页面
不同角色看到同一个 mock credential 的不同视图
```

---

## 7. 验收标准

```text
选择 Learner 后能生成 Evidence Bundle。
点击 Request Issuer 后，Issuer 队列能看到 pending。
选择 Evaluator 后能签名并生成 evaluatorSetHash。
选择 Issuer 后能 issue proof。
选择 Verifier 后能看到 proof active、trust level 和 hash match。
选择 Admin 后能看到 issuer registry 和 contract events。
```

---

## 8. 结论

v8.1 的重点是：

```text
从 role dashboard prototype
升级为
role workflow state-machine prototype
```

这才更接近真正网站。
