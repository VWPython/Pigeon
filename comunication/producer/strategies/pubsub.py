from comunication.producer.producerStrategy import ProducerStrategy
from comunication.connection import ConnectionRabbitMQ


class PubSub(ProducerStrategy):
    """
    Simple class that receive messages.
    """

    def __init__(self):
        """
        PubSub class constructor
        """

        self.rabbitMQ = ConnectionRabbitMQ()

    def receive(self, name):
        """
        Receive and print messages.
        """

        connection = self.rabbitMQ.establish_connection()
        channel = self.rabbitMQ.create_channel(connection)
        self.fanout_exchange_type_declare(channel, name)
        queue_name = self.create_temporary_queue(channel)
        self.binding(channel, name, queue_name)
        self.rabbitMQ.callback_consume(channel, queue_name)

        print(' [*] Waiting for messages. To exit press CTRL+C')

        self.rabbitMQ.wait_for_data(channel)

    def fanout_exchange_type_declare(self, channel, exchange_name):
        """
        Declare an exchange of type fanout that send messages to an exchange and
        the exchange must know exactly what to do with a message it receives

        On one side it receives messages from producers and the other side it
        pushes them to queues.

        The rules for that are defined by the exchange type (fanout) it just
        broadcasts all the messages it receives to all the queues it knows.

        Parameters:

            - channel: The channel connection.
            - exchange_name: Name of the exchange of type fanout

        Return: Nothing
        """

        channel.exchange_declare(exchange=exchange_name, type='fanout')

    def create_temporary_queue(self, channel):
        """
        Hear about all log messages, not just a subset of them, and it is also
        interested only in currently flowing messages not in the old ones.

        Connect to Rabbit we need a fresh, empty queue. To do it we could
        create a queue with a random name

        Once we disconnect the consumer the queue should be deleted.

        Parameters:

            - channel: The channel connection

        Return: The random queue name
        """

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        return queue_name

    def binding(self, channel, exchange_name, queue_name):
        """
        Tell the exchange to send messages to our queue. That relationship
        between exchange and a queue is called a binding.
        """

        channel.queue_bind(exchange=exchange_name, queue=queue_name)