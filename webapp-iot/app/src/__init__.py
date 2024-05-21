from flask import Flask
from config import Config
from src.services.DataAcquisitionService import Data_Acquisition
from src.models.mqtt_kafka_bridge import MQTTKafkaBridge
from src.models.kafka import KafkaManager
from src.models.database import Sensors_BD

from src.routes.AuthApi import auth_blueprint

app = Flask(__name__)

def init_app():
    app.config.from_object(Config)
    #app.register_blueprint(, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Inicializar KafkaManager
    kafka_manager = KafkaManager(Config.KAFKA_BROKER)

    # Iniciar thread del Servicio de Data Acquisition
    kafka_consumer = Data_Acquisition(kafka_manager, Config.TOPICS, Config.DATABASE_NAME, Config.DATABASE_MAX)
    #kafka_consumer.start()
    
    # Iniciar el thread del bridge MQTT-Kafka
    mqtt_kafka_bridge = MQTTKafkaBridge(Config.MQTT_BROKER, Config.KAFKA_BROKER, Config.TOPICS)
    #mqtt_kafka_bridge.start()
    
    app.kafka_consumer = kafka_consumer
    app.mqtt_kafka_bridge = mqtt_kafka_bridge

    return app

