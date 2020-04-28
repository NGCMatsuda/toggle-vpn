from unittest.mock import Mock

from shared.messaging import flask_plugins
from shared.messaging.delayed_messaging import deliver_queued_messages
from shared.messaging.flask_plugins import broadcast_messages_after_request
from shared_test.mocker_helper import patch


def test_broadcast_messages_after_request(test_app, mocker):
    deliver_queued_messages_ = patch(mocker, deliver_queued_messages, flask_plugins)

    messaging_mock = Mock()
    broadcast_messages_after_request(test_app, messaging_mock)

    _simulate_request(test_app)

    assert deliver_queued_messages_.call_count == 1


def _simulate_request(test_app):
    ctx = test_app.test_request_context()
    ctx.push()
    ctx.pop()
