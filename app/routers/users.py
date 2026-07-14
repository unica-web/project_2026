from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.data.db import SessionDep
from app.models.user import User, UserCreate, UserPublic
from app.models.registration import Registration


router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def get_users(session: SessionDep) -> list[UserPublic]:
    """
    Restituisce la lista di tutti gli utenti presenti nel database.
    """
    users = session.exec(select(User)).all()
    return users


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: SessionDep) -> UserPublic:
    """
    Crea un nuovo utente se lo username non esiste già.
    """
    existing_user = session.get(User, user.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username già esistente"
        )

    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/{username}")
def get_user(username: str, session: SessionDep) -> UserPublic:
    """
    Restituisce un utente tramite username.
    """
    user = session.get(User, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )

    return user


@router.delete("")
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


@router.delete("/{username}")
def delete_user(username: str, session: SessionDep):
    """
    Elimina un utente tramite username e tutte le sue registrazioni associate.
    """
    user = session.get(User, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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