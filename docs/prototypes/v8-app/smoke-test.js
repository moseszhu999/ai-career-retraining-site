window.ProofSkillSmokeTest = (() => {
  const requiredRoles = ['overview', 'learner', 'issuer', 'evaluator', 'verifier', 'admin'];
  const validLearnerTabs = ['learning', 'path', 'practice', 'evidence', 'certificate'];
  const knownAnchors = [
    'learning-ops',
    'review-queue',
    'contract-actions',
    'evaluator-assignment',
    'evaluator-rubric',
    'verifier-proof',
    'verifier-signals',
    'verifier-receipt',
    'admin-curriculum',
    'admin-quiz',
    'admin-practice',
    'admin-registry'
  ];

  function flattenMenu(nodes = []) {
    return nodes.flatMap((node) => [node, ...flattenMenu(node.children || [])]);
  }

  function pass(name, detail = '') {
    return { name, status: 'pass', detail };
  }

  function fail(name, detail = '') {
    return { name, status: 'fail', detail };
  }

  function run() {
    const menu = window.ProofSkillMenu;
    const modules = window.ProofSkillRoles || {};
    const flatMenu = flattenMenu(menu?.groups || []);
    const targetItems = flatMenu.filter((item) => item.target?.role);
    const checks = [];

    checks.push(window.bootstrap ? pass('Bootstrap JS loaded', 'accordion/collapse available') : fail('Bootstrap JS loaded', 'window.bootstrap missing'));
    checks.push(menu?.groups?.length ? pass('Menu config loaded', `${menu.groups.length} top-level groups`) : fail('Menu config loaded', 'window.ProofSkillMenu.groups missing'));
    checks.push(menu?.roles?.length >= requiredRoles.length ? pass('Role config loaded', `${menu.roles.length} roles`) : fail('Role config loaded', 'roles missing or incomplete'));

    requiredRoles.forEach((role) => {
      checks.push(modules[role]?.render && modules[role]?.bind ? pass(`Role module: ${role}`, 'render/bind ready') : fail(`Role module: ${role}`, 'missing render or bind'));
    });

    checks.push(window.ProofSkillState?.state ? pass('State store loaded', 'browser-local state ready') : fail('State store loaded', 'window.ProofSkillState missing'));
    checks.push(window.ProofSkillExport?.exportCertificatePdf ? pass('Certificate PDF export loaded', 'printable certificate ready') : fail('Certificate PDF export loaded', 'exportCertificatePdf missing'));
    checks.push(window.ProofSkillExport?.exportPracticePdf ? pass('Practice PDF export loaded', 'printable worksheet ready') : fail('Practice PDF export loaded', 'exportPracticePdf missing'));

    const invalidRoles = targetItems.filter((item) => !requiredRoles.includes(item.target.role));
    checks.push(invalidRoles.length === 0 ? pass('Menu target roles valid', `${targetItems.length} menu targets checked`) : fail('Menu target roles valid', invalidRoles.map((item) => item.id).join(', ')));

    const invalidLearnerTabs = targetItems.filter((item) => item.target.learnerTab && !validLearnerTabs.includes(item.target.learnerTab));
    checks.push(invalidLearnerTabs.length === 0 ? pass('Learner tab targets valid', 'all learner tabs mapped') : fail('Learner tab targets valid', invalidLearnerTabs.map((item) => item.id).join(', ')));

    const invalidAnchors = targetItems.filter((item) => item.target.anchor && !knownAnchors.includes(item.target.anchor));
    checks.push(invalidAnchors.length === 0 ? pass('Anchor targets registered', `${knownAnchors.length} known anchors`) : fail('Anchor targets registered', invalidAnchors.map((item) => item.id).join(', ')));

    const passed = checks.filter((item) => item.status === 'pass').length;
    return {
      passed,
      failed: checks.length - passed,
      total: checks.length,
      checks
    };
  }

  function renderTable() {
    const result = run();
    const rows = result.checks.map((check) => `
      <tr>
        <td>${check.name}</td>
        <td><span class="badge text-bg-${check.status === 'pass' ? 'success' : 'danger'}">${check.status}</span></td>
        <td class="text-secondary small">${check.detail}</td>
      </tr>
    `).join('');
    return {
      result,
      html: `<table class="table table-sm table-hover align-middle mb-0"><thead><tr><th>Check</th><th>Status</th><th>Detail</th></tr></thead><tbody>${rows}</tbody></table>`
    };
  }

  return { run, renderTable };
})();
