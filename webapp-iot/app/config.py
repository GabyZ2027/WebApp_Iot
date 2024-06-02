import os
class Config:
    DATABASE_NAME = 'sensors.db'
    DATABASE_MAX = 1000  # NUM REGISTROS
    MQTT_BROKER = "mqtt.eclipseprojects.io"
    KAFKA_BROKER = 'localhost:9092'
    SENSOR_TOPICS = ['temperature_assi', 'led_assi', 'humitat_assi']
    ACTUATOR_TOPICS = 'led_act'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'usuaris.db')
