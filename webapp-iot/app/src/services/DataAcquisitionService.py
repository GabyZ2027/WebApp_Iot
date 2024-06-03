from threading import Thread
import time

TS = 3  # seconds

class Data_Acquisition(Thread):
    """
    Data_Acquisition class for acquiring data from Kafka and storing it in a database.

    This class inherits from `Thread` to allow for background execution and is responsible for 
    consuming messages from Kafka, processing them, and sending requests to store these messages 
    in a database.

    Args:
        kafka_manager (KafkaManager): Instance of the Kafka manager.
        kafka_topics (list): List of Kafka topics to subscribe to.
        request_queue (Queue): Request queue for the database server.
    """

    def __init__(self, kafka_manager, kafka_topics, request_queue):
        """
        Initializes the Data_Acquisition instance.

        Args:
            kafka_manager (KafkaManager): Instance of the Kafka manager.
            kafka_topics (list): List of Kafka topics to subscribe to.
            request_queue (Queue): Request queue for the database server.
        """
        super().__init__()
        self.kafka_manager = kafka_manager
        self.kafka_topics = kafka_topics
        self.daemon = True
        self.consumers = []
        self.request_queue = request_queue

    def run(self):
        """
        Runs the main thread to subscribe to Kafka topics and start consuming messages.
        """
        for topic in self.kafka_topics:
            print(topic)
            consumer = self.kafka_manager.create_consumer(topic)
            self.consumers.append(consumer)
            thread = Thread(target=self.consume_messages, args=(consumer,))
            thread.start()

    def consume_messages(self, consumer):
        """
        Consumes messages from a Kafka consumer and stores them in the database.

        Args:
            consumer (KafkaConsumer): Kafka consumer from which messages will be read.
        """
        for message in consumer:
            if message is not None:
                msg_payload = message.value.decode('utf-8')
                msg_data = msg_payload.split(',')
                # print(f'Kafka message received on topic {consumer._topic.name.decode()}: {msg_payload}')
                self.save_message_to_db(msg_data)
                time.sleep(TS)

    def save_message_to_db(self, payload):
        """
        Creates a request to store a message in the database.

        Args:
            payload (list): List of data extracted from the Kafka message.
        """
        request = {'type': 'setLectura', 'id': int(payload[0]), 'lectura': str(payload[1])}
        self.request_queue.put(request)
