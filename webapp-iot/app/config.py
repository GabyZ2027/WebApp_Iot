class Config:
    DATABASE_NAME = 'sensors.db'
    DATABASE_MAX = 1000  # NUM REGISTROS
    MQTT_BROKER = "mqtt.eclipseprojects.io"
    KAFKA_BROKER = '172.17.0.3:9092'
    TOPICS = ['temperature4', 'led']

