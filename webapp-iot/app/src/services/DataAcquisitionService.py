from threading import Thread
import time

TS = 3  # segundos

class Data_Acquisition(Thread):
    def __init__(self, kafka_manager, kafka_topics, request_queue):
        super().__init__()
        self.kafka_manager = kafka_manager
        self.kafka_topics = kafka_topics
        self.daemon = True
        self.consumers = []
        self.request_queue = request_queue  # Cola de solicitudes para el servidor de la base de datos

    def run(self):
        for topic in self.kafka_topics:
            print(topic)
            consumer = self.kafka_manager.create_consumer(topic)
            self.consumers.append(consumer)
            thread = Thread(target=self.consume_messages, args=(consumer,))
            thread.start()

    def consume_messages(self, consumer):
        for message in consumer:
            if message is not None:
                msg_payload = message.value.decode('utf-8')
                msg_data = msg_payload.split(',')
                #print(f'Mensaje Kafka recibido en el topic {consumer._topic.name.decode()}: {msg_payload}')
                self.save_message_to_db(msg_data)
                time.sleep(TS)

    def save_message_to_db(self, payload):
        # Crear una solicitud para guardar el mensaje en la base de datos
        request = {'type': 'setLectura', 'id': int(payload[0]), 'lectura': str(payload[1])}
        self.request_queue.put(request)


"""
from multiprocessing import Process
import time
from src.models.kafka import KafkaManager
from src.models.S_database import Sensors_BD

TS = 3 # segundos

class Data_Acquisition(Process):
    def __init__(self, kafka_manager, kafka_topics, db):
        super().__init__()
        self.kafka_manager = kafka_manager
        self.kafka_topics = kafka_topics
        self.daemon = True
        self.consumers = []
        self.db = db

    def run(self):
        
        for topic in self.kafka_topics:
            self.consumers.append(self.kafka_manager.create_consumer(topic))
        while True:
            for consumer in self.consumers:
                for message in consumer:
                    if message is not None:
                        msg_payload = message.value.decode('utf-8')
                        msg_data = msg_payload.split(',')
                        print(f'Mensaje Kafka recibido en el topic {consumer._topic.name.decode()}: {msg_payload}')
                        self.save_message_to_db(msg_data)
                    #time.sleep(TS)
                   
            

    def save_message_to_db(self,payload):
        self.db.setLectura(int(payload[0]),str(payload[1])) 
"""