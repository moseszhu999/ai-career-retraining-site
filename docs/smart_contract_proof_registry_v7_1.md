# v7.1 Smart Contract Proof Registry Architecture

## 1. 关键纠偏

当前平台已经明确：

```text
No backend database.
No backend application server.
Frontend pages + smart contracts only.
```

因此，证书、成绩、Evidence Package 的可信性不能依赖中心化数据库。

正确结构应该是：

```text
Learner browser / frontend
-> computes hashes from exam result, project result, agent score, evidence package
-> wallet signs / submits proof transaction
-> smart contract stores proof record
-> verifier reads contract state and compares hashes
```

也就是说，v7 原型里的 Proof Registry 不是一个后台表，而应该映射到智能合约 Registry。

---

## 2. 不能上链的数据

为了保护隐私和商业敏感信息，以下内容不上链：

```text
raw exam answers
raw project files
raw trade documents
raw CSV data
personal identity documents
enterprise customer data
full learner profile
full agent rationale text
```

---

## 3. 可以上链的数据

链上只保存最小证明信息：

```text
credentialId
credentialType
issuer address
holder address
certificateHash
evidenceHash
scoreHash
schemaHash
overallScore or scoreBand
issuedAt
expiresAt
status
revocation status
```

其中：

```text
certificateHash = keccak256(canonical certificate JSON)
evidenceHash = keccak256(canonical evidence package JSON)
scoreHash = keccak256(canonical score breakdown JSON)
schemaHash = keccak256(schema version + rubric version + credential type)
```

---

## 4. 成绩链上证明

成绩不一定要把完整分项明文上链。

第一版建议：

```text
overallScore: 可选明文上链，例如 86
scoreHash: 必须上链，用于证明完整成绩明细没有被篡改
scoreBand: 可在前端 / verifier 页面显示，例如 Strong
```

这样既能让 Verifier 看到一个大概能力等级，又不会把完整考试答案和评分细节公开。

示例：

```json
{
  "overallScore": 86,
  "scoreBand": "Strong",
  "moduleScores": {
    "Data Literacy": 90,
    "Spreadsheet Reasoning": 84,
    "AI-assisted Analysis": 88,
    "Data Quality & Risk": 86
  },
  "agentScoreId": "agent_score_data_001",
  "rubricVersion": "data-rubric-v1"
}
```

链上保存：

```text
overallScore = 86
scoreHash = keccak256(the canonical JSON above)
```

---

## 5. 前端职责

由于没有后端，前端必须承担以下职责：

```text
load mock / real local assessment result
canonicalize certificate object
canonicalize evidence package object
canonicalize score object
compute certificateHash
compute evidenceHash
compute scoreHash
connect wallet
call smart contract registerCredentialProof
show tx hash / registry status
```

第一版静态原型中，这些都是 mock；后续真实版本中由浏览器完成。

---

## 6. 智能合约职责

智能合约只做可信登记与状态管理：

```text
registerCredentialProof
revokeCredential
expireCredential / status read
getCredentialProof
verifyCredentialProof
emit CredentialProofRegistered
emit CredentialProofRevoked
```

合约不做：

```text
不保存原始考试答案
不保存原始文件
不计算考试分数
不调用 AI
不保存用户个人资料
不做课程系统
不做数据库
```

---

## 7. Verifier 验证流程

Verifier 拿到分享链接或 QR 后：

```text
1. 读取 credentialId。
2. 前端调用合约 getCredentialProof。
3. 检查 issuer 是否可信。
4. 检查 status 是否 active。
5. 检查 revocationStatus 是否 not_revoked。
6. 检查 expiresAt 是否未过期。
7. 如果 learner 授权展示 Evidence Summary，前端重新计算 evidenceHash / scoreHash。
8. 与链上 hash 比对。
9. 展示 verified / mismatch / revoked / expired。
```

---

## 8. 合约字段建议

```solidity
struct CredentialProof {
    bytes32 credentialId;
    bytes32 certificateHash;
    bytes32 evidenceHash;
    bytes32 scoreHash;
    bytes32 schemaHash;
    address issuer;
    address holder;
    string credentialType;
    uint16 overallScore;
    uint64 issuedAt;
    uint64 expiresAt;
    ProofStatus status;
}
```

---

## 9. 两个 MVP 的链上记录示例

### 9.1 AI Data

```json
{
  "credentialId": "0xDATA_CREDENTIAL_ID_MOCK_001",
  "credentialType": "AI_DATA_ANALYSIS_ASSISTANT",
  "holder": "0xLearnerMiaMock",
  "overallScore": 86,
  "certificateHash": "0xCERT_HASH_DATA_MOCK_001",
  "evidenceHash": "0xEVIDENCE_HASH_DATA_MOCK_001",
  "scoreHash": "0xSCORE_HASH_DATA_MOCK_001",
  "status": "active"
}
```

### 9.2 Cross-border Trade

```json
{
  "credentialId": "0xTRADE_CREDENTIAL_ID_MOCK_001",
  "credentialType": "AI_TRADE_DOCUMENTATION_COMPLIANCE_ASSISTANT",
  "holder": "0xLearnerAaravMock",
  "overallScore": 88,
  "certificateHash": "0xCERT_HASH_TRADE_MOCK_001",
  "evidenceHash": "0xEVIDENCE_HASH_TRADE_MOCK_001",
  "scoreHash": "0xSCORE_HASH_TRADE_MOCK_001",
  "status": "active"
}
```

---

## 10. v7 HTML 原型应展示的内容

v7 静态原型中的 Proof Registry 区域应升级为：

```text
Smart Contract Proof Registry
```

并展示：

```text
frontend-generated certificate hash
frontend-generated evidence hash
frontend-generated score hash
mock wallet submit
mock contract event
mock verifier read
```

页面文案：

```text
No backend database is required. The frontend computes hashes from certificate, evidence, and score objects, then registers those hashes in a smart contract proof registry.
```

中文：

```text
不需要后端数据库。前端根据证书、证据包和成绩对象计算 hash，然后把这些 hash 登记到智能合约 Proof Registry 中。
```

---

## 11. 实现边界

当前 v7 原型仍然是 mock：

```text
no real wallet
no real transaction
no real deployed contract
no real chain RPC
no real scoring
```

但它必须在产品结构上表达：

```text
frontend-only app + smart contract proof registry
```

而不是：

```text
frontend + hidden backend database
```

---

## 12. 下一步

本文件之后应新增 Solidity 草案：

```text
contracts/ProofSkillCredentialRegistry.sol
```

并更新：

```text
docs/prototypes/v7-static-founder-demo.html
```

把 Proof Registry 区域改为 Smart Contract Proof Registry，并加入成绩链上证明 mock。
