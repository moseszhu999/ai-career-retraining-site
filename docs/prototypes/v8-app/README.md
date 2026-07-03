# v8-app Preview and Deployment Notes

## Current online prototype

Vercel preview:

```text
https://ai-career-retraining-site-5y5mhcxdv-aaronzhu1.vercel.app/docs/prototypes/v8-app
```

Do not change this route yet.

## Current prototype

Open locally:

```bash
open docs/prototypes/v8-app/index.html
```

Or open the launcher:

```bash
open docs/prototypes/index.html
```

The launcher points to:

```text
docs/prototypes/v8-app/index.html
```

## Manual demo flow

### Level 2 issuer-attested flow

```text
1. Open Learner role.
2. Click Generate Evidence Bundle.
3. Click Compute Hashes.
4. Click Request Issuer Attestation.
5. Switch to Issuer role.
6. Click Approve Evidence.
7. Click Issue IssuerAttested Proof.
8. Switch to Verifier role.
9. Click Read Contract.
10. Confirm status = active and trust level = IssuerAttested.
```

### Level 3 evaluator-signed flow

```text
1. Switch to Evaluator role.
2. Click Assign Review.
3. Click Sign Evaluation.
4. Switch to Issuer role.
5. Click Issue EvaluatorSigned Proof.
6. Switch to Verifier role.
7. Click Read Contract.
8. Confirm status = active and trust level = EvaluatorSigned.
```

## v8.3 online polish

v8.3 adds Bootstrap toast feedback for key actions:

```text
role switch
generate evidence
compute hashes
request issuer attestation
approve evidence
issue proof
sign evaluation
read contract
reset mock state
```

## Why this is not Streamlit

This app is intended to become a browser-first platform:

```text
frontend pages
wallet
smart contract
on-chain proof
no backend database
no backend application server
```

Streamlit would require a Python app server, so it is not the correct host for the user-facing platform.

## Recommended online deployment options

### Option A: GitHub Pages

Use this when we want a quick public prototype from the repository.

Recommended source:

```text
branch: main or waterfall-togaf-rebuild after merge
folder: /docs
```

Then open:

```text
/prototypes/
```

Current launcher:

```text
docs/prototypes/index.html
```

### Option B: Vercel

Use this when we want preview URLs for every commit / branch.

Suggested root directory:

```text
docs/prototypes/v8-app
```

No build command is required for the current static prototype.

### Option C: Netlify

Use this when we want a drag-and-drop static deployment or connected Git deploy.

Suggested publish directory:

```text
docs/prototypes/v8-app
```

No build command is required for the current static prototype.

## Current boundary

```text
No backend database.
No backend server.
No real wallet connection.
No real chain transaction.
No real deployed contract interaction.
No real exam.
No real agent scoring.
```

## Next recommended step

After the online workflow is stable, move toward:

```text
v8.4 task data extraction
```

That means moving hardcoded task/rubric/evidence demo content into static JSON files while keeping the app frontend-only.
