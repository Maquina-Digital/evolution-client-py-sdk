
import uuid
from typing import Tuple
from loguru import logger
from .client import EvolutionApiClient
from .models import Message, TextMessage, ButtonsMessage, PollMessage, MediaMessage

class MessagingService:
    """
    High-level facade that routes typed messages to specific client calls.
    You can wrap logging, idempotency and persistence outside this class.
    """
    def __init__(self, client: EvolutionApiClient) -> None:
        self.client = client

    def send(self, message: Message, idempotency_key: str | None = None) -> Tuple[int, str]:
        correlation_id = uuid.uuid4().hex[:16]
        logger.bind(correlation_id=correlation_id).info(f"Sending {message.type} to {message.number}")
        if isinstance(message, TextMessage):
            resp = self.client.send_text(number=message.number, text=message.text, delay=message.delay or 0)
        elif isinstance(message, ButtonsMessage):
            resp = self.client.send_buttons(
                number=message.number,
                text=message.text,
                buttons=[b.dict() for b in message.buttons],
                footer=message.footer,
                delay=message.delay or 0,
            )
        elif isinstance(message, PollMessage):
            resp = self.client.send_poll(
                number=message.number,
                name=message.name,
                selectableCount=message.selectableCount,
                values=message.values,
                delay=message.delay or 0,
            )
        elif isinstance(message, MediaMessage):
            resp = self.client.send_media(
                number=message.number,
                url_media=message.url,
                caption=message.caption,
                mime_type=message.mime_type,
                delay=message.delay or 0,
            )
        else:
            raise ValueError(f"Unsupported message type: {message.type}")
        try:
            body = resp.text
        except Exception:
            body = ""
        return resp.status_code, body
