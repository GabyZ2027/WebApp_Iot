import threading
import time
import paho.mqtt.client as mqtt
from pykafka import KafkaClient

class MQTTKafkaBridge:
    def __init__(self, mqtt_broker, kafka_broker, topics):
        self.mqtt_broker = mqtt_broker
        self.kafka_broker = kafka_broker
        self.topics = topics

        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"MQTTKafkaBridge")
        self.kafka_client = KafkaClient(hosts=self.kafka_broker)
        self.kafka_producers = {topic: self.kafka_client.topics[topic.encode('ascii')].get_sync_producer() for topic in self.topics}
        self.kafka_consumers = {topic: self.kafka_client.topics[topic.encode('ascii')].get_simple_consumer() for topic in self.topics}

        self.mqtt_client.MQTT2Kafka = lambda client, userdata, message: self.MQTT2Kafka(client, userdata, message, self.kafka_producers)

    def MQTT2Kafka(self, client, userdata, message, kafka_producers):
        msg_payload = str(message.payload.decode('utf-8'))
        mqtt_topic = message.topic
        print('Mensaje MQTT recibido en el topic', mqtt_topic, ':', msg_payload)
        
        kafka_producer = kafka_producers.get(mqtt_topic)
        if kafka_producer is not None:
            kafka_producer.produce(msg_payload.encode('ascii'))
            print('KAFKA: Publicado', msg_payload, 'al topic', kafka_producer._topic.name.decode())

    def Kafka2MQTT(self):
        while True:
            for topic, consumer in self.kafka_consumers.items():
                message = consumer.consume(block=False)
                if message is not None:
                    msg_payload = message.value.decode('ascii')
                    print('Mensaje Kafka recibido en el topic', topic, ':', msg_payload)
                    self.mqtt_client.publish(topic, msg_payload)
                    print('MQTT: Publicado', msg_payload, 'al topic', topic)
            time.sleep(1)

    def start(self):
        self.mqtt_client.connect(self.mqtt_broker)
        for topic in self.topics:
            self.mqtt_client.subscribe(topic)

        kafka_thread = threading.Thread(target=self.Kafka2MQTT)
        kafka_thread.start()

        self.mqtt_client.loop_start()
        self.kafka_thread = kafka_thread

    def stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        for consumer in self.kafka_consumers.values():
            consumer.stop()
        self.kafka_thread.join()
