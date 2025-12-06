import uuid
from typing import Tuple
from loguru import logger
from .async_client import AsyncEvolutionClient
from .models import (
    Message, TextMessage, ButtonsMessage, PollMessage, MediaMessage,
    AudioMessage, StickerMessage, LocationMessage, ListMessage, ReactionMessage
)

class AsyncMessagingService:
    """
    High-level facade that routes typed messages to specific client calls (Async).
    """
    def __init__(self, client: AsyncEvolutionClient) -> None:
        self.client = client

    async def send(self, message: Message, idempotency_key: str | None = None) -> Tuple[int, str]:
        correlation_id = uuid.uuid4().hex[:16]
        logger.bind(correlation_id=correlation_id).info(f"Sending {message.type} to {message.number}")
        if isinstance(message, TextMessage):
            resp = await self.client.send_text(number=message.number, text=message.text, delay=message.delay or 0)
        elif isinstance(message, ButtonsMessage):
            resp = await self.client.send_buttons(
                number=message.number,
                text=message.text,
                buttons=[b.model_dump() for b in message.buttons],
                footer=message.footer,
                delay=message.delay or 0,
            )
        elif isinstance(message, PollMessage):
            resp = await self.client.send_poll(
                number=message.number,
                name=message.name,
                selectableCount=message.selectableCount,
                values=message.values,
                delay=message.delay or 0,
            )
        elif isinstance(message, MediaMessage):
            resp = await self.client.send_media(
                number=message.number,
                url_media=message.url,
                caption=message.caption,
                mime_type=message.mime_type,
                delay=message.delay or 0,
            )
        elif isinstance(message, AudioMessage):
            resp = await self.client.send_audio(
                number=message.number,
                audio=message.url,
                delay=message.delay or 0,
            )
        elif isinstance(message, StickerMessage):
            resp = await self.client.send_sticker(
                number=message.number,
                sticker=message.url,
                delay=message.delay or 0,
            )
        elif isinstance(message, LocationMessage):
            resp = await self.client.send_location(
                number=message.number,
                latitude=message.latitude,
                longitude=message.longitude,
                name=message.name,
                address=message.address,
                delay=message.delay or 0,
            )
        elif isinstance(message, ListMessage):
            resp = await self.client.send_list(
                number=message.number,
                title=message.title,
                button_text=message.buttonText,
                sections=[s.model_dump() for s in message.sections],
                description=message.description,
                footer=message.footer,
                delay=message.delay or 0,
            )
        elif isinstance(message, ReactionMessage):
            resp = await self.client.send_reaction(
                key=message.key,
                reaction=message.reaction,
            )
        else:
            raise ValueError(f"Unsupported message type: {message.type}")
        try:
            body = resp.text
        except Exception:
            body = ""
        return resp.status_code, body
