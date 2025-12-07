from typing import List, Optional
from pydantic import BaseModel

class GroupParticipant(BaseModel):
    id: str
    admin: Optional[str] = None

class Group(BaseModel):
    id: str
    subject: str
    subjectOwner: Optional[str] = None
    subjectTime: Optional[int] = None
    size: Optional[int] = None
    creation: Optional[int] = None
    owner: Optional[str] = None
    restrict: Optional[bool] = None
    announce: Optional[bool] = None
    participants: List[GroupParticipant] = []
