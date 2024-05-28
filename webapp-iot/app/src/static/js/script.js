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


function FerGrafica(dades,temps,graf,nom_label,taula) {
    if (taula) {
        taula.destroy(); 
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
function Historial(path,graf,nom_label,taula) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', path, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var data = JSON.parse(xhr.responseText);
                taula.chart=FerGrafica(data.data,data.temps,graf,nom_label,taula.chart)
                console.log("Historial: ", data);
            } else {
                console.error("Error a l'obrindre el historial:", xhr.status);
            }
        }
    };
    xhr.send();
}

let charttemp;
let charthum;
let chartled;
var graf_temperatura = document.getElementById('Temperatura').getContext('2d');
var graf_humitat = document.getElementById('Humitat').getContext('2d');
/*var graf_led = document.getElementById('LedHistorial').getContext('2d');*/

setInterval(Historial,300000,'/sensor/temperatura/historial',graf_temperatura,'Temperatura',{ chart: charttemp })
setInterval(Historial,300000,'/sensor/humitat/historial',graf_humitat,'Humitat',{ chart: charthum })

/*
    Historial('/led/historial',graf_led,'LED',{chart: chartled});
}, 20000);
*/


//Actuador
function toggleLED(state) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/led', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("led-status=" + (state === 'on' ? '1' : '0'));
}

// Valors actuals
var T = document.getElementById("Tactual")
var H = document.getElementById("Hactual");

function Actual(path, variable){
    var r;
    r=new XMLHttpRequest();
    r.open('GET',path,true);
    r.send();
    r.onreadystatechange = function () {
        if (r.status==200 && r.readyState == 4){
            var response = JSON.parse(r.responseText);
            variable.textContent = response.data; 
        }
    }
}

setInterval(Actual,60000,'/sensor/temperatura', T)
setInterval(Actual,60000,'/sensor/humitat', T)

var L = document.getElementById("Led")

function update_led(variable) {
    var r;
    r=new XMLHttpRequest();
    r.open('GET','/led',true);
    r.send();
    r.onreadystatechange = function () {
        if (r.status==200 && r.readyState == 4){
            var response = JSON.parse(r.responseText);
            if (response.data === '1') {
                variable.src = "https://static.vecteezy.com/system/resources/previews/005/032/239/non_2x/bulb-light-on-free-vector.jpg";
            } else {
                variable.src = "https://cdn-icons-png.flaticon.com/512/32/32177.png";
            }
        }
    }
}

setInterval(update_led,60000,L)

