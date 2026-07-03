# v8.3 Online Prototype Polish

## 1. Scope

The Vercel preview is now online:

```text
https://ai-career-retraining-site-5y5mhcxdv-aaronzhu1.vercel.app/docs/prototypes/v8-app
```

Do not change the Vercel route yet.

v8.3 focuses only on online usability polish:

```text
click feedback
state-change feedback
online URL documentation
prototype acceptance checklist
manual demo flow
```

---

## 2. Do not change yet

For this round, avoid:

```text
Vercel root routing changes
framework migration
React/Vite migration
wallet integration
real RPC integration
backend/database work
```

---

## 3. Online prototype checklist

The online prototype should make the following demo flow obvious:

```text
1. Open Learner role.
2. Generate Evidence Bundle.
3. Compute Hashes.
4. Request Issuer Attestation.
5. Switch to Issuer role.
6. Approve Evidence.
7. Issue IssuerAttested Proof.
8. Switch to Verifier role.
9. Read Contract.
10. Verify active proof and trust level.
```

Optional Level 3 flow:

```text
1. Switch to Evaluator role.
2. Assign Review.
3. Sign Evaluation.
4. Switch to Issuer role.
5. Issue EvaluatorSigned Proof.
6. Switch to Verifier role.
7. Verify EvaluatorSigned trust level.
```

---

## 4. UI polish items

Use Bootstrap components only:

```text
Toast for button feedback
Alert for online prototype boundary
Badge for state changes
Card for quick demo flow
List-group for role switching
```

No custom UI framework.

---

## 5. Acceptance criteria

```text
Every main action gives visible feedback.
User can follow a role flow without reading code.
Current online URL is documented.
No deployment route changes are required.
No backend/server is introduced.
```
