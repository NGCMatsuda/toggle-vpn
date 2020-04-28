import logging
import threading

from shared.messaging.publisher import Publisher

messages = threading.local()


def queue_message(exchange, routing_key, message, **extra):
    global messages

    if not hasattr(messages, 'queue'):
        messages.queue = []

    messages.queue += [(exchange, routing_key, message, extra)]


def deliver_queued_messages(config):
    global messages

    if not hasattr(messages, 'queue'):
        return

    for (exchange, routing_key, message, extra) in messages.queue:
        try:
            publisher = Publisher(config)
            publisher.publish(exchange, routing_key, message, **extra)
        except Exception:
            logging.exception(f'Message {message} is not broadcasted')

    messages.queue = []
