from pykafka import KafkaClient
from time import time

class KafkaManager:
    def __init__(self, hosts):
        """
        Initializes the KafkaManager with the Kafka server's address.

        Args:
            hosts (str): The address of the Kafka server in the format "host:port".
        """
        self.hosts = hosts

    def create_producer(self, topic_name):
        """
        Creates a Kafka producer for the specified topic.

        Args:
            topic_name (str): The name of the topic to which the producer will send messages.

        Returns:
            pykafka.producer.Producer: An instance of the Kafka producer.
        """
        client = KafkaClient(hosts=self.hosts)
        topic = client.topics[topic_name.encode('utf-8')]
        producer = topic.get_producer()
        return producer

    def create_consumer(self, topic_name):
        """
        Creates a Kafka consumer for the specified topic.

        Args:
            topic_name (str): The name of the topic from which the consumer will receive messages.

        Returns:
            pykafka.simpleconsumer.SimpleConsumer: An instance of the Kafka consumer.
        """
        client = KafkaClient(hosts=self.hosts)
        topic = client.topics[topic_name.encode('utf-8')]
        consumer = topic.get_simple_consumer()
        return consumer
    
    def consume_latest(self,consumer, timeout: float = 2.0):
        """
        Consume mensajes de Kafka hasta que se recibe uno nuevo o hasta que se alcanza el timeout.
        
        :param consumer: Un consumidor de Pykafka configurado.
        :param timeout: Tiempo en segundos para esperar nuevos mensajes antes de detenerse.
        :return: Una lista de mensajes consumidos.
        """
        start_time = time()
        messages = []

        for message in consumer:
            if message is not None:
                messages.append(message.value.decode('utf-8'))
                print("Mensaje consumido:", message.value.decode('utf-8'))
                start_time = time() 

            if time() - start_time > timeout:
                break

        print("Fin del consumo")
        return messages


    def consume(self, consumer):
        """
        Consumes messages from the specified topic.

        Args:
            topic_name (str): The name of the topic from which the consumer will receive messages.

        Returns:
            list: A list of messages received from the topic.
        """
        #consumer = self.create_consumer(topic_name)
        messages = []
        for message in consumer:
            if message is not None:
                print("Mensaje consumido")
                print(message.value.decode('utf-8'))
                messages.append(message.value.decode('utf-8'))
        print("FI")
        return messages
    
    def produce(self, producer, message):
        """
        Produces a message to the specified topic.

        Args:
            topic_name (str): The name of the topic to which the producer will send the message.
            message (bytes): The message to be sent.

        Returns:
            None
        """
        producer.produce(message)
