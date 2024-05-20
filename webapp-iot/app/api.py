from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from kafka import KafkaManager

from database import Sensors_BD

app = Flask(__name__)
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class SensorData(db.Model):
    __tablename__ = 'SENSORS'
    sensor = db.Column(db.String, primary_key=True)
    data = db.Column(db.Date, primary_key=True)
    lectura = db.Column(db.String, nullable=False)
"""

@app.route('/sensor/temperatura/historial', methods=['GET'])
def temperatura_historial():
    lecturas = sensors_bd.getLecturesSen(10)
    return jsonify({"lecturas": lecturas})

@app.route('/sensor/humitat/historial', methods=['GET'])
def humitat_historial():
    lecturas = sensors_bd.getLecturesSen(10)
    return jsonify({"lecturas": lecturas})

@app.route('/led/historial', methods=['GET'])
def led_historial():
    lecturas = sensors_bd.getLecturesAct(10)
    return jsonify({"lecturas": lecturas})

@app.route('/sensor/humitat/', methods=['GET'])
def humitat():
    lectura = sensors_bd.getLecturaSen()
    return jsonify({"lectura": lectura})

@app.route('/sensor/temperatura', methods=['GET'])
def temperatura():
    lectura = sensors_bd.getLecturaAct()
    return jsonify({"lectura": lectura})

@app.route('/led', methods=['GET'])
def led_lectura():
    lectura = sensors_bd.getLecturaAct()
    return jsonify({"lectura": lectura})

@app.route('/led', methods=['POST'])
def control_led():
    data = request.get_data(as_text=True)
    if "led-status=1" in data:
        kafka_manager.produce("led", "1")
        return "LED ON"
    elif "led-status=0" in data:
        kafka_manager.produce("led", "0")
        return "LED OFF"
    else:
        return "Mensaje no reconocido"

if __name__ == '__main__':
    kafka_manager = KafkaManager("172.17.0.3")
    sensors_bd = Sensors_BD('database.db', max=5000)
    app.run(host='0.0.0.0', port=5000, debug=True)