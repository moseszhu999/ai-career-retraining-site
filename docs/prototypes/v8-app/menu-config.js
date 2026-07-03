window.ProofSkillMenu = {
  roles: [
    { id: 'overview', label: 'Overview', description: 'executive summary and guided demo' },
    { id: 'learner', label: 'Learner / Candidate', description: 'learn, practice, evidence, certificate' },
    { id: 'issuer', label: 'Issuer / Training Partner', description: 'learning ops, review, issue proof' },
    { id: 'evaluator', label: 'Evaluator / Reviewer', description: 'score and sign reviews' },
    { id: 'verifier', label: 'Verifier / Organization', description: 'proof and role-fit signals' },
    { id: 'admin', label: 'Admin / Contract Owner', description: 'curriculum and contract governance' }
  ],
  groups: [
    {
      id: 'platform',
      label: 'Platform',
      children: [
        { id: 'overview', label: 'Overview', target: { role: 'overview' } }
      ]
    },
    {
      id: 'learning',
      label: 'Learning & Credential',
      children: [
        {
          id: 'learner',
          label: 'Learner Workspace',
          target: { role: 'learner' },
          children: [
            { id: 'learner-learning', label: 'Learning', target: { role: 'learner', learnerTab: 'learning' } },
            { id: 'learner-path', label: 'My Path', target: { role: 'learner', learnerTab: 'path' } },
            { id: 'learner-practice', label: 'Practice Lab', target: { role: 'learner', learnerTab: 'practice' } },
            { id: 'learner-evidence', label: 'Evidence', target: { role: 'learner', learnerTab: 'evidence' } },
            { id: 'learner-certificate', label: 'Certificate / PDF', target: { role: 'learner', learnerTab: 'certificate' } }
          ]
        }
      ]
    },
    {
      id: 'operations',
      label: 'Operations & Review',
      children: [
        {
          id: 'issuer',
          label: 'Issuer / Training Partner',
          target: { role: 'issuer' },
          children: [
            { id: 'issuer-learning-ops', label: 'Learning Ops', target: { role: 'issuer', anchor: 'learning-ops' } },
            { id: 'issuer-review', label: 'Review Queue', target: { role: 'issuer', anchor: 'review-queue' } },
            { id: 'issuer-contract', label: 'Contract Actions', target: { role: 'issuer', anchor: 'contract-actions' } }
          ]
        },
        {
          id: 'evaluator',
          label: 'Evaluator',
          target: { role: 'evaluator' },
          children: [
            { id: 'evaluator-assignment', label: 'Assignment', target: { role: 'evaluator' } },
            { id: 'evaluator-rubric', label: 'Rubric Review', target: { role: 'evaluator' } }
          ]
        }
      ]
    },
    {
      id: 'verification',
      label: 'Verification',
      children: [
        {
          id: 'verifier',
          label: 'Verifier Workspace',
          target: { role: 'verifier' },
          children: [
            { id: 'verifier-proof', label: 'Proof Check', target: { role: 'verifier' } },
            { id: 'verifier-signals', label: 'Role-fit Signals', target: { role: 'verifier' } },
            { id: 'verifier-receipt', label: 'Receipt Preview', target: { role: 'verifier' } }
          ]
        }
      ]
    },
    {
      id: 'governance',
      label: 'Governance',
      children: [
        {
          id: 'admin',
          label: 'Admin Workspace',
          target: { role: 'admin' },
          children: [
            { id: 'admin-curriculum', label: 'Curriculum Builder', target: { role: 'admin' } },
            { id: 'admin-quiz', label: 'Quiz Bank', target: { role: 'admin' } },
            { id: 'admin-practice', label: 'Practice Templates', target: { role: 'admin' } },
            { id: 'admin-registry', label: 'Issuer Registry', target: { role: 'admin' } }
          ]
        }
      ]
    }
  ]
};
