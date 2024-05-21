from threading import Thread
import time
from src.models.kafka import KafkaManager
from src.models.database import Sensors_BD

TS = 1 #segons

class Data_Acquisition(Thread):
    def __init__(self, kafka_manager, kafka_topics, db_name, db_max):
        Thread.__init__(self)
        self.kafka_manager = kafka_manager
        self.kafka_topics = kafka_topics
        self.db = Sensors_BD(db_name, db_max)
        self.daemon = True

    def run(self):
        while True:
            for topic in self.kafka_topics:
                messages = self.kafka_manager.consume(topic)
                for msg_payload in messages:
                    print(f'Mensaje Kafka recibido en el topic {topic}: {msg_payload}')
                    self.save_message_to_db(topic, msg_payload)
            time.sleep(TS)

    def save_message_to_db(self, topic, payload):
        #cambiarlo a algo mas escalable que con una unica función
        #escribas en la bd, especificando el id que te viene en el mensaje
        if topic == 'temperature4':
            self.db.setLecturaSen(payload) 
        elif topic == 'led':
            self.db.setLecturaAct(payload)
