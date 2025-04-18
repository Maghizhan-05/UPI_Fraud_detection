document.addEventListener('DOMContentLoaded', () => {
  const app = document.getElementById('app');
  app.classList.add('fade-in');

  // Page transitions (existing)
  document.querySelectorAll('.transition-button').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const target = btn.getAttribute('href');
      app.classList.replace('fade-in','fade-out');
      setTimeout(() => window.location = target, 500);
    });
  });

  // Detect Fraud via AJAX
  const detectBtn = document.getElementById('detect-btn');
  const spinner   = document.getElementById('spinner');
  const results   = document.getElementById('results');

  detectBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    results.innerHTML = '';            // clear old
    spinner.classList.remove('hidden');

    try {
      const resp = await fetch('/api/detect');
      const { alerts } = await resp.json();
      renderResults(alerts);
    } catch (err) {
      results.innerHTML = `<p class="text-red-600">Error during fraud detection.</p>`;
    } finally {
      spinner.classList.add('hidden');
    }
  });

  function renderResults(alerts) {
    if (!alerts.length) {
      results.innerHTML = `<p class="text-green-700 font-semibold">No fraudulent transactions detected.</p>`;
      return;
    }
    let html = `<table class="min-w-full bg-white rounded-lg overflow-hidden shadow">
      <thead class="bg-gray-200"><tr>
        <th class="py-3 px-6 text-left">Transaction ID</th>
        <th class="py-3 px-6 text-left">Status</th>
      </tr></thead><tbody>`;
    alerts.forEach(id => {
      html += `<tr class="border-b border-gray-100 bg-red-100">
        <td class="py-3 px-6 font-mono text-sm">${id}</td>
        <td class="py-3 px-6 text-red-700 font-semibold">Fraud</td>
      </tr>`;
    });
    html += `</tbody></table>`;
    results.innerHTML = html;
  }
});
