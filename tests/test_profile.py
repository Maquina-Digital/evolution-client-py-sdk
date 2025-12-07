import unittest
import respx
from httpx import Response
from evolution_client import AsyncEvolutionClient

class TestProfileManagement(unittest.IsolatedAsyncioTestCase):
    async def test_profile_update_name(self):
        async with respx.mock:
            respx.post("https://api.example.com/chat/updateProfileName/default").mock(
                return_value=Response(200, json={"status": "success"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.profile_update_name(name="New Name")
                self.assertEqual(resp.status_code, 200)

    async def test_profile_update_status(self):
        async with respx.mock:
            respx.post("https://api.example.com/chat/updateProfileStatus/default").mock(
                return_value=Response(200, json={"status": "success"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.profile_update_status(status="Available")
                self.assertEqual(resp.status_code, 200)
