window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.issuer = {
  title: 'Issuer / Training Partner Dashboard',
  subtitle: 'Review evidence packages, check hashes, and issue credential proofs with issuer wallet.',
  render(state) {
    const data = window.ProofSkillData;
    const learners = data.learners.map((learner) => `
      <tr>
        <td><strong>${learner.name}</strong><br><small class="text-secondary">${learner.wallet}</small></td>
        <td>${learner.credential}</td>
        <td><span class="badge text-bg-${learner.status.includes('evaluator') ? 'success' : 'warning'}">${learner.status}</span></td>
        <td>${learner.score}</td>
        <td><button class="btn btn-sm btn-outline-primary">Open Review</button></td>
      </tr>
    `).join('');

    const hashRows = ['certificateHash', 'evidenceHash', 'scoreHash', 'schemaHash'].map((key) => `
      <tr><td>${key}</td><td><code>${data.evidencePackage[key]}</code></td><td><span class="badge text-bg-success">match</span></td></tr>
    `).join('');

    const rubricRows = data.rubrics.map((item) => `
      <tr>
        <td>${item.item}</td>
        <td>${item.weight}</td>
        <td>${item.evaluatorScore}</td>
        <td><span class="badge text-bg-${item.issuerCheck === 'pass' ? 'success' : 'warning'}">${item.issuerCheck}</span></td>
      </tr>
    `).join('');

    return `
      <div class="row g-3 mb-4">
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Review queue</div><div class="display-6">${state.issuerReview === 'not_requested' ? 2 : 3}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Issuer wallet</div><div class="display-6">OK</div><span class="badge text-bg-success">authorized</span></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Issued</div><div class="display-6">${state.issuedCount}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Can issue</div><div class="display-6">${state.issuerReview === 'approved' || state.evaluatorReview === 'evaluator_set_ready' ? 'Yes' : 'Review'}</div></div></div></div>
      </div>

      <div class="card mb-4">
        <div class="card-header bg-white fw-bold">Review Queue</div>
        <div class="card-body table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead><tr><th>Learner</th><th>Credential</th><th>Status</th><th>Score</th><th>Action</th></tr></thead>
            <tbody>${learners}</tbody>
          </table>
        </div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-xl-5">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Evidence Review Detail</div>
            <div class="card-body">
              <div class="alert alert-warning"><strong>Issuer decision:</strong> Verify evidence completeness, score hash, and schema version before signing.</div>
              <dl class="row small mb-0">
                <dt class="col-5">Learner</dt><dd class="col-7">Mia Chen</dd>
                <dt class="col-5">Credential</dt><dd class="col-7">AI Data Analysis Assistant</dd>
                <dt class="col-5">Overall score</dt><dd class="col-7">86 / 100</dd>
                <dt class="col-5">Privacy</dt><dd class="col-7">Raw files hidden by default</dd>
                <dt class="col-5">Evidence outputs</dt><dd class="col-7">4 files represented by evidenceHash</dd>
              </dl>
            </div>
          </div>
        </div>
        <div class="col-xl-7">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Hash Match Checklist</div>
            <div class="card-body table-responsive">
              <table class="table table-sm align-middle mb-0">
                <thead><tr><th>Field</th><th>Value</th><th>Status</th></tr></thead>
                <tbody>${hashRows}</tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Rubric Summary</div>
            <div class="card-body table-responsive">
              <table class="table table-sm table-hover align-middle mb-0">
                <thead><tr><th>Rubric</th><th>Weight</th><th>Score</th><th>Issuer check</th></tr></thead>
                <tbody>${rubricRows}</tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Issuer Contract Actions</div>
            <div class="card-body">
              <pre class="code-block">registerIssuerAttestedProof(
  credentialId,
  holder,
  credentialType,
  overallScore,
  certificateHash,
  evidenceHash,
  scoreHash,
  schemaHash,
  expiresAt
)</pre>
              <div class="d-flex flex-wrap gap-2">
                <button id="issuerApproveEvidence" class="btn btn-outline-primary">Approve Evidence</button>
                <button id="issuerIssueProof" class="btn btn-primary">Issue IssuerAttested Proof</button>
                <button id="issuerIssueEvaluatorProof" class="btn btn-outline-success">Issue EvaluatorSigned Proof</button>
                <button id="issuerRevoke" class="btn btn-outline-danger">Revoke Mock Credential</button>
              </div>
              <p class="text-secondary small mt-3 mb-0">All actions are frontend mock state changes. No real wallet transaction is sent.</p>
            </div>
          </div>
        </div>
      </div>
    `;
  },
  bind() {
    document.getElementById('issuerApproveEvidence')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.issuerReview = 'approved';
    }, 'Issuer approved Evidence Bundle'));

    document.getElementById('issuerIssueProof')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.proofStatus = 'active';
      s.trustLevel = 'IssuerAttested';
      s.issuerReview = 'issued';
      s.issuedCount += 1;
    }, 'Issuer registered IssuerAttested proof mock'));

    document.getElementById('issuerIssueEvaluatorProof')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.evaluatorReview = 'evaluator_set_ready';
      s.evaluatorSetHash = '0xEVALUATOR_SET_HASH_MOCK_001';
      s.proofStatus = 'active';
      s.trustLevel = 'EvaluatorSigned';
      s.issuerReview = 'issued';
      s.issuedCount += 1;
    }, 'Issuer registered EvaluatorSigned proof mock'));

    document.getElementById('issuerRevoke')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.proofStatus = 'revoked';
    }, 'Issuer revoked credential proof mock'));
  }
};
