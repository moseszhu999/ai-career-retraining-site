# v4.16.1 BLM Value Chain Scope Correction

This note corrects the architecture wording from v4.16.0.

## 1. Correction

Value chain is not a separate architecture layer after BLM.

Correct:

```text
BLM includes value chain analysis.
```

Incorrect:

```text
BLM -> Value Chain -> Business Architecture
```

The external consulting architecture sequence remains:

```text
BLM
-> Business Process / Business Architecture
-> Application Architecture
-> Data Architecture
-> Technical Architecture
```

## 2. Role of Value Chain inside BLM

Value chain belongs inside BLM because it helps answer:

```text
where value is created
where cost is concentrated
where repeatable manual work exists
where AI Agent automation can create measurable improvement
where governance is needed before Agent outputs enter formal workflow
```

Therefore BLM should include:

```text
Market Insight
Strategic Intent
Value Chain Analysis
Innovation Focus
Business Design
Key Capabilities
KPI / Results
```

## 3. Correct Interpretation

The corrected logic is:

```text
BLM
  -> market insight
  -> strategic intent
  -> value chain analysis
  -> value-chain automation opportunities
  -> innovation focus
  -> business design
  -> KPI direction
-> Business Process / Business Architecture
  -> scenario process
  -> capability map
  -> operating model
  -> Agent automation map
  -> governance process
-> Application Architecture
-> Data Architecture
-> Technical Architecture
```

## 4. Why This Matters

If value chain is treated as a standalone layer, the architecture becomes too fragmented.

If value chain is embedded inside BLM, it becomes the strategic basis for selecting business processes and application modules.

That is the correct consulting logic:

```text
BLM uses value chain to decide what business processes should be transformed.
Business architecture describes how those processes work.
Application architecture supports those processes.
Data architecture models the objects and evidence.
Technical architecture implements the system.
```

## 5. Updated One-Line Positioning

```text
Use BLM value-chain analysis to identify enterprise work steps that AI Agents can automate, then design business processes, applications, data, and technology to govern those Agent outputs.
```

Chinese:

```text
在 BLM 中用价值链分析找出可由 AI Agent 自动化的企业工作环节，再按业务流程、应用架构、数据架构和技术架构落地治理系统。
```
