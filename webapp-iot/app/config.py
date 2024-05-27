class Config:
    DATABASE_NAME = 'sensors.db'
    DATABASE_MAX = 1000  # NUM REGISTROS
    MQTT_BROKER = "mqtt.eclipseprojects.io"
    KAFKA_BROKER = '172.17.0.3:9092'
    SENSOR_TOPICS = ['temperature_assi', 'led_assi']
    ACTUATOR_TOPICS = 'led_act'

