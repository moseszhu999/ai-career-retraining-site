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

## Product resource library

The repository includes a unified resource index:

```text
product_resource_library.md
```

Use it as the main navigation document for:

```text
sales
lead follow-up
two-hour trial lesson delivery
5-day skill growth camp
5-day freelance monetization camp
enterprise AI training
compliance boundaries
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

## Entry product: 2-hour trial lesson

The site includes a dedicated page for:

```text
AI 技能成长 2 小时体验课
Recommended price: 99 / 199 RMB
```

Trial lesson promise:

```text
1. diagnose one skill goal
2. turn the goal into one micro real task
3. use AI to create the first draft
4. run one round of AI feedback and revision
5. produce one small visible artifact
6. recommend the next learning path
```

Example trial tasks:

```text
promotion report outline
job-switching portfolio sample
freelance service package draft
sales script
test case / bug report
Japanese business email
team AI workflow template
```

## Main paid product: 5-day skill growth camp

The repository includes a full 5-day curriculum:

```text
five_day_skill_growth_camp_curriculum.md
```

Positioning:

```text
2-hour trial lesson
-> 5-day skill growth camp
-> 4-week advanced cohort / freelance monetization camp / enterprise training
```

5-day camp promise:

```text
1 skill growth roadmap
3 visible portfolio artifacts
1 AI feedback revision record
1 outcome presentation script
1 30-day action plan
1 instructor review
```

Recommended price:

```text
3999 RMB
```

## Freelance monetization camp

The repository includes a full 5-day freelance monetization curriculum:

```text
five_day_freelance_monetization_camp_curriculum.md
```

Positioning:

```text
skill learning
-> sample artifacts
-> service package
-> quote sheet
-> client outreach script
-> delivery SOP
-> review and price-up path
```

5-day freelance camp promise:

```text
1 sellable service package
3 sample cases
1 quote sheet
1 client outreach script / profile intro
1 client requirement checklist
1 delivery SOP
1 review and price-up plan
```

Recommended price:

```text
4999 RMB
```

## Enterprise AI training program

The repository includes a full B2B enterprise training outline:

```text
enterprise_ai_training_program_outline.md
```

Positioning:

```text
AI lecture
-> enterprise sample class
-> department training camp
-> customized enterprise AI skill system
```

Enterprise product tiers:

```text
sample class: 3000 - 8000 RMB
department training camp: 30000 RMB+
custom enterprise training: 50000 - 200000 RMB+
```

Enterprise deliverables:

```text
AI skill map
high-frequency task list
AI workflow templates
prompt template library
employee practice tasks
scoring standards
sample outputs
common error library
presentation templates
training review report
follow-up recommendations
```

## Instructor manual

The repository includes a full instructor delivery manual:

```text
trial_lesson_instructor_manual.md
```

It covers:

```text
lesson goal
pre-class preparation
standard 120-minute flow
opening script
goal diagnosis questions
six trial task templates
AI feedback standards
closing script
post-class record template
qualification standards
compliance boundaries
```

## Sales follow-up SOP

The site includes a dedicated `跟进SOP` page for converting Feishu / WeCom leads into paid trial lessons.

It covers:

```text
lead status pipeline
5-minute first reply scripts
qualification questions
booking and payment scripts
after-class conversion scripts
objection handling
Feishu follow-up record template
```

Recommended lead statuses:

```text
新线索
已联系
已约时间
已付款
已上课
已转化
未转化
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
