const form = document.getElementById('portfolio-form');
const summaryCards = document.getElementById('summary-cards');
const recordsContainer = document.getElementById('records-container');

const numericFields = [
  'robinhood_value', 'schwab_jay_investment_value', 'schwab_jay_ira_value',
  'alo_401k_value', 'gap_401k_value', 'chevron_401k_value',
  'schwab_varsha_investment_value', 'schwab_jay_roth_value', '_529_kush_value',
  '_529_aadya_value', 'marcus_account_value', 'wells_fargo_value', 'citibank_varsha_value',
  'axisbank_value', 'mortgage_balance', 'coinbase_value', 'schwab_varsha_roth_value',
  'healthequity_fund_value', 'gap_etrade_value', 'monthly_expenses', 'varsha_monthly_expenses',
  'india_home_value', 'alo_ms_value'
];

function formatCurrency(value) {
  return Number(value || 0).toLocaleString('en-US', { style: 'currency', currency: 'USD' });
}

async function loadSummary() {
  const res = await fetch('/portfolio-monthly-balance/summary');
  const data = await res.json();
  const latest = data.latest_record || {};
  const summary = data.summary || {};

  summaryCards.innerHTML = `
    <div class="summary-card">
      <div class="summary-label">Latest month</div>
      <div class="summary-value">${latest.portfolio_month || 'N/A'}</div>
    </div>
    <div class="summary-card">
      <div class="summary-label">Net worth</div>
      <div class="summary-value">${formatCurrency(summary.networth)}</div>
    </div>
    <div class="summary-card">
      <div class="summary-label">Total assets</div>
      <div class="summary-value">${formatCurrency(summary.total_assets)}</div>
    </div>
    <div class="summary-card">
      <div class="summary-label">Total liabilities</div>
      <div class="summary-value">${formatCurrency(summary.total_liabilities)}</div>
    </div>
  `;
}

function renderRecords(items) {
  if (!items.length) {
    recordsContainer.innerHTML = '<p>No portfolio records yet.</p>';
    return;
  }

  recordsContainer.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Month</th>
          <th>Net</th>
          <th>Retirement</th>
          <th>Invest</th>
          <th>Cash</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        ${items.map(item => `
          <tr>
            <td>${item.portfolio_month}</td>
            <td>${formatCurrency(item.networth)}</td>
            <td>${formatCurrency(item.retirement_value)}</td>
            <td>${formatCurrency(item.investment_amount)}</td>
            <td>${formatCurrency(item.cash)}</td>
            <td><button class="danger" data-id="${item.id}" type="button">Delete</button></td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;

  recordsContainer.querySelectorAll('button[data-id]').forEach(button => {
    button.addEventListener('click', async () => {
      const id = button.dataset.id;
      const response = await fetch(`/portfolio-monthly-balance/${id}`, { method: 'DELETE' });
      if (response.ok) {
        loadRecords();
        loadSummary();
      }
    });
  });
}

async function loadRecords() {
  const res = await fetch('/portfolio-monthly-balance');
  const items = await res.json();
  renderRecords(items);
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());

  for (const key of numericFields) {
    data[key] = Number(data[key] || 0);
  }

  if (data.portfolio_date === '') {
    delete data.portfolio_date;
  }

  const response = await fetch('/portfolio-monthly-balance', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const errorText = await response.text();
    alert(`Failed to save portfolio: ${errorText}`);
    return;
  }

  form.reset();
  await loadRecords();
  await loadSummary();
});

loadSummary();
loadRecords();
