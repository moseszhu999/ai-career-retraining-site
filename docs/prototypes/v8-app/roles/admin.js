window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.admin = {
  title: 'Admin / Contract Owner Dashboard',
  subtitle: 'Manage issuer registry, curriculum governance, schema versions, contract config, and platform events.',
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
      <tr><td><code>${schema.id}</code></td><td><span class="badge text-bg-${schema.status === 'active' ? 'success' : 'warning'}">${schema.status}</span></td><td>${schema.credentials}</td></tr>
    `).join('');

    const lessonRows = data.learningModules.map((module) => `
      <tr>
        <td><strong>${module.title}</strong><br><small class="text-secondary">${module.objective}</small></td>
        <td>${module.type}</td>
        <td>${module.duration}</td>
        <td><span class="badge text-bg-${module.status === 'available' ? 'success' : 'warning'}">${module.status}</span></td>
        <td><button class="btn btn-sm btn-outline-primary">Edit</button></td>
      </tr>
    `).join('');

    const quizRows = data.quizQuestions.map((q, index) => `
      <tr><td>Q${index + 1}</td><td>${q.question}</td><td>${q.choices.length}</td><td><span class="badge text-bg-success">answer key ready</span></td></tr>
    `).join('');

    const taskRows = data.projectTasks.map((task) => `
      <tr><td><strong>${task.title}</strong><br><small class="text-secondary">${task.credentialId}</small></td><td>${task.difficulty}</td><td>${task.estimatedTime}</td><td>${task.evidenceOutputs.length}</td></tr>
    `).join('');

    return `
      <div class="row g-3 mb-4">
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Authorized issuers</div><div class="display-6">${state.issuerCount}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Learning modules</div><div class="display-6">${data.learningModules.length}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Schema versions</div><div class="display-6">${data.schemaVersions.length}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Owner</div><div class="display-6">Multisig</div></div></div></div>
      </div>

      <div id="admin-curriculum" class="card mb-4 border-primary">
        <div class="card-header bg-white fw-bold">Curriculum Governance / Course Builder</div>
        <div class="card-body">
          <div class="row g-3 mb-3">
            <div class="col-lg-4"><label class="form-label small text-secondary">Credential path</label><select class="form-select"><option>AI Data Analysis Assistant</option><option>AI Trade Documentation Assistant</option></select></div>
            <div class="col-lg-4"><label class="form-label small text-secondary">Publish mode</label><select class="form-select"><option>Draft -> Review -> Published</option><option>Pilot only</option><option>Archive old version</option></select></div>
            <div class="col-lg-4"><label class="form-label small text-secondary">Content policy</label><input class="form-control" value="No private learner answers inside published curriculum"></div>
          </div>
          <div class="table-responsive"><table class="table table-hover align-middle mb-0"><thead><tr><th>Module</th><th>Type</th><th>Duration</th><th>Status</th><th>Action</th></tr></thead><tbody>${lessonRows}</tbody></table></div>
          <div class="d-flex flex-wrap gap-2 mt-3"><button id="adminPublishCurriculum" class="btn btn-primary">Publish Curriculum Version Mock</button><button class="btn btn-outline-primary">Add Lesson Mock</button><button class="btn btn-outline-secondary">Archive Draft Mock</button></div>
        </div>
      </div>

      <div class="row g-3 mb-4">
        <div id="admin-quiz" class="col-xl-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Quiz Bank</div><div class="card-body table-responsive"><table class="table table-sm table-hover align-middle mb-0"><thead><tr><th>ID</th><th>Question</th><th>Choices</th><th>Status</th></tr></thead><tbody>${quizRows}</tbody></table></div></div></div>
        <div id="admin-practice" class="col-xl-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Practice Lab Templates</div><div class="card-body table-responsive"><table class="table table-sm table-hover align-middle mb-0"><thead><tr><th>Task</th><th>Difficulty</th><th>Time</th><th>Evidence outputs</th></tr></thead><tbody>${taskRows}</tbody></table></div></div></div>
      </div>

      <div class="row g-3 mb-4">
        <div id="admin-registry" class="col-xl-7"><div class="card h-100"><div class="card-header bg-white fw-bold">Issuer Registry</div><div class="card-body table-responsive"><table class="table table-hover align-middle"><thead><tr><th>Issuer</th><th>Type</th><th>Status</th><th>Action</th></tr></thead><tbody>${issuerRows}</tbody></table><button id="adminAddIssuer" class="btn btn-primary">Authorize New Issuer Mock</button></div></div></div>
        <div class="col-xl-5"><div class="card h-100"><div class="card-header bg-white fw-bold">Contract Configuration</div><div class="card-body"><dl class="row small mb-0"><dt class="col-5">Registry contract</dt><dd class="col-7"><code>${window.ProofSkillContract.address}</code></dd><dt class="col-5">Owner mode</dt><dd class="col-7">Multisig mock</dd><dt class="col-5">Proof statuses</dt><dd class="col-7">None · Active · Revoked · Expired</dd><dt class="col-5">Attestation levels</dt><dd class="col-7">Self · Issuer · Evaluator</dd><dt class="col-5">Raw data policy</dt><dd class="col-7">Never store private answers on-chain</dd></dl></div></div></div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Schema / Rubric Versions</div><div class="card-body table-responsive"><table class="table table-hover align-middle mb-0"><thead><tr><th>Version</th><th>Status</th><th>Credentials</th></tr></thead><tbody>${schemaRows}</tbody></table></div></div></div>
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Activity Log</div><div class="card-body activity-log">${log}</div></div></div>
      </div>
    `;
  },
  bind() {
    document.getElementById('adminAddIssuer')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.issuerCount += 1; }, 'Admin authorized new issuer wallet mock'));
    document.getElementById('adminPublishCurriculum')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.curriculumVersion = `curriculum-${Date.now()}`; }, 'Admin published curriculum version mock'));
  }
};
