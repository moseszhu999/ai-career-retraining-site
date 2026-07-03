window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.issuer = {
  title: 'Issuer / Training Partner Dashboard',
  subtitle: 'Review evidence bundles and issue or revoke credential proofs with issuer wallet.',
  render(state) {
    const queueRows = state.issuerReview === 'not_requested'
      ? '<tr><td colspan="5" class="text-secondary">No pending issuer request.</td></tr>'
      : `<tr><td>Mia Chen</td><td>AI Data Analysis</td><td><span class="badge text-bg-warning">${state.issuerReview}</span></td><td>86</td><td><button class="btn btn-sm btn-outline-primary">Open</button></td></tr>`;

    return `
      <div class="row g-3 mb-4">
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Review queue</div><div class="display-6">${state.issuerReview === 'review_pending' ? 1 : 0}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Issuer wallet</div><div class="display-6">OK</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Issued</div><div class="display-6">${state.issuedCount}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Can issue</div><div class="display-6">${state.issuerReview === 'approved' || state.evaluatorReview === 'evaluator_set_ready' ? 'Yes' : 'No'}</div></div></div></div>
      </div>

      <div class="card mb-3">
        <div class="card-header bg-white fw-bold">Pending Evidence Bundles</div>
        <div class="card-body table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead><tr><th>Learner</th><th>Credential</th><th>Status</th><th>Score</th><th>Action</th></tr></thead>
            <tbody>${queueRows}</tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <div class="card-header bg-white fw-bold">Issuer contract actions</div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-lg-6">
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
            </div>
            <div class="col-lg-6">
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
