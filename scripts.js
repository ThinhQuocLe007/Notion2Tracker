let charts = {};
let allData = [];

const getYear = dateStr => new Date(dateStr).getFullYear();
const getMonth = dateStr => String(new Date(dateStr).getMonth() + 1).padStart(2, '0');

function loadData() {
  fetch('get_data.php')
    .then(res => res.json())
    .then(data => {
      allData = data;
      populateDropdowns();
    });
}

function populateDropdowns() {
  const years = new Set();
  const months = new Set();

  allData.forEach(d => {
    years.add(getYear(d.Date));
    months.add(getMonth(d.Date));
  });

  const yearEl = document.getElementById('yearFilter');
  const monthEl = document.getElementById('monthFilter');
  yearEl.innerHTML = '<option value="all">All</option>';
  monthEl.innerHTML = '<option value="all">All</option>';

  [...years].sort().forEach(y => {
    const opt = new Option(y, y);
    yearEl.appendChild(opt);
  });
  [...months].sort().forEach(m => {
    const opt = new Option(m, m);
    monthEl.appendChild(opt);
  });

  const now = new Date();
  yearEl.value = now.getFullYear();
  monthEl.value = String(now.getMonth() + 1).padStart(2, '0');
  filterAndUpdateCharts(yearEl.value, monthEl.value);
}

function filterAndUpdateCharts(year, month) {
  let filtered = allData;

  if (year !== 'all') filtered = filtered.filter(d => getYear(d.Date) == year);
  if (month !== 'all') filtered = filtered.filter(d => getMonth(d.Date) === month);

  filtered.sort((a, b) => new Date(a.Date) - new Date(b.Date));

  updateChart('formulaChart', 'Formula');
  updateChart('walkingChart', 'Walking');
}

function updateChart(canvasId, dataKey) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  const color = canvas.dataset.color;

  const labels = allData.map(d => d.Date);
  const values = allData.map(d => parseFloat(d[dataKey]));

  if (charts[canvasId]) charts[canvasId].destroy();

  charts[canvasId] = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: dataKey,
        data: values,
        borderColor: color,
        backgroundColor: color + '33',
        fill: true,
        tension: 0.3,
        pointRadius: 3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: `${dataKey} Per Day` }
      },
      scales: {
        x: { title: { display: true, text: 'Date' } },
        y: { beginAtZero: true, title: { display: true, text: dataKey } }
      }
    }
  });
}

// Bind events
document.getElementById('yearFilter').addEventListener('change', () => {
  filterAndUpdateCharts(
    document.getElementById('yearFilter').value,
    document.getElementById('monthFilter').value
  );
});

document.getElementById('monthFilter').addEventListener('change', () => {
  filterAndUpdateCharts(
    document.getElementById('yearFilter').value,
    document.getElementById('monthFilter').value
  );
});

document.getElementById('updateButton').addEventListener('click', loadData);

// Initial load
loadData();
