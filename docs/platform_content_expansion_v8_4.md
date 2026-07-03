# v8.4 Platform Content Expansion：从骨架补成可演示平台

## 1. Problem

v8.3 已经上线，但仍然只是平台骨架：

```text
有角色
有状态
有 toast
有基础按钮
```

问题是：

```text
业务内容太薄。
不像一个真正的职业再培训 / 可信证书平台。
```

v8.4 要补真实感。

---

## 2. Goal

把当前 Bootstrap-first app 扩展为：

```text
有证书路径
有课程 / 项目任务
有 Evidence Builder
有 Rubric
有 Issuer Review Detail
有 Evaluator Scoring Detail
有 Verifier Credential Detail
有 Admin Contract Config
```

仍然保持：

```text
纯前端
Bootstrap-first
无后端数据库
无后台程序
无真实链交易
无真实 RPC
```

---

## 3. Content model

新增静态 mock data：

```text
mock-data.js
```

包含：

```text
credentialPaths
projectTasks
rubrics
learners
reviewQueue
contractRecords
issuerRegistry
schemaVersions
```

---

## 4. Role improvements

### Learner

补充：

```text
Credential Path cards
Task checklist
Evidence Builder fields
Score breakdown
Hash preview
```

### Issuer

补充：

```text
Review Queue
Evidence detail panel
Hash comparison
Issuer decision checklist
Contract call preview
```

### Evaluator

补充：

```text
Rubric scoring table
Risk flags
Review comments
Signature preview
```

### Verifier

补充：

```text
Credential detail
Trust explanation
Hash match checklist
Issuer authorization status
Verification receipt
```

### Admin

补充：

```text
Issuer registry
Schema versions
Rubric versions
Contract configuration
Event log
```

---

## 5. Acceptance criteria

```text
打开线上页面后，看起来像一个真实平台，而不是空壳。
每个角色至少有一个完整业务区域。
每个角色能看到不同业务数据。
用户能跟着页面走完整 demo。
所有 UI 仍然使用 Bootstrap 组件。
```
