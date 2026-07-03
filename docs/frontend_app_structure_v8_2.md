# v8.2 Bootstrap-first Frontend App Structure

## 1. Decision

The v8.1 prototype proved the role-based state-machine flow, but it still behaved like a single-file prototype with too much custom layout CSS.

v8.2 moves toward a real frontend website structure and adopts a Bootstrap-first rule:

```text
Use Bootstrap components first.
Do not reinvent the UI system.
Custom CSS is allowed only for small brand-level polish.
```

---

## 2. Frontend-only boundary

The platform still keeps the core architecture:

```text
No backend database.
No backend application server.
No real wallet connection in prototype.
No real chain transaction in prototype.
No real RPC in prototype.
```

But the code organization should start looking like a real frontend application.

---

## 3. Bootstrap-first UI rule

Use Bootstrap for:

```text
Layout: container-fluid, row, col, g-*
Sidebar: list-group, nav-pills
Top bar: navbar, card, d-flex
Dashboards: card, row, col
Stats: card, badge
Tables: table, table-hover, align-middle
Forms: form-control, input-group, form-select
Actions: btn, btn-outline-*
Progress: progress, progress-bar
Status: badge, alert
Modal / offcanvas later: Bootstrap modal, offcanvas
Tabs later: nav-tabs / tab-pane
Responsive: Bootstrap grid and utilities
```

Avoid:

```text
Custom grid systems
Custom button systems
Custom badge systems
Custom table systems
Custom sidebar CSS frameworks
Large handwritten CSS layout framework
```

---

## 4. Proposed file structure

```text
docs/prototypes/v8-app/
  index.html
  app.css
  app.js
  mock-state.js
  contract-abi.js
  roles/
    learner.js
    issuer.js
    evaluator.js
    verifier.js
    admin.js
```

---

## 5. File responsibilities

### index.html

Owns only:

```text
Bootstrap import
page shell
role navigation placeholder
workspace placeholder
script loading order
```

### app.css

Only brand polish:

```text
body background
brand accent variable
minor card polish
small code block style
```

It must not recreate Bootstrap components.

### mock-state.js

Owns:

```text
initial state
load/save/reset state
state mutation helpers
activity log
```

### contract-abi.js

Owns:

```text
mock contract address
ABI draft
attestation enum labels
proof status labels
```

### app.js

Owns:

```text
role routing
workspace render orchestration
event binding
state refresh
```

### roles/*.js

Each role owns its dashboard HTML and actions:

```text
Learner: tasks, local evidence, request attestation
Issuer: queue, approve, issue proof
Evaluator: assignment, score, sign evaluation
Verifier: read contract, show trust level
Admin: issuer registry, contract events
```

---

## 6. v8.2 prototype acceptance criteria

```text
Uses Bootstrap 5.3.
Has separate files, not one giant HTML.
Role selection changes dashboard.
Buttons mutate frontend state.
Learner request appears in Issuer queue.
Evaluator signature creates evaluatorSetHash.
Issuer issuing proof updates Verifier result.
Admin action updates issuer/event state.
No backend/database/API/RPC required.
```

---

## 7. Next implementation target

Create:

```text
docs/prototypes/v8-app/index.html
```

and supporting JS/CSS files.

This becomes the main prototype going forward. The old single-file prototypes remain as archived checkpoints.
