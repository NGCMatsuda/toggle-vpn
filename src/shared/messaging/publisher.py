import logging

import pika
from pika import PlainCredentials, BlockingConnection, ConnectionParameters
from pika.spec import PERSISTENT_DELIVERY_MODE


def prefix_params(params, prefix='meta'):
    return {f'{prefix}-{key}':value for key, value in params.items()}


class Publisher:
    def __init__(self, config):
        self.config = config

    def publish(self, exchange, routing_key, message, **extra):
        connection = self.__connect()
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, durable=True, exchange_type='topic')
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=str(message),
            properties=pika.BasicProperties(headers=prefix_params(extra), delivery_mode=PERSISTENT_DELIVERY_MODE)
        )
        connection.close()

        logging.info(f'Message sent to RabbitMQ to {exchange} exchange: {message}')

    def __connect(self):
        credentials = PlainCredentials(username=self.config.username, password=self.config.password)
        connection_parameters = ConnectionParameters(host=self.config.host, credentials=credentials)
        return BlockingConnection(connection_parameters)
