import decimal
import logging

import simplejson
from pika import PlainCredentials, ConnectionParameters, BlockingConnection

from shared.messaging.metadata import Metadata


def extract_metadata(params, prefix='meta'):
    return Metadata(
        {key.replace(f'{prefix}-', ''): value for key, value in params.items() if key.startswith(f'{prefix}-')}
    )


class Consumer:
    def __init__(self, config, service_name):
        self.config = config
        credentials = PlainCredentials(username=config.username, password=config.password)
        connection_parameters = ConnectionParameters(host=config.host, credentials=credentials)

        self.connection = BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()

        self.service_name = service_name

    def listen(self, topic, routing_key, message_process_fn, on_final_error=None, retry_timeout=3600000):
        self.channel.exchange_declare(topic, exchange_type='topic', durable=True)

        queue_name = f'{self.service_name}:{topic}:{routing_key}'
        retry_queue_name = f'{queue_name}:retry'

        self.channel.queue_declare(
            queue=queue_name,
            durable=True,
            arguments={
                'x-dead-letter-exchange': '',
                'x-dead-letter-routing-key': retry_queue_name
            })

        self.channel.queue_declare(
            queue=retry_queue_name,
            durable=True,
            arguments={
                'x-dead-letter-exchange': '',
                'x-dead-letter-routing-key': queue_name,
                'x-message-ttl': retry_timeout
            }
        )

        self.channel.queue_bind(
            exchange=topic,
            queue=queue_name,
            routing_key=routing_key
        )

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.__wrap_on_message_callback(message_process_fn, on_final_error)
        )

    def start(self):
        self.channel.start_consuming()

    def __wrap_on_message_callback(self, message_process_fn, on_final_error_fn):
        def _(channel, method, properties, body):
            try:
                logging.info(f'Received a message from queue {method.exchange}: {body}')

                body = simplejson.loads(body.decode('utf-8'), parse_float=decimal.Decimal)
                meta = extract_metadata(properties.headers)

                if self.config.retry_count and self.__message_retry_count(properties) > self.config.retry_count:
                    on_final_error_fn(properties, body) if on_final_error_fn else None
                else:
                    message_process_fn(body, meta)

            except Exception as e:
                logging.exception(e)
                channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                return

            channel.basic_ack(delivery_tag=method.delivery_tag)

        return _

    def __message_retry_count(self, message_properties):
        retries = message_properties.headers.get('x-death', [])
        return retries[0]['count'] if len(retries) > 0 else 0
