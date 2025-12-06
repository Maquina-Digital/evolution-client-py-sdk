import pytest
import respx
from httpx import Response
from evolution_client import (
    AsyncEvolutionClient, AsyncMessagingService,
    AudioMessage, StickerMessage, LocationMessage, ListMessage, ReactionMessage,
    ListSection, ListRow
)

@pytest.mark.asyncio
async def test_send_audio():
    async with respx.mock:
        respx.post("https://api.example.com/message/sendWhatsAppAudio/test_instance").mock(
            return_value=Response(200, json={"status": "PENDING"})
        )
        async with AsyncEvolutionClient("https://api.example.com", "test_instance", "key") as client:
            service = AsyncMessagingService(client)
            status, _ = await service.send(AudioMessage(number="12345", url="http://audio.mp3"))
            assert status == 200

@pytest.mark.asyncio
async def test_send_sticker():
    async with respx.mock:
        respx.post("https://api.example.com/message/sendSticker/test_instance").mock(
            return_value=Response(200, json={"status": "PENDING"})
        )
        async with AsyncEvolutionClient("https://api.example.com", "test_instance", "key") as client:
            service = AsyncMessagingService(client)
            status, _ = await service.send(StickerMessage(number="12345", url="http://sticker.webp"))
            assert status == 200

@pytest.mark.asyncio
async def test_send_location():
    async with respx.mock:
        respx.post("https://api.example.com/message/sendLocation/test_instance").mock(
            return_value=Response(200, json={"status": "PENDING"})
        )
        async with AsyncEvolutionClient("https://api.example.com", "test_instance", "key") as client:
            service = AsyncMessagingService(client)
            msg = LocationMessage(number="12345", latitude=10.0, longitude=20.0, name="Home")
            status, _ = await service.send(msg)
            assert status == 200

@pytest.mark.asyncio
async def test_send_reaction():
    async with respx.mock:
        respx.post("https://api.example.com/message/sendReaction/test_instance").mock(
            return_value=Response(200, json={"status": "PENDING"})
        )
        async with AsyncEvolutionClient("https://api.example.com", "test_instance", "key") as client:
            service = AsyncMessagingService(client)
            msg = ReactionMessage(number="12345", key={"id": "MSGID"}, reaction="👍")
            status, _ = await service.send(msg)
            assert status == 200

@pytest.mark.asyncio
async def test_send_list():
    async with respx.mock:
        respx.post("https://api.example.com/message/sendList/test_instance").mock(
            return_value=Response(200, json={"status": "PENDING"})
        )
        async with AsyncEvolutionClient("https://api.example.com", "test_instance", "key") as client:
            service = AsyncMessagingService(client)
            sections = [ListSection(title="Sec1", rows=[ListRow(title="Row1", rowId="id1")])]
            msg = ListMessage(number="12345", title="Menu", buttonText="Click", sections=sections)
            status, _ = await service.send(msg)
            assert status == 200
