from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration
from app.data.db import get_session #import database

router=APIRouter(
    prefix="/registrations",
)

@router.get("", status_code=status.HTTP_200_OK)
def get_registration(session: Session = Depends(get_session)):
    """restituisce tutte le registrazioni effettuate"""
    registrations=session.exec(select(Registration)).all()
    return registrations

@router.delete("", status_code=status.HTTP_200_OK)
def delete_registration(username: str, event_id: int,session: Session = Depends(get_session)):
    """eliminazione delle singole registrazioni tramite query parameter"""
    user=session.get(User, username)
    event=session.get(Event, event_id)
    registration=session.get(Registration,(username, event_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")

    session.delete(registration)
    session.commit()
    return {"message":"Registration deleted"}

