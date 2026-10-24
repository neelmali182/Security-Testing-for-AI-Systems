const runButton = document.querySelector('#run-scan');
const findingsBody = document.querySelector('#findings-body');

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderFinding(finding) {
  const row = document.createElement('tr');
  const checkCell = document.createElement('td');
  checkCell.append(element('div', 'check-name', finding.name));
  checkCell.append(element('div', 'check-id', finding.check_id));
  row.append(checkCell);

  const statusCell = document.createElement('td');
  statusCell.append(element('span', `status-pill ${finding.status === 'PASS' ? 'status-pass' : 'status-fail'}`, finding.status));
  row.append(statusCell);

  const severityCell = document.createElement('td');
  severityCell.append(element('span', `severity-pill severity-${finding.severity.toLowerCase()}`, finding.severity));
  row.append(severityCell);
  row.append(element('td', '', finding.summary));
  row.append(element('td', '', finding.evidence));
  return row;
}

async function runScan() {
  runButton.disabled = true;
  runButton.textContent = 'Running checks…';
  document.querySelector('#scan-status').textContent = 'Running';
  try {
    const response = await fetch('/api/scans', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_name: 'local-demo-model' }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'The scan could not be completed.');
    document.querySelector('#scan-status').textContent = result.status;
    document.querySelector('#scan-status').style.color = result.status === 'PASS' ? 'var(--green)' : 'var(--red)';
    document.querySelector('#scan-id').textContent = `ID ${result.scan_id.slice(0, 12)}`;
    document.querySelector('#passed-count').textContent = result.totals.passed;
    document.querySelector('#failed-count').textContent = result.totals.failed;
    document.querySelector('#last-run').textContent = `Completed ${new Date(result.created_at).toLocaleString()}`;
    findingsBody.replaceChildren(...result.findings.map(renderFinding));
  } catch (error) {
    document.querySelector('#scan-status').textContent = 'Error';
    findingsBody.replaceChildren();
    const row = document.createElement('tr');
    const cell = element('td', 'empty-state', error.message);
    cell.colSpan = 5;
    row.append(cell);
    findingsBody.append(row);
  } finally {
    runButton.disabled = false;
    runButton.innerHTML = '<span class="button-icon">▶</span> Run security scan';
  }
}

runButton.addEventListener('click', runScan);
