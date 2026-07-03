window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.learner = {
  title: 'Learner / Candidate Dashboard',
  subtitle: 'Complete tasks, generate local evidence, compute hashes, and request attestation.',
  render(state) {
    const evidenceBadge = state.evidence === 'generated'
      ? '<span class="badge text-bg-success">Generated</span>'
      : '<span class="badge text-bg-secondary">Not generated</span>';
    const proofBadge = state.proofStatus === 'active'
      ? `<span class="badge text-bg-success">${state.trustLevel}</span>`
      : '<span class="badge text-bg-secondary">Not registered</span>';

    return `
      <div class="row g-3 mb-4">
        <div class="col-md-4"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Credential path</div><div class="display-6">AI Data</div><span class="badge text-bg-primary">Level 2 target</span></div></div></div>
        <div class="col-md-4"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Local evidence</div><div class="h3 mb-2">${state.evidence === 'generated' ? 'Ready' : 'Draft'}</div>${evidenceBadge}</div></div></div>
        <div class="col-md-4"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Proof status</div><div class="h3 mb-2">${state.proofStatus}</div>${proofBadge}</div></div></div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">My task workspace</div>
            <div class="card-body">
              <p><strong>Sales Performance Mini BI Report</strong></p>
              <p class="text-secondary">Public task bundle is loaded in the frontend. Private answer files remain local or encrypted.</p>
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
            <div class="card-header bg-white fw-bold">Local Evidence Bundle</div>
            <div class="card-body">
              <pre class="code-block mb-0">${state.evidence === 'generated' ? JSON.stringify({ bundleType: 'EvidenceBundle', credentialType: 'AI_DATA_ANALYSIS_ASSISTANT', evidenceHash: state.hashesComputed ? '0xEVIDENCE_HASH_MOCK_001' : null, scoreHash: state.hashesComputed ? '0xSCORE_HASH_MOCK_001' : null, certificateHash: state.hashesComputed ? '0xCERT_HASH_MOCK_001' : null, overallScore: 86 }, null, 2) : 'No evidence generated yet.'}</pre>
            </div>
          </div>
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
