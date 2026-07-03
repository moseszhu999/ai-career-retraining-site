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

  function badge(value) {
    if (['active', 'generated', 'approved', 'issued', 'evaluator_set_ready'].includes(value)) {
      return `<span class="badge text-bg-success">${value}</span>`;
    }
    if (String(value).includes('pending') || String(value).includes('requested')) {
      return `<span class="badge text-bg-warning">${value}</span>`;
    }
    return `<span class="badge text-bg-secondary">${value}</span>`;
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
  }

  function mutate(mutator, eventMessage) {
    window.ProofSkillState.mutate(mutator, eventMessage);
    render();
  }

  mobileRoleSelect.addEventListener('change', (event) => setRole(event.target.value));

  resetStateBtn.addEventListener('click', () => {
    window.ProofSkillState.reset();
    render();
  });

  render();

  return {
    render,
    setRole,
    mutate
  };
})();
