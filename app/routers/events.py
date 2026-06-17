from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from app.models.user import User
from app.models.event import Event, CreateEvent
from app.models.registration import Registration
from app.data.db import get_session  # import database

events_router = APIRouter(
    prefix="/events"
    # tags=["events"]
)


# restituzione lista con tutti gli elementi programmati
@events_router.get("", status_code=status.HTTP_200_OK)
def get_events(session: Session = Depends(get_session)):
    events = session.exec(select(Event)).all()
    return events


# creazione nuovo evento
@events_router.post("", status_code=status.HTTP_201_CREATED)
def create_event(event: CreateEvent, session: Session = Depends(get_session)):
    db_event = Event.model_validate(event)

    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event
    """creazione della tabella:
    [
      {
        "title": "string",
        "description": "string",
        "date": "2026-05-22T16:46:29.137Z",
        "location": "string",
        "id": 0
      }
    ]"""


# restituzione evento con ID
@events_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_event(id: int, session: Session = Depends(get_session)):
    # event = session.query(Event).get(id)
    event = session.get(Event, id)
    if event:
        return event
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@events_router.post("/{id}/register", status_code=status.HTTP_200_OK)
def register_id_event(id: int, user: User, session: Session = Depends(get_session)):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    db_user = session.get(User, User.username)
    if not db_user:
        session.add(user)  # (username=user.username)
        session.commit()

    return {"User registered successfully"}


@events_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_event(id: int, event_update: Event, session: Session = Depends(get_session)):
    db_event = session.get(Event, id)

    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    db_event.title = event_update.title
    db_event.date = event_update.date
    db_event.description = event_update.description
    db_event.location = event_update.location

    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@events_router.delete("", status_code=status.HTTP_200_OK)
def delete_all_event(session: Session = Depends(get_session)):
    registrations = session.exec(select(Registration)).all()
    for reg in registrations:
        session.delete(reg)

    events = session.exec(select(Event)).all()
    for event in events:
        session.delete(event)
        session.commit()

    return {"Events deleted successfully"}  # per messaggi, status_code 200_ok


@events_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_event(id: int, session: Session = Depends(get_session)):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    registrations = session.exec(select(Registration).where(Registration.event_id == id))
    for reg in registrations:
        session.delete(reg)

    session.delete(event)
    session.commit()
    return {"Event deleted successfully"}
