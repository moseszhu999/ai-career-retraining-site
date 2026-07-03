# Deploy v8.2 Prototype to Vercel

## Recommendation

Use Vercel for the online prototype.

Why:

```text
Vercel gives preview URLs.
Vercel connects directly to GitHub.
Every commit / PR can create a preview deployment.
The current app is static HTML/CSS/JS, so no backend is needed.
Later we can migrate to Vite / React without changing hosting direction.
```

## Current app entry

```text
docs/prototypes/v8-app/index.html
```

## Option A: Deploy from repository root

This repository now includes:

```text
vercel.json
```

It rewrites:

```text
/ -> /docs/prototypes/v8-app/index.html
/:path* -> /docs/prototypes/v8-app/:path*
```

So if Vercel imports the repository root, the prototype should open from:

```text
/
```

No build command is required.

## Option B: Deploy only the app folder

In Vercel project settings:

```text
Root Directory: docs/prototypes/v8-app
Framework Preset: Other
Build Command: empty
Output Directory: empty or .
Install Command: empty
```

This is simpler if we only want to publish the prototype app.

## Recommended for now

Use Option A while this repo still contains docs and prototypes together.

Reason:

```text
vercel.json keeps the public URL clean
existing docs stay available in repo
main prototype opens directly at /
```

## Future migration

When we move from prototype to real app, create a dedicated app directory:

```text
apps/web
```

Then Vercel Root Directory can become:

```text
apps/web
```

## Boundary

This Vercel deployment is still static:

```text
No backend database.
No backend server.
No real wallet transaction.
No real RPC.
No real deployed contract interaction.
```

It is for visual and workflow validation first.
