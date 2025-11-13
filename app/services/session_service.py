from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from typing import List, Optional

from app.repository import session_repository
from app.schemas.session import SessionCreate
from app.models.session import Session as SessionModel

# හෝයම්: session id generate කිරීම
def _generate_session_id() -> str:
    return uuid4().hex

def list_sessions(db: Session, skip: int = 0, limit: int = 100) -> List[SessionModel]:
    return session_repository.list_sessions(db, skip, limit)

def get_session_by_id(db: Session, session_id: int) -> Optional[SessionModel]:
    return session_repository.get_session_by_id(db, session_id)

def get_session_by_sid(db: Session, sid: str) -> Optional[SessionModel]:
    return session_repository.get_session_by_session_id(db, sid)

def create_new_session(db: Session, session_in: SessionCreate, ttl_minutes: Optional[int] = None) -> SessionModel:
    sid = _generate_session_id()
    expires_at = None
    if ttl_minutes:
        expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
    return session_repository.create_session(db, session_in, session_id=sid, expires_at=expires_at)

def touch_session(db: Session, session_obj: SessionModel) -> SessionModel:
    return session_repository.update_last_active(db, session_obj)

def remove_session(db: Session, session_id: int) -> bool:
    return session_repository.delete_session(db, session_id)
