import time
import paho.mqtt.client as mqtt
from pykafka import KafkaClient
from multiprocessing import Process

class MQTTKafkaBridge:
    def __init__(self, mqtt_broker, kafka_broker, mqtt_topics, kafka_topic):
        self.mqtt_broker = mqtt_broker
        self.kafka_broker = kafka_broker
        self.mqtt_topics = mqtt_topics
        self.kafka_topic = kafka_topic
        self.mqtt_kafka_process = None
        self.kafka_mqtt_process = None

    def consume_kafka_publish_mqtt(self):
        kafka_client = KafkaClient(hosts=self.kafka_broker)
        kafka_topic = kafka_client.topics[self.kafka_topic.encode('ascii')]
        kafka_consumer = kafka_topic.get_simple_consumer()

        mqtt_client = mqtt.Client()
        mqtt_client.connect(self.mqtt_broker)

        for message in kafka_consumer:
            if message is not None:
                msg_payload = message.value.decode('ascii')
                mqtt_client.publish(self.kafka_topic, msg_payload)
                print(f'MQTT: Publicado {msg_payload} en el topic {self.kafka_topic}')

    def on_message(self, client, userdata, message, kafka_producers):
        msg_payload = str(message.payload.decode('utf-8'))
        mqtt_topic = message.topic
        print(f'Mensaje MQTT recibido en el topic {mqtt_topic}: {msg_payload}')
        
        kafka_producer = kafka_producers[mqtt_topic]
        print(kafka_producer)
        kafka_producer.produce(msg_payload.encode('ascii'))
        print(f'KAFKA: Publicado {msg_payload} al topic {kafka_producer._topic.name.decode()}')


    def consume_mqtt_publish_kafka(self):
        mqtt_client = mqtt.Client()
        mqtt_client.connect(self.mqtt_broker)

        kafka_client = KafkaClient(hosts=self.kafka_broker)
        kafka_producers = {}
        
        for mqtt_topic in self.mqtt_topics:
            kafka_topic_name = mqtt_topic
            kafka_topic = kafka_client.topics[kafka_topic_name.encode('ascii')]
            kafka_producers[mqtt_topic] = kafka_topic.get_sync_producer()
            
        mqtt_client.on_message = lambda client, userdata, message: self.on_message(client, userdata, message, kafka_producers)
        
        for topic in self.mqtt_topics:
            mqtt_client.subscribe(topic)

        mqtt_client.loop_forever()

    def start(self):
        self.mqtt_kafka_process = Process(target=self.consume_mqtt_publish_kafka)
        self.kafka_mqtt_process = Process(target=self.consume_kafka_publish_mqtt)

        self.mqtt_kafka_process.start()
        self.kafka_mqtt_process.start()

        self.mqtt_kafka_process.join()
        self.kafka_mqtt_process.join()

if __name__ == "__main__":
    mqtt_kafka_bridge = MQTTKafkaBridge("mqtt.eclipseprojects.io", "172.17.0.3:9092", ["temperature_assi", "led_assi","humitat_assi"], "led_act")

    mqtt_kafka_process = Process(target=mqtt_kafka_bridge.consume_mqtt_publish_kafka)
    kafka_mqtt_process = Process(target=mqtt_kafka_bridge.consume_kafka_publish_mqtt)

    mqtt_kafka_process.start()
    kafka_mqtt_process.start()

    mqtt_kafka_process.join()
    kafka_mqtt_process.join()
