window.ProofSkillDemoRoutes = [
  {
    id: 'three-minute',
    title: '3-minute executive demo',
    audience: 'Investor / first meeting',
    duration: '3 min',
    promise: 'Show the product story, trust model, and verifier outcome without deep operations detail.',
    steps: [
      { label: 'Overview', target: { role: 'overview' }, talk: 'ProofSkill AI turns practical AI training into verifiable skill credentials.' },
      { label: 'Learner certificate', target: { role: 'learner', learnerTab: 'certificate' }, talk: 'Learner gets a portable certificate with evidence hashes and visual issuer seal.' },
      { label: 'Verifier signals', target: { role: 'verifier', anchor: 'verifier-signals' }, talk: 'Verifier sees proof status, role-fit signals, and use-boundary notes.' }
    ]
  },
  {
    id: 'eight-minute',
    title: '8-minute product demo',
    audience: 'Training partner / pilot buyer',
    duration: '8 min',
    promise: 'Show the real workflow from curriculum setup to evidence, issuing, and verification.',
    steps: [
      { label: 'Overview', target: { role: 'overview' }, talk: 'Start with the end-to-end workflow and smoke test status.' },
      { label: 'Admin curriculum', target: { role: 'admin', anchor: 'admin-curriculum' }, talk: 'Admin publishes courses, quiz bank, and practice templates.' },
      { label: 'Learner learning', target: { role: 'learner', learnerTab: 'learning' }, talk: 'Learner studies modules and passes quiz.' },
      { label: 'Learner practice', target: { role: 'learner', learnerTab: 'practice' }, talk: 'Learner completes practice lab and can download worksheet PDF.' },
      { label: 'Learner evidence', target: { role: 'learner', learnerTab: 'evidence' }, talk: 'Evidence bundle and hashes are prepared before issuer review.' },
      { label: 'Issuer review', target: { role: 'issuer', anchor: 'review-queue' }, talk: 'Training partner reviews evidence and readiness before signing.' },
      { label: 'Verifier proof', target: { role: 'verifier', anchor: 'verifier-proof' }, talk: 'Verifier checks credential proof without seeing private raw files.' }
    ]
  },
  {
    id: 'fifteen-minute',
    title: '15-minute technical demo',
    audience: 'Technical partner / internal team',
    duration: '15 min',
    promise: 'Show configured navigation, state transitions, trust levels, PDF exports, and contract-shaped proof flow.',
    steps: [
      { label: 'Smoke test', target: { role: 'overview' }, talk: 'Confirm Bootstrap, menu, role modules, exports, and targets are loaded.' },
      { label: 'Admin registry', target: { role: 'admin', anchor: 'admin-registry' }, talk: 'Issuer registry and governance are explicit.' },
      { label: 'Admin templates', target: { role: 'admin', anchor: 'admin-practice' }, talk: 'Practice templates define expected evidence outputs.' },
      { label: 'Learner practice PDF', target: { role: 'learner', learnerTab: 'practice' }, talk: 'Practice worksheet can be printed or saved as PDF.' },
      { label: 'Learner certificate PDF', target: { role: 'learner', learnerTab: 'certificate' }, talk: 'Certificate has visual seal and verification references.' },
      { label: 'Issuer contract action', target: { role: 'issuer', anchor: 'contract-actions' }, talk: 'Issuer action mirrors contract-shaped proof registration.' },
      { label: 'Evaluator rubric', target: { role: 'evaluator', anchor: 'evaluator-rubric' }, talk: 'Higher-trust path adds rubric scoring and evaluatorSetHash.' },
      { label: 'Verifier receipt', target: { role: 'verifier', anchor: 'verifier-receipt' }, talk: 'Verifier can produce a receipt-style proof check.' }
    ]
  }
];
