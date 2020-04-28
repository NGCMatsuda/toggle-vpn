import logging

from shared.messaging.delayed_messaging import deliver_queued_messages


def broadcast_messages_after_request(app, config):
    @app.teardown_request
    def _deliver_queued_messages(response_or_exception):
        try:
            deliver_queued_messages(config)
        except Exception as exception:
            logging.exception(exception)

        return response_or_exception
