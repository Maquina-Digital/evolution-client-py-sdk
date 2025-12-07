from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field, field_validator

class InstanceConnectionState(BaseModel):
    state: str
    statusReason: Optional[int] = None

class Instance(BaseModel):
    instance: Dict[str, Any] = Field(default_factory=dict)
    # Adjust fields based on actual API response for fetchInstances
    # Usually returns a list of objects with instance name, status, etc.
    # For now, we'll use a flexible dict or specific fields if known.
    name: str
    status: str = "close"

class InstanceConfig(BaseModel):
    instanceName: str
    token: Optional[str] = None
    qrcode: bool = True
