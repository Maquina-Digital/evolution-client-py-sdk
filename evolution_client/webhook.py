
import hmac, hashlib, json
from typing import Any, Dict, Tuple

def verify_signature(raw_body: bytes, signature: str, secret: str | None) -> bool:
    if not secret:
        return True
    mac = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature or "")

def normalize_event_type(event: str | None, payload: Dict[str, Any]) -> str:
    t = payload.get("type") or event or "message"
    if t == "button_response":
        return "button_response"
    if t in ("poll_update", "poll_vote", "poll"):
        return "poll_update"
    return "message"

def extract_from_number(payload: Dict[str, Any]) -> str:
    from_number = payload.get("from")
    if not from_number:
        rjid = payload.get("remoteJid", "")
        if isinstance(rjid, str) and "@c.us" in rjid:
            from_number = rjid.split("@")[0]
    return from_number or ""

def dedupe_key(raw_body: bytes, payload: Dict[str, Any]) -> str:
    return payload.get("id") or payload.get("key", {}).get("id") or hashlib.md5(raw_body).hexdigest()
