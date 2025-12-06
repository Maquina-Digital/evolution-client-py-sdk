
from typing import List, Optional, Literal, Union, Dict, Any
from pydantic import BaseModel, Field, constr, conint, field_validator

Phone = constr(strip_whitespace=True, min_length=5, max_length=32)

class BaseMessage(BaseModel):
    type: Literal["text", "buttons", "poll", "media", "audio", "sticker", "location", "list", "reaction"]
    number: Phone
    delay: Optional[int] = Field(default=0, ge=0)

class TextMessage(BaseMessage):
    type: Literal["text"] = "text"
    text: constr(min_length=1)

class ButtonItem(BaseModel):
    id: constr(min_length=1, max_length=64)
    label: constr(min_length=1, max_length=64)

class ButtonsMessage(BaseMessage):
    type: Literal["buttons"] = "buttons"
    text: constr(min_length=1)
    footer: Optional[str] = None
    buttons: List[ButtonItem]

    @field_validator("buttons")
    @classmethod
    def max_buttons(cls, v):
        if not (1 <= len(v) <= 3):
            raise ValueError("1 to 3 buttons allowed by WhatsApp clients")
        return v

class PollMessage(BaseMessage):
    type: Literal["poll"] = "poll"
    name: constr(min_length=1, max_length=100)
    selectableCount: conint(ge=1, le=5) = 1
    values: List[constr(min_length=1, max_length=100)]

    @field_validator("values")
    @classmethod
    def at_least_two_options(cls, v):
        if len(v) < 2:
            raise ValueError("Poll must have at least two options")
        return v

class MediaMessage(BaseMessage):
    type: Literal["media"] = "media"
    url: constr(min_length=5)
    caption: Optional[str] = None
    mime_type: Optional[str] = None

class AudioMessage(BaseMessage):
    type: Literal["audio"] = "audio"
    url: constr(min_length=5)

class StickerMessage(BaseMessage):
    type: Literal["sticker"] = "sticker"
    url: constr(min_length=5)

class LocationMessage(BaseMessage):
    type: Literal["location"] = "location"
    latitude: float
    longitude: float
    name: Optional[str] = None
    address: Optional[str] = None

class ReactionMessage(BaseMessage):
    type: Literal["reaction"] = "reaction"
    key: Dict[str, Any]  # The key of the message to react to
    reaction: str  # Emoji

class ListRow(BaseModel):
    title: constr(min_length=1)
    description: Optional[str] = None
    rowId: constr(min_length=1)

class ListSection(BaseModel):
    title: constr(min_length=1)
    rows: List[ListRow]

class ListMessage(BaseMessage):
    type: Literal["list"] = "list"
    title: constr(min_length=1)
    description: Optional[str] = None
    buttonText: constr(min_length=1)
    footer: Optional[str] = None
    sections: List[ListSection]

Message = Union[
    TextMessage, 
    ButtonsMessage, 
    PollMessage, 
    MediaMessage,
    AudioMessage,
    StickerMessage,
    LocationMessage,
    ReactionMessage,
    ListMessage
]
