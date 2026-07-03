window.ProofSkillApp = (() => {
  const roles = [
    { id: 'learner', label: 'Learner / Candidate', description: 'tasks, local evidence, proof request' },
    { id: 'issuer', label: 'Issuer / Training Partner', description: 'review, issue, revoke proof' },
    { id: 'evaluator', label: 'Evaluator / Reviewer', description: 'score and sign reviews' },
    { id: 'verifier', label: 'Verifier / Employer', description: 'read contract proof' },
    { id: 'admin', label: 'Admin / Contract Owner', description: 'issuer registry and events' }
  ];

  const roleNav = document.getElementById('roleNav');
  const mobileRoleSelect = document.getElementById('mobileRoleSelect');
  const workspace = document.getElementById('workspace');
  const workspaceTitle = document.getElementById('workspaceTitle');
  const workspaceSubtitle = document.getElementById('workspaceSubtitle');
  const globalState = document.getElementById('globalState');
  const resetStateBtn = document.getElementById('resetStateBtn');
  const toastContainer = document.getElementById('toastContainer');

  const demoGuide = {
    learner: {
      badge: 'Step 1',
      title: 'Learner creates evidence',
      body: 'Review the credential path, inspect the task checklist, generate evidence, compute hashes, then request issuer attestation.',
      next: 'Next role: Issuer'
    },
    issuer: {
      badge: 'Step 2',
      title: 'Issuer reviews and signs',
      body: 'Open the review queue, inspect evidence details, check hash matches and rubric summary, then issue an attested proof.',
      next: 'Next role: Verifier'
    },
    evaluator: {
      badge: 'Optional Step',
      title: 'Evaluator signs higher-trust review',
      body: 'Use this path when the credential needs human reviewer scoring before the issuer creates an EvaluatorSigned proof.',
      next: 'Next role: Issuer'
    },
    verifier: {
      badge: 'Step 3',
      title: 'Verifier checks contract proof',
      body: 'Read the credential proof, check status, trust level, issuer authorization, hash match, expiration, and revocation state.',
      next: 'Demo complete'
    },
    admin: {
      badge: 'Governance',
      title: 'Admin manages contract registry',
      body: 'Inspect issuer registry, schema versions, contract configuration, and event log. Admin does not manage learner private files.',
      next: 'Supports issuer governance'
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
    if (['active', 'generated', 'approved', 'issued', 'evaluator_set_ready'].includes(value)) {
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
      <div class="d-flex justify-content-between mb-1"><span>Evidence</span>${badge(state.evidence)}</div>
      <div class="d-flex justify-content-between mb-1"><span>Issuer review</span>${badge(state.issuerReview)}</div>
      <div class="d-flex justify-content-between mb-1"><span>Evaluator</span>${badge(state.evaluatorReview)}</div>
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
    const guide = demoGuide[roleId] || demoGuide.learner;
    return `
      <div class="alert alert-primary d-flex flex-column flex-lg-row align-items-lg-center justify-content-between gap-3">
        <div>
          <span class="badge text-bg-light text-primary border me-2">${guide.badge}</span>
          <strong>${guide.title}</strong>
          <div class="small mt-1">${guide.body}</div>
        </div>
        <div class="text-lg-end">
          <span class="badge text-bg-primary">${guide.next}</span>
          <div class="small mt-1"><code>#${roleId}</code> shareable role URL</div>
        </div>
      </div>
    `;
  }

  function renderWorkspace() {
    const state = window.ProofSkillState.state;
    const roleModule = window.ProofSkillRoles[state.currentRole];

    workspaceTitle.textContent = roleModule.title;
    workspaceSubtitle.textContent = roleModule.subtitle;
    workspace.innerHTML = renderDemoGuide(state.currentRole) + roleModule.render(state);
    roleModule.bind(state);
  }

  function render() {
    renderRoleNav();
    renderGlobalState();
    renderWorkspace();
  }

  function setRole(roleId, options = {}) {
    if (!validRole(roleId)) return;
    window.ProofSkillState.mutate((state) => {
      state.currentRole = roleId;
    });
    if (!options.fromHash && window.location.hash !== `#${roleId}`) {
      history.replaceState(null, '', `#${roleId}`);
    }
    render();
    const role = roles.find((item) => item.id === roleId);
    if (role && !options.silent) showToast(`Switched to ${role.label}`, 'primary');
  }

  function mutate(mutator, eventMessage) {
    window.ProofSkillState.mutate(mutator, eventMessage);
    render();
    if (eventMessage) showToast(eventMessage, 'success');
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
    history.replaceState(null, '', `#${stateRole}`);
  }

  render();

  return {
    render,
    setRole,
    mutate,
    showToast
  };
})();
