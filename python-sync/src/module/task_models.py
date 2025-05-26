from pydantic import BaseModel
from typing import List, Optional, Literal

from src.module.message_models import MessageRequest, MessageResponse


class Thread(BaseModel):
    request: MessageRequest
    response: Optional[MessageResponse] = None


class Task(BaseModel):
    id_task: str
    id_team_agent: str
    id_team: str
    title: str
    content: Optional[List[Thread]] = []
    driver: Literal["auto", "agent", "user"]
    created_at: str
    updated_at: str
