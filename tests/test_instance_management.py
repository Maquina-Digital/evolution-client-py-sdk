import unittest
import respx
from httpx import Response
from evolution_client import AsyncEvolutionClient

class TestInstanceManagement(unittest.IsolatedAsyncioTestCase):
    async def test_create_instance(self):
        async with respx.mock:
            respx.post("https://api.example.com/instance/create").mock(
                return_value=Response(201, json={"instance": {"instanceName": "new_instance"}, "hash": "123"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.create_instance(instance_name="new_instance")
                self.assertEqual(resp.status_code, 201)
                self.assertEqual(resp.json()["instance"]["instanceName"], "new_instance")

    async def test_connect_instance(self):
        async with respx.mock:
            respx.get("https://api.example.com/instance/connect/my_instance").mock(
                return_value=Response(200, json={"base64": "QR_CODE_DATA"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.connect_instance(instance_name="my_instance")
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.json()["base64"], "QR_CODE_DATA")

    async def test_logout_instance(self):
        async with respx.mock:
            respx.delete("https://api.example.com/instance/logout/my_instance").mock(
                return_value=Response(200, json={"status": "logged_out"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.logout_instance(instance_name="my_instance")
                self.assertEqual(resp.status_code, 200)

    async def test_delete_instance(self):
        async with respx.mock:
            respx.delete("https://api.example.com/instance/delete/my_instance").mock(
                return_value=Response(200, json={"status": "deleted"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.delete_instance(instance_name="my_instance")
                self.assertEqual(resp.status_code, 200)

    async def test_fetch_instances(self):
        async with respx.mock:
            respx.get("https://api.example.com/instance/fetchInstances").mock(
                return_value=Response(200, json=[{"instance": {"instanceName": "inst1"}}])
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.fetch_instances()
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(len(resp.json()), 1)
