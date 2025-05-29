console.log('script loaded')

let currentFilter = 'week' ; // default chart 
let chartInstance = null ; 



// called when button clicked 
function setFilter(filter){
  currentFilter = filter ; 
  loadAndRenderChart() ; 
}

// Load data + Filter data 
function loadAndRenderChart(){
  fetch('fetch_data.php')
  .then(response => response.json())
  .then(data => {
    const today = new Date() ; 
    let filtered = [] ; 
    // Filter data  
    if (currentFilter == 'month'){
      const year = today.getFullYear() ; 
      const month = today.getMonth() ; 

      filtered = data.filter(item => {
        const d = new Date(item.Date) ; 
        return d.getFullYear() == year && d.getMonth() == month ; 
      }) 
    } else if (currentFilter == 'week') {
      const startOfWeek = new Date(today) ; 
      const day = today.getDay() ; 
      const diff = day == 0 ? 6 : day - 1 ; 
      startOfWeek.setDate(today.getDate() - diff) ; 
      startOfWeek.setHours(0, 0, 0, 0) ; 

      filtered = data.filter(item => {
          const d = new Date(item.Date) ; 
          return d >= startOfWeek ; 
      }) ; 
    } ; 

    // Render ther chart 
    filtered.sort((a,b) => new Date(a.Date) - new Date(b.Date)) ; 
    renderChart(filtered)
  })
  .catch(error => console.log('Fetch error', error)) ; 
}

function renderChart(data) {
  const labels = data.map(i => i.Date);
  const values = data.map(i => Number(i.DATA_TIME));

  // Destroy previous chart if exists
  if (chartInstance) {
    chartInstance.destroy();
  }

  const ctx = document.getElementById('time_allocation_chart').getContext('2d');
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'DATA_TIME',
        data: values,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { title: { display: true, text: 'Date' } },
        y: { title: { display: true, text: 'DATA_TIME' }, beginAtZero: true }
      }
    }
  });
}

// Load chart initially
loadAndRenderChart();