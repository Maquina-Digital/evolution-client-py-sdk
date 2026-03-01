"""Comprehensive tests for ALL async client methods — new and existing."""
import unittest
import respx
from httpx import Response
from evolution_client import AsyncEvolutionClient


BASE = "https://api.example.com"
INST = "default"


class TestSendMessages(unittest.IsolatedAsyncioTestCase):
    """Tests for all send_* methods."""

    async def test_send_contact(self):
        async with respx.mock:
            respx.post(f"{BASE}/message/sendContact/{INST}").mock(
                return_value=Response(200, json={"status": "sent"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.send_contact(
                    number="5511999999999", contact_name="Alice", contact_number="5511888888888"
                )
                self.assertEqual(resp.status_code, 200)

    async def test_send_ptv(self):
        async with respx.mock:
            respx.post(f"{BASE}/message/sendPtv/{INST}").mock(
                return_value=Response(200, json={"status": "sent"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.send_ptv(number="5511999999999", ptv="https://video.mp4")
                self.assertEqual(resp.status_code, 200)

    async def test_send_status(self):
        async with respx.mock:
            respx.post(f"{BASE}/message/sendStatus/{INST}").mock(
                return_value=Response(200, json={"status": "posted"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.send_status(type="text", content="Hello world!")
                self.assertEqual(resp.status_code, 200)


class TestCallEndpoint(unittest.IsolatedAsyncioTestCase):
    async def test_send_fake_call(self):
        async with respx.mock:
            respx.post(f"{BASE}/call/offer/{INST}").mock(
                return_value=Response(200, json={"status": "offered"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.send_fake_call(number="5511999999999")
                self.assertEqual(resp.status_code, 200)


class TestInstanceExtended(unittest.IsolatedAsyncioTestCase):
    async def test_restart_instance(self):
        async with respx.mock:
            respx.put(f"{BASE}/instance/restart/{INST}").mock(
                return_value=Response(200, json={"status": "restarted"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.restart_instance()
                self.assertEqual(resp.status_code, 200)

    async def test_set_presence(self):
        async with respx.mock:
            respx.post(f"{BASE}/instance/setPresence/{INST}").mock(
                return_value=Response(200, json={"status": "available"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.set_presence(presence="available")
                self.assertEqual(resp.status_code, 200)

    async def test_get_instance_status(self):
        async with respx.mock:
            respx.get(f"{BASE}/instance/connectionState/{INST}").mock(
                return_value=Response(200, json={"state": "open"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.get_instance_status()
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.json()["state"], "open")


class TestProxy(unittest.IsolatedAsyncioTestCase):
    async def test_set_proxy(self):
        async with respx.mock:
            respx.post(f"{BASE}/proxy/set/{INST}").mock(
                return_value=Response(200, json={"status": "set"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.set_proxy(proxy_url="http://proxy:8080")
                self.assertEqual(resp.status_code, 200)

    async def test_find_proxy(self):
        async with respx.mock:
            respx.get(f"{BASE}/proxy/find/{INST}").mock(
                return_value=Response(200, json={"proxy": "http://proxy:8080"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_proxy()
                self.assertEqual(resp.status_code, 200)


class TestSettings(unittest.IsolatedAsyncioTestCase):
    async def test_set_settings(self):
        async with respx.mock:
            respx.post(f"{BASE}/settings/set/{INST}").mock(
                return_value=Response(200, json={"status": "ok"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.set_settings(settings={"rejectCall": True})
                self.assertEqual(resp.status_code, 200)

    async def test_find_settings(self):
        async with respx.mock:
            respx.get(f"{BASE}/settings/find/{INST}").mock(
                return_value=Response(200, json={"rejectCall": True})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_settings()
                self.assertEqual(resp.status_code, 200)


class TestChatExtended(unittest.IsolatedAsyncioTestCase):
    async def test_check_wa_number(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/whatsappNumbers/{INST}").mock(
                return_value=Response(200, json=[{"exists": True, "jid": "5511@s.whatsapp.net"}])
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.check_wa_number(numbers=["5511999999999"])
                self.assertEqual(resp.status_code, 200)

    async def test_delete_chat(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/deleteMessage/{INST}").mock(
                return_value=Response(200, json={"status": "deleted"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.delete_chat(number="5511999999999")
                self.assertEqual(resp.status_code, 200)

    async def test_fetch_profile_picture_url(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/fetchProfilePictureUrl/{INST}").mock(
                return_value=Response(200, json={"profilePictureUrl": "https://img.jpg"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.fetch_profile_picture_url(number="5511999999999")
                self.assertEqual(resp.status_code, 200)
                self.assertIn("profilePictureUrl", resp.json())

    async def test_get_base64_media(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/getBase64FromMediaMessage/{INST}").mock(
                return_value=Response(200, json={"base64": "iVBOR..."})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.get_base64_media(message_id="msg123")
                self.assertEqual(resp.status_code, 200)

    async def test_update_message(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/updateMessage/{INST}").mock(
                return_value=Response(200, json={"status": "updated"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.update_message(number="5511999999999", message_id="msg123", text="edited")
                self.assertEqual(resp.status_code, 200)

    async def test_set_chat_presence(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/presence/{INST}").mock(
                return_value=Response(200, json={"status": "composing"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.set_chat_presence(number="5511999999999", presence="composing")
                self.assertEqual(resp.status_code, 200)

    async def test_block_contact(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/blockContact/{INST}").mock(
                return_value=Response(200, json={"status": "blocked"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.block_contact(number="5511999999999", status="block")
                self.assertEqual(resp.status_code, 200)

    async def test_find_contacts(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/findContacts/{INST}").mock(
                return_value=Response(200, json=[{"id": "5511@s.whatsapp.net"}])
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_contacts()
                self.assertEqual(resp.status_code, 200)

    async def test_find_messages(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/findMessages/{INST}").mock(
                return_value=Response(200, json=[{"id": "msg1"}])
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_messages(where={"key": {"remoteJid": "5511@s.whatsapp.net"}})
                self.assertEqual(resp.status_code, 200)


class TestLabel(unittest.IsolatedAsyncioTestCase):
    async def test_label_find(self):
        async with respx.mock:
            respx.get(f"{BASE}/label/findLabels/{INST}").mock(
                return_value=Response(200, json=[{"id": "1", "name": "Urgent"}])
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.label_find()
                self.assertEqual(resp.status_code, 200)

    async def test_label_handle(self):
        async with respx.mock:
            respx.post(f"{BASE}/label/handleLabel/{INST}").mock(
                return_value=Response(200, json={"status": "added"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.label_handle(number="5511999999999", label_id="1", action="add")
                self.assertEqual(resp.status_code, 200)


class TestProfileExtended(unittest.IsolatedAsyncioTestCase):
    async def test_profile_fetch_business(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/fetchBusinessProfile/{INST}").mock(
                return_value=Response(200, json={"wid": "5511@s.whatsapp.net"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.profile_fetch_business(number="5511999999999")
                self.assertEqual(resp.status_code, 200)

    async def test_profile_fetch(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/fetchProfile/{INST}").mock(
                return_value=Response(200, json={"name": "Jonas"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.profile_fetch(number="5511999999999")
                self.assertEqual(resp.status_code, 200)

    async def test_profile_update_picture(self):
        async with respx.mock:
            respx.post(f"{BASE}/profile/updateProfilePicture/{INST}").mock(
                return_value=Response(200, json={"status": "updated"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.profile_update_picture(picture="https://img.jpg")
                self.assertEqual(resp.status_code, 200)

    async def test_profile_update_privacy(self):
        async with respx.mock:
            respx.post(f"{BASE}/profile/updatePrivacySettings/{INST}").mock(
                return_value=Response(200, json={"status": "updated"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.profile_update_privacy(settings={"readreceipts": "all"})
                self.assertEqual(resp.status_code, 200)


class TestGroupExtended(unittest.IsolatedAsyncioTestCase):
    async def test_group_update_subject(self):
        async with respx.mock:
            respx.post(f"{BASE}/group/updateSubject/{INST}").mock(
                return_value=Response(200, json={"status": "updated"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_update_subject(group_jid="123@g.us", subject="New Subject")
                self.assertEqual(resp.status_code, 200)

    async def test_group_update_description(self):
        async with respx.mock:
            respx.post(f"{BASE}/group/updateDescription/{INST}").mock(
                return_value=Response(200, json={"status": "updated"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_update_description(group_jid="123@g.us", description="New Desc")
                self.assertEqual(resp.status_code, 200)

    async def test_group_find_infos(self):
        async with respx.mock:
            respx.get(f"{BASE}/group/findGroupInfos/{INST}").mock(
                return_value=Response(200, json=[{"id": "123@g.us", "subject": "Test"}])
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_find_infos(group_jid="123@g.us")
                self.assertEqual(resp.status_code, 200)

    async def test_group_get_participants(self):
        async with respx.mock:
            respx.get(f"{BASE}/group/participants/{INST}").mock(
                return_value=Response(200, json=[{"id": "5511@s.whatsapp.net"}])
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_get_participants(group_jid="123@g.us")
                self.assertEqual(resp.status_code, 200)

    async def test_group_get_invite_code(self):
        async with respx.mock:
            respx.get(f"{BASE}/group/inviteCode/{INST}").mock(
                return_value=Response(200, json={"inviteCode": "ABCDEF"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_get_invite_code(group_jid="123@g.us")
                self.assertEqual(resp.status_code, 200)

    async def test_group_revoke_invite(self):
        async with respx.mock:
            respx.post(f"{BASE}/group/revokeInviteCode/{INST}").mock(
                return_value=Response(200, json={"status": "revoked"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_revoke_invite(group_jid="123@g.us")
                self.assertEqual(resp.status_code, 200)

    async def test_group_send_invite(self):
        async with respx.mock:
            respx.post(f"{BASE}/group/sendInvite/{INST}").mock(
                return_value=Response(200, json={"status": "sent"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_send_invite(group_jid="123@g.us", numbers=["5511999999999"])
                self.assertEqual(resp.status_code, 200)

    async def test_group_update_settings(self):
        async with respx.mock:
            respx.post(f"{BASE}/group/updateSetting/{INST}").mock(
                return_value=Response(200, json={"status": "updated"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_update_settings(group_jid="123@g.us", action="announcement")
                self.assertEqual(resp.status_code, 200)

    async def test_group_toggle_ephemeral(self):
        async with respx.mock:
            respx.post(f"{BASE}/group/toggleEphemeral/{INST}").mock(
                return_value=Response(200, json={"status": "enabled"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_toggle_ephemeral(group_jid="123@g.us", expiration=86400)
                self.assertEqual(resp.status_code, 200)

    async def test_group_leave(self):
        async with respx.mock:
            respx.delete(f"{BASE}/group/leaveGroup/{INST}").mock(
                return_value=Response(200, json={"status": "left"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_leave(group_jid="123@g.us")
                self.assertEqual(resp.status_code, 200)


class TestIntegrationsEvents(unittest.IsolatedAsyncioTestCase):
    async def test_set_webhook(self):
        async with respx.mock:
            respx.post(f"{BASE}/webhook/set/{INST}").mock(
                return_value=Response(200, json={"status": "set"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.set_webhook(url="https://hook.example.com")
                self.assertEqual(resp.status_code, 200)

    async def test_find_webhook(self):
        async with respx.mock:
            respx.get(f"{BASE}/webhook/find/{INST}").mock(
                return_value=Response(200, json={"url": "https://hook.example.com"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_webhook()
                self.assertEqual(resp.status_code, 200)

    async def test_set_websocket(self):
        async with respx.mock:
            respx.post(f"{BASE}/websocket/set/{INST}").mock(
                return_value=Response(200, json={"status": "set"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.set_websocket(enabled=True)
                self.assertEqual(resp.status_code, 200)

    async def test_find_websocket(self):
        async with respx.mock:
            respx.get(f"{BASE}/websocket/find/{INST}").mock(
                return_value=Response(200, json={"enabled": True})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_websocket()
                self.assertEqual(resp.status_code, 200)

    async def test_set_rabbitmq(self):
        async with respx.mock:
            respx.post(f"{BASE}/rabbitmq/set/{INST}").mock(
                return_value=Response(200, json={"status": "set"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.set_rabbitmq(enabled=True, events=["messages.upsert"])
                self.assertEqual(resp.status_code, 200)

    async def test_find_rabbitmq(self):
        async with respx.mock:
            respx.get(f"{BASE}/rabbitmq/find/{INST}").mock(
                return_value=Response(200, json={"enabled": True})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_rabbitmq()
                self.assertEqual(resp.status_code, 200)

    async def test_set_and_find_sqs(self):
        async with respx.mock:
            respx.post(f"{BASE}/sqs/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/sqs/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_sqs(enabled=True)
                r2 = await c.find_sqs()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)

    async def test_set_and_find_nats(self):
        async with respx.mock:
            respx.post(f"{BASE}/nats/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/nats/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_nats(enabled=True)
                r2 = await c.find_nats()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)

    async def test_set_and_find_pusher(self):
        async with respx.mock:
            respx.post(f"{BASE}/pusher/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/pusher/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_pusher(enabled=True)
                r2 = await c.find_pusher()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)


class TestIntegrationsChatbot(unittest.IsolatedAsyncioTestCase):
    async def test_set_and_find_chatwoot(self):
        async with respx.mock:
            respx.post(f"{BASE}/chatwoot/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/chatwoot/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_chatwoot(settings={"enabled": True})
                r2 = await c.find_chatwoot()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)

    async def test_set_and_find_typebot(self):
        async with respx.mock:
            respx.post(f"{BASE}/typebot/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/typebot/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_typebot(settings={"enabled": True})
                r2 = await c.find_typebot()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)

    async def test_set_and_find_openai(self):
        async with respx.mock:
            respx.post(f"{BASE}/openai/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/openai/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_openai(settings={"apiKey": "sk-..."})
                r2 = await c.find_openai()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)

    async def test_set_and_find_dify(self):
        async with respx.mock:
            respx.post(f"{BASE}/dify/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/dify/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_dify(settings={"enabled": True})
                r2 = await c.find_dify()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)

    async def test_set_and_find_flowise(self):
        async with respx.mock:
            respx.post(f"{BASE}/flowise/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/flowise/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_flowise(settings={"enabled": True})
                r2 = await c.find_flowise()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)

    async def test_set_and_find_n8n(self):
        async with respx.mock:
            respx.post(f"{BASE}/n8n/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/n8n/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_n8n(settings={"enabled": True})
                r2 = await c.find_n8n()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)


class TestIntegrationsChannel(unittest.IsolatedAsyncioTestCase):
    async def test_set_and_find_evolution_channel(self):
        async with respx.mock:
            respx.post(f"{BASE}/channel/evolution/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/channel/evolution/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_evolution_channel(settings={"enabled": True})
                r2 = await c.find_evolution_channel()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)

    async def test_set_and_find_cloud_api(self):
        async with respx.mock:
            respx.post(f"{BASE}/channel/cloudApi/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/channel/cloudApi/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_cloud_api(settings={"token": "tok"})
                r2 = await c.find_cloud_api()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)


class TestStorage(unittest.IsolatedAsyncioTestCase):
    async def test_set_and_find_s3(self):
        async with respx.mock:
            respx.post(f"{BASE}/s3/set/{INST}").mock(return_value=Response(200, json={}))
            respx.get(f"{BASE}/s3/find/{INST}").mock(return_value=Response(200, json={}))
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                r1 = await c.set_s3(settings={"bucket": "my-bucket"})
                r2 = await c.find_s3()
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)


class TestConstructorPropertiesExposed(unittest.IsolatedAsyncioTestCase):
    """Verify the structural fix: constructor params are accessible as attributes."""

    async def test_properties_exposed(self):
        async with AsyncEvolutionClient("https://api.example.com", "inst1", "my-key", timeout=30, verify_ssl=False) as c:
            self.assertEqual(c.base_url, "https://api.example.com")
            self.assertEqual(c.base, "https://api.example.com")
            self.assertEqual(c.instance, "inst1")
            self.assertEqual(c.api_key, "my-key")
            self.assertEqual(c.timeout, 30)
            self.assertEqual(c.verify_ssl, False)


class TestNewMissingEndpoints(unittest.IsolatedAsyncioTestCase):
    """Tests for endpoints discovered during second cross-check."""

    async def test_delete_message_for_everyone(self):
        async with respx.mock:
            respx.delete(f"{BASE}/chat/deleteMessageForEveryone/{INST}").mock(
                return_value=Response(200, json={"status": "deleted"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.delete_message_for_everyone(message_id="msg1", remote_jid="5511@s.whatsapp.net")
                self.assertEqual(resp.status_code, 200)

    async def test_find_status_message(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/findStatusMessage/{INST}").mock(
                return_value=Response(200, json=[{"id": "status1"}])
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_status_message()
                self.assertEqual(resp.status_code, 200)

    async def test_find_chats(self):
        async with respx.mock:
            respx.post(f"{BASE}/chat/findChats/{INST}").mock(
                return_value=Response(200, json=[{"id": "chat1"}])
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.find_chats()
                self.assertEqual(resp.status_code, 200)

    async def test_profile_remove_picture(self):
        async with respx.mock:
            respx.delete(f"{BASE}/profile/removeProfilePicture/{INST}").mock(
                return_value=Response(200, json={"status": "removed"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.profile_remove_picture()
                self.assertEqual(resp.status_code, 200)

    async def test_profile_fetch_privacy(self):
        async with respx.mock:
            respx.get(f"{BASE}/profile/fetchPrivacySettings/{INST}").mock(
                return_value=Response(200, json={"readreceipts": "all"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.profile_fetch_privacy()
                self.assertEqual(resp.status_code, 200)

    async def test_group_find_by_invite_code(self):
        async with respx.mock:
            respx.get(f"{BASE}/group/inviteInfo/{INST}").mock(
                return_value=Response(200, json={"id": "123@g.us", "subject": "Group"})
            )
            async with AsyncEvolutionClient(BASE, INST, "key") as c:
                resp = await c.group_find_by_invite_code(invite_code="ABCDEF")
                self.assertEqual(resp.status_code, 200)
