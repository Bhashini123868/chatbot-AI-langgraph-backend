import datetime
from typing import Optional

from pydantic.v1 import BaseModel


class SessionCreate(BaseModel):
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class SessionResponse(BaseModel):
    id: int
    session_id: str
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True