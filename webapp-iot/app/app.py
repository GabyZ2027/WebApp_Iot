from flask import Flask
from config import Config
from app.services.DataAcquisitionService import Data_Acquisition
from app.models.mqtt_kafka_bridge import MQTTKafkaBridge
from app.models.kafka import KafkaManager
from app.models.database import Sensors_BD

from routes import AuthApi, api

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api.app, url_prefix='/')
app.register_blueprint(AuthApi.app, url_prefix='/auth')

@app.before_first_request
def setup():
    # Inicializar KafkaManager
    kafka_manager = KafkaManager(Config.KAFKA_BROKER)

    # Iniciar thread del Servicio de Data Acquisition
    kafka_consumer = Data_Acquisition(kafka_manager, Config.TOPICS, Config.DATABASE_NAME, Config.DATABASE_MAX)
    kafka_consumer.start()
    
    # Iniciar el thread del bridge MQTT-Kafka
    mqtt_kafka_bridge = MQTTKafkaBridge(Config.MQTT_BROKER, Config.KAFKA_BROKER, Config.TOPICS)
    mqtt_kafka_bridge.start()
    
    app.kafka_consumer = kafka_consumer
    app.mqtt_kafka_bridge = mqtt_kafka_bridge



if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("Proceso interrumpido por el usuario.")
    finally:
        # Detener los consumidores al finalizar la aplicación
        app.kafka_consumer.join()
        app.mqtt_kafka_bridge.stop()
