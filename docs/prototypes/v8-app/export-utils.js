window.ProofSkillExport = (() => {
  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function openPrintWindow(title, body) {
    const win = window.open('', '_blank', 'width=980,height=760');
    if (!win) {
      alert('Popup blocked. Please allow popups to export printable PDF.');
      return;
    }

    win.document.write(`<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>${escapeHtml(title)}</title>
  <style>
    @page { size: A4; margin: 18mm; }
    body { font-family: Arial, Helvetica, sans-serif; color: #111827; margin: 0; }
    .page { max-width: 760px; margin: 0 auto; }
    .muted { color: #6b7280; }
    .small { font-size: 12px; }
    .title { font-size: 34px; font-weight: 800; margin: 0 0 8px; }
    .subtitle { font-size: 16px; color: #4b5563; margin: 0 0 24px; }
    .card { border: 1px solid #d1d5db; border-radius: 14px; padding: 18px; margin: 14px 0; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .label { font-size: 11px; color: #6b7280; text-transform: uppercase; font-weight: 700; letter-spacing: .04em; }
    .value { font-size: 15px; font-weight: 700; margin-top: 3px; word-break: break-word; }
    .seal { width: 132px; height: 132px; border: 4px solid #b91c1c; border-radius: 999px; color: #b91c1c; display: flex; align-items: center; justify-content: center; text-align: center; font-weight: 800; line-height: 1.15; transform: rotate(-12deg); }
    .seal-wrap { display: flex; justify-content: flex-end; margin-top: 10px; }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; }
    th, td { border: 1px solid #d1d5db; padding: 8px; text-align: left; vertical-align: top; }
    th { background: #f3f4f6; font-size: 12px; text-transform: uppercase; }
    code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; word-break: break-all; }
    .footer { margin-top: 28px; padding-top: 12px; border-top: 1px solid #d1d5db; font-size: 11px; color: #6b7280; }
    .no-print { margin: 0 0 18px; padding: 12px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; }
    @media print { .no-print { display: none; } body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
  </style>
</head>
<body>
  <div class="page">
    <div class="no-print"><strong>Export:</strong> Use your browser's Print / Save as PDF option.</div>
    ${body}
  </div>
  <script>setTimeout(() => window.print(), 250);</script>
</body>
</html>`);
    win.document.close();
  }

  function certificateBody() {
    const data = window.ProofSkillData;
    const record = data.contractRecord;
    const evidence = data.evidencePackage;
    return `
      <div class="title">Certificate of Verified Skill</div>
      <p class="subtitle">AI Data Analysis Assistant · Issuer-attested learning and evidence credential</p>
      <div class="card">
        <div class="grid">
          <div><div class="label">Learner</div><div class="value">Mia Chen</div></div>
          <div><div class="label">Wallet</div><div class="value"><code>${escapeHtml(record.holder)}</code></div></div>
          <div><div class="label">Credential</div><div class="value">AI Data Analysis Assistant</div></div>
          <div><div class="label">Trust level</div><div class="value">${escapeHtml(record.attestationLevel)}</div></div>
          <div><div class="label">Overall score</div><div class="value">${escapeHtml(evidence.overallScore)} / 100 · ${escapeHtml(evidence.scoreBand)}</div></div>
          <div><div class="label">Issued / expires</div><div class="value">${escapeHtml(record.issuedAt)} / ${escapeHtml(record.expiresAt)}</div></div>
        </div>
        <div class="seal-wrap"><div class="seal">PROOFSKILL<br>ISSUER<br>SEAL</div></div>
      </div>
      <div class="card">
        <div class="label">Verification references</div>
        <table>
          <tr><th>Field</th><th>Value</th></tr>
          <tr><td>Credential ID</td><td><code>${escapeHtml(record.credentialId)}</code></td></tr>
          <tr><td>Issuer</td><td><code>${escapeHtml(record.issuer)}</code></td></tr>
          <tr><td>Certificate hash</td><td><code>${escapeHtml(evidence.certificateHash)}</code></td></tr>
          <tr><td>Evidence hash</td><td><code>${escapeHtml(evidence.evidenceHash)}</code></td></tr>
          <tr><td>Score hash</td><td><code>${escapeHtml(evidence.scoreHash)}</code></td></tr>
          <tr><td>Schema hash</td><td><code>${escapeHtml(evidence.schemaHash)}</code></td></tr>
        </table>
      </div>
      <div class="footer">Prototype certificate. Visual seal is mock only. Real version should bind issuer wallet signature, contract record, and revocation status.</div>
    `;
  }

  function practiceBody() {
    const data = window.ProofSkillData;
    const task = data.projectTasks[0];
    const checklist = task.checklist.map((item) => `<tr><td>${escapeHtml(item)}</td><td>□</td></tr>`).join('');
    const outputs = task.evidenceOutputs.map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    return `
      <div class="title">Practice Lab Worksheet</div>
      <p class="subtitle">${escapeHtml(task.title)} · ${escapeHtml(task.difficulty)} · ${escapeHtml(task.estimatedTime)}</p>
      <div class="card">
        <div class="label">Instructions</div>
        <p>Complete the practice lab, write your assumptions, and prepare the evidence outputs. This worksheet can be saved as PDF for offline practice or trainer review.</p>
        <table>
          <tr><th>Checklist item</th><th>Done</th></tr>
          ${checklist}
        </table>
      </div>
      <div class="card">
        <div class="label">Expected evidence outputs</div>
        <ul>${outputs}</ul>
      </div>
      <div class="card">
        <div class="label">Learner notes</div>
        <p style="min-height: 120px; border-bottom: 1px solid #d1d5db;"></p>
        <p style="min-height: 120px; border-bottom: 1px solid #d1d5db;"></p>
      </div>
      <div class="footer">Prototype worksheet. Real version can include assignment ID, deadline, trainer comments, and submission QR/proof link.</div>
    `;
  }

  function exportCertificatePdf() {
    openPrintWindow('ProofSkill Certificate', certificateBody());
  }

  function exportPracticePdf() {
    openPrintWindow('ProofSkill Practice Lab Worksheet', practiceBody());
  }

  return { exportCertificatePdf, exportPracticePdf };
})();
