window.ProofSkillRoles = window.ProofSkillRoles || {};

window.ProofSkillRoles.learner = {
  title: 'Learner / Candidate Dashboard',
  subtitle: 'Learn, practice, build evidence, and request attestation.',
  render(state) {
    const data = window.ProofSkillData;
    const tab = state.learnerTab || 'learning';
    const tabs = [
      ['learning', 'Learning'],
      ['path', 'My Path'],
      ['practice', 'Practice Lab'],
      ['evidence', 'Evidence'],
      ['certificate', 'Certificate']
    ].map(([id, label]) => `
      <button class="nav-link ${tab === id ? 'active' : ''}" data-learner-tab="${id}" type="button">${label}</button>
    `).join('');

    const evidenceBadge = state.evidence === 'generated'
      ? '<span class="badge text-bg-success">Generated</span>'
      : '<span class="badge text-bg-secondary">Not generated</span>';
    const proofBadge = state.proofStatus === 'active'
      ? `<span class="badge text-bg-success">${state.trustLevel}</span>`
      : '<span class="badge text-bg-secondary">Not registered</span>';

    const modules = data.learningModules.map((module) => {
      const done = state.completedLessons?.includes(module.id) || (module.id === 'quiz-1' && state.quizStatus === 'passed') || (module.id === 'lab-1' && state.practiceStatus === 'submitted');
      const active = state.activeLesson === module.id;
      return `
        <button class="list-group-item list-group-item-action ${active ? 'active' : ''}" data-lesson="${module.id}">
          <div class="d-flex justify-content-between align-items-start gap-2">
            <div>
              <div class="fw-bold">${module.title}</div>
              <div class="small ${active ? 'text-white-50' : 'text-secondary'}">${module.type} · ${module.duration}</div>
            </div>
            <span class="badge text-bg-${done ? 'success' : active ? 'light' : 'secondary'}">${done ? 'done' : module.status}</span>
          </div>
        </button>
      `;
    }).join('');

    const activeLesson = data.learningModules.find((item) => item.id === state.activeLesson) || data.learningModules[0];
    const lessonPoints = activeLesson.keyPoints.map((item) => `<li>${item}</li>`).join('');
    const quizRows = data.quizQuestions.map((q, index) => `
      <div class="border rounded-3 p-3 mb-2">
        <div class="fw-bold mb-2">Q${index + 1}. ${q.question}</div>
        <select class="form-select form-select-sm">
          ${q.choices.map((choice) => `<option>${choice}</option>`).join('')}
        </select>
        <div class="small text-secondary mt-2">Expected answer: ${q.answer}</div>
      </div>
    `).join('');

    const paths = data.credentialPaths.map((path) => `
      <div class="col-lg-6">
        <div class="card h-100 border-${path.id === 'ai-data' ? 'primary' : 'secondary'}">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
              <h5 class="card-title mb-0">${path.title}</h5>
              <span class="badge text-bg-${path.level === 'EvaluatorSigned' ? 'success' : 'primary'}">${path.level}</span>
            </div>
            <p class="text-secondary small">${path.description}</p>
            <div class="mb-2"><span class="badge text-bg-light text-secondary border">${path.duration}</span> <span class="badge text-bg-light text-secondary border">${path.status}</span></div>
            <div class="small text-uppercase text-secondary fw-bold mt-3">Modules</div>
            <ul class="small mb-3">${path.modules.map((item) => `<li>${item}</li>`).join('')}</ul>
            <div class="small text-uppercase text-secondary fw-bold">Target roles</div>
            <p class="small mb-0">${path.targetRoles.join(' · ')}</p>
          </div>
        </div>
      </div>
    `).join('');

    const task = data.projectTasks[0];
    const taskChecklist = task.checklist.map((item, index) => `
      <li class="list-group-item d-flex justify-content-between align-items-center">
        <span>${item}</span>
        <span class="badge text-bg-${index < 2 || state.practiceStatus === 'submitted' ? 'success' : 'secondary'}">${index < 2 || state.practiceStatus === 'submitted' ? 'done' : 'todo'}</span>
      </li>
    `).join('');

    const scoreRows = data.scoreBreakdown.map((row) => `
      <tr>
        <td>${row.area}</td>
        <td style="width: 36%"><div class="progress"><div class="progress-bar" style="width:${row.score}%">${row.score}</div></div></td>
        <td class="text-secondary small">${row.note}</td>
      </tr>
    `).join('');

    const learningSection = `
      <div class="card mb-4">
        <div class="card-header bg-white fw-bold">Learning Workspace</div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-xl-4"><div class="list-group">${modules}</div></div>
            <div class="col-xl-8">
              <div class="card border-primary h-100">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
                    <div><h5 class="card-title mb-1">${activeLesson.title}</h5><p class="text-secondary mb-0">${activeLesson.objective}</p></div>
                    <span class="badge text-bg-primary">${activeLesson.type}</span>
                  </div>
                  <hr>
                  <div class="row g-3">
                    <div class="col-lg-6">
                      <div class="small text-uppercase text-secondary fw-bold mb-2">Key learning points</div>
                      <ul>${lessonPoints}</ul>
                      <div class="small text-uppercase text-secondary fw-bold mb-2">Learning output</div>
                      <p class="mb-0">${activeLesson.output}</p>
                    </div>
                    <div class="col-lg-6">
                      <div class="small text-uppercase text-secondary fw-bold mb-2">Quiz / practice preview</div>
                      ${activeLesson.type === 'quiz' ? quizRows : '<div class="alert alert-light border mb-0">Complete this lesson, then move to quiz or practice lab. Learning actions update browser-local state only.</div>'}
                    </div>
                  </div>
                  <hr>
                  <div class="d-flex flex-wrap gap-2">
                    <button id="markLessonComplete" class="btn btn-primary">Mark Lesson Complete</button>
                    <button id="takeQuiz" class="btn btn-outline-primary">Take Quiz Mock</button>
                    <button id="submitPractice" class="btn btn-outline-success">Submit Practice Lab</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    const pathSection = `
      <div class="card mb-4">
        <div class="card-header bg-white fw-bold">Credential Path Catalog</div>
        <div class="card-body"><div class="row g-3">${paths}</div></div>
      </div>
    `;

    const practiceSection = `
      <div class="row g-3 mb-4">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Practice Lab · ${task.title}</div>
            <div class="card-body">
              <p class="text-secondary">Difficulty: ${task.difficulty} · Estimated time: ${task.estimatedTime}</p>
              <ul class="list-group mb-3">${taskChecklist}</ul>
              <div class="small text-uppercase text-secondary fw-bold mb-2">Expected evidence outputs</div>
              <div class="d-flex flex-wrap gap-2 mb-3">${task.evidenceOutputs.map((item) => `<span class="badge text-bg-light text-secondary border">${item}</span>`).join('')}</div>
              <label class="form-label small text-secondary">Practice answer draft</label>
              <textarea class="form-control mb-3" rows="4">I cleaned the sales data, defined margin metrics, and found an abnormal discount pattern in the East region.</textarea>
              <div class="d-flex flex-wrap gap-2">
                <button id="submitPractice" class="btn btn-success">Submit Practice Lab</button>
                <button id="downloadPracticePdf" class="btn btn-outline-primary">Download worksheet PDF</button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">AI Review Mock</div>
            <div class="card-body">
              <div class="alert alert-info">AI review is a learning assistant only. Final certificate evidence still needs issuer review.</div>
              <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between"><span>Metric definitions clear</span><span class="badge text-bg-success">pass</span></li>
                <li class="list-group-item d-flex justify-content-between"><span>Discount anomaly explained</span><span class="badge text-bg-success">pass</span></li>
                <li class="list-group-item d-flex justify-content-between"><span>Manager-facing summary concise</span><span class="badge text-bg-warning">improve</span></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    `;

    const evidenceSection = `
      <div class="row g-3 mb-4">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Evidence Builder</div>
            <div class="card-body">
              <div class="row g-2 mb-3">
                <div class="col-md-6"><label class="form-label small text-secondary">Insight summary</label><textarea class="form-control" rows="3">Revenue grew in East region, but discount leakage reduced margin.</textarea></div>
                <div class="col-md-6"><label class="form-label small text-secondary">Risk note</label><textarea class="form-control" rows="3">Abnormal discount pattern needs manager review before forecast update.</textarea></div>
              </div>
              <div class="d-flex flex-wrap gap-2 mb-3">
                <button id="learnerGenerateEvidence" class="btn btn-primary">Generate Evidence Bundle</button>
                <button id="learnerComputeHashes" class="btn btn-outline-primary">Compute Hashes</button>
                <button id="learnerRequestIssuer" class="btn btn-outline-success">Request Issuer Attestation</button>
              </div>
              <pre class="code-block mb-0">${state.evidence === 'generated' ? JSON.stringify(data.evidencePackage, null, 2) : 'No evidence generated yet.'}</pre>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Score Breakdown Preview</div>
            <div class="card-body table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead><tr><th>Area</th><th>Score</th><th>Reviewer note</th></tr></thead>
                <tbody>${scoreRows}</tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    `;

    const certificateSection = `
      <div class="row g-3 mb-4">
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Certificate Readiness</div>
            <div class="card-body">
              <ul class="list-group mb-3">
                <li class="list-group-item d-flex justify-content-between"><span>Learning complete</span><span class="badge text-bg-${state.learningProgress >= 100 ? 'success' : 'secondary'}">${state.learningProgress >= 100 ? 'ready' : 'pending'}</span></li>
                <li class="list-group-item d-flex justify-content-between"><span>Quiz passed</span><span class="badge text-bg-${state.quizStatus === 'passed' ? 'success' : 'secondary'}">${state.quizStatus}</span></li>
                <li class="list-group-item d-flex justify-content-between"><span>Practice submitted</span><span class="badge text-bg-${state.practiceStatus === 'submitted' ? 'success' : 'secondary'}">${state.practiceStatus}</span></li>
                <li class="list-group-item d-flex justify-content-between"><span>Evidence generated</span>${evidenceBadge}</li>
                <li class="list-group-item d-flex justify-content-between"><span>Proof status</span>${proofBadge}</li>
              </ul>
              <div class="d-flex flex-wrap gap-2">
                <button id="learnerRequestIssuer" class="btn btn-success">Request Issuer Attestation</button>
                <button id="downloadCertificatePdf" class="btn btn-primary">Download sealed certificate PDF</button>
                <button id="learnerSelfAttest" class="btn btn-outline-warning">Self-attest Low Trust</button>
              </div>
              <p class="small text-secondary mt-3 mb-0">The seal shown here is a visual prototype. Real certificate validity should bind issuer wallet signature and proof registry status.</p>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header bg-white fw-bold">Credential Preview</div>
            <div class="card-body">
              <div class="border rounded-4 p-4 bg-light position-relative overflow-hidden">
                <div class="small text-uppercase text-secondary fw-bold">Certificate of Verified Skill</div>
                <h4 class="mt-2">AI Data Analysis Assistant</h4>
                <p class="text-secondary mb-3">Issued to Mia Chen · ${state.trustLevel === 'none' ? 'IssuerAttested' : state.trustLevel}</p>
                <dl class="row small mb-0">
                  <dt class="col-5">Learning progress</dt><dd class="col-7">${state.learningProgress}%</dd>
                  <dt class="col-5">Quiz score</dt><dd class="col-7">${state.quizScore ?? '--'}</dd>
                  <dt class="col-5">Evidence</dt><dd class="col-7">${state.evidence}</dd>
                  <dt class="col-5">Proof</dt><dd class="col-7">${state.proofStatus}</dd>
                </dl>
                <div style="position:absolute;right:18px;bottom:18px;width:116px;height:116px;border:4px solid #b91c1c;border-radius:999px;color:#b91c1c;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;line-height:1.15;transform:rotate(-12deg);opacity:.9;">PROOFSKILL<br>ISSUER<br>SEAL</div>
              </div>
              <pre class="code-block mt-3 mb-0">${JSON.stringify({ learner: 'Mia Chen', credential: 'AI Data Analysis Assistant', learningProgress: state.learningProgress, quizScore: state.quizScore, evidence: state.evidence, proofStatus: state.proofStatus, trustLevel: state.trustLevel }, null, 2)}</pre>
            </div>
          </div>
        </div>
      </div>
    `;

    const sectionMap = { learning: learningSection, path: pathSection, practice: practiceSection, evidence: evidenceSection, certificate: certificateSection };

    return `
      <div class="alert alert-primary d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div><strong>Current learner:</strong> Mia Chen · Wallet 0xLearnerMiaMock · Goal: AI Data Analysis Assistant</div>
        <span class="badge text-bg-light text-primary border">learn → practice → evidence → certificate</span>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-md-3"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Learning progress</div><div class="display-6">${state.learningProgress || 0}%</div><div class="progress"><div class="progress-bar" style="width:${state.learningProgress || 0}%"></div></div></div></div></div>
        <div class="col-md-3"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Quiz</div><div class="h3 mb-2">${state.quizScore ?? '--'}</div><span class="badge text-bg-${state.quizStatus === 'passed' ? 'success' : 'secondary'}">${state.quizStatus || 'not_started'}</span></div></div></div>
        <div class="col-md-3"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Local evidence</div><div class="h3 mb-2">${state.evidence === 'generated' ? 'Ready' : 'Draft'}</div>${evidenceBadge}</div></div></div>
        <div class="col-md-3"><div class="card stat-card h-100"><div class="card-body"><div class="small text-uppercase text-secondary fw-bold">Proof status</div><div class="h3 mb-2">${state.proofStatus}</div>${proofBadge}</div></div></div>
      </div>

      <div class="card mb-4">
        <div class="card-body">
          <ul class="nav nav-pills gap-2">${tabs}</ul>
        </div>
      </div>

      ${sectionMap[tab] || learningSection}
    `;
  },
  bind() {
    document.querySelectorAll('[data-learner-tab]').forEach((button) => {
      button.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
        s.learnerTab = button.dataset.learnerTab;
      }, `Opened learner section: ${button.textContent.trim()}`));
    });

    document.querySelectorAll('[data-lesson]').forEach((button) => {
      button.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
        s.activeLesson = button.dataset.lesson;
      }, `Opened ${button.textContent.trim().split('\n')[0]}`));
    });

    document.getElementById('markLessonComplete')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      const lessonId = s.activeLesson || 'lesson-1';
      s.completedLessons = Array.from(new Set([...(s.completedLessons || []), lessonId]));
      s.learningProgress = Math.max(s.learningProgress || 0, Math.min(60, (s.completedLessons.length / window.ProofSkillData.learningModules.length) * 100));
    }, 'Lesson marked complete'));

    document.getElementById('takeQuiz')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.learnerTab = 'learning';
      s.activeLesson = 'quiz-1';
      s.quizStatus = 'passed';
      s.quizScore = 88;
      s.learningProgress = Math.max(s.learningProgress || 0, 75);
    }, 'Quiz completed with score 88'));

    document.getElementById('submitPractice')?.addEventListener('click', () => window.ProofSkillApp.mutate((s) => {
      s.learnerTab = 'practice';
      s.activeLesson = 'lab-1';
      s.practiceStatus = 'submitted';
      s.learningProgress = 100;
    }, 'Practice lab submitted'));

    document.getElementById('downloadPracticePdf')?.addEventListener('click', () => window.ProofSkillExport?.exportPracticePdf());
    document.getElementById('downloadCertificatePdf')?.addEventListener('click', () => window.ProofSkillExport?.exportCertificatePdf());

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
