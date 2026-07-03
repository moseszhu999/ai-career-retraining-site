window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.verifier = {
  title: 'Verifier / Organization Dashboard',
  subtitle: 'Verify credential proof, inspect trust level, and review work-readiness signals.',
  render(state) {
    const data = window.ProofSkillData;
    const candidate = data.candidateSkillProfile;
    const record = {
      ...data.contractRecord,
      status: state.proofStatus === 'active' ? 'Active' : state.proofStatus,
      attestationLevel: state.trustLevel === 'none' ? data.contractRecord.attestationLevel : state.trustLevel
    };
    const meaning = state.proofStatus === 'active'
      ? `Valid proof. Trust level: ${record.attestationLevel}. Verifier can rely on contract status, issuer authorization, and hash match.`
      : state.proofStatus === 'revoked'
        ? 'Credential proof is revoked. Verifier should not accept this credential.'
        : 'No active contract proof available yet. Use Learner and Issuer flows first, or inspect the mock contract record below.';

    const checklist = [
      ['Credential exists', state.proofStatus === 'active' ? 'pass' : 'pending'],
      ['Status active', state.proofStatus === 'active' ? 'pass' : 'pending'],
      ['Issuer authorized', 'pass'],
      ['Hash match', state.proofStatus === 'active' ? 'pass' : 'pending'],
      ['Not revoked', state.proofStatus === 'revoked' ? 'fail' : 'pass'],
      ['Not expired', 'pass']
    ].map(([item, status]) => `<li class="list-group-item d-flex justify-content-between"><span>${item}</span><span class="badge text-bg-${status === 'pass' ? 'success' : status === 'fail' ? 'danger' : 'secondary'}">${status}</span></li>`).join('');

    const roleRows = data.employerRoles.map((role) => `
      <tr><td><strong>${role.title}</strong><br><small class="text-secondary">${role.companyType}</small></td><td>${role.preferredCredential}</td><td>${role.minimumTrust}</td></tr>
    `).join('');

    const fitRows = data.jobFitMatrix.map((row) => `
      <tr><td>${row.signal}</td><td>${row.required}</td><td style="width: 30%"><div class="progress"><div class="progress-bar" style="width:${row.candidate}%">${row.candidate}</div></div></td><td><code>${row.evidence}</code></td></tr>
    `).join('');

    const riskRows = data.hiringRiskNotes.map((item) => `<tr><td>${item.risk}</td><td>${item.mitigation}</td></tr>`).join('');

    return `
      <div id="verifier-proof" class="row g-3 mb-4">
        <div class="col-lg-5"><div class="card h-100"><div class="card-header bg-white fw-bold">Verify Credential</div><div class="card-body"><p class="text-secondary">Verifier reads smart contract proof. No backend lookup.</p><label class="form-label small text-secondary">Credential ID or proof link</label><div class="input-group mb-3"><input id="verifierCredentialId" class="form-control" value="${data.contractRecord.credentialId}"><button id="verifierReadContract" class="btn btn-primary">Read Contract</button></div><div class="alert alert-info mb-0">Credential verification is a work-readiness signal. It is not an automatic decision system.</div></div></div></div>
        <div class="col-lg-7"><div class="card h-100 border-primary"><div class="card-header bg-white fw-bold">Candidate Skill Signal Profile</div><div class="card-body"><div class="d-flex justify-content-between gap-3 flex-wrap mb-3"><div><h4 class="mb-1">${candidate.name}</h4><div class="text-secondary small">${candidate.wallet}</div><div class="mt-2"><span class="badge text-bg-primary">${candidate.credential}</span> <span class="badge text-bg-success">${candidate.trustLevel}</span></div></div><div class="text-end"><div class="small text-uppercase text-secondary fw-bold">Role-fit signal</div><div class="display-6">${candidate.overallFit}</div><span class="badge text-bg-success">${candidate.recommendedRole}</span></div></div><div class="row g-3"><div class="col-md-6"><div class="small text-uppercase text-secondary fw-bold mb-2">Strengths</div><ul class="small mb-0">${candidate.strengths.map((item) => `<li>${item}</li>`).join('')}</ul></div><div class="col-md-6"><div class="small text-uppercase text-secondary fw-bold mb-2">Limits</div><ul class="small mb-0">${candidate.limits.map((item) => `<li>${item}</li>`).join('')}</ul></div></div></div></div></div>
      </div>

      <div id="verifier-signals" class="row g-3 mb-4">
        <div class="col-xl-7"><div class="card h-100"><div class="card-header bg-white fw-bold">Role-fit Signal Matrix</div><div class="card-body table-responsive"><table class="table table-hover align-middle mb-0"><thead><tr><th>Signal</th><th>Required</th><th>Candidate</th><th>Evidence</th></tr></thead><tbody>${fitRows}</tbody></table></div></div></div>
        <div class="col-xl-5"><div class="card h-100"><div class="card-header bg-white fw-bold">Role Requirement Reference</div><div class="card-body table-responsive"><table class="table table-sm table-hover align-middle mb-0"><thead><tr><th>Role</th><th>Credential</th><th>Trust</th></tr></thead><tbody>${roleRows}</tbody></table></div></div></div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Contract Verification Result</div><div class="card-body"><div class="row g-3 mb-3"><div class="col-md-6"><div class="border rounded-3 p-3"><div class="small text-uppercase text-secondary fw-bold">Status</div><strong>${record.status}</strong></div></div><div class="col-md-6"><div class="border rounded-3 p-3"><div class="small text-uppercase text-secondary fw-bold">Trust level</div><strong>${record.attestationLevel}</strong></div></div><div class="col-md-6"><div class="border rounded-3 p-3"><div class="small text-uppercase text-secondary fw-bold">Issuer</div><strong>${record.issuer}</strong></div></div><div class="col-md-6"><div class="border rounded-3 p-3"><div class="small text-uppercase text-secondary fw-bold">Revocation</div><strong>${record.revocation}</strong></div></div></div><p class="mb-0 text-secondary">${meaning}</p></div></div></div>
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Verification Checklist</div><div class="card-body"><ul class="list-group">${checklist}</ul></div></div></div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Use-boundary Notes</div><div class="card-body table-responsive"><table class="table table-sm table-hover align-middle mb-0"><thead><tr><th>Boundary</th><th>Handling</th></tr></thead><tbody>${riskRows}</tbody></table></div></div></div>
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Credential Detail</div><div class="card-body"><dl class="row small mb-0"><dt class="col-5">Holder</dt><dd class="col-7">${record.holder}</dd><dt class="col-5">Issued at</dt><dd class="col-7">${record.issuedAt}</dd><dt class="col-5">Expires at</dt><dd class="col-7">${record.expiresAt}</dd><dt class="col-5">Score hash</dt><dd class="col-7"><code>${data.evidencePackage.scoreHash}</code></dd><dt class="col-5">Evidence hash</dt><dd class="col-7"><code>${data.evidencePackage.evidenceHash}</code></dd></dl></div></div></div>
      </div>

      <div id="verifier-receipt" class="card">
        <div class="card-header bg-white fw-bold">Verification Receipt Preview</div>
        <div class="card-body"><pre class="code-block mb-3">${JSON.stringify({ credentialId: record.credentialId, status: record.status, attestationLevel: record.attestationLevel, issuerAuthorized: true, hashMatch: state.proofStatus === 'active', candidate: candidate.name, roleFitSignal: candidate.overallFit, revocation: record.revocation, checkedAt: 'browser-local mock time' }, null, 2)}</pre><p class="small text-secondary mb-0">Raw answers, raw project files, personal data, and trade documents are hidden by default.</p></div>
      </div>
    `;
  },
  bind() {
    document.getElementById('verifierReadContract')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.lastVerifierRead = document.getElementById('verifierCredentialId')?.value || 'unknown'; }, `Verifier read contract proof for ${document.getElementById('verifierCredentialId')?.value || 'unknown'}`));
  }
};
