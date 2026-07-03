window.ProofSkillData = {
  credentialPaths: [
    {
      id: 'ai-data',
      title: 'AI Data Analysis Assistant',
      level: 'IssuerAttested',
      duration: '2 weeks',
      status: 'active path',
      description: 'Spreadsheet reasoning, data quality checks, insight writing, and mini BI report delivery.',
      modules: ['Spreadsheet cleanup', 'Metric reasoning', 'Chart interpretation', 'AI-assisted insight review'],
      targetRoles: ['Junior Data Analyst', 'Operations Analyst', 'AI Data Assistant']
    },
    {
      id: 'trade-docs',
      title: 'AI Trade Documentation Assistant',
      level: 'EvaluatorSigned',
      duration: '3 weeks',
      status: 'pilot path',
      description: 'Trade document consistency review across PO, invoice, packing list, inspection note, and BL summary.',
      modules: ['Five-document matching', 'Exception detection', 'Human review boundary', 'Evidence packaging'],
      targetRoles: ['Trade Documentation Assistant', 'Supply Chain Ops', 'Receivable Review Assistant']
    }
  ],
  projectTasks: [
    {
      id: 'task-data-bi',
      credentialId: 'ai-data',
      title: 'Sales Performance Mini BI Report',
      difficulty: 'Foundation',
      estimatedTime: '90 min',
      checklist: ['Clean sample CSV', 'Calculate margin by region', 'Identify abnormal discount pattern', 'Write a 5-bullet executive summary'],
      evidenceOutputs: ['cleaning-notes.md', 'metrics-table.csv', 'chart-screenshot.png', 'executive-summary.md']
    },
    {
      id: 'task-trade-review',
      credentialId: 'trade-docs',
      title: 'Trade Document Consistency Review',
      difficulty: 'Professional',
      estimatedTime: '2.5 h',
      checklist: ['Match PO and invoice quantity', 'Check packing list against inspection note', 'Flag ship-date mismatch', 'Write review questions for human approver'],
      evidenceOutputs: ['exception-table.xlsx', 'document-review-note.md', 'risk-summary.pdf']
    }
  ],
  scoreBreakdown: [
    { area: 'Task understanding', score: 90, note: 'Understands objective and constraints.' },
    { area: 'Evidence quality', score: 86, note: 'Evidence bundle is complete and traceable.' },
    { area: 'Risk detection', score: 82, note: 'Finds major anomalies, misses one edge case.' },
    { area: 'Communication', score: 88, note: 'Clear summary and reviewer questions.' }
  ],
  rubrics: [
    { item: 'Completeness', weight: '25%', evaluatorScore: 22, issuerCheck: 'pass' },
    { item: 'Correctness', weight: '30%', evaluatorScore: 26, issuerCheck: 'pass' },
    { item: 'Risk awareness', weight: '25%', evaluatorScore: 21, issuerCheck: 'review' },
    { item: 'Communication', weight: '20%', evaluatorScore: 18, issuerCheck: 'pass' }
  ],
  learners: [
    { name: 'Mia Chen', wallet: '0xLearnerMiaMock', credential: 'AI Data Analysis Assistant', score: 86, status: 'issuer review requested' },
    { name: 'Aarav Patel', wallet: '0xLearnerAaravMock', credential: 'AI Trade Documentation Assistant', score: 88, status: 'evaluator review ready' }
  ],
  evidencePackage: {
    credentialType: 'AI_DATA_ANALYSIS_ASSISTANT',
    learnerWallet: '0xLearnerMiaMock',
    evidenceHash: '0xEVIDENCE_HASH_MOCK_001',
    scoreHash: '0xSCORE_HASH_MOCK_001',
    certificateHash: '0xCERT_HASH_MOCK_001',
    schemaHash: '0xSCHEMA_HASH_V1',
    overallScore: 86,
    scoreBand: 'Strong',
    privacy: 'raw files hidden by default'
  },
  contractRecord: {
    credentialId: '0xDATA_CREDENTIAL_ID_MOCK_001',
    holder: '0xLearnerMiaMock',
    issuer: '0xAuthorizedIssuerMock',
    status: 'Active',
    attestationLevel: 'IssuerAttested',
    issuedAt: '2026-07-03',
    expiresAt: '2027-07-03',
    revocation: 'not_revoked'
  },
  issuerRegistry: [
    { wallet: '0xAuthorizedIssuerMock', name: 'ProofSkill Platform Issuer', status: 'active', type: 'platform' },
    { wallet: '0xTrainingPartnerMock', name: 'Training Partner Mock', status: 'active', type: 'partner' },
    { wallet: '0xEnterpriseAcademyMock', name: 'Enterprise Academy Mock', status: 'pending', type: 'enterprise' }
  ],
  schemaVersions: [
    { id: 'credential-schema-v1', status: 'active', credentials: 2 },
    { id: 'evidence-bundle-v1', status: 'active', credentials: 2 },
    { id: 'trade-rubric-v1', status: 'pilot', credentials: 1 }
  ]
};
