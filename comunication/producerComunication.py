from comunication.producer.strategies.simple import Simple
from comunication.producer.strategies.pubsub import PubSub


class ProducerComunication(object):
    """
    Maintains a reference to a Strategia object and can allow it to access your
    data.
    """

    SIMPLE = 0
    PUBSUB = 1
    strategy = None

    def __init__(self, comunication):
        """
        ConsumerComunication constructor
        """

        if comunication == self.SIMPLE:
            self.strategy = Simple()
        elif comunication == self.PUBSUB:
            self.strategy = PubSub()
        else:
            raise NameError('Communication type not found')

    def send(self, message, queue):
        self.strategy.send(message, queue)
