window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.admin = {
  title: 'Admin / Contract Owner Dashboard',
  subtitle: 'Manage issuer registry, schema versions, and contract events.',
  render(state) {
    const log = state.events.length
      ? state.events.map((event) => `<div class="activity-log-item">${event}</div>`).join('')
      : '<div class="text-secondary">No events yet.</div>';

    return `
      <div class="row g-3 mb-4">
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Authorized issuers</div><div class="display-6">${state.issuerCount}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Schemas</div><div class="display-6">3</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Events</div><div class="display-6">${state.events.length}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Owner</div><div class="display-6">Multisig</div></div></div></div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Issuer Registry</div>
            <div class="card-body table-responsive">
              <table class="table table-hover align-middle">
                <thead><tr><th>Wallet</th><th>Status</th><th>Action</th></tr></thead>
                <tbody>
                  <tr><td>0xAuthorizedIssuerMock</td><td><span class="badge text-bg-success">active</span></td><td><button class="btn btn-sm btn-outline-danger">Remove</button></td></tr>
                  <tr><td>0xTrainingPartnerMock</td><td><span class="badge text-bg-success">active</span></td><td><button class="btn btn-sm btn-outline-danger">Remove</button></td></tr>
                </tbody>
              </table>
              <button id="adminAddIssuer" class="btn btn-primary">Authorize New Issuer Mock</button>
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
