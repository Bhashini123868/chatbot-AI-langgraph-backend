from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionResponse

def list_sessions(db: Session, skip: int = 0, limit: int = 100) -> List[SessionModel]:
    return db.query(SessionModel).order_by(SessionModel.created_at.desc()).offset(skip).limit(limit).all()

def get_session_by_id(db: Session, session_id: int) -> Optional[SessionModel]:
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()

def get_session_by_session_id(db: Session, sid: str) -> Optional[SessionModel]:
    return db.query(SessionModel).filter(SessionModel.session_id == sid).first()

def create_session(db: Session, session_in: SessionCreate, session_id: str, expires_at: Optional[datetime] = None) -> SessionModel:
    db_obj = SessionModel(
        session_id=session_id,
        ip_address=session_in.ip_address,
        user_agent=session_in.user_agent,
        expires_at=expires_at
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_last_active(db: Session, session_obj: SessionModel) -> SessionModel:
    session_obj.last_active = datetime.utcnow()
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj

def delete_session(db: Session, session_id: int) -> bool:
    obj = get_session_by_id(db, session_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
