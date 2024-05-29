// Actuador
function toggleLED(state) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/led', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("led-status=" + (state === 'on' ? '1' : '0'));
}

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