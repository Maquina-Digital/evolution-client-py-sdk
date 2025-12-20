import json
from typing import Optional, Dict, Any, Callable, Type
from loguru import logger
from pydantic import ValidationError
from .models.webhooks import (
    WebhookEvent,
    MessageUpsertEvent,
    MessageUpdateEvent,
    ConnectionUpdateEvent,
    QrCodeEvent,
    WebhookBase,
    RawWebhookPayload
)
from .webhook import verify_signature

class WebhookHandler:
    """
    Handler for processing incoming Evolution API webhooks.
    
    This handler is resilient to malformed payloads:
    - It NEVER raises ValidationError to consumers
    - It NEVER returns None
    - On parse failure, it returns RawWebhookPayload with original data
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

    def handle(self, payload: Dict[str, Any], signature: Optional[str] = None) -> WebhookEvent:
        """
        Process a webhook payload.
        
        This method is guaranteed to:
        - NEVER raise ValidationError
        - NEVER return None
        - Always return either a parsed event model OR RawWebhookPayload
        
        Args:
            payload: The webhook payload as a dictionary
            signature: Optional HMAC signature for verification
            
        Returns:
            WebhookEvent: Either a known parsed model or RawWebhookPayload fallback
        """
        # 1. Verify Signature (if secret is set)
        if self.secret:
            # Note: Signature verification usually requires raw bytes body.
            # Here we assume the caller handles that check before passing the dict,
            # OR we might need to change this signature to accept raw bytes.
            pass

        # 2. Parse Model (tolerant - never raises, never returns None)
        event_obj = self._parse_event(payload)

        # 3. Dispatch to registered handlers
        event_type = payload.get("event")
        if event_type:
            handler = self._handlers.get(event_type)
            if handler:
                try:
                    handler(event_obj)
                except Exception as e:
                    logger.error(f"Error in webhook handler for '{event_type}': {e}")
        
        return event_obj

    def _parse_event(self, payload: Dict[str, Any]) -> WebhookEvent:
        """
        Parse payload into appropriate event model.
        
        This method implements a tolerant parsing strategy:
        1. Try to parse into the strict, known event model
        2. If that fails, try WebhookBase for unknown but valid events
        3. If all parsing fails, return RawWebhookPayload
        
        This method NEVER raises and NEVER returns None.
        """
        event_type = payload.get("event")
        
        # Try strict parsing based on event type
        try:
            if event_type == "messages.upsert":
                return MessageUpsertEvent(**payload)
            elif event_type == "messages.update":
                return MessageUpdateEvent(**payload)
            elif event_type == "connection.update":
                return ConnectionUpdateEvent(**payload)
            elif event_type == "qrcode.updated":
                return QrCodeEvent(**payload)
            
            # Unknown event type - try WebhookBase
            return WebhookBase(**payload)
            
        except ValidationError as e:
            logger.warning(f"Payload validation failed for event '{event_type}': {e}")
            # Safely extract event_type as string (may be non-string in malformed payloads)
            safe_event_type = str(event_type) if event_type is not None else None
            return RawWebhookPayload(
                raw_payload=payload,
                event_type=safe_event_type,
                parse_error=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error parsing event '{event_type}': {e}")
            safe_event_type = str(event_type) if event_type is not None else None
            return RawWebhookPayload(
                raw_payload=payload,
                event_type=safe_event_type,
                parse_error=str(e)
            )


