# v7.3 Attestation Trust Levels：纯前端证据证书的信任等级落地

## 1. 本版目标

v7.2 已经明确：当前产品不是传统后台考试系统，而是：

```text
Frontend-only Evidence Credential
+
Smart Contract Proof Registry
```

但只说“证据上链”还不够。Verifier 真正关心的是：

```text
这个证书是谁证明的？
是学习者自己证明，还是机构证明？
有没有评审员签名？
合约里如何区分？
页面上如何展示？
```

本版把三种信任等级正式落到产品、合约和 Verifier 视图中。

---

## 2. 三层信任等级

### Level 1：Self-attested

学习者自己完成任务，自己生成 Evidence Bundle，自己把 hash 上链。

```text
issuer = learner wallet
holder = learner wallet
attestationLevel = SelfAttested
```

适合：

```text
作品集
学习记录
低风险能力展示
个人成长证明
```

Verifier 应看到：

```text
Self-attested by holder wallet.
No authorized issuer reviewed this credential.
```

### Level 2：Issuer-attested

授权机构审核 Evidence Bundle 后，用自己的 issuer wallet 签发。

```text
issuer = authorized issuer wallet
holder = learner wallet
attestationLevel = IssuerAttested
```

适合：

```text
培训机构证书
企业内部培训
付费证书
合作方认证
```

Verifier 应看到：

```text
Issuer-attested by authorized issuer.
```

### Level 3：Evaluator-signed

一个或多个评审员对 Evidence Bundle 或项目作品评分，形成 evaluator signature set，再由 issuer 汇总签发。

```text
issuer = authorized issuer wallet
holder = learner wallet
evaluatorSetHash = hash(evaluator addresses + score signatures + rubric version)
attestationLevel = EvaluatorSigned
```

适合：

```text
高价值项目制评测
招聘场景
B2B 认证
贸易单证项目审核
法律/合规类助理认证
```

Verifier 应看到：

```text
Issuer-attested + evaluator-signed.
Evaluator signature hash is recorded.
```

---

## 3. 合约字段升级

原 CredentialProof 需要新增：

```text
attestationLevel
evaluatorSetHash
```

升级后的核心结构：

```solidity
struct CredentialProof {
    bytes32 credentialId;
    bytes32 certificateHash;
    bytes32 evidenceHash;
    bytes32 scoreHash;
    bytes32 schemaHash;
    bytes32 evaluatorSetHash;
    address issuer;
    address holder;
    string credentialType;
    uint16 overallScore;
    uint64 issuedAt;
    uint64 expiresAt;
    ProofStatus status;
    AttestationLevel attestationLevel;
}
```

---

## 4. 注册函数分层

建议合约分三类注册函数：

```text
registerSelfAttestedProof
registerIssuerAttestedProof
registerEvaluatorSignedProof
```

### 4.1 registerSelfAttestedProof

任何钱包都可以调用。

```text
issuer = msg.sender
holder = msg.sender
attestationLevel = SelfAttested
```

### 4.2 registerIssuerAttestedProof

只有 authorizedIssuer 可以调用。

```text
issuer = msg.sender
holder = learner wallet
attestationLevel = IssuerAttested
```

### 4.3 registerEvaluatorSignedProof

只有 authorizedIssuer 可以调用，同时 evaluatorSetHash 不能为空。

```text
issuer = msg.sender
holder = learner wallet
evaluatorSetHash != 0
attestationLevel = EvaluatorSigned
```

---

## 5. 前端展示规则

### 5.1 Self-attested badge

```text
Self-attested
Low trust
Portfolio / learning record only
```

颜色：黄色 / 灰色。

### 5.2 Issuer-attested badge

```text
Issuer-attested
Authorized issuer reviewed
```

颜色：蓝色。

### 5.3 Evaluator-signed badge

```text
Evaluator-signed
Issuer + evaluator evidence
```

颜色：绿色 / teal。

---

## 6. Verifier 决策规则

Verifier 页面不能只显示 valid / invalid。

必须显示：

```text
contract status
revocation status
expiration status
issuer address
issuer authorization
attestation level
score hash match
evidence hash match
schema hash match
evaluator set hash, if any
```

Verifier 判断建议：

| Attestation Level | Trust Meaning | Product Wording |
| --- | --- | --- |
| SelfAttested | 用户自己声明 | Good for portfolio, not formal certification |
| IssuerAttested | 授权机构签发 | Suitable for training / employment screening |
| EvaluatorSigned | 机构 + 评审员证明 | Strongest project-based credential |

---

## 7. 两个 MVP 的默认信任等级

### AI Data Analysis Assistant

第一版建议默认：

```text
IssuerAttested
```

因为它适合培训机构或平台官方签发。

未来可支持：

```text
SelfAttested portfolio mode
EvaluatorSigned hiring mode
```

### Cross-border Trade Documentation

第一版建议默认：

```text
EvaluatorSigned
```

原因：贸易单证、供应链、贸易融资场景更需要人工或机构复核。

---

## 8. v7 原型应该补的展示

在 Founder Demo 中新增：

```text
Trust Level cards
Self-attested / Issuer-attested / Evaluator-signed comparison
Verifier result shows attestation level
Smart Contract section shows evaluatorSetHash
Founder Dashboard shows backend DB = 0, smart contract = 1, trust levels = 3
```

---

## 9. 结论

纯前端证据证书不是“大家自己随便上链”。

正确产品形态是：

```text
public frontend task bundle
local private evidence bundle
smart contract proof registry
issuer wallet attestation
evaluator signature set, optional
verifier trust-level display
```

这才能让无后端架构仍然具备可解释的信任分层。
