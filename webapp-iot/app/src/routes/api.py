from flask import Flask, jsonify, request, Blueprint
from src.models.kafka import KafkaManager
from src.models.S_database import Sensors_BD


api_blueprint = Blueprint('api_blueprint',__name__)

kafka_manager = KafkaManager("172.17.0.3")
sensors_bd = Sensors_BD('sensors.db', max=5000)

@app.route('/sensor/temperatura/historial', methods=['GET'])
def temperatura_historial():
    temperatura_historial = sensors_bd.getLectures(1,10)
    return jsonify({"temps": temperatura_historial[0],"data": temperatura_historial[1]})

@app.route('/sensor/humitat/historial', methods=['GET'])
def humitat_historial():
    humitat_historial = sensors_bd.getLectures(2,10)
    return jsonify({"temps": humitat_historial[0],"data": humitat_historial[1]})

@app.route('/led/historial', methods=['GET'])
def led_historial():
    led_historial = sensors_bd.getLectures(0,10)
    return jsonify({"temps": led_historial[0],"data": led_historial[1]})

@app.route('/sensor/humitat', methods=['GET'])
def humitat():
    humitat = sensors_bd.getLectura(2)
    return jsonify({"temps": humitat[0],"data": humitat[1]})


@app.route('/sensor/temperatura', methods=['GET'])
def temperatura():
    temperatura = sensors_bd.getLectura(1)
    return jsonify({"temps": temperatura[0],"data": temperatura[1]})


@app.route('/led', methods=['GET', 'POST'])
def led():
    if request.method == 'GET':
        led = sensors_bd.getLectura(0)
        return jsonify({"temps": led[0],"data": led[1]})
    
    elif request.method == 'POST':
        data = request.get_data(as_text=True)
        if "led-status=1" in data:
            kafka_manager.produce("led", "1")
            return "LED ON"
        elif "led-status=0" in data:
            kafka_manager.produce("led", "0")
            return "LED OFF"
        else:
            return "Message not reconised"

