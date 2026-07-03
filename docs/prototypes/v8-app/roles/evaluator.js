window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.evaluator = {
  title: 'Evaluator / Reviewer Dashboard',
  subtitle: 'Score project evidence and sign evaluations for issuer review.',
  render(state) {
    return `
      <div class="row g-3 mb-4">
        <div class="col-md-4"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Assignment</div><div class="display-6">${state.evaluatorReview === 'not_assigned' ? '0' : '1'}</div></div></div></div>
        <div class="col-md-4"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Signature</div><div class="display-6">${state.evaluatorSetHash ? 'Ready' : 'Missing'}</div></div></div></div>
        <div class="col-md-4"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">evaluatorSetHash</div><div class="h4 text-truncate">${state.evaluatorSetHash || 'None'}</div></div></div></div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Review Assignment</div>
            <div class="card-body">
              <p><strong>Trade Document Consistency Review</strong></p>
              <p class="text-secondary">Review evidence package summary, score with rubric, and sign evaluation.</p>
              <div class="mb-3">
                <div class="d-flex justify-content-between"><span>Consistency check</span><strong>92</strong></div>
                <div class="progress"><div class="progress-bar" style="width:92%"></div></div>
              </div>
              <div class="mb-3">
                <div class="d-flex justify-content-between"><span>Human review boundary</span><strong>84</strong></div>
                <div class="progress"><div class="progress-bar bg-success" style="width:84%"></div></div>
              </div>
              <div class="d-flex flex-wrap gap-2">
                <button id="evaluatorAssign" class="btn btn-outline-primary">Assign Review</button>
                <button id="evaluatorSign" class="btn btn-primary">Sign Evaluation</button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Evaluator signature preview</div>
            <div class="card-body">
              <pre class="code-block mb-0">${state.evaluatorSetHash ? JSON.stringify({ evaluator: '0xEvaluatorMock', credentialId: '0xTRADE_CREDENTIAL_ID_MOCK_001', score: 88, rubricVersion: 'trade-rubric-v1', signature: '0xSIG_MOCK', evaluatorSetHash: state.evaluatorSetHash }, null, 2) : 'No evaluator signature yet.'}</pre>
            </div>
          </div>
        </div>
      </div>
    `;
  },
  bind() {
    document.getElementById('evaluatorAssign')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.evaluatorReview = 'review_assigned';
    }, 'Evaluator review assigned'));

    document.getElementById('evaluatorSign')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.evaluatorReview = 'evaluator_set_ready';
      s.evaluatorSetHash = '0xEVALUATOR_SET_HASH_MOCK_001';
    }, 'Evaluator signed review and generated evaluatorSetHash'));
  }
};
