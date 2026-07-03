window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.admin = {
  title: 'Admin / Contract Owner Dashboard',
  subtitle: 'Manage issuer registry, schema versions, contract config, and platform events.',
  render(state) {
    const data = window.ProofSkillData;
    const log = state.events.length
      ? state.events.map((event) => `<div class="activity-log-item">${event}</div>`).join('')
      : '<div class="text-secondary">No events yet.</div>';

    const issuerRows = data.issuerRegistry.map((issuer) => `
      <tr>
        <td><strong>${issuer.name}</strong><br><small class="text-secondary">${issuer.wallet}</small></td>
        <td>${issuer.type}</td>
        <td><span class="badge text-bg-${issuer.status === 'active' ? 'success' : 'warning'}">${issuer.status}</span></td>
        <td><button class="btn btn-sm btn-outline-danger">Remove</button></td>
      </tr>
    `).join('');

    const schemaRows = data.schemaVersions.map((schema) => `
      <tr>
        <td><code>${schema.id}</code></td>
        <td><span class="badge text-bg-${schema.status === 'active' ? 'success' : 'warning'}">${schema.status}</span></td>
        <td>${schema.credentials}</td>
      </tr>
    `).join('');

    return `
      <div class="row g-3 mb-4">
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Authorized issuers</div><div class="display-6">${state.issuerCount}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Schemas</div><div class="display-6">${data.schemaVersions.length}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Events</div><div class="display-6">${state.events.length}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Owner</div><div class="display-6">Multisig</div></div></div></div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-xl-7">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Issuer Registry</div>
            <div class="card-body table-responsive">
              <table class="table table-hover align-middle">
                <thead><tr><th>Issuer</th><th>Type</th><th>Status</th><th>Action</th></tr></thead>
                <tbody>${issuerRows}</tbody>
              </table>
              <button id="adminAddIssuer" class="btn btn-primary">Authorize New Issuer Mock</button>
            </div>
          </div>
        </div>
        <div class="col-xl-5">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Contract Configuration</div>
            <div class="card-body">
              <dl class="row small mb-0">
                <dt class="col-5">Registry contract</dt><dd class="col-7"><code>${window.ProofSkillContract.address}</code></dd>
                <dt class="col-5">Owner mode</dt><dd class="col-7">Multisig mock</dd>
                <dt class="col-5">Proof statuses</dt><dd class="col-7">None · Active · Revoked · Expired</dd>
                <dt class="col-5">Attestation levels</dt><dd class="col-7">Self · Issuer · Evaluator</dd>
                <dt class="col-5">Raw data policy</dt><dd class="col-7">Never store private answers on-chain</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Schema / Rubric Versions</div>
            <div class="card-body table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead><tr><th>Version</th><th>Status</th><th>Credentials</th></tr></thead>
                <tbody>${schemaRows}</tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Activity Log</div>
            <div class="card-body activity-log">${log}</div>
          </div>
        </div>
      </div>
    `;
  },
  bind() {
    document.getElementById('adminAddIssuer')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.issuerCount += 1;
    }, 'Admin authorized new issuer wallet mock'));
  }
};
