from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from datetime import datetime

from app.models import registration
from app.models.user import User, CreateUser
from app.models.event import Event, CreateEvent
from app.models.registration import Registration
from app.data.db import get_session #import database

router = APIRouter(prefix="/events")

#restituzione lista con tutti gli elementi programmati
@router.get("", status_code=status.HTTP_200_OK)
def get_events(session: Session = Depends(get_session)):
    """restituzione lista eventi esistenti"""
    events=session.exec(select(Event)).all()
    return events
#creazione nuovo evento
@router.post("", status_code=status.HTTP_201_CREATED)
def create_event(event:CreateEvent, session: Session = Depends(get_session)):
    """creazione singolo evento"""
    db_event = Event.model_validate(event)

    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


# restituzione evento con ID
@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_event(id: int, session: Session = Depends(get_session)):
    """restituzione evento con id indicato"""
    # event = session.query(Event).get(id)
    event = session.get(Event, id)
    if event:
        return event
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/{id}/register", status_code=status.HTTP_200_OK)
def register_to_event(id: int, user_data: CreateUser, session: Session = Depends(get_session)):
    """registrazione utente ad un evento con l'id indicato. se l'utente non esiste si procede alla creazione"""
    #Verifica che l'evento esista
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    #Verifica se l'utente esiste già, altrimenti lo prepara per la creazione
    user = session.get(User, user_data.username)
    if not user:
        user = User(username=user_data.username, name=user_data.name, email=user_data.email)
        session.add(user)

    #Verifica e crea la registrazione
    registration = session.get(Registration, (user_data.username, id))
    if not registration:
        # Crea il collegamento tra username e l'id dell'evento
        new_registration = Registration(username=user_data.username, event_id=id)
        session.add(new_registration)

    #Salva l'utente E la registrazione nel database in un colpo solo
    session.commit()

    return {"message":"User successfully registered to the event"}


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_event(id: int, event_update: CreateEvent, session: Session = Depends(get_session)):
    """aggiornamento evento"""
    db_event = session.get(Event, id)

    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    db_event.title = event_update.title

    if isinstance(event_update.date, str):
        db_event.date = datetime.fromisoformat(event_update.date)
    else:
        db_event.date = event_update.date

    db_event.description = event_update.description
    db_event.location = event_update.location

    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@router.delete("", status_code=status.HTTP_200_OK)
def delete_all_event(session: Session = Depends(get_session)):
    """eliminazione di tutti gli eventi"""
    registrations = session.exec(select(Registration)).all()
    for reg in registrations:
        session.delete(reg)

    events = session.exec(select(Event)).all()
    for event in events:
        session.delete(event)
        session.commit()

    return {"message":"Events deleted successfully"}  # per messaggi, status_code 200_ok

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_event(id: int, session: Session = Depends(get_session)):
    """eliminazione singolo evento con id indicato"""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    registrations = session.exec(select(Registration).where(Registration.event_id == id))
    for reg in registrations:
        session.delete(reg)

    session.delete(event)
    session.commit()
    return {"message":"Event deleted successfully"}

