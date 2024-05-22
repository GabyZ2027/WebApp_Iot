from pykafka import KafkaClient

class KafkaManager:
    def __init__(self, hosts):
        """
        Initializes the KafkaManager with the Kafka server's address.

        Args:
            hosts (str): The address of the Kafka server in the format "host:port".
        """
        self.client = KafkaClient(hosts=hosts)

    def create_producer(self, topic_name):
        """
        Creates a Kafka producer for the specified topic.

        Args:
            topic_name (str): The name of the topic to which the producer will send messages.

        Returns:
            pykafka.producer.Producer: An instance of the Kafka producer.
        """
        topic = self.client.topics[topic_name.encode('utf-8')]
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
        topic = self.client.topics[topic_name.encode('utf-8')]
        consumer = topic.get_simple_consumer()
        return consumer
    
    def consume(self, topic_name):
        """
        Consumes messages from the specified topic.

        Args:
            topic_name (str): The name of the topic from which the consumer will receive messages.

        Returns:
            list: A list of messages received from the topic.
        """
        consumer = self.create_consumer(topic_name)
        messages = []
        for message in consumer:
            if message is not None:
                messages.append(message.value.decode('utf-8'))
        return messages
    def produce(self, topic_name, message):
        """
        Produces a message to the specified topic.

        Args:
            topic_name (str): The name of the topic to which the producer will send the message.
            message (bytes): The message to be sent.

        Returns:
            None
        """
        producer = self.create_producer(topic_name)
        producer.produce(message)
