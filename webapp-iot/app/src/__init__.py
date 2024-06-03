from flask import Flask
from multiprocessing import Process, Queue
from config import Config
from src.services.DataAcquisitionService import Data_Acquisition
#from mqtt_kafka_bridge import MQTTKafkaBridge
from src.models.kafka import KafkaManager
from src.models.S_database import DatabaseServer

from src.routes.api import api_blueprint, set_queues
from src.routes.AuthApi import set_queues as auth_set_queues
from src.routes.AuthApi import auth_blueprint, login_manager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

def init_app():
    """
    Initializes the Flask application with configurations, blueprints, and necessary services.

    Returns:
        app (Flask): The initialized Flask application.
    """
    # Load configuration from the Config object
    app.config.from_object(Config)
    
    # Register blueprints for API and authentication routes
    app.register_blueprint(api_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Enable CSRF protection
    CSRFProtect()
    
    # Initialize the login manager with the app and set the login view
    login_manager.init_app(app)
    login_manager.login_view = 'auth_blueprint.login'

    # Initialize KafkaManager with the Kafka broker address
    kafka_manager = KafkaManager(Config.KAFKA_BROKER)
    app.kafka_manager = kafka_manager

    # Create queues for inter-process communication
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
        'general': Queue(),
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
        'general': Queue(),
    }
    
    # Set the request and response queues for the API and authentication routes
    set_queues(request_queues, response_queues)
    auth_set_queues(request_queues, response_queues)
    
    # Initialize and start the DatabaseServer process
    db_server = DatabaseServer(Config.DATABASE_NAME, Config.DATABASE_MAX, request_queues, response_queues)
    db_server.start()

    # Initialize and start the Data Acquisition process
    data_acquisition_process = Data_Acquisition(kafka_manager, Config.SENSOR_TOPICS, request_queues['general'])
    data_acquisition_process.start()
    
    # Optionally initialize and start the MQTT-Kafka bridge
    # mqtt_kafka_bridge = MQTTKafkaBridge(Config.MQTT_BROKER, Config.KAFKA_BROKER, Config.SENSOR_TOPICS, Config.ACTUATOR_TOPICS)
    # mqtt_kafka_bridge.start()
    
    # Store processes in the app context for later use
    app.data_acquisition_process = data_acquisition_process
    # app.mqtt_kafka_bridge = mqtt_kafka_bridge
    
    return app

