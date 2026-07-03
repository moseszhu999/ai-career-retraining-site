window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.verifier = {
  title: 'Verifier / Employer Dashboard',
  subtitle: 'Read contract proof, check trust level, and verify hash status.',
  render(state) {
    const meaning = state.proofStatus === 'active'
      ? `Valid proof. Trust level: ${state.trustLevel}. Verifier can rely on contract status and hash match.`
      : state.proofStatus === 'revoked'
        ? 'Credential proof is revoked. Verifier should not accept this credential.'
        : 'No active contract proof available yet.';

    return `
      <div class="row g-3">
        <div class="col-lg-5">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Verify Credential</div>
            <div class="card-body">
              <p class="text-secondary">Verifier reads smart contract proof. No backend lookup.</p>
              <div class="input-group mb-3">
                <input id="verifierCredentialId" class="form-control" value="0xDATA_CREDENTIAL_ID_MOCK_001">
                <button id="verifierReadContract" class="btn btn-primary">Read Contract</button>
              </div>
              <div class="alert alert-info mb-0">A valid hash is not enough. Verifier also checks issuer authorization and attestation level.</div>
            </div>
          </div>
        </div>
        <div class="col-lg-7">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Contract Verification Result</div>
            <div class="card-body">
              <div class="row g-3 mb-3">
                <div class="col-md-6"><div class="border rounded-3 p-3"><div class="small text-uppercase text-secondary fw-bold">Status</div><strong>${state.proofStatus}</strong></div></div>
                <div class="col-md-6"><div class="border rounded-3 p-3"><div class="small text-uppercase text-secondary fw-bold">Trust level</div><strong>${state.trustLevel}</strong></div></div>
                <div class="col-md-6"><div class="border rounded-3 p-3"><div class="small text-uppercase text-secondary fw-bold">Hash match</div><strong>${state.proofStatus === 'active' ? 'true' : 'unknown'}</strong></div></div>
                <div class="col-md-6"><div class="border rounded-3 p-3"><div class="small text-uppercase text-secondary fw-bold">Revocation</div><strong>${state.proofStatus === 'revoked' ? 'revoked' : 'not_revoked'}</strong></div></div>
              </div>
              <p class="mb-0 text-secondary">${meaning}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card mt-3">
        <div class="card-header bg-white fw-bold">Authorized Evidence Summary</div>
        <div class="card-body">
          <p>Completed a simulated trade document review, detected quantity discrepancy, shipping date risk, and generated human review questions.</p>
          <p class="small text-secondary mb-0">Raw answers, raw project files, personal data, and trade documents are hidden by default.</p>
        </div>
      </div>
    `;
  },
  bind() {
    document.getElementById('verifierReadContract')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.lastVerifierRead = document.getElementById('verifierCredentialId')?.value || 'unknown';
    }, `Verifier read contract proof for ${document.getElementById('verifierCredentialId')?.value || 'unknown'}`));
  }
};
