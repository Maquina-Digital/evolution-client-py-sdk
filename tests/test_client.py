"""Tests for the sync EvolutionApiClient — structural fixes and new endpoints."""
import unittest
from unittest.mock import patch, MagicMock
from evolution_client import EvolutionApiClient


class TestSyncClientStructural(unittest.TestCase):
    """Verify constructor properties are exposed and HTTP method helpers exist."""

    def test_constructor_properties_exposed(self):
        client = EvolutionApiClient("https://api.example.com", "inst1", "my-key", timeout=30, verify_ssl=False)
        self.assertEqual(client.base_url, "https://api.example.com")
        self.assertEqual(client.base, "https://api.example.com")
        self.assertEqual(client.instance, "inst1")
        self.assertEqual(client.api_key, "my-key")
        self.assertEqual(client.timeout, 30)
        self.assertEqual(client.verify_ssl, False)

    def test_has_all_http_helpers(self):
        client = EvolutionApiClient("https://api.example.com", "inst1", "key")
        self.assertTrue(callable(client._get))
        self.assertTrue(callable(client._post))
        self.assertTrue(callable(client._put))
        self.assertTrue(callable(client._delete))
        self.assertTrue(callable(client._request))

    def test_endpoint_builder(self):
        client = EvolutionApiClient("https://api.example.com/", "myinst", "key")
        self.assertEqual(client._endpoint("/chat/test"), "https://api.example.com/chat/test/myinst")


class TestSyncClientNewMethods(unittest.TestCase):
    """Verify new methods build correct URLs and payloads using mock."""

    def setUp(self):
        self.client = EvolutionApiClient("https://api.example.com", "default", "key")
        self.mock_resp = MagicMock()
        self.mock_resp.status_code = 200
        self.mock_resp.json.return_value = {}
        self.mock_resp.text = "{}"
        # Patch _request on the instance so all calls go through mock
        self.patcher = patch.object(self.client, '_request', return_value=self.mock_resp)
        self.mock_request = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_check_wa_number(self):
        self.client.check_wa_number(numbers=["5511999999999"])
        self.mock_request.assert_called_once_with(
            "POST",
            "https://api.example.com/chat/whatsappNumbers/default",
            payload={"numbers": ["5511999999999"]},
        )

    def test_fetch_profile_picture_url(self):
        self.client.fetch_profile_picture_url(number="5511999999999")
        self.mock_request.assert_called_once_with(
            "POST",
            "https://api.example.com/chat/fetchProfilePictureUrl/default",
            payload={"number": "5511999999999"},
        )

    def test_group_find_infos(self):
        self.client.group_find_infos(group_jid="123@g.us")
        self.mock_request.assert_called_once_with(
            "GET",
            "https://api.example.com/group/findGroupInfos/default",
            params={"groupJid": "123@g.us"},
        )

    def test_set_webhook(self):
        self.client.set_webhook(url="https://hook.example.com")
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "POST")
        self.assertIn("/webhook/set/", args[0][1])

    def test_set_s3(self):
        self.client.set_s3(settings={"bucket": "b"})
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "POST")
        self.assertIn("/s3/set/", args[0][1])

    def test_send_contact(self):
        self.client.send_contact(number="5511999999999", contact_name="A", contact_number="5511888888888")
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "POST")
        self.assertIn("/message/sendContact/", args[0][1])

    def test_send_fake_call(self):
        self.client.send_fake_call(number="5511999999999")
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "POST")
        self.assertIn("/call/offer/", args[0][1])

    def test_restart_instance(self):
        self.client.restart_instance()
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "PUT")

    def test_get_instance_status(self):
        self.client.get_instance_status()
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "GET")

    def test_find_settings(self):
        self.client.find_settings()
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "GET")

    def test_label_find(self):
        self.client.label_find()
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "GET")

    def test_group_leave(self):
        self.client.group_leave(group_jid="123@g.us")
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "DELETE")

    def test_delete_message_for_everyone(self):
        self.client.delete_message_for_everyone(message_id="m1", remote_jid="5511@s.whatsapp.net")
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "DELETE")

    def test_find_chats(self):
        self.client.find_chats()
        self.mock_request.assert_called_once()

    def test_find_status_message(self):
        self.client.find_status_message()
        self.mock_request.assert_called_once()

    def test_profile_remove_picture(self):
        self.client.profile_remove_picture()
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "DELETE")

    def test_profile_fetch_privacy(self):
        self.client.profile_fetch_privacy()
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "GET")

    def test_group_find_by_invite_code(self):
        self.client.group_find_by_invite_code(invite_code="ABC")
        self.mock_request.assert_called_once()
        args = self.mock_request.call_args
        self.assertEqual(args[0][0], "GET")
