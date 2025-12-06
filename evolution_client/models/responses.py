from typing import Optional, Dict, Any
from pydantic import BaseModel

class EvolutionResponse(BaseModel):
    """Base model for API responses."""
    status: int
    data: Dict[str, Any]

class SendMessageResponse(BaseModel):
    """
    Response model for sending a message.
    """
    key: Dict[str, Any]
    message: Dict[str, Any]
    messageTimestamp: int
    status: str
