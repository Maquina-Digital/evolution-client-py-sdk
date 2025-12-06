"""
import pytest
import respx
from httpx import Response
from evolution_client import AsyncEvolutionClient, AsyncMessagingService, TextMessage

@pytest.mark.asyncio
async def test_async_client_send_text():
    async with respx.mock:
        route = respx.post("https://api.example.com/message/sendText/test_instance").mock(
            return_value=Response(200, json={"status": "PENDING"})
        )

        async with AsyncEvolutionClient(
            base_url="https://api.example.com",
            instance="test_instance",
            api_key="secret"
        ) as client:
            resp = await client.send_text(number="12345", text="Hello")
            assert resp.status_code == 200
            assert route.called

@pytest.mark.asyncio
async def test_async_service_send_text():
    async with respx.mock:
        respx.post("https://api.example.com/message/sendText/test_instance").mock(
            return_value=Response(200, json={"status": "PENDING"})
        )

        async with AsyncEvolutionClient(
            base_url="https://api.example.com",
            instance="test_instance",
            api_key="secret"
        ) as client:
            service = AsyncMessagingService(client)
            status, body = await service.send(TextMessage(number="12345", text="Hello"))
            assert status == 200
"""
