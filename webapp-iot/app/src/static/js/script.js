/*const salesData = {
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
});*/

const chartOptions = {
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true
            }
        }]
    }
};

let charttemp = null;
let charthum = null;
var graf_temperatura = document.getElementById('Temperatura').getContext('2d');
var graf_humitat = document.getElementById('Humitat').getContext('2d');

function FerGrafica(dades, temps, graf, nom_label, chart) {
    if (chart) {
        chart.destroy();
    }
    var variable_dades = {
        labels: temps,
        datasets: [{
            label: nom_label,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: dades
        }]
    };
    return new Chart(graf, {
        type: 'line',
        data: variable_dades,
        options: chartOptions
    });
}

// Historials
function Historial(path, graf, nom_label, chartVarName) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', path, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var data = JSON.parse(xhr.responseText);
                window[chartVarName] = FerGrafica(data.data, data.temps, graf, nom_label, window[chartVarName]);
                console.log("Historial: ", data);
            } else {
                console.error("Error a l'obrindre el historial:", xhr.status);
            }
        }
    };
    xhr.send();
}

Historial('/sensor/temperatura/historial', graf_temperatura, 'Temperatura', 'charttemp');
Historial('/sensor/humitat/historial', graf_humitat, 'Humitat', 'charthum');

setInterval(function() {
    Historial('/sensor/temperatura/historial', graf_temperatura, 'Temperatura', 'charttemp');
}, 30000);

setInterval(function() {
    Historial('/sensor/humitat/historial', graf_humitat, 'Humitat', 'charthum');
}, 30000);

// Actuador
function toggleLED(state) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/led', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("led-status=" + (state === 'on' ? '1' : '0'));
}

// Valores actuales
var T = document.getElementById("Tactual");
var H = document.getElementById("Hactual");

function Actual(path, variable) {
    var r = new XMLHttpRequest();
    r.open('GET', path, true);
    r.send();
    r.onreadystatechange = function () {
        if (r.status == 200 && r.readyState == 4) {
            var response = JSON.parse(r.responseText);
            variable.textContent = response.data;
        }
    }
}

Actual('/sensor/temperatura', T);
Actual('/sensor/humitat', H);

setInterval(function() {
    Actual('/sensor/temperatura', T);
}, 30000);

setInterval(function() {
    Actual('/sensor/humitat', H);
}, 30000);

var L = document.getElementById("Led");

function update_led(variable) {
    var r = new XMLHttpRequest();
    r.open('GET', '/led', true);
    r.send();
    r.onreadystatechange = function () {
        if (r.status == 200 && r.readyState == 4) {
            var response = JSON.parse(r.responseText);
            if (response.data === '1') {
                variable.src = "https://static.vecteezy.com/system/resources/previews/005/032/239/non_2x/bulb-light-on-free-vector.jpg";
            } else {
                variable.src = "https://cdn-icons-png.flaticon.com/512/32/32177.png";
            }
        }
    }
}

setInterval(function() {
    update_led(L);
}, 20000);
