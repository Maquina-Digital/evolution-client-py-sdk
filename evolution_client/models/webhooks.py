from typing import List, Optional, Any, Dict, Literal, Union
from pydantic import BaseModel, Field

# --- Base Models ---

class WebhookBase(BaseModel):
    """Base class for all webhook payloads."""
    event: str
    instance: str
    data: Dict[str, Any]
    sender: Optional[str] = None  # Derived field, not always in raw payload

class MessageData(BaseModel):
    """Common data structure for message events."""
    key: Dict[str, Any]
    pushName: Optional[str] = None
    message: Dict[str, Any]
    messageType: str
    messageTimestamp: Union[int, str]
    owner: Optional[bool] = False
    source: Optional[str] = None


class RawWebhookPayload(BaseModel):
    """
    Fallback container for webhook payloads that fail strict validation.
    
    This is returned by the SDK when external payloads cannot be parsed
    into known event models. It preserves the original data for consumer
    inspection while preventing ValidationError from propagating.
    """
    model_config = {"extra": "allow"}
    
    raw_payload: Dict[str, Any]
    event_type: Optional[str] = None
    parse_error: str


# --- Specific Event Models ---

class MessageUpsertEvent(WebhookBase):
    """
    Event: messages.upsert
    Triggered when a new message is received.
    """
    event: Literal["messages.upsert"]
    data: MessageData

class MessageUpdateEvent(WebhookBase):
    """
    Event: messages.update
    Triggered when a message status changes (delivered, read, etc).
    """
    event: Literal["messages.update"]
    data: Dict[str, Any]  # Structure varies significantly for updates

class ConnectionUpdateEvent(WebhookBase):
    """
    Event: connection.update
    Triggered when instance connection state changes.
    """
    event: Literal["connection.update"]
    data: Dict[str, Any]  # e.g. {'state': 'open', 'statusReason': 200}

class QrCodeEvent(WebhookBase):
    """
    Event: qrcode.updated
    Triggered when a new QR code is generated for scanning.
    """
    event: Literal["qrcode.updated"]
    data: Dict[str, Any]  # e.g. {'qrcode': '...', 'pairingCode': '...'}

# --- Union Type ---

WebhookEvent = Union[
    MessageUpsertEvent,
    MessageUpdateEvent,
    ConnectionUpdateEvent,
    QrCodeEvent,
    WebhookBase,  # Fallback for unknown but valid events
    RawWebhookPayload,  # Fallback for unparseable payloads
]

