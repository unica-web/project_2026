from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from app.models.registration import Registration
from app.models.user import User, CreateUser
from app.data.db import get_session

router = APIRouter(prefix="/users",)


# GET /users
@router.get("", response_model=list[User])
def get_users(session: Session = Depends(get_session)):
    """Questa query diventerà solo: SELECT user.username FROM user (Funzionerà al 100%)"""
    db_users = session.exec(select(User)).all()

    return db_users


# POST /users
@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, session: Session = Depends(get_session)):
    """creazione  utente e verifica se il nome utente esiste già"""
    db_users = session.get(User, user.username)
    if db_users:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_users=User.model_validate(user)

    session.add(db_users)
    session.commit()
    session.refresh(db_users)

    return db_users

@router.get("/{username}", response_model=User)
def get_user(username: str, session: Session = Depends(get_session)):
    """restituzione singolo utente di una lista dato il suo username"""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("", status_code=status.HTTP_200_OK)
def delete_all_users(session: Session = Depends(get_session)):
    """cancellazione di tutti gli utenti regustrati"""
    registrations=session.exec(select(Registration)).all()
    for reg in registrations:
        session.delete(reg)

    users=session.exec(select(User)).all()
    for user in users:
        session.delete(user)
        session.commit()

    return {"message":"Users deleted successfully"} #status_code 200_ok


@router.delete("/{username}", status_code=status.HTTP_200_OK)
def delete_user(username: str, session: Session = Depends(get_session)):
    """eliminazione singolo utente dato lo username"""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    registrations=session.exec(select(Registration).where(Registration.username==username))
    for reg in registrations:
        session.delete(reg)

    session.delete(user)
    session.commit()
    return {"message":"User deleted successfully"} #status_code 200_ok
