# v9 Demo QA Checklist

Scope: Bootstrap navigation, guided demo, printable outputs, and stable prototype handoff.

## 1. Entry

- Open `/docs/prototypes/v8-app#overview`.
- Confirm Overview loads first.
- Confirm left menu renders Bootstrap Accordion groups.
- Confirm mobile select still switches workspace.

## 2. Bootstrap menu

- Platform -> Overview opens overview.
- Learning & Credential -> Learner Workspace opens Learner.
- Learner -> Learning opens learner learning tab.
- Learner -> My Path opens learner path tab.
- Learner -> Practice Lab opens learner practice tab.
- Learner -> Evidence opens learner evidence tab.
- Learner -> Certificate / PDF opens learner certificate tab.
- Operations & Review -> Issuer -> Learning Ops scrolls to cohort monitor.
- Operations & Review -> Issuer -> Review Queue scrolls to review queue.
- Operations & Review -> Issuer -> Contract Actions scrolls to contract actions.
- Operations & Review -> Evaluator -> Assignment scrolls to assignment.
- Operations & Review -> Evaluator -> Rubric Review scrolls to rubric.
- Verification -> Verifier -> Proof Check scrolls to proof check.
- Verification -> Verifier -> Role-fit Signals scrolls to signal matrix.
- Verification -> Verifier -> Receipt Preview scrolls to receipt preview.
- Governance -> Admin -> Curriculum Builder scrolls to curriculum.
- Governance -> Admin -> Quiz Bank scrolls to quiz bank.
- Governance -> Admin -> Practice Templates scrolls to practice templates.
- Governance -> Admin -> Issuer Registry scrolls to issuer registry.

## 3. Guided demo route

- Run next demo step from Overview.
- Step 1 opens Overview.
- Step 2 opens Admin curriculum section.
- Step 3 opens Learner learning.
- Step 4 marks quiz state.
- Step 5 opens Practice Lab.
- Step 6 opens Evidence.
- Step 7 opens Issuer Learning Ops.
- Step 8 opens Issuer Contract Actions.
- Step 9 opens Evaluator Rubric Review.
- Step 10 opens Verifier Role-fit Signals.

## 4. Learner exports

- Learner -> Practice Lab -> Download worksheet PDF opens printable worksheet.
- Learner -> Certificate / PDF -> Download sealed certificate PDF opens printable certificate.
- Certificate shows visual issuer seal.
- Browser Save as PDF works.

## 5. State reset

- Reset mock state returns current workspace to initial local state.
- Restart demo returns to Overview and demo step 0.

## Boundary

This is a static browser prototype. It does not persist to a server, connect a wallet, or write a real contract transaction.
