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

function toggleLED(state) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/led"/*posar ip servidor martí*/, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("led-status=" + (state === 'on' ? '1' : '0'));
}

var T = document.getElementById("Tactual")
var H = document.getElementById("Hactual");
function Actual(path, variable){
    var r;
    r=new XMLHttpRequest();
    r.open('GET',path,true);
    r.send();
    r.onreadystatechange = function () {
        if (r.status==200 && r.readyState == 4){
            var response = r.responseText;
            variable.textContent=response;
        }
    }
}
setInterval(function() {
    Actual('/sensor/temperatura', T);
    Actual('/sensor/humitat', H);
}, 20000);

var L = document.getElementById("Led")

function update_led(variable) {
    var r;
    r=new XMLHttpRequest();
    r.open('GET','/led',true);
    r.send();
    r.onreadystatechange = function () {
        if (r.status==200 && r.readyState == 4){
            var response = r.responseText;
            if (response === 'on') {
                variable.src = "https://static.vecteezy.com/system/resources/previews/005/032/239/non_2x/bulb-light-on-free-vector.jpg";
            } else {
                variable.src = "https://cdn-icons-png.flaticon.com/512/32/32177.png";
            }
        }
    }
}
setInterval(function() {
    update_led(L);
}, 2000);