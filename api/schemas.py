from pydantic import BaseModel
from typing import List, Optional

class TopProduct(BaseModel):
    term: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    total_messages: int

class MessageResult(BaseModel):
    message_id: int
    message_text: str

class VisualStats(BaseModel):
    image_category: str
    total_images: int
