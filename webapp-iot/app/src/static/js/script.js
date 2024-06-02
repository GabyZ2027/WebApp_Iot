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

function FerGrafica(dades, temps, graf, nom_label, chart, backgroundColor = 'rgba(54, 162, 235, 0.2)', borderColor = 'rgba(54, 162, 235, 1)', borderWidth = 1) {
    if (chart) {
        chart.destroy();
    }
    var variable_dades = {
        labels: temps,
        datasets: [{
            label: nom_label,
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            borderWidth: borderWidth,
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
function Historial(path, graf, nom_label, chartVarName,backgroundColor = 'rgba(54, 162, 235, 0.2)',borderColor = 'rgba(54, 162, 235, 1)') {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', path, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var data = JSON.parse(xhr.responseText);
                window[chartVarName] = FerGrafica(data.data, data.temps, graf, nom_label, window[chartVarName],backgroundColor ,borderColor);
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

setInterval(Historial,30000,'/sensor/temperatura/historial', graf_temperatura, 'Temperatura', 'charttemp','rgba(255, 99, 132, 0.2)','rgba(255, 99, 132, 1)');

setInterval(Historial,30000,'/sensor/humitat/historial', graf_humitat, 'Humitat', 'charthum','rgba(54, 162, 235, 0.2)','rgba(54, 162, 235, 1)');

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

setInterval(Actual,3000,'/sensor/temperatura', T);

setInterval(Actual,3000,'/sensor/humitat', H);
