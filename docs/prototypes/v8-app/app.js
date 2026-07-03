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

  function renderWorkspace() {
    const state = window.ProofSkillState.state;
    const roleModule = window.ProofSkillRoles[state.currentRole];

    workspaceTitle.textContent = roleModule.title;
    workspaceSubtitle.textContent = roleModule.subtitle;
    workspace.innerHTML = roleModule.render(state);
    roleModule.bind(state);
  }

  function render() {
    renderRoleNav();
    renderGlobalState();
    renderWorkspace();
  }

  function setRole(roleId) {
    window.ProofSkillState.mutate((state) => {
      state.currentRole = roleId;
    });
    render();
    const role = roles.find((item) => item.id === roleId);
    if (role) showToast(`Switched to ${role.label}`, 'primary');
  }

  function mutate(mutator, eventMessage) {
    window.ProofSkillState.mutate(mutator, eventMessage);
    render();
    if (eventMessage) showToast(eventMessage, 'success');
  }

  mobileRoleSelect.addEventListener('change', (event) => setRole(event.target.value));

  resetStateBtn.addEventListener('click', () => {
    window.ProofSkillState.reset();
    render();
    showToast('Mock state reset', 'secondary');
  });

  render();

  return {
    render,
    setRole,
    mutate,
    showToast
  };
})();
