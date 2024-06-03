var ledBackground = document.getElementById('ledBackground');
var ledCheckbox = document.getElementById('ledCheckbox');
ledCheckbox.addEventListener("change", toggleLED);

function toggleLED() {
    var newState = ledCheckbox.checked ? 'on' : 'off';
    if (ledCheckbox.checked==true) {
        ledBackground.style.backgroundColor='rgb(249, 255, 199)';
    }
    else {
        ledBackground.style.backgroundColor='rgb(233, 233, 233)';
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/led', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("led-status=" + (newState === 'on' ? '1' : '0'));
}

function update_led() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/led', true);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (xhr.status == 200 && xhr.readyState == 4) {
            var response = JSON.parse(xhr.responseText);
            if (response.data === '1') {
                ledCheckbox.checked = true;
                ledBackground.style.backgroundColor = 'rgb(249, 255, 199)';
            } else {
                ledCheckbox.checked = false;
                ledBackground.style.backgroundColor = 'rgb(233, 233, 233)';
            }
        }
    }
}

setInterval(update_led, 2000);
