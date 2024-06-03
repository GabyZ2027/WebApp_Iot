from pykafka import KafkaClient
from time import time

class KafkaManager:
    """
    KafkaManager class for managing Kafka producers and consumers.

    This class provides methods to create Kafka producers and consumers, and to produce and consume messages
    from Kafka topics.

    Args:
        hosts (str): The address of the Kafka server in the format "host:port".
    """

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
    
    def consume_latest(self, consumer, timeout: float = 2.0):
        """
        Consumes messages from Kafka until a new message is received or the timeout is reached.

        Args:
            consumer (pykafka.simpleconsumer.SimpleConsumer): A configured Kafka consumer.
            timeout (float): Time in seconds to wait for new messages before stopping.

        Returns:
            list: A list of consumed messages.
        """
        start_time = time()
        messages = []

        for message in consumer:
            if message is not None:
                messages.append(message.value.decode('utf-8'))
                print("Consumed message:", message.value.decode('utf-8'))
                start_time = time()

            if time() - start_time > timeout:
                break

        print("End of consumption")
        return messages

    def consume(self, consumer):
        """
        Consumes messages from the specified consumer.

        Args:
            consumer (pykafka.simpleconsumer.SimpleConsumer): A configured Kafka consumer.

        Returns:
            list: A list of messages received from the topic.
        """
        messages = []
        for message in consumer:
            if message is not None:
                print("Consumed message:", message.value.decode('utf-8'))
                messages.append(message.value.decode('utf-8'))
        print("End of consumption")
        return messages
    
    def produce(self, producer, message):
        """
        Produces a message to the specified topic.

        Args:
            producer (pykafka.producer.Producer): A configured Kafka producer.
            message (bytes): The message to be sent.

        Returns:
            None
        """
        producer.produce(message)
