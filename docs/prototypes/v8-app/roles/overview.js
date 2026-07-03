window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.overview = {
  title: 'Platform Overview',
  subtitle: 'Learning, evidence, attestation, and verification in one browser-first workflow.',
  render(state) {
    const data = window.ProofSkillData;
    const smoke = window.ProofSkillSmokeTest?.renderTable();
    const smokeResult = smoke?.result || { passed: 0, failed: 0, total: 0 };
    const smokeTable = smoke?.html || '<div class="text-secondary">Smoke test utility not loaded.</div>';
    const routes = window.ProofSkillDemoRoutes || [];
    const routeCards = routes.map((route) => `
      <div class="col-xl-4">
        <div class="card h-100">
          <div class="card-header bg-white d-flex justify-content-between align-items-center gap-2">
            <strong>${route.title}</strong>
            <span class="badge text-bg-primary">${route.duration}</span>
          </div>
          <div class="card-body">
            <div class="small text-uppercase text-secondary fw-bold mb-1">Audience</div>
            <p class="mb-2">${route.audience}</p>
            <div class="small text-uppercase text-secondary fw-bold mb-1">Promise</div>
            <p class="text-secondary small">${route.promise}</p>
            <div class="list-group list-group-flush border rounded-3">
              ${route.steps.map((step, index) => `
                <button class="list-group-item list-group-item-action small" data-route-step-role="${step.target.role}" data-route-step-tab="${step.target.learnerTab || ''}" data-route-step-anchor="${step.target.anchor || ''}">
                  <div class="fw-semibold">${index + 1}. ${step.label}</div>
                  <div class="text-secondary">${step.talk}</div>
                </button>
              `).join('')}
            </div>
          </div>
        </div>
      </div>
    `).join('');

    return `
      <div class="p-4 p-lg-5 bg-white rounded-4 shadow-sm border mb-4">
        <div class="row g-4 align-items-center">
          <div class="col-lg-8">
            <span class="badge text-bg-success mb-3">Online prototype</span>
            <h2 class="display-6 fw-bold mb-3">ProofSkill AI turns practical training into verifiable skill credentials.</h2>
            <p class="lead text-secondary mb-4">The prototype links curriculum, practice labs, evidence bundles, issuer review, optional evaluator review, and verifier-facing proof checks.</p>
            <div class="d-flex flex-wrap gap-2">
              <button class="btn btn-primary" onclick="window.ProofSkillApp.runNextDemoStep()">Start guided demo</button>
              <button class="btn btn-outline-primary" onclick="window.ProofSkillApp.setRole('learner')">Learner journey</button>
              <button class="btn btn-outline-secondary" onclick="window.ProofSkillApp.setRole('verifier')">Verifier view</button>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="card bg-light border-0">
              <div class="card-body">
                <div class="row g-3 text-center">
                  <div class="col-6"><div class="display-6 fw-bold">6</div><div class="small text-secondary">workspaces</div></div>
                  <div class="col-6"><div class="display-6 fw-bold">${data.credentialPaths.length}</div><div class="small text-secondary">paths</div></div>
                  <div class="col-6"><div class="display-6 fw-bold">${data.learningModules.length}</div><div class="small text-secondary">modules</div></div>
                  <div class="col-6"><div class="display-6 fw-bold">${data.cohorts.length}</div><div class="small text-secondary">cohorts</div></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4 border-${smokeResult.failed === 0 ? 'success' : 'danger'}">
        <div class="card-header bg-white d-flex justify-content-between align-items-center flex-wrap gap-2">
          <strong>Built-in Smoke Test</strong>
          <div><span class="badge text-bg-${smokeResult.failed === 0 ? 'success' : 'danger'}">${smokeResult.passed}/${smokeResult.total} passed</span> <button id="rerunSmokeTest" class="btn btn-sm btn-outline-primary">Re-run</button></div>
        </div>
        <div class="card-body table-responsive">${smokeTable}</div>
      </div>

      <div class="card mb-4">
        <div class="card-header bg-white fw-bold">Demo Route Selector</div>
        <div class="card-body"><div class="row g-3">${routeCards}</div></div>
      </div>

      <div class="card mb-4">
        <div class="card-header bg-white fw-bold">End-to-end flow</div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md"><div class="card h-100 border-primary"><div class="card-body text-center"><span class="badge text-bg-primary mb-2">Admin</span><p class="small mb-0">publish curriculum and schema</p></div></div></div>
            <div class="col-md"><div class="card h-100 border-primary"><div class="card-body text-center"><span class="badge text-bg-primary mb-2">Learner</span><p class="small mb-0">study, quiz, practice, evidence</p></div></div></div>
            <div class="col-md"><div class="card h-100 border-primary"><div class="card-body text-center"><span class="badge text-bg-primary mb-2">Issuer</span><p class="small mb-0">monitor cohort and issue proof</p></div></div></div>
            <div class="col-md"><div class="card h-100 border-primary"><div class="card-body text-center"><span class="badge text-bg-primary mb-2">Evaluator</span><p class="small mb-0">optional review and signature</p></div></div></div>
            <div class="col-md"><div class="card h-100 border-primary"><div class="card-body text-center"><span class="badge text-bg-primary mb-2">Verifier</span><p class="small mb-0">check proof and evidence signals</p></div></div></div>
          </div>
        </div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Prototype proves</div><div class="card-body"><ul class="mb-0"><li>Training flow can create structured evidence.</li><li>Issuers can review evidence before signing.</li><li>Trust levels can be explained clearly.</li><li>Verifier view can avoid exposing private raw files.</li></ul></div></div></div>
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Boundary</div><div class="card-body"><ul class="mb-0"><li>Frontend mock state only.</li><li>No real wallet transaction yet.</li><li>No backend database yet.</li><li>No real scoring engine yet.</li></ul></div></div></div>
      </div>
    `;
  },
  bind() {
    document.getElementById('rerunSmokeTest')?.addEventListener('click', () => window.ProofSkillApp.render());
    document.querySelectorAll('[data-route-step-role]').forEach((button) => {
      button.addEventListener('click', () => window.ProofSkillApp.setMenuTarget({
        role: button.dataset.routeStepRole,
        learnerTab: button.dataset.routeStepTab || null,
        anchor: button.dataset.routeStepAnchor || null
      }));
    });
  }
};
