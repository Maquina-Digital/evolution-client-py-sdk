import asyncio
from typing import Any, Dict, List, Optional
import httpx
from loguru import logger
from .exceptions import EvolutionApiError
from .utils import get_media_type


class AsyncEvolutionClient:
    def __init__(
            self,
            base_url: str,
            instance: str,
            api_key: str,
            timeout: int = 15,
            retries: int = 3,
            verify_ssl: bool = True,
            headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.base = self.base_url
        self.instance = instance
        self.api_key = api_key
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.retries = max(0, retries)
        self._client = httpx.AsyncClient(
            headers={"apikey": api_key, "Content-Type": "application/json", **(headers or {})},
            timeout=timeout,
            verify=verify_ssl,
        )

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # ── internal helpers ──────────────────────────────────────────────

    def _endpoint(self, path: str) -> str:
        return f"{self.base}{path}/{self.instance}"

    async def _request(
        self,
        method: str,
        url: str,
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """Unified request method with retry logic for all HTTP verbs."""
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.retries + 2):
            try:
                logger.debug(f"[EvolutionAPI] {method} {url} attempt={attempt}")
                kwargs: Dict[str, Any] = {}
                if payload is not None:
                    kwargs["json"] = payload
                if params is not None:
                    kwargs["params"] = params
                resp = await self._client.request(method, url, **kwargs)
                if resp.status_code in (200, 201):
                    return resp
                if resp.status_code == 429 or resp.status_code >= 500:
                    sleep_s = min(2 ** attempt, 8)
                    logger.warning(f"[EvolutionAPI] transient status={resp.status_code}; retry in {sleep_s}s")
                    await asyncio.sleep(sleep_s)
                    continue
                return resp
            except httpx.RequestError as e:
                last_exc = e
                sleep_s = min(2 ** attempt, 8)
                logger.warning(f"[EvolutionAPI] network error: {e}; retry in {sleep_s}s")
                await asyncio.sleep(sleep_s)
        raise EvolutionApiError(f"EvolutionAPI request failed after retries: {last_exc}")

    async def _post(self, url: str, payload: Dict[str, Any]) -> httpx.Response:
        return await self._request("POST", url, payload=payload)

    async def _get(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return await self._request("GET", url, params=params)

    async def _put(self, url: str, payload: Dict[str, Any]) -> httpx.Response:
        return await self._request("PUT", url, payload=payload)

    async def _delete(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return await self._request("DELETE", url, params=params)

    # ── Send Message ──────────────────────────────────────────────────

    async def send_text(self, *, number: str, text: str, delay: int = 0) -> httpx.Response:
        url = self._endpoint("/message/sendText")
        payload = {"number": number, "text": text, "delay": delay}
        return await self._post(url, payload)

    async def send_buttons(
            self, *, number: str, text: str, buttons: List[Dict[str, str]], footer: Optional[str] = None, delay: int = 0
    ) -> httpx.Response:
        url = self._endpoint("/message/sendButtons")
        payload: Dict[str, Any] = {"number": number, "text": text, "delay": delay}
        if footer:
            payload["footer"] = footer
        payload["buttons"] = [
            {"buttonId": b["id"], "buttonText": {"displayText": b["label"]}, "type": 1}
            for b in buttons
        ]
        return await self._post(url, payload)

    async def send_poll(
            self, *, number: str, name: str, selectableCount: int, values: List[str], delay: int = 0
    ) -> httpx.Response:
        url = self._endpoint("/message/sendPoll")
        payload = {
            "number": number,
            "name": name,
            "selectableCount": selectableCount,
            "values": values,
            "delay": delay,
        }
        return await self._post(url, payload)

    async def send_media(
            self, *, number: str, url_media: str,
            caption: Optional[str] = None,
            mime_type: Optional[str] = None,
            delay: int = 0
    ) -> httpx.Response:
        url = self._endpoint("/message/sendMedia")
        media_type = mime_type or get_media_type(url_media)
        payload: Dict[str, Any] = {
            "number": number,
            "media": url_media,
            "delay": delay,
            "mediatype": media_type,
        }
        if caption:
            payload["caption"] = caption
        return await self._post(url, payload)

    async def reply_message(
            self,
            *,
            number: str,
            message_id: str,
            text: str,
            delay: int = 0,
    ) -> httpx.Response:
        """Reply to a specific WhatsApp message via EvolutionAPI."""
        url = self._endpoint("/message/reply")
        payload = {
            "number": number,
            "reply_to": message_id,
            "text": text,
            "delay": delay,
        }
        return await self._post(url, payload)

    async def send_audio(self, *, number: str, audio: str, delay: int = 0) -> httpx.Response:
        url = self._endpoint("/message/sendWhatsAppAudio")
        payload = {"number": number, "audio": audio, "delay": delay}
        return await self._post(url, payload)

    async def send_sticker(self, *, number: str, sticker: str, delay: int = 0) -> httpx.Response:
        url = self._endpoint("/message/sendSticker")
        payload = {"number": number, "sticker": sticker, "delay": delay}
        return await self._post(url, payload)

    async def send_location(
            self, *, number: str, latitude: float, longitude: float, name: Optional[str] = None,
            address: Optional[str] = None, delay: int = 0
    ) -> httpx.Response:
        url = self._endpoint("/message/sendLocation")
        payload = {
            "number": number,
            "latitude": latitude,
            "longitude": longitude,
            "delay": delay
        }
        if name:
            payload["name"] = name
        if address:
            payload["address"] = address
        return await self._post(url, payload)

    async def send_reaction(self, *, key: Dict[str, Any], reaction: str) -> httpx.Response:
        url = self._endpoint("/message/sendReaction")
        payload = {"reactionMessage": {"key": key, "reaction": reaction}}
        return await self._post(url, payload)

    async def send_list(
            self, *, number: str, title: str, button_text: str, sections: List[Dict[str, Any]],
            description: Optional[str] = None, footer: Optional[str] = None, delay: int = 0
    ) -> httpx.Response:
        url = self._endpoint("/message/sendList")
        payload = {
            "number": number,
            "title": title,
            "buttonText": button_text,
            "sections": sections,
            "delay": delay
        }
        if description:
            payload["description"] = description
        if footer:
            payload["footer"] = footer
        return await self._post(url, payload)

    async def send_contact(
            self, *, number: str, contact_name: str, contact_number: str,
            organization: Optional[str] = None, email: Optional[str] = None,
            delay: int = 0
    ) -> httpx.Response:
        """Send a contact card."""
        url = self._endpoint("/message/sendContact")
        contact = {
            "fullName": contact_name,
            "wuid": contact_number,
            "phoneNumber": contact_number,
        }
        if organization:
            contact["organization"] = organization
        if email:
            contact["email"] = email
        payload: Dict[str, Any] = {"number": number, "contact": [contact], "delay": delay}
        return await self._post(url, payload)

    async def send_ptv(self, *, number: str, ptv: str, delay: int = 0) -> httpx.Response:
        """Send a PTV (push-to-video) message."""
        url = self._endpoint("/message/sendPtv")
        payload = {"number": number, "ptv": ptv, "delay": delay}
        return await self._post(url, payload)

    async def send_status(
            self, *, type: str, content: str, caption: Optional[str] = None,
            background_color: Optional[str] = None, font: Optional[int] = None,
            all_contacts: bool = True, status_jid_list: Optional[List[str]] = None,
    ) -> httpx.Response:
        """Post a WhatsApp status/story."""
        url = self._endpoint("/message/sendStatus")
        payload: Dict[str, Any] = {
            "type": type,
            "content": content,
            "allContacts": all_contacts,
        }
        if caption:
            payload["caption"] = caption
        if background_color:
            payload["backgroundColor"] = background_color
        if font is not None:
            payload["font"] = font
        if status_jid_list:
            payload["statusJidList"] = status_jid_list
        return await self._post(url, payload)

    # ── Call ───────────────────────────────────────────────────────────

    async def send_fake_call(
            self, *, number: str, is_video: bool = False, call_duration: int = 5
    ) -> httpx.Response:
        """Send a fake call notification."""
        url = self._endpoint("/call/offer")
        payload = {
            "number": number,
            "isVideo": is_video,
            "callDuration": call_duration,
        }
        return await self._post(url, payload)

    # ── Instance Management ───────────────────────────────────────────

    async def create_instance(
            self, *, instance_name: str, token: Optional[str] = None, qrcode: bool = True
    ) -> httpx.Response:
        """Create a new Evolution API instance."""
        url = f"{self.base}/instance/create"
        payload = {
            "instanceName": instance_name,
            "qrcode": qrcode
        }
        if token:
            payload["token"] = token
        return await self._post(url, payload)

    async def connect_instance(self, instance_name: Optional[str] = None) -> httpx.Response:
        """Fetch the QR Code for an instance."""
        target_instance = instance_name or self.instance
        url = f"{self.base}/instance/connect/{target_instance}"
        return await self._get(url)

    async def logout_instance(self, instance_name: Optional[str] = None) -> httpx.Response:
        """Logout an instance."""
        target_instance = instance_name or self.instance
        url = f"{self.base}/instance/logout/{target_instance}"
        return await self._delete(url)

    async def delete_instance(self, instance_name: Optional[str] = None) -> httpx.Response:
        """Delete an instance."""
        target_instance = instance_name or self.instance
        url = f"{self.base}/instance/delete/{target_instance}"
        return await self._delete(url)

    async def fetch_instances(self) -> httpx.Response:
        """List all instances."""
        url = f"{self.base}/instance/fetchInstances"
        return await self._get(url)

    async def restart_instance(self, instance_name: Optional[str] = None) -> httpx.Response:
        """Restart an instance."""
        target_instance = instance_name or self.instance
        url = f"{self.base}/instance/restart/{target_instance}"
        return await self._put(url, {})

    async def set_presence(self, *, presence: str) -> httpx.Response:
        """Set instance presence (available, unavailable)."""
        url = self._endpoint("/instance/setPresence")
        payload = {"presence": presence}
        return await self._post(url, payload)

    async def get_instance_status(self, instance_name: Optional[str] = None) -> httpx.Response:
        """Get the connection status of an instance."""
        target_instance = instance_name or self.instance
        url = f"{self.base}/instance/connectionState/{target_instance}"
        return await self._get(url)

    # ── Proxy ─────────────────────────────────────────────────────────

    async def set_proxy(self, *, proxy_url: str, enabled: bool = True) -> httpx.Response:
        """Set proxy for the instance."""
        url = self._endpoint("/proxy/set")
        payload = {"enabled": enabled, "proxy": proxy_url}
        return await self._post(url, payload)

    async def find_proxy(self) -> httpx.Response:
        """Get proxy settings for the instance."""
        url = self._endpoint("/proxy/find")
        return await self._get(url)

    # ── Settings ──────────────────────────────────────────────────────

    async def set_settings(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Set instance settings."""
        url = self._endpoint("/settings/set")
        return await self._post(url, settings)

    async def find_settings(self) -> httpx.Response:
        """Get instance settings."""
        url = self._endpoint("/settings/find")
        return await self._get(url)

    # ── Chat Management ───────────────────────────────────────────────

    async def check_wa_number(self, *, numbers: List[str]) -> httpx.Response:
        """Check if numbers are registered on WhatsApp."""
        url = self._endpoint("/chat/whatsappNumbers")
        payload = {"numbers": numbers}
        return await self._post(url, payload)

    async def chat_archive(self, *, number: str, archive: bool = True) -> httpx.Response:
        """Archive or unarchive a chat."""
        url = self._endpoint("/chat/archiveChat")
        payload = {"number": number, "archive": archive}
        return await self._post(url, payload)

    async def chat_mark_read(self, *, number: str, read: bool = True) -> httpx.Response:
        """Mark a chat as read or unread."""
        endpoint = "/chat/markMessageAsRead" if read else "/chat/markMessageAsUnread"
        url = self._endpoint(endpoint)
        payload = {"read": read}
        return await self._post(url, payload)

    async def delete_chat(self, *, number: str) -> httpx.Response:
        """Delete a chat."""
        url = self._endpoint("/chat/deleteMessage")
        payload = {"number": number}
        return await self._post(url, payload)

    async def delete_message_for_everyone(self, *, message_id: str, remote_jid: str, from_me: bool = True) -> httpx.Response:
        """Delete a message for everyone in the chat (Baileys only)."""
        url = self._endpoint("/chat/deleteMessageForEveryone")
        return await self._delete(url, params={"id": message_id, "remoteJid": remote_jid, "fromMe": str(from_me).lower()})

    async def fetch_profile_picture_url(self, *, number: str) -> httpx.Response:
        """Fetch contact/group profile picture URL."""
        url = self._endpoint("/chat/fetchProfilePictureUrl")
        payload = {"number": number}
        return await self._post(url, payload)

    async def get_base64_media(self, *, message_id: str) -> httpx.Response:
        """Get media in base64 from a message."""
        url = self._endpoint("/chat/getBase64FromMediaMessage")
        payload = {"key": {"id": message_id}}
        return await self._post(url, payload)

    async def update_message(self, *, number: str, message_id: str, text: str) -> httpx.Response:
        """Update/edit a sent message."""
        url = self._endpoint("/chat/updateMessage")
        payload = {
            "number": number,
            "key": {"id": message_id},
            "text": text,
        }
        return await self._post(url, payload)

    async def set_chat_presence(self, *, number: str, presence: str, delay: int = 0) -> httpx.Response:
        """Set presence (composing, recording, paused) in a specific chat."""
        url = self._endpoint("/chat/presence")
        payload = {"number": number, "presence": presence, "delay": delay}
        return await self._post(url, payload)

    async def block_contact(self, *, number: str, status: str) -> httpx.Response:
        """Block or unblock a contact. status: 'block' or 'unblock'."""
        url = self._endpoint("/chat/blockContact")
        payload = {"number": number, "status": status}
        return await self._post(url, payload)

    async def find_contacts(self, *, where: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """Find contacts, optionally filtered."""
        url = self._endpoint("/chat/findContacts")
        payload = {"where": where or {}}
        return await self._post(url, payload)

    async def find_messages(self, *, where: Dict[str, Any], limit: int = 100) -> httpx.Response:
        """Find messages matching a filter."""
        url = self._endpoint("/chat/findMessages")
        payload = {"where": where, "limit": limit}
        return await self._post(url, payload)

    async def find_status_message(self) -> httpx.Response:
        """Find status/story messages (Baileys only)."""
        url = self._endpoint("/chat/findStatusMessage")
        return await self._post(url, {})

    async def find_chats(self) -> httpx.Response:
        """Find all chats for the instance."""
        url = self._endpoint("/chat/findChats")
        return await self._post(url, {})

    # ── Label ─────────────────────────────────────────────────────────

    async def label_find(self) -> httpx.Response:
        """Find all labels."""
        url = self._endpoint("/label/findLabels")
        return await self._get(url)

    async def label_handle(self, *, number: str, label_id: str, action: str) -> httpx.Response:
        """Add or remove a label from a chat. action: 'add' or 'remove'."""
        url = self._endpoint("/label/handleLabel")
        payload = {"number": number, "labelId": label_id, "action": action}
        return await self._post(url, payload)

    # ── Profile Management ────────────────────────────────────────────

    async def profile_fetch_business(self, *, number: str) -> httpx.Response:
        """Fetch business profile."""
        url = self._endpoint("/chat/fetchBusinessProfile")
        payload = {"number": number}
        return await self._post(url, payload)

    async def profile_fetch(self, *, number: str) -> httpx.Response:
        """Fetch normal profile."""
        url = self._endpoint("/chat/fetchProfile")
        payload = {"number": number}
        return await self._post(url, payload)

    async def profile_update_name(self, name: str) -> httpx.Response:
        """Update profile name."""
        url = self._endpoint("/profile/updateProfileName")
        payload = {"name": name}
        return await self._post(url, payload)

    async def profile_update_status(self, status: str) -> httpx.Response:
        """Update profile status (about)."""
        url = self._endpoint("/profile/updateProfileStatus")
        payload = {"status": status}
        return await self._post(url, payload)

    async def profile_update_picture(self, *, picture: str) -> httpx.Response:
        """Update profile picture. picture: URL or base64."""
        url = self._endpoint("/profile/updateProfilePicture")
        payload = {"picture": picture}
        return await self._post(url, payload)

    async def profile_remove_picture(self) -> httpx.Response:
        """Remove profile picture."""
        url = self._endpoint("/profile/removeProfilePicture")
        return await self._delete(url)

    async def profile_fetch_privacy(self) -> httpx.Response:
        """Fetch privacy settings."""
        url = self._endpoint("/profile/fetchPrivacySettings")
        return await self._get(url)

    async def profile_update_privacy(self, *, settings: Dict[str, str]) -> httpx.Response:
        """Update privacy settings."""
        url = self._endpoint("/profile/updatePrivacySettings")
        return await self._post(url, settings)

    # ── Group Management ──────────────────────────────────────────────

    async def group_create(
            self, *, subject: str, participants: List[str], description: Optional[str] = None
    ) -> httpx.Response:
        """Create a new group."""
        url = self._endpoint("/group/create")
        payload = {
            "subject": subject,
            "participants": participants
        }
        if description:
            payload["description"] = description
        return await self._post(url, payload)

    async def group_update_picture(self, *, group_jid: str, image_url: str) -> httpx.Response:
        """Update group profile picture."""
        url = self._endpoint("/group/updateProfilePicture")
        payload = {"id": group_jid, "image": image_url}
        return await self._post(url, payload)

    async def group_update_subject(self, *, group_jid: str, subject: str) -> httpx.Response:
        """Update group subject."""
        url = self._endpoint("/group/updateSubject")
        payload = {"id": group_jid, "subject": subject}
        return await self._post(url, payload)

    async def group_update_description(self, *, group_jid: str, description: str) -> httpx.Response:
        """Update group description."""
        url = self._endpoint("/group/updateDescription")
        payload = {"id": group_jid, "description": description}
        return await self._post(url, payload)

    async def group_fetch_all(self) -> httpx.Response:
        """Fetch all groups."""
        url = self._endpoint("/group/fetchAllGroups")
        return await self._get(url)

    async def group_find_infos(self, *, group_jid: str) -> httpx.Response:
        """Fetch detailed group info by JID."""
        url = self._endpoint("/group/findGroupInfos")
        return await self._get(url, params={"groupJid": group_jid})

    async def group_find_by_invite_code(self, *, invite_code: str) -> httpx.Response:
        """Find a group by its invite code (Baileys only)."""
        url = self._endpoint("/group/inviteInfo")
        return await self._get(url, params={"inviteCode": invite_code})

    async def group_get_participants(self, *, group_jid: str) -> httpx.Response:
        """Get participants of a group."""
        url = self._endpoint("/group/participants")
        return await self._get(url, params={"groupJid": group_jid})

    async def group_get_invite_code(self, *, group_jid: str) -> httpx.Response:
        """Get the invite code for a group."""
        url = self._endpoint("/group/inviteCode")
        return await self._get(url, params={"groupJid": group_jid})

    async def group_revoke_invite(self, *, group_jid: str) -> httpx.Response:
        """Revoke a group's invite link."""
        url = self._endpoint("/group/revokeInviteCode")
        payload = {"id": group_jid}
        return await self._post(url, payload)

    async def group_send_invite(self, *, group_jid: str, numbers: List[str], description: Optional[str] = None) -> httpx.Response:
        """Send invite link to numbers."""
        url = self._endpoint("/group/sendInvite")
        payload: Dict[str, Any] = {"id": group_jid, "numbers": numbers}
        if description:
            payload["description"] = description
        return await self._post(url, payload)

    async def group_participants_update(
            self, *, group_jid: str, action: str, participants: List[str]
    ) -> httpx.Response:
        """Update group participants (add, remove, promote, demote)."""
        url = self._endpoint("/group/updateParticipant")
        payload = {
            "id": group_jid,
            "action": action,
            "participants": participants
        }
        return await self._post(url, payload)

    async def group_update_settings(self, *, group_jid: str, action: str) -> httpx.Response:
        """Update group settings (announcement, not_announcement, locked, unlocked)."""
        url = self._endpoint("/group/updateSetting")
        payload = {"id": group_jid, "action": action}
        return await self._post(url, payload)

    async def group_toggle_ephemeral(self, *, group_jid: str, expiration: int) -> httpx.Response:
        """Toggle ephemeral messages. expiration: 0 (off), 86400, 604800, 7776000."""
        url = self._endpoint("/group/toggleEphemeral")
        payload = {"id": group_jid, "expiration": expiration}
        return await self._post(url, payload)

    async def group_leave(self, *, group_jid: str) -> httpx.Response:
        """Leave a group."""
        url = self._endpoint("/group/leaveGroup")
        return await self._delete(url, params={"groupJid": group_jid})

    # ── Integrations: Events ──────────────────────────────────────────

    async def set_webhook(self, *, url: str, events: Optional[List[str]] = None, enabled: bool = True, **kwargs) -> httpx.Response:
        """Configure a webhook for the instance."""
        endpoint = self._endpoint("/webhook/set")
        payload: Dict[str, Any] = {"url": url, "enabled": enabled, **kwargs}
        if events:
            payload["events"] = events
        return await self._post(endpoint, payload)

    async def find_webhook(self) -> httpx.Response:
        """Get webhook configuration."""
        url = self._endpoint("/webhook/find")
        return await self._get(url)

    async def set_websocket(self, *, enabled: bool = True, events: Optional[List[str]] = None) -> httpx.Response:
        """Configure websocket events."""
        url = self._endpoint("/websocket/set")
        payload: Dict[str, Any] = {"enabled": enabled}
        if events:
            payload["events"] = events
        return await self._post(url, payload)

    async def find_websocket(self) -> httpx.Response:
        """Get websocket configuration."""
        url = self._endpoint("/websocket/find")
        return await self._get(url)

    async def set_rabbitmq(self, *, enabled: bool = True, events: Optional[List[str]] = None) -> httpx.Response:
        """Configure RabbitMQ events."""
        url = self._endpoint("/rabbitmq/set")
        payload: Dict[str, Any] = {"enabled": enabled}
        if events:
            payload["events"] = events
        return await self._post(url, payload)

    async def find_rabbitmq(self) -> httpx.Response:
        """Get RabbitMQ configuration."""
        url = self._endpoint("/rabbitmq/find")
        return await self._get(url)

    async def set_sqs(self, *, enabled: bool = True, events: Optional[List[str]] = None) -> httpx.Response:
        """Configure SQS events."""
        url = self._endpoint("/sqs/set")
        payload: Dict[str, Any] = {"enabled": enabled}
        if events:
            payload["events"] = events
        return await self._post(url, payload)

    async def find_sqs(self) -> httpx.Response:
        """Get SQS configuration."""
        url = self._endpoint("/sqs/find")
        return await self._get(url)

    async def set_nats(self, *, enabled: bool = True, events: Optional[List[str]] = None) -> httpx.Response:
        """Configure NATS events."""
        url = self._endpoint("/nats/set")
        payload: Dict[str, Any] = {"enabled": enabled}
        if events:
            payload["events"] = events
        return await self._post(url, payload)

    async def find_nats(self) -> httpx.Response:
        """Get NATS configuration."""
        url = self._endpoint("/nats/find")
        return await self._get(url)

    async def set_pusher(self, *, enabled: bool = True, events: Optional[List[str]] = None, **kwargs) -> httpx.Response:
        """Configure Pusher events."""
        url = self._endpoint("/pusher/set")
        payload: Dict[str, Any] = {"enabled": enabled, **kwargs}
        if events:
            payload["events"] = events
        return await self._post(url, payload)

    async def find_pusher(self) -> httpx.Response:
        """Get Pusher configuration."""
        url = self._endpoint("/pusher/find")
        return await self._get(url)

    # ── Integrations: Chatbot ─────────────────────────────────────────

    async def set_chatwoot(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure Chatwoot integration."""
        url = self._endpoint("/chatwoot/set")
        return await self._post(url, settings)

    async def find_chatwoot(self) -> httpx.Response:
        """Get Chatwoot configuration."""
        url = self._endpoint("/chatwoot/find")
        return await self._get(url)

    async def set_typebot(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure Typebot integration."""
        url = self._endpoint("/typebot/set")
        return await self._post(url, settings)

    async def find_typebot(self) -> httpx.Response:
        """Get Typebot configuration."""
        url = self._endpoint("/typebot/find")
        return await self._get(url)

    async def set_openai(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure OpenAI integration."""
        url = self._endpoint("/openai/set")
        return await self._post(url, settings)

    async def find_openai(self) -> httpx.Response:
        """Get OpenAI configuration."""
        url = self._endpoint("/openai/find")
        return await self._get(url)

    async def set_dify(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure Dify integration."""
        url = self._endpoint("/dify/set")
        return await self._post(url, settings)

    async def find_dify(self) -> httpx.Response:
        """Get Dify configuration."""
        url = self._endpoint("/dify/find")
        return await self._get(url)

    async def set_flowise(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure Flowise integration."""
        url = self._endpoint("/flowise/set")
        return await self._post(url, settings)

    async def find_flowise(self) -> httpx.Response:
        """Get Flowise configuration."""
        url = self._endpoint("/flowise/find")
        return await self._get(url)

    async def set_n8n(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure N8N integration."""
        url = self._endpoint("/n8n/set")
        return await self._post(url, settings)

    async def find_n8n(self) -> httpx.Response:
        """Get N8N configuration."""
        url = self._endpoint("/n8n/find")
        return await self._get(url)

    # ── Integrations: Channel ─────────────────────────────────────────

    async def set_evolution_channel(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure Evolution Channel integration."""
        url = self._endpoint("/channel/evolution/set")
        return await self._post(url, settings)

    async def find_evolution_channel(self) -> httpx.Response:
        """Get Evolution Channel configuration."""
        url = self._endpoint("/channel/evolution/find")
        return await self._get(url)

    async def set_cloud_api(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure Cloud Official WhatsApp API integration."""
        url = self._endpoint("/channel/cloudApi/set")
        return await self._post(url, settings)

    async def find_cloud_api(self) -> httpx.Response:
        """Get Cloud Official API configuration."""
        url = self._endpoint("/channel/cloudApi/find")
        return await self._get(url)

    # ── Storage ───────────────────────────────────────────────────────

    async def set_s3(self, *, settings: Dict[str, Any]) -> httpx.Response:
        """Configure S3 storage. All credentials are passed through from the calling application."""
        url = self._endpoint("/s3/set")
        return await self._post(url, settings)

    async def find_s3(self) -> httpx.Response:
        """Get S3 configuration."""
        url = self._endpoint("/s3/find")
        return await self._get(url)
