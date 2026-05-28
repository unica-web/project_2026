from fastapi import APIRouter
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event


router = APIRouter(tags=["events"])


@router.get("/events")
def get_events(session: SessionDep):
    """
    Restituisce la lista di tutti gli eventi presenti nel database.
    """
    events = session.exec(select(Event)).all()
    return events


@router.post("/events", status_code=201)
def create_event(event: Event, session: SessionDep):
    """
    Crea un nuovo evento e lo salva nel database.
    """
    session.add(event)
    session.commit()
    session.refresh(event)
    return event