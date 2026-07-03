# v8-app Preview and Deployment Notes

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

After confirming the visual prototype, add a minimal deployment config:

```text
vercel.json
```

or configure GitHub Pages from `/docs`.
