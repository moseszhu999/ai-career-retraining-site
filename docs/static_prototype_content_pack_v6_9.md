# v6.9 Static Prototype Content Pack：静态原型内容与 Mock 数据

## 1. 本版目标

v6.8 已经定义静态原型页面结构。本版提供可直接放入未来 HTML / Streamlit / Figma 原型的内容包。

本文件仍然不写代码，只准备：

```text
页面文案
按钮文案
mock learner
mock verifier
mock question
mock project task
mock agent score
mock evidence package
mock certificate
mock proof credential
mock proof registry
mock verifier result
```

双 MVP：

```text
A. AI Data Analysis Assistant Certificate
B. AI Cross-border Trade Documentation & Compliance Assistant Certificate
```

---

## 2. 全站统一文案

### 2.1 Product tagline

```text
Verifiable AI-era skill certificates backed by tasks, evidence, agent scoring, and crypto proof.
```

中文：

```text
用任务、证据、Agent 评分和链上证明，签发可验证的 AI 时代能力证书。
```

### 2.2 Hero title

```text
Prove real work skills, not just course completion.
```

中文：

```text
证明真实工作能力，而不只是完成课程。
```

### 2.3 Hero subtitle

```text
Learners complete realistic tasks. Agents score structured evidence. Certificates become verifiable proof for employers, clients, schools, and partners.
```

中文：

```text
学习者完成真实任务，Agent 基于结构化证据评分，证书可被雇主、客户、学校和合作方验证。
```

### 2.4 CTA buttons

```text
Explore Certificates
Try Data Analysis Demo
Try Trade Documentation Demo
Verify a Credential
View Proof Registry
Founder Demo Route
```

### 2.5 How it works

```text
1. Choose a certificate path.
2. Complete practice and exam tasks.
3. Submit a realistic project.
4. Receive agent-scored evidence.
5. Claim a proof-backed credential.
6. Share with a verifier.
```

中文：

```text
1. 选择证书路径。
2. 完成练习和考试任务。
3. 提交一个真实项目任务。
4. 获得 Agent 自动评分和证据包。
5. 领取带 Proof 的证书。
6. 分享给验证方。
```

---

## 3. Mock Learners

```json
[
  {
    "learner_id": "learner_001",
    "display_name": "Mia Chen",
    "profile_type": "career_switcher",
    "target_certificate": "AI_DATA_ANALYSIS_ASSISTANT",
    "country": "Singapore",
    "status": "certificate_eligible"
  },
  {
    "learner_id": "learner_002",
    "display_name": "Aarav Patel",
    "profile_type": "trade_operations_assistant",
    "target_certificate": "AI_TRADE_DOCUMENTATION_COMPLIANCE_ASSISTANT",
    "country": "India",
    "status": "certificate_eligible"
  }
]
```

---

## 4. Mock Verifiers

```json
[
  {
    "verifier_id": "verifier_001",
    "name": "Northstar Retail Ops",
    "type": "employer",
    "role": "Operations Manager",
    "use_case": "Hiring a junior data operations analyst"
  },
  {
    "verifier_id": "verifier_002",
    "name": "Harbor Trade Finance Desk",
    "type": "trade_finance",
    "role": "Document Review Analyst",
    "use_case": "Checking whether a candidate can pre-review trade documents"
  },
  {
    "verifier_id": "verifier_003",
    "name": "SMB Exporter Network",
    "type": "business_partner",
    "role": "Exporter Owner",
    "use_case": "Evaluating a freelance trade documentation assistant"
  }
]
```

---

# Part A：AI Data Analysis Assistant Content Pack

## 5. A Landing Page Content

### 5.1 Title

```text
AI Data Analysis Assistant Certificate
```

### 5.2 Subtitle

```text
Prove you can turn business data into clear, verified insights with AI.
```

### 5.3 Value bullets

```text
Analyze spreadsheet data with AI support.
Detect anomalies and data quality risks.
Explain business metrics clearly.
Create an evidence-backed mini BI report.
Share a verifiable credential with employers or clients.
```

### 5.4 Who it is for

```text
Operations assistants
Sales operations teams
Finance/admin staff
Career switchers
Small business analysts
Freelancers preparing business reports
```

### 5.5 What the verifier sees

```text
Certificate status
Issuer
Validity period
Overall score band
Module score summary
Project evidence summary
Proof registry status
```

---

## 6. A Mock Capability Scores

```json
{
  "credential_type": "AI_DATA_ANALYSIS_ASSISTANT",
  "learner_id": "learner_001",
  "overall_score": 86,
  "score_band": "Strong",
  "module_scores": {
    "DA1_Data_Literacy": 90,
    "DA2_Spreadsheet_Reasoning": 84,
    "DA3_AI_Assisted_Analysis": 88,
    "DA4_Insight_Communication": 82,
    "DA5_Data_Quality_Risk": 86
  }
}
```

---

## 7. A Practice / Exam Mock Questions

### A-Q1

```json
{
  "question_id": "A-Q1",
  "type": "single_choice",
  "capability_id": "DA1",
  "stem": "A sales table contains order_date, region, product, revenue, and customer_count. Which field is best for comparing sales performance by location?",
  "options": ["order_date", "region", "product", "customer_count"],
  "answer_key": "region",
  "feedback": "Region is the location dimension used for geographic comparison."
}
```

### A-Q2

```json
{
  "question_id": "A-Q2",
  "type": "single_choice",
  "capability_id": "DA2",
  "stem": "Last month revenue was 10,000 and this month revenue was 12,000. What is the growth rate?",
  "options": ["10%", "20%", "120%", "2,000%"],
  "answer_key": "20%",
  "feedback": "Growth rate = (12,000 - 10,000) / 10,000 = 20%."
}
```

### A-Q3

```json
{
  "question_id": "A-Q3",
  "type": "multi_choice",
  "capability_id": "DA5",
  "stem": "Which cases may indicate data quality issues?",
  "options": ["Negative revenue", "Blank customer_count", "Product name has two spellings", "All monthly sales are exactly identical"],
  "answer_key": ["Negative revenue", "Blank customer_count", "Product name has two spellings", "All monthly sales are exactly identical"],
  "feedback": "Each option may indicate missing data, invalid values, inconsistent labels, or suspicious patterns."
}
```

### A-Q4

```json
{
  "question_id": "A-Q4",
  "type": "single_choice",
  "capability_id": "DA4",
  "stem": "Which chart best shows revenue changes over 12 months?",
  "options": ["Pie chart", "Line chart", "Organization chart", "Gauge only"],
  "answer_key": "Line chart",
  "feedback": "A line chart is appropriate for showing trends over time."
}
```

### A-Q5

```json
{
  "question_id": "A-Q5",
  "type": "true_false",
  "capability_id": "DA5",
  "stem": "AI says that three days of rising sales prove the full-year trend will rise. This is a reliable conclusion.",
  "answer_key": false,
  "feedback": "Three days is too small a sample for a full-year trend conclusion."
}
```

### A-Q6

```json
{
  "question_id": "A-Q6",
  "type": "short_answer",
  "capability_id": "DA3",
  "stem": "Given region, channel, revenue, and ad_spend, write three business questions worth analyzing.",
  "rubric": ["Uses available fields", "Links questions to business value", "Avoids unsupported assumptions"],
  "scoring_method": "rubric_agent_score"
}
```

### A-Q7

```json
{
  "question_id": "A-Q7",
  "type": "multi_choice",
  "capability_id": "DA5",
  "stem": "Which fields should not be uploaded directly to an external AI tool?",
  "options": ["customer_email", "passport_number", "anonymized_region", "credit_card_number"],
  "answer_key": ["customer_email", "passport_number", "credit_card_number"],
  "feedback": "Direct identifiers and payment data require strong privacy controls."
}
```

### A-Q8

```json
{
  "question_id": "A-Q8",
  "type": "ordering",
  "capability_id": "DA1",
  "stem": "Order the basic data analysis workflow.",
  "items": ["Understand business question", "Check data quality", "Calculate metrics", "Interpret results", "Recommend action"],
  "answer_key": ["Understand business question", "Check data quality", "Calculate metrics", "Interpret results", "Recommend action"]
}
```

### A-Q9

```json
{
  "question_id": "A-Q9",
  "type": "scenario",
  "capability_id": "DA4_DA5",
  "stem": "AI says North region performed best, but the table shows South has the highest revenue. What should the learner do?",
  "expected_points": ["Check original data", "Identify AI error", "Correct the conclusion", "Explain verification basis"],
  "scoring_method": "rubric_agent_score"
}
```

### A-Q10

```json
{
  "question_id": "A-Q10",
  "type": "structured_output",
  "capability_id": "DA3_DA4_DA5",
  "stem": "Write three business findings and one data risk note based on a small sales table.",
  "rubric": ["Accuracy", "Insight quality", "Clarity", "Risk awareness"],
  "scoring_method": "rubric_agent_score"
}
```

---

## 8. A Project Task Mock Content

### 8.1 Project title

```text
Sales Performance Mini BI Report
```

### 8.2 Business goal

```text
The company wants to understand 12 months of sales performance across regions and channels, identify growth opportunities, and detect data quality risks before using the report in a management meeting.
```

### 8.3 Mock CSV sample

```csv
order_date,region,channel,product_category,revenue,customer_count,refund_count,ad_spend
2026-01-31,North,Online,Home,12000,180,4,2100
2026-01-31,South,Retail,Home,15000,220,5,2600
2026-02-28,North,Online,Home,12800,190,3,2200
2026-02-28,South,Retail,Home,14900,218,8,2700
2026-03-31,North,Online,Electronics,9000,110,6,3000
2026-03-31,South,Online,Electronics,21000,260,5,3200
2026-04-30,West,Retail,Home,-500,70,2,900
2026-04-30,East,Online,Home,13200,,3,1800
```

### 8.4 Submission requirements

```text
metric_definition.md
insight_summary.md
anomaly_notes.md
chart_recommendation.md
business_recommendation.md
data_risk_note.md
```

### 8.5 Expected project output summary

```text
The learner should identify South as a strong region, note the negative revenue in West as a data anomaly, flag missing customer_count in East, recommend a line chart for monthly trends and bar chart by region/channel, and warn that the dataset contains quality issues before executive use.
```

---

## 9. A Mock Agent Score

```json
{
  "agent_score_id": "agent_score_data_001",
  "target_type": "project_submission",
  "target_id": "project_submission_data_001",
  "model_version": "mock-agent-v0",
  "rubric_version": "data-rubric-v1",
  "overall_score": 86,
  "confidence": 0.82,
  "risk_flags": ["minor_data_quality_issue_noted"],
  "score_breakdown": {
    "metric_accuracy": 88,
    "anomaly_detection": 92,
    "insight_quality": 84,
    "chart_recommendation": 82,
    "data_risk_awareness": 90,
    "communication_clarity": 80
  },
  "rationale_hash": "hash_mock_data_rationale_001"
}
```

---

## 10. A Mock Evidence Package

```json
{
  "evidence_package_id": "evidence_data_001",
  "credential_type": "AI_DATA_ANALYSIS_ASSISTANT",
  "learner_id": "learner_001",
  "exam_session_id": "exam_data_001",
  "project_submission_id": "project_submission_data_001",
  "project_output_hash": "hash_data_project_output_001",
  "agent_score_id": "agent_score_data_001",
  "final_score": 86,
  "status": "ready_for_certificate"
}
```

---

## 11. A Mock Certificate

```json
{
  "certificate_id": "cert_data_001",
  "certificate_name": "AI Data Analysis Assistant Certificate",
  "issuer": "AI Career Retraining Site",
  "learner_display_name": "Mia Chen",
  "issued_at": "2026-07-03",
  "expires_at": "2028-07-03",
  "overall_score_band": "Strong",
  "overall_score": 86,
  "evidence_package_id": "evidence_data_001",
  "proof_status": "registered",
  "revocation_status": "active"
}
```

---

# Part B：Cross-border Trade Content Pack

## 12. B Landing Page Content

### 12.1 Title

```text
AI Cross-border Trade Documentation & Compliance Assistant Certificate
```

### 12.2 Subtitle

```text
Prove you can review trade documents, detect discrepancies, and prepare evidence packages with AI-assisted checks.
```

### 12.3 Value bullets

```text
Understand common trade documents.
Check PO, invoice, packing list, and shipping summaries for consistency.
Identify missing files and review questions.
Use AI safely as a pre-review assistant.
Prepare proof-ready evidence packages for verifiers.
```

### 12.4 Who it is for

```text
Export assistants
Import operations staff
Cross-border e-commerce teams
Logistics coordinators
Trade finance document assistants
Freelance trade documentation support workers
```

### 12.5 What the verifier sees

```text
Certificate status
Issuer
Validity period
Trade document literacy score
Consistency check score
Project discrepancy summary
Evidence package proof status
```

---

## 13. B Mock Capability Scores

```json
{
  "credential_type": "AI_TRADE_DOCUMENTATION_COMPLIANCE_ASSISTANT",
  "learner_id": "learner_002",
  "overall_score": 88,
  "score_band": "Strong",
  "module_scores": {
    "TR1_Trade_Document_Literacy": 90,
    "TR2_Document_Consistency_Check": 92,
    "TR3_Compliance_Awareness": 80,
    "TR4_Supply_Chain_Evidence": 88,
    "TR5_AI_Assisted_Document_Review": 90
  }
}
```

---

## 14. B Practice / Exam Mock Questions

### B-Q1

```json
{
  "question_id": "B-Q1",
  "type": "single_choice",
  "capability_id": "TR1",
  "stem": "What is the main purpose of a Commercial Invoice?",
  "options": ["Record buyer, seller, goods, price, and transaction amount", "Prove an employee completed training", "Track website visits", "Record warehouse temperature only"],
  "answer_key": "Record buyer, seller, goods, price, and transaction amount"
}
```

### B-Q2

```json
{
  "question_id": "B-Q2",
  "type": "single_choice",
  "capability_id": "TR1",
  "stem": "Which information is commonly found in a Packing List?",
  "options": ["Cartons, quantity, weight, package details", "Employee salary", "Marketing campaign clicks", "Bank loan interest only"],
  "answer_key": "Cartons, quantity, weight, package details"
}
```

### B-Q3

```json
{
  "question_id": "B-Q3",
  "type": "multi_choice",
  "capability_id": "TR2",
  "stem": "Which fields should be checked across PO, invoice, and packing list?",
  "options": ["Goods description", "Quantity", "Currency and amount", "Random weather"],
  "answer_key": ["Goods description", "Quantity", "Currency and amount"]
}
```

### B-Q4

```json
{
  "question_id": "B-Q4",
  "type": "true_false",
  "capability_id": "TR3",
  "stem": "An AI-suggested HS code can be used as the final declaration decision without human confirmation.",
  "answer_key": false
}
```

### B-Q5

```json
{
  "question_id": "B-Q5",
  "type": "single_choice",
  "capability_id": "TR3",
  "stem": "What does a Certificate of Origin primarily indicate?",
  "options": ["Country or region of origin", "Employee degree", "Warehouse rent", "Customer satisfaction score"],
  "answer_key": "Country or region of origin"
}
```

### B-Q6

```json
{
  "question_id": "B-Q6",
  "type": "scenario",
  "capability_id": "TR2_TR5",
  "stem": "PO quantity is 1000, Invoice quantity is 1000, but Packing List quantity is 980. What should the learner do?",
  "expected_points": ["Flag discrepancy", "Explain possible impact", "Request human confirmation", "Add to risk list"],
  "scoring_method": "rubric_agent_score"
}
```

### B-Q7

```json
{
  "question_id": "B-Q7",
  "type": "multi_choice",
  "capability_id": "TR4",
  "stem": "Which documents are suitable for a trade evidence package?",
  "options": ["PO", "Commercial Invoice", "Packing List", "Bill of Lading summary", "Inspection Note"],
  "answer_key": ["PO", "Commercial Invoice", "Packing List", "Bill of Lading summary", "Inspection Note"]
}
```

### B-Q8

```json
{
  "question_id": "B-Q8",
  "type": "true_false",
  "capability_id": "TR3_TR5",
  "stem": "AI pre-review can replace the final judgment of customs, banks, lawyers, or professional document examiners.",
  "answer_key": false
}
```

### B-Q9

```json
{
  "question_id": "B-Q9",
  "type": "structured_output",
  "capability_id": "TR2",
  "stem": "Given a PO and invoice summary, output a field discrepancy table.",
  "rubric": ["Field coverage", "Discrepancy accuracy", "Clear format"],
  "scoring_method": "rubric_agent_score"
}
```

### B-Q10

```json
{
  "question_id": "B-Q10",
  "type": "scenario",
  "capability_id": "TR5",
  "stem": "Goods description, quantity, and delivery date are inconsistent across documents. Generate three human review questions.",
  "rubric": ["Question clarity", "Risk coverage", "Human review boundary"],
  "scoring_method": "rubric_agent_score"
}
```

---

## 15. B Project Task Mock Content

### 15.1 Project title

```text
Trade Document Consistency Review
```

### 15.2 Business scenario

```text
A small exporter is preparing a trade finance package. Before submitting documents, the team wants an AI-assisted pre-review to detect discrepancies, missing files, and questions that require human confirmation.
```

### 15.3 Mock document summaries

```text
Purchase Order:
PO-2026-0710, Buyer: Harbor Retail Ltd., Seller: Sunrise Export Co., Product: Smart LED Desk Lamp, Quantity: 1000 pcs, Unit Price: USD 12.00, Total: USD 12,000, Delivery: FOB Shanghai, Required Ship Date: 2026-08-15.

Commercial Invoice:
INV-2026-0788, Buyer: Harbor Retail Ltd., Seller: Sunrise Export Co., Product: Smart LED Desk Lamp, Quantity: 1000 pcs, Unit Price: USD 12.00, Total: USD 12,000, Currency: USD, Invoice Date: 2026-08-10.

Packing List:
PL-2026-0788, Product: LED Desk Lamp, Quantity: 980 pcs, Cartons: 98, Gross Weight: 1,176 kg, Net Weight: 980 kg.

Bill of Lading Summary:
BL-SHA-2026-0912, Shipper: Sunrise Export Co., Consignee: Harbor Retail Ltd., Port of Loading: Shanghai, Port of Discharge: Los Angeles, Ship Date: 2026-08-18.

Inspection Note:
Inspection completed for 980 pcs. 20 pcs pending replacement due to packaging defects.
```

### 15.4 Submission requirements

```text
trade_document_summary.md
five_document_match_table.md
discrepancy_list.md
missing_document_list.md
manual_review_questions.md
evidence_package_summary.md
```

### 15.5 Expected project output summary

```text
The learner should identify the 1000 vs 980 quantity discrepancy, ship date mismatch against the required date, product description variation, inspection note explaining 20 pending units, and generate human review questions before final submission.
```

---

## 16. B Mock Agent Score

```json
{
  "agent_score_id": "agent_score_trade_001",
  "target_type": "project_submission",
  "target_id": "project_submission_trade_001",
  "model_version": "mock-agent-v0",
  "rubric_version": "trade-rubric-v1",
  "overall_score": 88,
  "confidence": 0.84,
  "risk_flags": ["human_review_required_for_quantity_discrepancy"],
  "score_breakdown": {
    "field_extraction_accuracy": 90,
    "consistency_check_coverage": 92,
    "discrepancy_detection": 94,
    "compliance_boundary_awareness": 82,
    "evidence_package_completeness": 86
  },
  "rationale_hash": "hash_mock_trade_rationale_001"
}
```

---

## 17. B Mock Evidence Package

```json
{
  "evidence_package_id": "evidence_trade_001",
  "credential_type": "AI_TRADE_DOCUMENTATION_COMPLIANCE_ASSISTANT",
  "learner_id": "learner_002",
  "exam_session_id": "exam_trade_001",
  "project_submission_id": "project_submission_trade_001",
  "document_set_hash": "hash_trade_document_set_001",
  "project_output_hash": "hash_trade_project_output_001",
  "agent_score_id": "agent_score_trade_001",
  "final_score": 88,
  "status": "ready_for_certificate"
}
```

---

## 18. B Mock Certificate

```json
{
  "certificate_id": "cert_trade_001",
  "certificate_name": "AI Cross-border Trade Documentation & Compliance Assistant Certificate",
  "issuer": "AI Career Retraining Site",
  "learner_display_name": "Aarav Patel",
  "issued_at": "2026-07-03",
  "expires_at": "2028-07-03",
  "overall_score_band": "Strong",
  "overall_score": 88,
  "evidence_package_id": "evidence_trade_001",
  "proof_status": "registered",
  "revocation_status": "active"
}
```

---

# Shared Proof / Verifier Content

## 19. Mock Proof Credentials

```json
[
  {
    "proof_credential_id": "proof_cred_data_001",
    "credential_type": "AI_DATA_ANALYSIS_ASSISTANT",
    "issuer_did": "did:example:issuer-ai-career-site",
    "holder_did": "did:example:holder-mia-chen",
    "subject_id_hash": "hash_subject_mia_001",
    "certificate_id": "cert_data_001",
    "claims_hash": "hash_claims_data_001",
    "evidence_package_hash": "hash_evidence_data_001",
    "issued_at": "2026-07-03",
    "expires_at": "2028-07-03",
    "status": "active",
    "revocation_status": "not_revoked",
    "proof_chain_record_id": "chain_record_data_001",
    "schema_version": "proof-schema-v1"
  },
  {
    "proof_credential_id": "proof_cred_trade_001",
    "credential_type": "AI_TRADE_DOCUMENTATION_COMPLIANCE_ASSISTANT",
    "issuer_did": "did:example:issuer-ai-career-site",
    "holder_did": "did:example:holder-aarav-patel",
    "subject_id_hash": "hash_subject_aarav_001",
    "certificate_id": "cert_trade_001",
    "claims_hash": "hash_claims_trade_001",
    "evidence_package_hash": "hash_evidence_trade_001",
    "issued_at": "2026-07-03",
    "expires_at": "2028-07-03",
    "status": "active",
    "revocation_status": "not_revoked",
    "proof_chain_record_id": "chain_record_trade_001",
    "schema_version": "proof-schema-v1"
  }
]
```

## 20. Mock Proof Registry

```json
[
  {
    "proof_chain_record_id": "chain_record_data_001",
    "proof_hash": "0xDATA_PROOF_HASH_MOCK_001",
    "credential_type": "AI_DATA_ANALYSIS_ASSISTANT",
    "issuer": "did:example:issuer-ai-career-site",
    "issued_at": "2026-07-03",
    "status": "registered",
    "revocation_status": "not_revoked",
    "schema_version": "proof-schema-v1"
  },
  {
    "proof_chain_record_id": "chain_record_trade_001",
    "proof_hash": "0xTRADE_PROOF_HASH_MOCK_001",
    "credential_type": "AI_TRADE_DOCUMENTATION_COMPLIANCE_ASSISTANT",
    "issuer": "did:example:issuer-ai-career-site",
    "issued_at": "2026-07-03",
    "status": "registered",
    "revocation_status": "not_revoked",
    "schema_version": "proof-schema-v1"
  }
]
```

## 21. Mock Verifier Results

### 21.1 Data verifier result

```json
{
  "verification_event_id": "verify_data_001",
  "verifier_id": "verifier_001",
  "proof_credential_id": "proof_cred_data_001",
  "result": "valid",
  "issuer": "AI Career Retraining Site",
  "credential_type": "AI Data Analysis Assistant Certificate",
  "issued_at": "2026-07-03",
  "expires_at": "2028-07-03",
  "revocation_status": "not_revoked",
  "overall_score_band": "Strong",
  "capability_summary": {
    "Data Literacy": "Strong",
    "Spreadsheet Reasoning": "Good",
    "AI-assisted Analysis": "Strong",
    "Insight Communication": "Good",
    "Data Quality & Risk": "Strong"
  },
  "authorized_evidence_summary": "Completed a mini BI report from mock sales data, identified anomalies, recommended charts, and flagged data quality risks."
}
```

### 21.2 Trade verifier result

```json
{
  "verification_event_id": "verify_trade_001",
  "verifier_id": "verifier_002",
  "proof_credential_id": "proof_cred_trade_001",
  "result": "valid",
  "issuer": "AI Career Retraining Site",
  "credential_type": "AI Cross-border Trade Documentation & Compliance Assistant Certificate",
  "issued_at": "2026-07-03",
  "expires_at": "2028-07-03",
  "revocation_status": "not_revoked",
  "overall_score_band": "Strong",
  "capability_summary": {
    "Trade Document Literacy": "Strong",
    "Document Consistency Check": "Strong",
    "Compliance Awareness": "Good",
    "Supply Chain Evidence": "Strong",
    "AI-assisted Document Review": "Strong"
  },
  "authorized_evidence_summary": "Completed a simulated trade document review, detected quantity discrepancy, shipping date risk, and generated human review questions."
}
```

---

## 22. Founder Demo Script

### 22.1 Three-minute route

```text
1. Start at Home: explain verifiable skill certificate platform.
2. Open Certificate Catalog: show Data and Trade MVPs.
3. Open AI Data Landing: explain broad market and fast cold start.
4. Jump to Agent Score Report: show agent-scored project evidence.
5. Open Certificate Detail: show certificate is backed by Evidence Package.
6. Open Claim Proof: show hash-only proof registration.
7. Open Verifier Result: show employer/client verification.
```

### 22.2 Five-minute route

```text
1. Home
2. Certificate Catalog
3. AI Data Path Dashboard
4. AI Data Project Task
5. Agent Score Report
6. Evidence Package
7. Certificate Detail
8. Claim Proof Credential
9. Verifier Portal
10. Trade Landing as second vertical expansion
```

### 22.3 Eight-minute route

```text
1. Explain market research: broad vertical universe, not founder-bias.
2. Show Top 5 Evidence Pack logic.
3. Show dual MVP choice.
4. Walk through Data MVP.
5. Walk through Trade MVP.
6. Show shared ProofCredential schema.
7. Show Verifier Portal.
8. Close with no-code static prototype boundary.
```

---

## 23. Page Button Text

```text
Start Assessment
Continue Practice
Preview Exam
Submit Project
View Agent Score
View Evidence Package
Claim Proof Credential
Connect Wallet / DID Mock
Generate Claims Hash
Register Proof Hash Mock
Share Proof Link
Verify Credential
View Verifier Result
Return to Founder Dashboard
```

---

## 24. Static Prototype Boundary Copy

Use this copy in footer or Founder Dashboard:

```text
Static prototype only. No real wallet connection, no real chain transaction, no real database, no real exam, no real agent call, and no real legal, trade, financial, tax, medical, or compliance advice.
```

中文：

```text
仅静态原型。不连接真实钱包，不发真实链交易，不使用真实数据库，不运行真实考试，不调用真实 Agent，也不提供法律、贸易、金融、税务、医疗或合规意见。
```

---

## 25. v6.9 验收标准

```text
首页文案可直接用于静态原型。
两个 MVP 都有 mock learner、mock questions、mock project task、mock agent score、mock certificate。
ProofCredential 和 ProofRegistry 有 mock 数据。
Verifier Result 有可展示的验证结果。
Founder Demo Script 支持 3/5/8 分钟演示。
所有数据均为 mock，不涉及真实敏感数据。
原型边界文案明确。
```

---

## 26. 下一步

v7.0 可以开始进入真正静态原型实现，但建议先做一个实现前门禁：

```text
v6.10 Static Prototype Implementation Gate
```

确认：

```text
1. 先实现单页 HTML，还是 Streamlit？
2. 先只做 Founder Demo，还是做 Learner + Verifier 双入口？
3. 是否继续保持双 MVP，还是先做 AI Data 单 MVP？
4. 静态原型是否需要多语言？
5. 是否需要 Bootstrap / Tailwind / 原生 CSS？
```
