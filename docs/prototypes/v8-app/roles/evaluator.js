window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.evaluator = {
  title: 'Evaluator / Reviewer Dashboard',
  subtitle: 'Review submitted evidence, score with rubric, and sign evaluator review.',
  render(state) {
    const data = window.ProofSkillData;
    const task = data.projectTasks[1];
    const rubricRows = data.rubrics.map((item) => `
      <tr>
        <td>${item.item}</td>
        <td>${item.weight}</td>
        <td><input class="form-control form-control-sm" value="${item.evaluatorScore}"></td>
        <td><span class="badge text-bg-${item.issuerCheck === 'pass' ? 'success' : 'warning'}">${item.issuerCheck}</span></td>
      </tr>
    `).join('');

    return `
      <div class="row g-3 mb-4">
        <div class="col-md-4"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Assigned projects</div><div class="display-6">${state.evaluatorReview === 'not_assigned' ? '0' : '1'}</div><span class="badge text-bg-primary">trade-docs</span></div></div></div>
        <div class="col-md-4"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Signature</div><div class="display-6">${state.evaluatorSetHash ? 'Ready' : 'Missing'}</div></div></div></div>
        <div class="col-md-4"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">evaluatorSetHash</div><div class="h4 text-truncate">${state.evaluatorSetHash || 'None'}</div></div></div></div>
      </div>

      <div class="row g-3 mb-4">
        <div id="evaluator-assignment" class="col-xl-5"><div class="card h-100"><div class="card-header bg-white fw-bold">Review Assignment · ${task.title}</div><div class="card-body"><p class="text-secondary">Difficulty: ${task.difficulty} · Estimated time: ${task.estimatedTime}</p><div class="alert alert-warning"><strong>Risk flags:</strong> quantity mismatch, ship-date mismatch, replacement quantity pending human confirmation.</div><ul class="list-group mb-3">${task.checklist.map((item) => `<li class="list-group-item d-flex justify-content-between"><span>${item}</span><span class="badge text-bg-success">checked</span></li>`).join('')}</ul><div class="d-flex flex-wrap gap-2"><button id="evaluatorAssign" class="btn btn-outline-primary">Assign Review</button><button id="evaluatorSign" class="btn btn-primary">Sign Evaluation</button></div></div></div></div>
        <div id="evaluator-rubric" class="col-xl-7"><div class="card h-100"><div class="card-header bg-white fw-bold">Rubric Scoring</div><div class="card-body table-responsive"><table class="table table-hover align-middle mb-3"><thead><tr><th>Rubric item</th><th>Weight</th><th>Score</th><th>Review flag</th></tr></thead><tbody>${rubricRows}</tbody></table><label class="form-label small text-secondary">Evaluator comment</label><textarea class="form-control" rows="3">Strong evidence package. Main issue is that replacement quantity must be routed to a human approver before final certificate issuance.</textarea></div></div></div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Evidence Summary</div><div class="card-body"><dl class="row small mb-0"><dt class="col-5">Learner</dt><dd class="col-7">Aarav Patel</dd><dt class="col-5">Credential</dt><dd class="col-7">AI Trade Documentation Assistant</dd><dt class="col-5">Evidence package</dt><dd class="col-7">exception-table.xlsx · document-review-note.md · risk-summary.pdf</dd><dt class="col-5">Boundary</dt><dd class="col-7">This review is not legal, tax, or financial advice.</dd></dl></div></div></div>
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Evaluator Signature Preview</div><div class="card-body"><pre class="code-block mb-0">${state.evaluatorSetHash ? JSON.stringify({ evaluator: '0xEvaluatorMock', credentialId: '0xTRADE_CREDENTIAL_ID_MOCK_001', score: 88, rubricVersion: 'trade-rubric-v1', signature: '0xSIG_MOCK', evaluatorSetHash: state.evaluatorSetHash }, null, 2) : 'No evaluator signature yet.'}</pre></div></div></div>
      </div>
    `;
  },
  bind() {
    document.getElementById('evaluatorAssign')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.evaluatorReview = 'review_assigned'; }, 'Evaluator review assigned'));
    document.getElementById('evaluatorSign')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.evaluatorReview = 'evaluator_set_ready'; s.evaluatorSetHash = '0xEVALUATOR_SET_HASH_MOCK_001'; }, 'Evaluator signed review and generated evaluatorSetHash'));
  }
};
