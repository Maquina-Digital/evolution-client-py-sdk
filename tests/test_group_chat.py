import unittest
import respx
from httpx import Response
from evolution_client import AsyncEvolutionClient

class TestGroupChatManagement(unittest.IsolatedAsyncioTestCase):
    async def test_group_create(self):
        async with respx.mock:
            respx.post("https://api.example.com/group/create/default").mock(
                return_value=Response(200, json={"status": "created", "gid": "123@g.us"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.group_create(subject="Test Group", participants=["123", "456"])
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.json()["gid"], "123@g.us")

    async def test_group_update_picture(self):
        async with respx.mock:
            respx.post("https://api.example.com/group/updateProfilePicture/default").mock(
                return_value=Response(200, json={"status": "updated"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.group_update_picture(group_jid="123@g.us", image_url="http://img.png")
                self.assertEqual(resp.status_code, 200)

    async def test_group_fetch_all(self):
        async with respx.mock:
            respx.get("https://api.example.com/group/fetchAllGroups/default").mock(
                return_value=Response(200, json=[{"id": "123@g.us", "subject": "Test"}])
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.group_fetch_all()
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(len(resp.json()), 1)

    async def test_group_participants_update(self):
        async with respx.mock:
            respx.post("https://api.example.com/group/updateParticipant/default").mock(
                return_value=Response(200, json={"status": "success"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.group_participants_update(group_jid="123@g.us", action="add", participants=["789"])
                self.assertEqual(resp.status_code, 200)

    async def test_chat_archive(self):
        async with respx.mock:
            respx.post("https://api.example.com/chat/archiveChat/default").mock(
                return_value=Response(200, json={"status": "archived"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.chat_archive(number="12345", archive=True)
                self.assertEqual(resp.status_code, 200)

    async def test_chat_mark_read(self):
        async with respx.mock:
            respx.post("https://api.example.com/chat/markMessageAsRead/default").mock(
                return_value=Response(200, json={"status": "read"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.chat_mark_read(number="12345", read=True)
                self.assertEqual(resp.status_code, 200)

    async def test_chat_mark_unread(self):
        async with respx.mock:
            respx.post("https://api.example.com/chat/markMessageAsUnread/default").mock(
                return_value=Response(200, json={"status": "unread"})
            )
            async with AsyncEvolutionClient("https://api.example.com", "default", "key") as client:
                resp = await client.chat_mark_read(number="12345", read=False)
                self.assertEqual(resp.status_code, 200)
