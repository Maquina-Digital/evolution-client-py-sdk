import pytest
from evolution_client import WebhookHandler, MessageUpsertEvent, MessageUpdateEvent

def test_webhook_handler_routing():
    handler = WebhookHandler()
    received_events = []

    @handler.on("messages.upsert")
    def on_message(event: MessageUpsertEvent):
        received_events.append(event)

    payload = {
        "event": "messages.upsert",
        "instance": "test_instance",
        "data": {
            "key": {"remoteJid": "123@s.whatsapp.net", "id": "ABC"},
            "message": {"conversation": "Hello"},
            "messageType": "conversation",
            "messageTimestamp": 1600000000,
            "pushName": "Test User"
        }
    }

    event = handler.handle(payload)
    
    assert isinstance(event, MessageUpsertEvent)
    assert len(received_events) == 1
    assert received_events[0].data.pushName == "Test User"

def test_webhook_handler_unknown_event():
    handler = WebhookHandler()
    payload = {
        "event": "unknown.event",
        "instance": "test",
        "data": {}
    }
    event = handler.handle(payload)
    assert event.event == "unknown.event"

def test_webhook_handler_missing_event_field():
    handler = WebhookHandler()
    payload = {"foo": "bar"}
    event = handler.handle(payload)
    assert event is None
