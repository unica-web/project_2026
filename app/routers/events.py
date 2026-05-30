from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event, EventCreate, EventPublic
from app.models.user import User
from app.models.registration import Registration


router = APIRouter(prefix="/events")


@router.get("")
def get_all_events(session: SessionDep) -> list[EventPublic]:
    """Restituisce la lista di tutti gli eventi disponibili."""
    events = session.exec(select(Event)).all()
    return events


@router.post("")
def add_event(session: SessionDep, event: EventCreate):
    """Aggiunge un nuovo evento."""
    session.add(Event.model_validate(event))
    session.commit()
    return "Event successfully added"


@router.get("/{id}")
def get_event_by_id(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to get")]
) -> EventPublic:
    """Restituisce l'evento con l'id specificato."""
    event = session.get(Event, id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.put("/{id}")
def update_event(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to update")],
    new_event: EventCreate
):
    """Aggiorna l'evento con l'id specificato."""
    event = session.get(Event, id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location

    session.add(event)
    session.commit()

    return "Event successfully updated"

@router.post("/{id}/register", status_code=status.HTTP_201_CREATED)
def register_user_to_event(id: int, user: User, session: SessionDep) -> Registration:
    """Registra un utente a un evento."""
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found."
        )

    existing_user = session.get(User, user.username)

    if existing_user is None:
        session.add(user)
        session.commit()
        session.refresh(user)

    existing_registration = session.get(Registration, (user.username, id))

    if existing_registration is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered to this event."
        )

    registration = Registration(username=user.username, event_id=id)

    session.add(registration)
    session.commit()
    session.refresh(registration)

    return registration


@router.delete("")
def delete_all_events(session: SessionDep) -> dict[str, str]:
    """Elimina tutti gli eventi e tutte le registrazioni associate."""
    registrations = session.exec(select(Registration)).all()

    for registration in registrations:
        session.delete(registration)

    events = session.exec(select(Event)).all()

    for event in events:
        session.delete(event)

    session.commit()

    return {"message": "All events deleted successfully."}


@router.delete("/{id}")
def delete_event(id: int, session: SessionDep) -> dict[str, str]:
    """Elimina un evento tramite id e tutte le registrazioni associate."""
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found."
        )

    registrations = session.exec(
        select(Registration).where(Registration.event_id == id)
    ).all()

    for registration in registrations:
        session.delete(registration)

    session.delete(event)
    session.commit()

    return {"message": "Event deleted successfully."}