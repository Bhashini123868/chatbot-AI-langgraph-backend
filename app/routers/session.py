from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.dbconnection import get_db
from app.schemas.session import SessionCreate, SessionResponse
from app.services import session_service

router = APIRouter()

@router.get("/", response_model=List[SessionResponse])
def read_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return session_service.list_sessions(db, skip, limit)

@router.get("/id/{id}", response_model=SessionResponse)
def read_session_by_id(id: int, db: Session = Depends(get_db)):
    obj = session_service.get_session_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Session not found")
    return obj

@router.get("/sid/{session_id}", response_model=SessionResponse)
def read_session_by_sid(session_id: str, db: Session = Depends(get_db)):
    obj = session_service.get_session_by_sid(db, session_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Session not found")
    # update last_active on read (optional)
    session_service.touch_session(db, obj)
    return obj

@router.post("/", response_model=SessionResponse, status_code=201)
def create_session(session_in: SessionCreate, db: Session = Depends(get_db), ttl_minutes: Optional[int] = Query(None, description="optional TTL in minutes")):
    obj = session_service.create_new_session(db, session_in, ttl_minutes)
    return obj

@router.delete("/{id}", status_code=204)
def delete_session(id: int, db: Session = Depends(get_db)):
    ok = session_service.remove_session(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
    return
