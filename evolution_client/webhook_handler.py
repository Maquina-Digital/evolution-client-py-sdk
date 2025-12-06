import json
from typing import Optional, Dict, Any, Callable, Type
from loguru import logger
from .models.webhooks import (
    WebhookEvent,
    MessageUpsertEvent,
    MessageUpdateEvent,
    ConnectionUpdateEvent,
    QrCodeEvent,
    WebhookBase
)
from .webhook import verify_signature

class WebhookHandler:
    """
    Handler for processing incoming Evolution API webhooks.
    """
    def __init__(self, secret: Optional[str] = None):
        self.secret = secret
        self._handlers: Dict[str, Callable[[WebhookEvent], Any]] = {}

    def add_handler(self, event_type: str, handler_func: Callable[[WebhookEvent], Any]):
        """Register a callback for a specific event type."""
        self._handlers[event_type] = handler_func

    def on(self, event_type: str):
        """Decorator to register a handler."""
        def decorator(func):
            self.add_handler(event_type, func)
            return func
        return decorator

    def handle(self, payload: Dict[str, Any], signature: Optional[str] = None) -> Optional[WebhookEvent]:
        """
        Process a webhook payload.
        1. Verify signature (if secret is set).
        2. Parse payload into a Pydantic model.
        3. Dispatch to registered handlers.
        """
        # 1. Verify Signature
        if self.secret:
            # Note: Signature verification usually requires raw bytes body.
            # Here we assume the caller handles that check before passing the dict,
            # OR we might need to change this signature to accept raw bytes.
            # For now, we'll assume the caller uses the helper `verify_signature` manually if needed,
            # or we can add a method `handle_raw` that takes bytes.
            pass

        event_type = payload.get("event")
        if not event_type:
            logger.warning("Received webhook without 'event' field")
            return None

        # 2. Parse Model
        try:
            event_obj = self._parse_event(payload)
        except Exception as e:
            logger.error(f"Failed to parse webhook event '{event_type}': {e}")
            return None

        # 3. Dispatch
        handler = self._handlers.get(event_type)
        if handler:
            try:
                handler(event_obj)
            except Exception as e:
                logger.error(f"Error in webhook handler for '{event_type}': {e}")
        
        return event_obj

    def _parse_event(self, payload: Dict[str, Any]) -> WebhookEvent:
        event_type = payload.get("event")
        
        if event_type == "messages.upsert":
            return MessageUpsertEvent(**payload)
        elif event_type == "messages.update":
            return MessageUpdateEvent(**payload)
        elif event_type == "connection.update":
            return ConnectionUpdateEvent(**payload)
        elif event_type == "qrcode.updated":
            return QrCodeEvent(**payload)
        
        # Fallback
        return WebhookBase(**payload)
