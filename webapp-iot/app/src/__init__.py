from flask import Flask
from multiprocessing import Process,Queue
from config import Config
from src.services.DataAcquisitionService import Data_Acquisition
#from mqtt_kafka_bridge import MQTTKafkaBridge
from src.models.kafka import KafkaManager
from src.models.S_database import DatabaseServer

from src.routes.api import api_blueprint,set_queues
from src.routes.AuthApi import set_queues as sq
from src.routes.AuthApi import auth_blueprint,login_manager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)


def init_app():
    app.config.from_object(Config)
    app.register_blueprint(api_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    CSRFProtect()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_blueprint.login'

    # Inicializar KafkaManager
    kafka_manager = KafkaManager(Config.KAFKA_BROKER)
    app.kafka_manager = kafka_manager

    #Inicio proceso Database
    request_queues = {
        'temperatura': Queue(),
        'temperatura_hist': Queue(),
        'humedad': Queue(),
        'humedad_hist': Queue(),
        'led': Queue(),
        'led_hist': Queue(),
        'auth': Queue(),
        'register': Queue(),
        'login': Queue(),
        'general':Queue(),
    }

    response_queues = {
        'temperatura': Queue(),
        'temperatura_hist': Queue(),
        'humedad': Queue(),
        'humedad_hist': Queue(),
        'led': Queue(),
        'led_hist': Queue(),
        'auth': Queue(),
        'register': Queue(),
        'login': Queue(),
        'general':Queue(),
    }
    set_queues(request_queues,response_queues)

    sq(request_queues,response_queues)
    
    db_server = DatabaseServer(Config.DATABASE_NAME, Config.DATABASE_MAX, request_queues, response_queues)
    db_server.start()

    # Iniciar proceso del Servicio de Data Acquisition
    data_acquisition_process = Data_Acquisition(kafka_manager, Config.SENSOR_TOPICS, request_queues['general'])
    data_acquisition_process.start()
    
    # Iniciar el proceso del bridge MQTT-Kafka
    #mqtt_kafka_bridge = MQTTKafkaBridge(Config.MQTT_BROKER, Config.KAFKA_BROKER, Config.SENSOR_TOPICS, Config.ACTUATOR_TOPICS)
    #mqtt_kafka_bridge.start()
    
    app.data_acquisition_process = data_acquisition_process
    #app.mqtt_kafka_bridge = mqtt_kafka_bridge
    
    return app

