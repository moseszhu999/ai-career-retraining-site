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
  cohorts: [
    {
      id: 'cohort-ai-data-2026-07',
      name: 'AI Data Assistant · July Pilot',
      path: 'AI Data Analysis Assistant',
      learners: 18,
      avgProgress: 62,
      quizPassRate: '72%',
      practiceSubmitted: 9,
      evidenceReady: 4,
      status: 'active'
    },
    {
      id: 'cohort-trade-2026-07',
      name: 'Trade Documentation · Pilot Batch',
      path: 'AI Trade Documentation Assistant',
      learners: 8,
      avgProgress: 48,
      quizPassRate: '50%',
      practiceSubmitted: 3,
      evidenceReady: 1,
      status: 'pilot'
    }
  ],
  learnerProgress: [
    { name: 'Mia Chen', wallet: '0xLearnerMiaMock', path: 'AI Data Analysis Assistant', progress: 100, quiz: 88, practice: 'submitted', evidence: 'ready', nextAction: 'issuer review' },
    { name: 'Ken Sato', wallet: '0xLearnerKenMock', path: 'AI Data Analysis Assistant', progress: 75, quiz: 82, practice: 'in progress', evidence: 'not ready', nextAction: 'submit practice' },
    { name: 'Lina Garcia', wallet: '0xLearnerLinaMock', path: 'AI Data Analysis Assistant', progress: 50, quiz: null, practice: 'not started', evidence: 'not ready', nextAction: 'take quiz' },
    { name: 'Aarav Patel', wallet: '0xLearnerAaravMock', path: 'AI Trade Documentation Assistant', progress: 90, quiz: 91, practice: 'submitted', evidence: 'ready', nextAction: 'evaluator review' }
  ],
  curriculumOps: [
    { item: 'Lesson 1 · Spreadsheet Data Hygiene', status: 'published', completions: 14, issue: 'none' },
    { item: 'Lesson 2 · Metrics and Business Questions', status: 'published', completions: 10, issue: 'needs example update' },
    { item: 'Quiz · Data Quality Judgment', status: 'published', completions: 13, issue: '2 weak questions' },
    { item: 'Practice Lab · Mini BI Report', status: 'active', completions: 9, issue: 'mentor review queue growing' }
  ],
  learningModules: [
    {
      id: 'lesson-1',
      title: 'Lesson 1 · Spreadsheet Data Hygiene',
      type: 'lesson',
      duration: '18 min',
      status: 'available',
      objective: 'Learn how to inspect missing values, duplicate rows, inconsistent date formats, and suspicious outliers before using AI assistance.',
      keyPoints: ['Check schema before asking AI', 'Separate raw data from cleaned data', 'Document every assumption', 'Never hide anomalies just to make charts look clean'],
      output: 'Short cleaning note with before/after field list'
    },
    {
      id: 'lesson-2',
      title: 'Lesson 2 · Metrics and Business Questions',
      type: 'lesson',
      duration: '22 min',
      status: 'locked after lesson 1',
      objective: 'Translate business questions into metrics such as revenue, margin, discount leakage, region growth, and customer risk.',
      keyPoints: ['Metric = formula + business meaning', 'Do not mix revenue and margin', 'Segment before conclusion', 'Explain uncertainty'],
      output: 'Metric definition table'
    },
    {
      id: 'quiz-1',
      title: 'Quiz · Data Quality Judgment',
      type: 'quiz',
      duration: '8 questions',
      status: 'available',
      objective: 'Check whether the learner can recognize when AI output is unsafe because the source data is inconsistent.',
      keyPoints: ['Missing value handling', 'Duplicate detection', 'Wrong aggregation', 'Overconfident AI summary'],
      output: 'Quiz score stored locally before evidence generation'
    },
    {
      id: 'lab-1',
      title: 'Practice Lab · Mini BI Report',
      type: 'practice',
      duration: '45 min',
      status: 'available',
      objective: 'Build a mini BI report from cleaned sample data and write a manager-facing summary.',
      keyPoints: ['Clean sample data', 'Calculate region margin', 'Find discount anomaly', 'Write evidence-backed conclusion'],
      output: 'Mini BI report evidence bundle'
    }
  ],
  quizQuestions: [
    {
      question: 'A CSV has duplicate order IDs with different revenue values. What should the learner do first?',
      choices: ['Average the revenue automatically', 'Delete the smaller value', 'Flag the conflict and inspect source rows', 'Ask AI to guess the correct row'],
      answer: 'Flag the conflict and inspect source rows'
    },
    {
      question: 'AI says East region is best because revenue is highest. What metric may still change the conclusion?',
      choices: ['Font size', 'Gross margin', 'File name', 'Row order'],
      answer: 'Gross margin'
    },
    {
      question: 'Which item belongs in the evidence bundle?',
      choices: ['Only final chart', 'Cleaning assumptions and metric definitions', 'Private password', 'Unverified customer gossip'],
      answer: 'Cleaning assumptions and metric definitions'
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
