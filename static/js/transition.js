document.addEventListener('DOMContentLoaded', () => {
  const app = document.getElementById('app');
  const fileInput = document.getElementById('file-input');
  const uploadBtn = document.getElementById('upload-btn');
  const trainBtn  = document.getElementById('train-btn');
  const detectBtn = document.getElementById('detect-btn');
  const spinner   = document.getElementById('spinner');
  const message   = document.getElementById('message');
  const results   = document.getElementById('results');

  const showSpinner = () => spinner.classList.remove('hidden');
  const hideSpinner = () => spinner.classList.add('hidden');

  const postJSON = async (url, data) => {
    const resp = await fetch(url, data);
    return resp.json();
  };

  uploadBtn.addEventListener('click', async () => {
    if (!fileInput.files.length) return;
    showSpinner(); message.textContent = '';
    const form = new FormData(); form.append('file', fileInput.files[0]);
    const res = await postJSON('/api/upload', { method:'POST', body: form });
    hideSpinner();
    message.textContent = res.status === 'uploaded' ? '✅ Uploaded' : res.error;
  });

  trainBtn.addEventListener('click', async () => {
    showSpinner(); message.textContent = '';
    const res = await postJSON('/api/train', { method:'POST' });
    hideSpinner();
    message.textContent = res.status === 'trained' ? '✅ Trained' : res.error;
  });

  detectBtn.addEventListener('click', async () => {
    showSpinner(); message.textContent = '';
    const res = await fetch('/api/detect');
    const data = await res.json();
    hideSpinner();
    if (data.error) {
      message.textContent = data.error;
      return;
    }
    if (!data.alerts.length) {
      results.innerHTML = '<p class="text-green-700">No fraud detected</p>';
    } else {
      let html = '<table class="min-w-full bg-white rounded overflow-hidden shadow"><thead class="bg-gray-200"><tr>' +
                 '<th>Txn ID</th><th>Status</th></tr></thead><tbody>';
      data.alerts.forEach(id => {
        html += `<tr class="bg-red-100"><td>${id}</td><td>Fraud</td></tr>`;
      });
      html += '</tbody></table>';
      results.innerHTML = html;
    }
  });

  // initial fade-in
  app.classList.add('fade-in');
});