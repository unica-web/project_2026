from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.data.db import SessionDep
from app.models.user import User
from app.models.registration import Registration


router = APIRouter(tags=["users"])


@router.get("/users")
def get_users(session: SessionDep):
    """
    Restituisce la lista di tutti gli utenti presenti nel database.
    """
    users = session.exec(select(User)).all()
    return users


@router.post("/users", status_code=201)
def create_user(user: User, session: SessionDep):
    """
    Crea un nuovo utente se lo username non esiste già.
    """
    existing_user = session.get(User, user.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Username già esistente"
        )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/users/{username}")
def get_user(username: str, session: SessionDep):
    """
    Restituisce un utente tramite username.
    """
    user = session.get(User, username)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Utente non trovato"
        )

    return user


@router.delete("/users")
def delete_users(session: SessionDep):
    """
    Elimina tutti gli utenti e tutte le registrazioni associate.
    """
    registrations = session.exec(select(Registration)).all()

    for registration in registrations:
        session.delete(registration)

    users = session.exec(select(User)).all()

    for user in users:
        session.delete(user)

    session.commit()

    return {"message": "Tutti gli utenti sono stati eliminati"}


@router.delete("/users/{username}")
def delete_user(username: str, session: SessionDep):
    """
    Elimina un utente tramite username e tutte le sue registrazioni associate.
    """
    user = session.get(User, username)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Utente non trovato"
        )

    registrations = session.exec(
        select(Registration).where(Registration.username == username)
    ).all()

    for registration in registrations:
        session.delete(registration)

    session.delete(user)
    session.commit()

    return {"message": "Utente eliminato correttamente"}