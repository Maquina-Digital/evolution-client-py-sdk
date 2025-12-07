
import hashlib
from typing import Any, Dict

def idempotency_from_payload(prefix: str, payload: Dict[str, Any]) -> str:
    raw = (prefix + "|" + str(sorted(payload.items()))).encode()
    return hashlib.sha256(raw).hexdigest()

import mimetypes
from typing import Optional

def get_media_type(url: str) -> str:
    """
    Detect media type (image, video, audio, document) based on file URL extension.
    Defaults to 'document' if unknown.
    """
    mime_type, _ = mimetypes.guess_type(url)
    
    if not mime_type:
        return "document"

    if mime_type.startswith("image/"):
        return "image"
    elif mime_type.startswith("video/"):
        return "video"
    elif mime_type.startswith("audio/"):
        return "audio"
    
    return "document"
