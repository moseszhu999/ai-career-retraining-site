window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.issuer = {
  title: 'Issuer / Training Partner Dashboard',
  subtitle: 'Monitor learning cohorts, review evidence packages, and issue credential proofs.',
  render(state) {
    const data = window.ProofSkillData;
    const cohortRows = data.cohorts.map((cohort) => `
      <tr>
        <td><strong>${cohort.name}</strong><br><small class="text-secondary">${cohort.path}</small></td>
        <td>${cohort.learners}</td>
        <td style="width: 22%"><div class="progress"><div class="progress-bar" style="width:${cohort.avgProgress}%">${cohort.avgProgress}%</div></div></td>
        <td>${cohort.quizPassRate}</td>
        <td>${cohort.practiceSubmitted}</td>
        <td>${cohort.evidenceReady}</td>
        <td><span class="badge text-bg-${cohort.status === 'active' ? 'success' : 'warning'}">${cohort.status}</span></td>
      </tr>
    `).join('');

    const learnerProgressRows = data.learnerProgress.map((learner) => `
      <tr>
        <td><strong>${learner.name}</strong><br><small class="text-secondary">${learner.wallet}</small></td>
        <td>${learner.path}</td>
        <td style="width: 18%"><div class="progress"><div class="progress-bar" style="width:${learner.progress}%">${learner.progress}%</div></div></td>
        <td>${learner.quiz ?? '--'}</td>
        <td><span class="badge text-bg-${learner.practice === 'submitted' ? 'success' : learner.practice === 'in progress' ? 'warning' : 'secondary'}">${learner.practice}</span></td>
        <td><span class="badge text-bg-${learner.evidence === 'ready' ? 'success' : 'secondary'}">${learner.evidence}</span></td>
        <td>${learner.nextAction}</td>
      </tr>
    `).join('');

    const curriculumRows = data.curriculumOps.map((item) => `
      <tr>
        <td>${item.item}</td>
        <td><span class="badge text-bg-${item.status === 'published' ? 'success' : 'primary'}">${item.status}</span></td>
        <td>${item.completions}</td>
        <td><span class="badge text-bg-${item.issue === 'none' ? 'success' : 'warning'}">${item.issue}</span></td>
      </tr>
    `).join('');

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
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Active cohorts</div><div class="display-6">${data.cohorts.length}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Learning evidence ready</div><div class="display-6">${data.cohorts.reduce((sum, c) => sum + c.evidenceReady, 0)}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Issued</div><div class="display-6">${state.issuedCount}</div></div></div></div>
        <div class="col-md-3"><div class="card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Issuer wallet</div><div class="display-6">OK</div><span class="badge text-bg-success">authorized</span></div></div></div>
      </div>

      <div id="learning-ops" class="card mb-4 border-primary">
        <div class="card-header bg-white fw-bold">Learning Ops · Cohort Monitor</div>
        <div class="card-body table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead><tr><th>Cohort</th><th>Learners</th><th>Avg progress</th><th>Quiz pass</th><th>Practice</th><th>Evidence ready</th><th>Status</th></tr></thead>
            <tbody>${cohortRows}</tbody>
          </table>
        </div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-xl-8"><div class="card h-100"><div class="card-header bg-white fw-bold">Learner Progress and Next Actions</div><div class="card-body table-responsive"><table class="table table-hover align-middle mb-0"><thead><tr><th>Learner</th><th>Path</th><th>Progress</th><th>Quiz</th><th>Practice</th><th>Evidence</th><th>Next action</th></tr></thead><tbody>${learnerProgressRows}</tbody></table></div></div></div>
        <div class="col-xl-4"><div class="card h-100"><div class="card-header bg-white fw-bold">Curriculum Ops</div><div class="card-body table-responsive"><table class="table table-sm align-middle mb-0"><thead><tr><th>Item</th><th>Status</th><th>Done</th><th>Issue</th></tr></thead><tbody>${curriculumRows}</tbody></table></div></div></div>
      </div>

      <div id="review-queue" class="card mb-4">
        <div class="card-header bg-white fw-bold">Credential Review Queue</div>
        <div class="card-body table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead><tr><th>Learner</th><th>Credential</th><th>Status</th><th>Score</th><th>Action</th></tr></thead>
            <tbody>${learners}</tbody>
          </table>
        </div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-xl-5"><div class="card h-100"><div class="card-header bg-white fw-bold">Evidence Review Detail</div><div class="card-body"><div class="alert alert-warning"><strong>Issuer decision:</strong> Verify learning completion, practice submission, evidence completeness, score hash, and schema version before signing.</div><dl class="row small mb-0"><dt class="col-5">Learner</dt><dd class="col-7">Mia Chen</dd><dt class="col-5">Learning progress</dt><dd class="col-7">100%</dd><dt class="col-5">Quiz score</dt><dd class="col-7">88 / 100</dd><dt class="col-5">Practice lab</dt><dd class="col-7">submitted</dd><dt class="col-5">Overall score</dt><dd class="col-7">86 / 100</dd><dt class="col-5">Evidence outputs</dt><dd class="col-7">4 files represented by evidenceHash</dd></dl></div></div></div>
        <div class="col-xl-7"><div class="card h-100"><div class="card-header bg-white fw-bold">Hash Match Checklist</div><div class="card-body table-responsive"><table class="table table-sm align-middle mb-0"><thead><tr><th>Field</th><th>Value</th><th>Status</th></tr></thead><tbody>${hashRows}</tbody></table></div></div></div>
      </div>

      <div id="contract-actions" class="row g-3">
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Rubric Summary</div><div class="card-body table-responsive"><table class="table table-sm table-hover align-middle mb-0"><thead><tr><th>Rubric</th><th>Weight</th><th>Score</th><th>Issuer check</th></tr></thead><tbody>${rubricRows}</tbody></table></div></div></div>
        <div class="col-lg-6"><div class="card h-100"><div class="card-header bg-white fw-bold">Issuer Contract Actions</div><div class="card-body"><pre class="code-block">registerIssuerAttestedProof(
  credentialId,
  holder,
  credentialType,
  overallScore,
  certificateHash,
  evidenceHash,
  scoreHash,
  schemaHash,
  expiresAt
)</pre><div class="d-flex flex-wrap gap-2"><button id="issuerApproveEvidence" class="btn btn-outline-primary">Approve Evidence</button><button id="issuerIssueProof" class="btn btn-primary">Issue IssuerAttested Proof</button><button id="issuerIssueEvaluatorProof" class="btn btn-outline-success">Issue EvaluatorSigned Proof</button><button id="issuerRevoke" class="btn btn-outline-danger">Revoke Mock Credential</button></div><p class="text-secondary small mt-3 mb-0">All actions are frontend mock state changes. No real wallet transaction is sent.</p></div></div></div>
      </div>
    `;
  },
  bind() {
    document.getElementById('issuerApproveEvidence')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.issuerReview = 'approved'; }, 'Issuer approved Evidence Bundle'));
    document.getElementById('issuerIssueProof')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.proofStatus = 'active'; s.trustLevel = 'IssuerAttested'; s.issuerReview = 'issued'; s.issuedCount += 1; }, 'Issuer registered IssuerAttested proof mock'));
    document.getElementById('issuerIssueEvaluatorProof')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.evaluatorReview = 'evaluator_set_ready'; s.evaluatorSetHash = '0xEVALUATOR_SET_HASH_MOCK_001'; s.proofStatus = 'active'; s.trustLevel = 'EvaluatorSigned'; s.issuerReview = 'issued'; s.issuedCount += 1; }, 'Issuer registered EvaluatorSigned proof mock'));
    document.getElementById('issuerRevoke')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => { s.proofStatus = 'revoked'; }, 'Issuer revoked credential proof mock'));
  }
};
