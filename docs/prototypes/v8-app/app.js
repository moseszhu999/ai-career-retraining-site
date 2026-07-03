window.ProofSkillApp = (() => {
  const roles = [
    { id: 'learner', label: 'Learner / Candidate', description: 'learn, practice, evidence, certificate' },
    { id: 'issuer', label: 'Issuer / Training Partner', description: 'learning ops, review, issue proof' },
    { id: 'evaluator', label: 'Evaluator / Reviewer', description: 'score and sign reviews' },
    { id: 'verifier', label: 'Verifier / Employer', description: 'proof and role-fit signals' },
    { id: 'admin', label: 'Admin / Contract Owner', description: 'curriculum and contract governance' }
  ];

  const roleNav = document.getElementById('roleNav');
  const mobileRoleSelect = document.getElementById('mobileRoleSelect');
  const workspace = document.getElementById('workspace');
  const workspaceTitle = document.getElementById('workspaceTitle');
  const workspaceSubtitle = document.getElementById('workspaceSubtitle');
  const globalState = document.getElementById('globalState');
  const resetStateBtn = document.getElementById('resetStateBtn');
  const toastContainer = document.getElementById('toastContainer');

  const demoSteps = [
    {
      role: 'admin',
      title: 'Admin publishes curriculum',
      note: 'Show course builder, quiz bank, practice templates, issuer registry, and content policy.',
      apply: (s) => {
        s.currentRole = 'admin';
        s.curriculumVersion = 'curriculum-demo-v1';
      }
    },
    {
      role: 'learner',
      title: 'Learner starts learning path',
      note: 'Show Learning tab with lesson modules, current lesson, and progress state.',
      apply: (s) => {
        s.currentRole = 'learner';
        s.learnerTab = 'learning';
        s.activeLesson = 'lesson-1';
        s.learningProgress = 25;
      }
    },
    {
      role: 'learner',
      title: 'Learner passes quiz',
      note: 'Show quiz completion and score before practice evidence.',
      apply: (s) => {
        s.currentRole = 'learner';
        s.learnerTab = 'learning';
        s.activeLesson = 'quiz-1';
        s.quizStatus = 'passed';
        s.quizScore = 88;
        s.learningProgress = 75;
      }
    },
    {
      role: 'learner',
      title: 'Learner submits practice lab',
      note: 'Show Practice Lab, AI review mock, and submitted practice state.',
      apply: (s) => {
        s.currentRole = 'learner';
        s.learnerTab = 'practice';
        s.activeLesson = 'lab-1';
        s.practiceStatus = 'submitted';
        s.learningProgress = 100;
      }
    },
    {
      role: 'learner',
      title: 'Learner creates evidence bundle',
      note: 'Show Evidence Builder, evidence JSON, and frontend hash computation.',
      apply: (s) => {
        s.currentRole = 'learner';
        s.learnerTab = 'evidence';
        s.evidence = 'generated';
        s.hashesComputed = true;
      }
    },
    {
      role: 'issuer',
      title: 'Training partner monitors cohort',
      note: 'Show cohort progress, learner next actions, curriculum issues, and evidence readiness.',
      apply: (s) => {
        s.currentRole = 'issuer';
        s.issuerReview = 'review_pending';
      }
    },
    {
      role: 'issuer',
      title: 'Issuer approves and issues proof',
      note: 'Show evidence review, hash checklist, rubric summary, and contract action preview.',
      apply: (s) => {
        s.currentRole = 'issuer';
        s.issuerReview = 'issued';
        s.proofStatus = 'active';
        s.trustLevel = 'IssuerAttested';
        s.issuedCount = Math.max(s.issuedCount || 0, 1);
      }
    },
    {
      role: 'evaluator',
      title: 'Evaluator path for higher trust',
      note: 'Show rubric scoring, risk flags, review comments, and evaluatorSetHash preview.',
      apply: (s) => {
        s.currentRole = 'evaluator';
        s.evaluatorReview = 'evaluator_set_ready';
        s.evaluatorSetHash = '0xEVALUATOR_SET_HASH_MOCK_001';
      }
    },
    {
      role: 'verifier',
      title: 'Verifier checks proof and role-fit signals',
      note: 'Show credential verification, role-fit matrix, use-boundary notes, and receipt preview.',
      apply: (s) => {
        s.currentRole = 'verifier';
        s.proofStatus = 'active';
        s.trustLevel = s.trustLevel === 'none' ? 'IssuerAttested' : s.trustLevel;
      }
    }
  ];

  const demoGuide = {
    learner: {
      badge: 'Learning flow',
      title: 'Learner moves from study to evidence',
      body: 'Use Learning, Practice Lab, Evidence, and Certificate tabs to show the full learner journey.',
      next: 'Next role: Issuer'
    },
    issuer: {
      badge: 'Training partner',
      title: 'Issuer monitors learning and signs credentials',
      body: 'Show cohort progress first, then review evidence and issue an attested proof.',
      next: 'Next role: Verifier'
    },
    evaluator: {
      badge: 'Higher trust',
      title: 'Evaluator signs stronger review evidence',
      body: 'Use this path when a credential needs rubric scoring and human reviewer signature.',
      next: 'Next role: Issuer'
    },
    verifier: {
      badge: 'Work-readiness',
      title: 'Verifier checks proof and role-fit signals',
      body: 'Credential verification is a signal: check proof status, trust level, role-fit matrix, and use boundaries.',
      next: 'Demo complete'
    },
    admin: {
      badge: 'Governance',
      title: 'Admin governs curriculum and contract registry',
      body: 'Inspect course builder, quiz bank, practice templates, issuer registry, and contract configuration.',
      next: 'Next role: Learner'
    }
  };

  function validRole(roleId) {
    return roles.some((role) => role.id === roleId);
  }

  function roleFromHash() {
    const hash = window.location.hash.replace('#', '').trim();
    return validRole(hash) ? hash : null;
  }

  function badge(value) {
    if (['active', 'generated', 'approved', 'issued', 'evaluator_set_ready', 'passed', 'submitted'].includes(value)) {
      return `<span class="badge text-bg-success">${value}</span>`;
    }
    if (String(value).includes('pending') || String(value).includes('requested')) {
      return `<span class="badge text-bg-warning">${value}</span>`;
    }
    return `<span class="badge text-bg-secondary">${value}</span>`;
  }

  function showToast(message, tone = 'success') {
    if (!toastContainer || !window.bootstrap) return;

    const toast = document.createElement('div');
    toast.className = 'toast align-items-center border-0 shadow-sm';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.setAttribute('aria-atomic', 'true');
    toast.innerHTML = `
      <div class="toast-header">
        <span class="badge text-bg-${tone} me-2">ProofSkill</span>
        <strong class="me-auto">Action completed</strong>
        <small>now</small>
        <button type="button" class="btn-close ms-2 mb-1" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">${message}</div>
    `;

    toastContainer.appendChild(toast);
    const instance = new bootstrap.Toast(toast, { delay: 2600 });
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
    instance.show();
  }

  function renderGlobalState() {
    const state = window.ProofSkillState.state;
    globalState.innerHTML = `
      <div class="d-flex justify-content-between mb-1"><span>Learning</span>${badge(`${state.learningProgress || 0}%`)}</div>
      <div class="d-flex justify-content-between mb-1"><span>Quiz</span>${badge(state.quizStatus)}</div>
      <div class="d-flex justify-content-between mb-1"><span>Practice</span>${badge(state.practiceStatus)}</div>
      <div class="d-flex justify-content-between mb-1"><span>Evidence</span>${badge(state.evidence)}</div>
      <div class="d-flex justify-content-between mb-1"><span>Issuer review</span>${badge(state.issuerReview)}</div>
      <div class="d-flex justify-content-between mb-1"><span>Contract proof</span>${badge(state.proofStatus)}</div>
      <div class="d-flex justify-content-between mb-1"><span>Trust</span>${badge(state.trustLevel)}</div>
    `;
  }

  function renderRoleNav() {
    const state = window.ProofSkillState.state;
    roleNav.innerHTML = roles.map((role) => `
      <button class="list-group-item list-group-item-action ${state.currentRole === role.id ? 'active' : ''}" data-role="${role.id}">
        <div class="fw-bold">${role.label}</div>
        <div class="small ${state.currentRole === role.id ? 'text-white-50' : 'text-secondary'}">${role.description}</div>
      </button>
    `).join('');

    roleNav.querySelectorAll('[data-role]').forEach((button) => {
      button.addEventListener('click', () => setRole(button.dataset.role));
    });

    mobileRoleSelect.value = state.currentRole;
  }

  function renderDemoGuide(roleId) {
    const state = window.ProofSkillState.state;
    const guide = demoGuide[roleId] || demoGuide.learner;
    const stepIndex = Math.min(state.demoStep || 0, demoSteps.length - 1);
    const step = demoSteps[stepIndex];
    return `
      <div class="alert alert-primary d-flex flex-column flex-xl-row align-items-xl-center justify-content-between gap-3">
        <div>
          <span class="badge text-bg-light text-primary border me-2">${guide.badge}</span>
          <strong>${guide.title}</strong>
          <div class="small mt-1">${guide.body}</div>
          <div class="small mt-2"><strong>Guided demo ${stepIndex + 1}/${demoSteps.length}:</strong> ${step.title} · ${step.note}</div>
        </div>
        <div class="text-xl-end">
          <span class="badge text-bg-primary">${guide.next}</span>
          <div class="small mt-1"><code>#${roleId}</code> shareable role URL</div>
          <div class="d-flex flex-wrap gap-2 justify-content-xl-end mt-2">
            <button id="runDemoStepBtn" class="btn btn-sm btn-primary">Run next demo step</button>
            <button id="restartDemoBtn" class="btn btn-sm btn-outline-secondary">Restart demo</button>
          </div>
        </div>
      </div>
    `;
  }

  function bindDemoControls() {
    document.getElementById('runDemoStepBtn')?.addEventListener('click', runNextDemoStep);
    document.getElementById('restartDemoBtn')?.addEventListener('click', restartDemo);
  }

  function renderWorkspace() {
    const state = window.ProofSkillState.state;
    const roleModule = window.ProofSkillRoles[state.currentRole];

    workspaceTitle.textContent = roleModule.title;
    workspaceSubtitle.textContent = roleModule.subtitle;
    workspace.innerHTML = renderDemoGuide(state.currentRole) + roleModule.render(state);
    bindDemoControls();
    roleModule.bind(state);
  }

  function render() {
    renderRoleNav();
    renderGlobalState();
    renderWorkspace();
  }

  function syncHash(roleId) {
    if (window.location.hash !== `#${roleId}`) history.replaceState(null, '', `#${roleId}`);
  }

  function setRole(roleId, options = {}) {
    if (!validRole(roleId)) return;
    window.ProofSkillState.mutate((state) => {
      state.currentRole = roleId;
    });
    if (!options.fromHash) syncHash(roleId);
    render();
    const role = roles.find((item) => item.id === roleId);
    if (role && !options.silent) showToast(`Switched to ${role.label}`, 'primary');
  }

  function mutate(mutator, eventMessage) {
    window.ProofSkillState.mutate(mutator, eventMessage);
    render();
    if (eventMessage) showToast(eventMessage, 'success');
  }

  function runNextDemoStep() {
    let appliedStep;
    window.ProofSkillState.mutate((state) => {
      const index = Math.min(state.demoStep || 0, demoSteps.length - 1);
      appliedStep = demoSteps[index];
      appliedStep.apply(state);
      state.demoStep = index >= demoSteps.length - 1 ? demoSteps.length - 1 : index + 1;
    }, `Guided demo: ${appliedStep?.title || 'step advanced'}`);
    if (appliedStep?.role) syncHash(appliedStep.role);
    render();
    showToast(`Guided demo: ${appliedStep?.title || 'step advanced'}`, 'primary');
  }

  function restartDemo() {
    window.ProofSkillState.reset();
    window.ProofSkillState.mutate((state) => {
      state.currentRole = 'admin';
      state.demoStep = 0;
    }, 'Guided demo restarted');
    syncHash('admin');
    render();
    showToast('Guided demo restarted', 'secondary');
  }

  mobileRoleSelect.addEventListener('change', (event) => setRole(event.target.value));

  window.addEventListener('hashchange', () => {
    const roleId = roleFromHash();
    if (roleId) setRole(roleId, { fromHash: true, silent: true });
  });

  resetStateBtn.addEventListener('click', () => {
    window.ProofSkillState.reset();
    const roleId = roleFromHash() || 'learner';
    window.ProofSkillState.mutate((state) => {
      state.currentRole = roleId;
    });
    render();
    showToast('Mock state reset', 'secondary');
  });

  const initialRole = roleFromHash();
  if (initialRole) {
    window.ProofSkillState.mutate((state) => {
      state.currentRole = initialRole;
    });
  } else {
    const stateRole = window.ProofSkillState.state.currentRole || 'learner';
    syncHash(stateRole);
  }

  render();

  return {
    render,
    setRole,
    mutate,
    showToast,
    runNextDemoStep,
    restartDemo
  };
})();
