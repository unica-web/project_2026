from fastapi import APIRouter, Query, HTTPException
from app.models.registration import Registration
from app.data.db import SessionDep
from typing import Annotated
from sqlmodel import select

registration_router=APIRouter(prefix="/registrations", tags=["Registrations"])

@registration_router.get("/")
def gell_all_registration(
    session: SessionDep,
    sort: Annotated[bool, Query(description="Ordinami gli utenti in ordine crescente o decrescente")]=False
):
    registration= session.exec(select(Registration))

   
    if sort:
        return sorted(registration, key=lambda x: x.username)
    else:
        return list(registration)
    
@registration_router.delete("/")
def delete_registration(
    session:SessionDep,
    username: Annotated[str, Query(description="Username dell'utente")],
    event_id: Annotated[str, Query(description="Id dell'evento")]
):
    
    registrazione = session.get(Registration, (username, event_id))

    if not registrazione:
        raise HTTPException(status_code=404, detail="Registrazione non trovata")
    
    session.delete(registrazione)
    session.commit()

    return "Registrazione eliminata"