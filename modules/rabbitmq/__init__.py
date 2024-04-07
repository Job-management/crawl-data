import pika


class RabbitMQChannel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="localhost")
            )
            cls._instance._channel = cls._instance._connection.channel()
            cls._instance._channel.queue_declare(queue="raw-data")
        return cls._instance

    @property
    def getChannel(self):
        return self._channel

    def publishMessage(self, message, rk="", ex=""):
        self._channel.basic_publish(exchange=ex, routing_key=rk, body=message)

    def close_connection(self):
        self._channel.close()
        self._connection.close()
