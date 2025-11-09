
import hashlib
from typing import Any, Dict

def idempotency_from_payload(prefix: str, payload: Dict[str, Any]) -> str:
    raw = (prefix + "|" + str(sorted(payload.items()))).encode()
    return hashlib.sha256(raw).hexdigest()
