window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.learner = {
  title: 'Learner / Candidate Dashboard',
  subtitle: 'Choose a credential path, complete project tasks, build evidence, and request attestation.',
  render(state) {
    const data = window.ProofSkillData;
    const paths = data.credentialPaths.map((path) => `
      <div class="col-lg-6">
        <div class="card h-100 border-${path.id === 'ai-data' ? 'primary' : 'secondary'}">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
              <h5 class="card-title mb-0">${path.title}</h5>
              <span class="badge text-bg-${path.level === 'EvaluatorSigned' ? 'success' : 'primary'}">${path.level}</span>
            </div>
            <p class="text-secondary small">${path.description}</p>
            <div class="mb-2"><span class="badge text-bg-light text-secondary border">${path.duration}</span> <span class="badge text-bg-light text-secondary border">${path.status}</span></div>
            <div class="small text-uppercase text-secondary fw-bold mt-3">Modules</div>
            <ul class="small mb-3">${path.modules.map((item) => `<li>${item}</li>`).join('')}</ul>
            <div class="small text-uppercase text-secondary fw-bold">Target roles</div>
            <p class="small mb-0">${path.targetRoles.join(' · ')}</p>
          </div>
        </div>
      </div>
    `).join('');

    const task = data.projectTasks[0];
    const taskChecklist = task.checklist.map((item, index) => `
      <li class="list-group-item d-flex justify-content-between align-items-center">
        <span>${item}</span>
        <span class="badge text-bg-${index < 2 ? 'success' : 'secondary'}">${index < 2 ? 'done' : 'todo'}</span>
      </li>
    `).join('');

    const scoreRows = data.scoreBreakdown.map((row) => `
      <tr>
        <td>${row.area}</td>
        <td style="width: 36%"><div class="progress"><div class="progress-bar" style="width:${row.score}%">${row.score}</div></div></td>
        <td class="text-secondary small">${row.note}</td>
      </tr>
    `).join('');

    const evidenceBadge = state.evidence === 'generated'
      ? '<span class="badge text-bg-success">Generated</span>'
      : '<span class="badge text-bg-secondary">Not generated</span>';
    const proofBadge = state.proofStatus === 'active'
      ? `<span class="badge text-bg-success">${state.trustLevel}</span>`
      : '<span class="badge text-bg-secondary">Not registered</span>';

    return `
      <div class="alert alert-primary d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div><strong>Current learner:</strong> Mia Chen · Wallet 0xLearnerMiaMock · Goal: AI Data Analysis Assistant</div>
        <span class="badge text-bg-light text-primary border">portfolio + issuer attestation path</span>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-md-4"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Credential paths</div><div class="display-6">2</div><span class="badge text-bg-primary">active catalog</span></div></div></div>
        <div class="col-md-4"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Local evidence</div><div class="h3 mb-2">${state.evidence === 'generated' ? 'Ready' : 'Draft'}</div>${evidenceBadge}</div></div></div>
        <div class="col-md-4"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Proof status</div><div class="h3 mb-2">${state.proofStatus}</div>${proofBadge}</div></div></div>
      </div>

      <div class="card mb-4">
        <div class="card-header bg-white fw-bold">Credential Path Catalog</div>
        <div class="card-body"><div class="row g-3">${paths}</div></div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Project Task · ${task.title}</div>
            <div class="card-body">
              <p class="text-secondary">Difficulty: ${task.difficulty} · Estimated time: ${task.estimatedTime}</p>
              <ul class="list-group mb-3">${taskChecklist}</ul>
              <div class="small text-uppercase text-secondary fw-bold mb-2">Expected evidence outputs</div>
              <div class="d-flex flex-wrap gap-2 mb-3">${task.evidenceOutputs.map((item) => `<span class="badge text-bg-light text-secondary border">${item}</span>`).join('')}</div>
              <div class="d-flex flex-wrap gap-2">
                <button id="learnerGenerateEvidence" class="btn btn-primary">Generate Evidence Bundle</button>
                <button id="learnerComputeHashes" class="btn btn-outline-primary">Compute Hashes</button>
                <button id="learnerRequestIssuer" class="btn btn-outline-success">Request Issuer Attestation</button>
                <button id="learnerSelfAttest" class="btn btn-outline-warning">Self-attest Low Trust</button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Evidence Builder</div>
            <div class="card-body">
              <div class="row g-2 mb-3">
                <div class="col-md-6"><label class="form-label small text-secondary">Insight summary</label><textarea class="form-control" rows="3">Revenue grew in East region, but discount leakage reduced margin.</textarea></div>
                <div class="col-md-6"><label class="form-label small text-secondary">Risk note</label><textarea class="form-control" rows="3">Abnormal discount pattern needs manager review before forecast update.</textarea></div>
              </div>
              <pre class="code-block mb-0">${state.evidence === 'generated' ? JSON.stringify(data.evidencePackage, null, 2) : 'No evidence generated yet.'}</pre>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header bg-white fw-bold">Score Breakdown Preview</div>
        <div class="card-body table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead><tr><th>Area</th><th>Score</th><th>Reviewer note</th></tr></thead>
            <tbody>${scoreRows}</tbody>
          </table>
        </div>
      </div>
    `;
  },
  bind() {
    document.getElementById('learnerGenerateEvidence')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.evidence = 'generated';
    }, 'Learner generated local Evidence Bundle'));

    document.getElementById('learnerComputeHashes')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.evidence = 'generated';
      s.hashesComputed = true;
    }, 'Frontend computed certificateHash, evidenceHash, and scoreHash'));

    document.getElementById('learnerRequestIssuer')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.evidence = 'generated';
      s.hashesComputed = true;
      s.issuerReview = 'review_pending';
    }, 'Learner requested issuer attestation'));

    document.getElementById('learnerSelfAttest')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.proofStatus = 'active';
      s.trustLevel = 'SelfAttested';
      s.issuedCount += 1;
    }, 'Learner registered self-attested proof mock'));
  }
};
