import time
from typing import Any, Dict, List, Optional
import httpx
from loguru import logger
from .exceptions import EvolutionApiError


class EvolutionApiClient:
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
        self.base = base_url.rstrip("/")
        self.instance = instance
        self.retries = max(0, retries)
        self._client = httpx.Client(
            headers={"apikey": api_key, "Content-Type": "application/json", **(headers or {})},
            timeout=timeout,
            verify=verify_ssl,
        )

    def _endpoint(self, path: str) -> str:
        return f"{self.base}{path}/{self.instance}"

    def _post(self, url: str, payload: Dict[str, Any]) -> httpx.Response:
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.retries + 2):  # initial + retries
            try:
                logger.debug(f"[EvolutionAPI] POST {url} attempt={attempt} payload={payload}")
                resp = self._client.post(url, json=payload)
                # Successful
                if resp.status_code in (200, 201):
                    return resp
                # Retry only on 429/5xx
                if resp.status_code == 429 or resp.status_code >= 500:
                    sleep_s = min(2 ** attempt, 8)
                    logger.warning(f"[EvolutionAPI] transient status={resp.status_code}; retry in {sleep_s}s")
                    time.sleep(sleep_s)
                    continue
                # Non-retryable
                return resp
            except httpx.RequestError as e:
                last_exc = e
                sleep_s = min(2 ** attempt, 8)
                logger.warning(f"[EvolutionAPI] network error: {e}; retry in {sleep_s}s")
                time.sleep(sleep_s)
        # Exhausted
        raise EvolutionApiError(f"EvolutionAPI request failed after retries: {last_exc}")

    # Public senders
    def send_text(self, *, number: str, text: str, delay: int = 0) -> httpx.Response:
        url = self._endpoint("/message/sendText")
        payload = {"number": number, "text": text, "delay": delay}
        return self._post(url, payload)

    def send_buttons(
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
        return self._post(url, payload)

    def send_poll(
            self, *, number: str, name: str, selectableCount: int, values: List[str], delay: int = 0
    ) -> httpx.Response:
        url = self._endpoint("/message/sendPoll")
        # 'flat' format for broader compatibility
        payload = {
            "number": number,
            "name": name,
            "selectableCount": selectableCount,
            "values": values,
            "delay": delay,
        }
        return self._post(url, payload)

    def send_media_old(
            self, *, number: str, url_media: str, caption: Optional[str] = None, mime_type: Optional[str] = None,
            delay: int = 0
    ) -> httpx.Response:
        url = self._endpoint("/message/sendMedia")
        payload: Dict[str, Any] = {"number": number, "media": url_media, "delay": delay}
        if caption:
            payload["caption"] = caption
        if mime_type:
            payload["mimeType"] = mime_type
        return self._post(url, payload)

    def send_media(
            self, *, number: str, url_media: str,
            caption: Optional[str] = None,
            mime_type: Optional[str] = None,
            delay: int = 0
    ) -> httpx.Response:
        url = self._endpoint("/message/sendMedia")
        payload: Dict[str, Any] = {
            "number": number,
            "media": url_media,
            "delay": delay,
            "mediatype": mime_type or "image",  # ✅ key updated
        }
        if caption:
            payload["caption"] = caption
        return self._post(url, payload)

    def reply_message(
            self,
            *,
            number: str,
            message_id: str,
            text: str,
            delay: int = 0,
    ) -> httpx.Response:
        """
        Reply to a specific WhatsApp message via EvolutionAPI.
        """
        url = self._endpoint("/message/reply")
        payload = {
            "number": number,
            "reply_to": message_id,
            "text": text,
            "delay": delay,
        }
        return self._post(url, payload)

    def send_audio(self, *, number: str, audio: str, delay: int = 0) -> httpx.Response:
        url = self._endpoint("/message/sendWhatsAppAudio")
        payload = {"number": number, "audio": audio, "delay": delay}
        return self._post(url, payload)

    def send_sticker(self, *, number: str, sticker: str, delay: int = 0) -> httpx.Response:
        url = self._endpoint("/message/sendSticker")
        payload = {"number": number, "sticker": sticker, "delay": delay}
        return self._post(url, payload)

    def send_location(
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
        return self._post(url, payload)

    def send_reaction(self, *, key: Dict[str, Any], reaction: str) -> httpx.Response:
        url = self._endpoint("/message/sendReaction")
        payload = {"reactionMessage": {"key": key, "reaction": reaction}}
        return self._post(url, payload)

    def send_list(
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
        return self._post(url, payload)

    # Instance Management
    def create_instance(
            self, *, instance_name: str, token: Optional[str] = None, qrcode: bool = True
    ) -> httpx.Response:
        """
        Create a new Evolution API instance.
        """
        url = f"{self.base}/instance/create"
        payload = {
            "instanceName": instance_name,
            "qrcode": qrcode
        }
        if token:
            payload["token"] = token
        return self._post(url, payload)

    def connect_instance(self, instance_name: Optional[str] = None) -> httpx.Response:
        """
        Fetch the QR Code for an instance.
        If instance_name is not provided, uses the client's configured instance.
        """
        target_instance = instance_name or self.instance
        url = f"{self.base}/instance/connect/{target_instance}"
        return self._client.get(url)

    def logout_instance(self, instance_name: Optional[str] = None) -> httpx.Response:
        """
        Logout an instance.
        """
        target_instance = instance_name or self.instance
        url = f"{self.base}/instance/logout/{target_instance}"
        return self._client.delete(url)

    def delete_instance(self, instance_name: Optional[str] = None) -> httpx.Response:
        """
        Delete an instance.
        """
        target_instance = instance_name or self.instance
        url = f"{self.base}/instance/delete/{target_instance}"
        return self._client.delete(url)

    def fetch_instances(self) -> httpx.Response:
        """
        List all instances.
        """
        url = f"{self.base}/instance/fetchInstances"
        return self._client.get(url)
