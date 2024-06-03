from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from src.models.kafka import KafkaManager
from config import Config
from time import sleep
from queue import Queue

api_blueprint = Blueprint('api_blueprint', __name__)

kafka_manager = KafkaManager(Config.KAFKA_BROKER)

producer = kafka_manager.create_producer(Config.ACTUATOR_TOPICS)

def set_queues(s_request_queues, s_response_queues):
    """
    Sets the request and response queues for inter-process communication.

    Args:
        s_request_queues (dict): A dictionary of request queues.
        s_response_queues (dict): A dictionary of response queues.
    """
    global request_queues, response_queues
    request_queues = s_request_queues
    response_queues = s_response_queues

@api_blueprint.route('/sensor/temperatura/historial', methods=['GET'])
def temperatura_historial():
    """
    Retrieves the temperature sensor's historical data.

    Returns:
        Response: A JSON response containing the temperature data.
    """
    request_msg = {'type': 'getLectures', 'id': 0, 'quantitat': 10}
    request_queues['temperatura_hist'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['temperatura_hist'].get()
    if response[0] == "get" + str(request_msg['id']):
        return jsonify({"temps": [t[1] for t in response[1][::-1]], "data": [t[0] for t in response[1][::-1]]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/sensor/humitat/historial', methods=['GET'])
def humitat_historial():
    """
    Retrieves the humidity sensor's historical data.

    Returns:
        Response: A JSON response containing the humidity data.
    """
    request_msg = {'type': 'getLectures', 'id': 1, 'quantitat': 10}
    request_queues['humedad_hist'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['humedad_hist'].get()
    if response[0] == "get" + str(request_msg['id']):
        return jsonify({"temps": [h[1] for h in response[1][::-1]], "data": [h[0] for h in response[1][::-1]]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/led/historial', methods=['GET'])
@login_required
def led_historial():
    """
    Retrieves the LED's historical data.

    Returns:
        Response: A JSON response containing the LED data.
    """
    request_msg = {'type': 'getLectures', 'id': 2, 'quantitat': 10}
    request_queues['led_hist'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['led_hist'].get()
    if response[0] == "get" + str(request_msg['id']):
        return jsonify({"temps": [l[2] for l in response[1][::-1]], "data": [l[1] for l in response[1][::-1]]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/sensor/humitat', methods=['GET'])
def humitat():
    """
    Retrieves the current humidity reading.

    Returns:
        Response: A JSON response containing the current humidity data.
    """
    request_msg = {'type': 'getLectura', 'id': 1}
    request_queues['humedad'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['humedad'].get()
    print("hum:", response)
    if response[0] == request_msg['id']:
        return jsonify({"humidity": response[2], "data": response[1]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/sensor/temperatura', methods=['GET'])
def temperatura():
    """
    Retrieves the current temperature reading.

    Returns:
        Response: A JSON response containing the current temperature data.
    """
    request_msg = {'type': 'getLectura', 'id': 0}
    request_queues['temperatura'].put(request_msg)
    response = False
    while isinstance(response, bool):
        print(response)
        response = response_queues['temperatura'].get()
    print("temp:", response)
    if response[0] == request_msg['id']:
        return jsonify({"temps": response[2], "data": response[1]})
    else:
        return jsonify({"error": "Invalid response ID"}), 500

@api_blueprint.route('/led', methods=['GET', 'POST'])
@login_required
def led():
    """
    Handles the LED control.

    Returns:
        Response: A JSON response containing the LED status.
    """
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

