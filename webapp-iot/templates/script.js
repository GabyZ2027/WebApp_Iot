const salesData = {
    labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
    datasets: [{
        label: 'Ventas',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        data: [65, 59, 80, 81, 56, 55]
    }]
};  
const chartOptions = {
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true
            }
        }]
    }
};
const graf_temperatura = document.getElementById('Temperatura').getContext('2d');
const temp = new Chart(graf_temperatura, {
    type: 'line',
    data: salesData,
    options: chartOptions
});

const graf_humitat = document.getElementById('Humitat').getContext('2d');
const hum = new Chart(graf_humitat, {
    type: 'line',
    data: salesData,
    options: chartOptions
});
