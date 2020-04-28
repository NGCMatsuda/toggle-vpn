from unittest.mock import Mock, call

from shared.messaging.delayed_messaging import queue_message, deliver_queued_messages, messages
from shared.messaging.publisher import Publisher


def test_queue_message():
    messages_list = [
        ('exchange1', 'routing-key1', 'message1', dict(tenant_id=1)),
        ('exchange2', 'routing-key2', 'message2', dict(tenant_id=2)),
        ('exchange3', 'routing-key3', 'message3', dict(tenant_id=3))
    ]

    for (exchange, routing_key, message, extra) in messages_list:
        queue_message(exchange, routing_key, message, **extra)

    assert messages.queue == messages_list


def test_deliver_queued_messages(mocker):
    messages.queue = [
        ('exchange1', 'routing-key1', 'message1', dict(tenant_id=1)),
        ('exchange2', 'routing-key2', 'message2', dict(tenant_id=2)),
    ]

    publish_ = mocker.patch.object(Publisher, 'publish')
    deliver_queued_messages(Mock())

    publish_.assert_has_calls([
        call('exchange1', 'routing-key1', 'message1', tenant_id=1),
        call('exchange2', 'routing-key2', 'message2', tenant_id=2)
    ])

    assert messages.queue == []


def test_deliver_queued_messages_exception_on_broadcast(mocker):
    messages.queue = [
        ('exchange1', 'routing-key2', 'message1', dict(tenant_id=1)),
        ('exchange2', 'routing-key3', 'message2', dict(tenant_id=2)),
    ]

    publish_ = mocker.patch.object(Publisher, 'publish')
    publish_.side_effect = Exception('Cannot broadcast!')
    deliver_queued_messages(Mock())

    publish_.assert_has_calls([
        call('exchange1', 'routing-key2', 'message1', tenant_id=1),
        call('exchange2', 'routing-key3', 'message2', tenant_id=2)
    ])

    assert messages.queue == []
