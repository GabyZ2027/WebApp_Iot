from flask import Blueprint, jsonify, request, current_app
from src.models.kafka import KafkaManager
from config import Config
from time import sleep
from queue import Queue

api_blueprint = Blueprint('api_blueprint', __name__)

kafka_manager = KafkaManager(Config.KAFKA_BROKER)

producer = kafka_manager.create_producer(Config.ACTUATOR_TOPICS)



def set_queues(s_request_queues, s_response_queues):
    global request_queues, response_queues
    request_queues = s_request_queues
    response_queues = s_response_queues

@api_blueprint.route('/sensor/temperatura/historial', methods=['GET'])
def temperatura_historial():
    request_msg = {'type': 'getLectures', 'id': 0, 'quantitat': 10}
    request_queues['temperatura_hist'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['temperatura_hist'].get()
    if response[0] == "get" + str(request_msg['id']):
        return jsonify({"temps": [t[1] for t in response[1]], "data": [t[0] for t in response[1]]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/sensor/humitat/historial', methods=['GET'])
def humitat_historial():
    request_msg = {'type': 'getLectures', 'id': 1, 'quantitat': 10}
    request_queues['humedad_hist'].put(request_msg)  
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['humedad_hist'].get()
    if response[0] == "get" + str(request_msg['id']):
        return jsonify({"temps": [h[1] for h in response[1]], "data": [h[0] for h in response[1]]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/led/historial', methods=['GET'])
def led_historial():
    request_msg = {'type': 'getLectures', 'id': 2, 'quantitat': 10}
    request_queues['led_hist'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['led_hist'].get()
    if response[0] == "get" + str(request_msg['id']):
        return jsonify({"temps": [l[2] for l in response[1]], "data": [l[1] for l in response[1]]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/sensor/humitat', methods=['GET'])
def humitat():
    request_msg = {'type': 'getLectura', 'id': 1}
    request_queues['humedad'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['humedad'].get()
    print("hum:",response)
    if response[0] == request_msg['id']:
        return jsonify({"humidity": response[2], "data": response[1]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/sensor/temperatura', methods=['GET'])
def temperatura():
    request_msg = {'type': 'getLectura', 'id': 0}
    request_queues['temperatura'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['temperatura'].get()
    print("temp:",response)
    if response[0] == request_msg['id']:
        return jsonify({"temps": response[2], "data": response[1]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/led', methods=['GET', 'POST'])
def led():
    if request.method == 'GET':
        request_msg = {'type': 'getLectura', 'id': 2}
        request_queues['led'].put(request_msg)
        response = False
        while isinstance(response, bool):
            print(response)
            response = response_queues['led'].get()
        return jsonify({"temps": response[2], "data": response[1]})
    elif request.method == 'POST':
        data = request.get_data(as_text=True)
        if "led-status=1" in data:
            led_message = "1"
            kafka_manager.produce(producer, led_message.encode('utf-8'))
            return "LED ON"
        elif "led-status=0" in data:
            led_message = "0"
            kafka_manager.produce(producer, led_message.encode('utf-8'))
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