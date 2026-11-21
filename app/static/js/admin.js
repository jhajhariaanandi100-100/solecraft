// SOLECRAFT ADMIN DASHBOARD ANALYTICS

document.addEventListener('DOMContentLoaded', function () {
  // Revenue Trend Chart
  const revCtx = document.getElementById('revenueTrendChart');
  if (revCtx && window.adminChartData) {
    new Chart(revCtx, {
      type: 'line',
      data: {
        labels: window.adminChartData.dateLabels,
        datasets: [{
          label: 'Revenue ($)',
          data: window.adminChartData.revenueData,
          borderColor: '#FF6B35',
          backgroundColor: 'rgba(255, 107, 53, 0.1)',
          borderWidth: 3,
          pointBackgroundColor: '#FF6B35',
          pointRadius: 5,
          tension: 0.35,
          fill: true
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(0, 0, 0, 0.05)' }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  // Category Breakdown Doughnut Chart
  const catCtx = document.getElementById('categoryDoughnutChart');
  if (catCtx && window.adminCatData) {
    new Chart(catCtx, {
      type: 'doughnut',
      data: {
        labels: window.adminCatData.labels,
        datasets: [{
          data: window.adminCatData.counts,
          backgroundColor: [
            '#111111',
            '#FF6B35',
            '#2B2D42',
            '#8D99AE',
            '#E63946',
            '#457B9D',
            '#2A9D8F',
            '#E76F51'
          ],
          borderWidth: 2,
          borderColor: '#FFFFFF'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' }
        },
        cutout: '68%'
      }
    });
  }
});
