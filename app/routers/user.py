from fastapi import APIRouter, Path, HTTPException, Query
from app.models.userDB import User
#verificare from app.models.registration import Registration
from app.data.db import SessionDep
from typing import Annotated
from sqlmodel import select

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("/")
def get_all_user(
    session: SessionDep,
    sort: Annotated[bool, Query(description="Ordinami gli utenti in ordine crescente o decrescente")]=False
    )->list[User]:
    # Restituisce la lista di tutti gli utenti

    users = session.exec(select(User))

    if sort:
        return sorted(users, key=lambda x: x.username)
    else:
        return list(users)

@user_router.get("/{username}")
def get_user_by_username(
    session: SessionDep,
    username: Annotated[str, Path(description="Username dell'utente")]
    )->User:
    #Restituisce l'utente con l'username cercato

    user=session.get(User, username)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    
@user_router.post("/")
def new_user(
    session:SessionDep,
    user:User):
    #Aggiungi un nuovo utente
    
    userExist=session.get(User, user.username)
    
    if userExist:
        raise HTTPException(status_code=409, detail="L'Username esiste già non trovato")
    else:
        newUser = User.model_validate(user)
        session.add(newUser)
        session.commit()
        return "Utente aggiunto con successo"