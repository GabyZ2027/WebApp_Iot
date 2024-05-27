from flask import Blueprint, jsonify, request, current_app
from time import sleep
api_blueprint = Blueprint('api_blueprint', __name__)

def set_queues(s_request_queue,s_response_queue):
    global request_queue, response_queue
    request_queue = s_request_queue
    response_queue = s_response_queue

@api_blueprint.route('/sensor/temperatura/historial', methods=['GET'])
def temperatura_historial():
    request_msg = {'type': 'getLectures', 'id': 0, 'quantitat': 10}
    request_queue.put(request_msg)
    sleep(3)
    temperatura_historial = False
    while(not temperatura_historial):
        temperatura_historial = response_queue.get()
    print(f'getLectures response: {temperatura_historial}')
    if not isinstance(temperatura_historial, list):
        return jsonify({"error": "Error retrieving temperature history"}), 500

    return jsonify({"temps": [t[1] for t in temperatura_historial], "data": [t[0] for t in temperatura_historial]})

@api_blueprint.route('/sensor/humitat/historial', methods=['GET'])
def humitat_historial():
    request_msg = {'type': 'getLectures', 'id': 2, 'quantitat': 10}
    request_queue.put(request_msg)
    humitat_historial = False
    while(not humitat_historial):
        humitat_historial = response_queue.get()
    
    if not isinstance(humitat_historial, list):
        return jsonify({"error": "Error retrieving humidity history"}), 500

    return jsonify({"temps": [h[1] for h in humitat_historial], "data": [h[0] for h in humitat_historial]})

@api_blueprint.route('/led/historial', methods=['GET'])
def led_historial():
    request_msg = {'type': 'getLectures', 'id': 0, 'quantitat': 10}
    request_queue.put(request_msg)
    led_historial = False
    while(not led_historial):
        led_historial = response_queue.get()
    if not isinstance(led_historial, list):
        return jsonify({"error": "Error retrieving LED history"}), 500

    return jsonify({"temps": [l[1] for l in led_historial], "data": [l[0] for l in led_historial]})

@api_blueprint.route('/sensor/humitat', methods=['GET'])
def humitat():
    request_msg = {'type': 'getLectura', 'id': 2}
    request_queue.put(request_msg)
    humitat = False
    while(not humitat):
        humitat = response_queue.get()
    if not isinstance(humitat, tuple):
        return jsonify({"error": "Error retrieving humidity"}), 500

    return jsonify({"temps": humitat[1], "data": humitat[0]})

@api_blueprint.route('/sensor/temperatura', methods=['GET'])
def temperatura():
    request_msg = {'type': 'getLectura', 'id': 1}
    request_queue.put(request_msg)
    temperatura = False
    while(not temperatura):
        temperatura = response_queue.get()
    if not isinstance(temperatura, tuple):
        return jsonify({"error": "Error retrieving temperature"}), 500

    return jsonify({"temps": temperatura[1], "data": temperatura[0]})

@api_blueprint.route('/led', methods=['GET', 'POST'])
def led():
    if request.method == 'GET':
        request_msg = {'type': 'getLectura', 'id': 0}
        request_queue.put(request_msg)
        led = False
        while(not led):
            led = response_queue.get()
        
        if not isinstance(led, tuple):
            return jsonify({"error": "Error retrieving LED status"}), 500

        return jsonify({"temps": led[1], "data": led[0]})
    
    elif request.method == 'POST':
        data = request.get_data(as_text=True)
        if "led-status=1" in data:
            current_app.kafka_manager.produce("led", "1")
            return "LED ON"
        elif "led-status=0" in data:
            current_app.kafka_manager.produce("led", "0")
            return "LED OFF"
        else:
            return "Message not recognized"

"""
from flask import Blueprint, jsonify, request, current_app
from src.models.kafka import KafkaManager
from config import Config

kafka_manager = KafkaManager(Config.KAFKA_BROKER)

api_blueprint = Blueprint('api_blueprint', __name__)
def set_db(bd):
    global sensors_bd
    sensors_bd = bd

@api_blueprint.route('/sensor/temperatura/historial', methods=['GET'])
def temperatura_historial():
    temperatura_historial = sensors_bd.getLectures(1, 10)
    return jsonify({"temps": temperatura_historial[0], "data": temperatura_historial[1]})

@api_blueprint.route('/sensor/humitat/historial', methods=['GET'])
def humitat_historial():
    humitat_historial = sensors_bd.getLectures(2, 10)
    return jsonify({"temps": humitat_historial[0], "data": humitat_historial[1]})

@api_blueprint.route('/led/historial', methods=['GET'])
def led_historial():
    led_historial = sensors_bd.getLectures(0, 10)
    return jsonify({"temps": led_historial[0], "data": led_historial[1]})

@api_blueprint.route('/sensor/humitat', methods=['GET'])
def humitat():
    humitat = sensors_bd.getLectura(2)
    return jsonify({"temps": humitat[0], "data": humitat[1]})

@api_blueprint.route('/sensor/temperatura', methods=['GET'])
def temperatura():
    temperatura = sensors_bd.getLectura(1)
    return jsonify({"temps": temperatura[0], "data": temperatura[1]})

@api_blueprint.route('/led', methods=['GET', 'POST'])
def led():
    if request.method == 'GET':
        led = sensors_bd.getLectura(0)
        return jsonify({"temps": led[0], "data": led[1]})
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
"""