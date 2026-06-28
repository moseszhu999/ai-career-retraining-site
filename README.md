# AI Skill Growth Education Platform

Public Streamlit landing page for:

```text
AI 技能成长教育平台
用 AI 更快学会新技能，并做出可展示、可交付、可变现的成果。
```

## Streamlit deploy settings

Use Streamlit Community Cloud with:

```text
Repository: moseszhu999/ai-career-retraining-site
Branch: main
Main file path: streamlit_app.py
Python: 3.12
```

## Product positioning

This is not limited to new hires.

The platform is for working professionals and freelancers who need to:

```text
learn new skills
improve current skills
prepare for promotion
switch jobs or roles
pursue higher-paying opportunities
learn monetizable freelance skills
package services and deliver client work
build visible work artifacts
```

## Core learning loop

```text
set skill goal
learn with AI
practice real tasks
receive AI feedback
revise output
build portfolio artifacts
package the skill into work or service value
present the result
```

## Lead capture

The booking page supports:

```text
booking form
consultation summary
TXT download
CSV download
mailto link
session lead table
optional webhook submission
```

## Mainland-first lead saving

For mainland China use cases, do **not** make Google Sheet the primary option.

Recommended options:

```text
1. Feishu / Lark robot webhook
2. WeCom / Enterprise WeChat robot webhook
3. Tencent Cloud Function
4. Alibaba Cloud Function
5. Self-hosted backend API
6. Tencent Docs / WPS / Kingsoft form workflow via CSV import
```

### Optional Streamlit Secrets

Feishu / Lark robot:

```toml
LEAD_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
WEBHOOK_PROVIDER = "feishu"
OWNER_EMAIL = "your-email@example.com"
```

WeCom / Enterprise WeChat robot:

```toml
LEAD_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"
WEBHOOK_PROVIDER = "wecom"
OWNER_EMAIL = "your-email@example.com"
```

Generic backend API, Tencent Cloud Function, Alibaba Cloud Function, Supabase, etc.:

```toml
LEAD_WEBHOOK_URL = "https://your-api-endpoint"
WEBHOOK_PROVIDER = "generic"
OWNER_EMAIL = "your-email@example.com"
```

If `LEAD_WEBHOOK_URL` is not configured, the site still works, but leads must be downloaded as TXT/CSV or sent manually.

## Freelancer monetization loop

```text
skill learning
-> sample artifacts
-> service package
-> quote sheet
-> client outreach script
-> delivery SOP
-> review and price-up path
```

## Product promise

```text
Help professionals and freelancers use AI to learn and improve job skills faster, then prove their ability through reviewable work outcomes, service packages, and career or income narratives.
```

## Compliance boundary

Do not sell this as:

```text
K12 tutoring
official certificate
guaranteed employment
salary guarantee
guaranteed freelance income
regulated professional qualification training
```
