from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
def get_events(session: SessionDep):
    """Restituisce tutti gli eventi presenti nel database."""
    return session.exec(select(Event)).all()


@router.post("/")
def create_event(event: Event, session: SessionDep):
    """Crea un nuovo evento nel database."""
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("/{event_id}")
def get_event(event_id: int, session: SessionDep):
    """Restituisce un evento tramite il suo id."""
    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    return event


@router.put("/{event_id}")
def update_event(event_id: int, updated_event: Event, session: SessionDep):
    """Aggiorna un evento esistente."""
    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    event.title = updated_event.title
    event.description = updated_event.description
    event.date = updated_event.date
    event.location = updated_event.location

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@router.post("/{event_id}/register")
def register_user_to_event(event_id: int, user: User, session: SessionDep):
    """Registra un utente a un evento."""
    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    existing_user = session.get(User, user.username)

    if existing_user is None:
        session.add(user)
        session.commit()
        session.refresh(user)

    registration = Registration(username=user.username, event_id=event_id)

    session.add(registration)
    session.commit()
    session.refresh(registration)

    return registration