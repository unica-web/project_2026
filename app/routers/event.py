from fastapi import APIRouter, HTTPException, status
from app.models.eventDB import Event
from app.models.userDB import User
from app.models.registration import Registration
from app.data.db import SessionDep  # Importiamo la stessa scorciatoia di Simone
from sqlmodel import select



event_router = APIRouter(prefix="/events", tags=["Events"])


@event_router.get("/")
def get_all_events(session: SessionDep) -> list[Event]:
    eventi = session.exec(select(Event)).all()  #Serve per eseguiire la domanda
    return eventi


# 3. API: Crea un nuovo evento (POST /events)
@event_router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: Event, session: SessionDep):


    session.add(event)   # Aggiungo l'evento ricevuto dal frontend al database
    session.commit()  # Salvo le modifiche
    session.refresh(event)  # Aggiorno i dati

    return event


@event_router.get("/{id}", response_model=Event, status_code=status.HTTP_200_OK)
def get_event(id: int, session: SessionDep):


    evento = session.get(Event, id)   #Per andare a cercare uno specifico evento


    if not evento: # Se non ce resituisce un codice errore
        raise HTTPException(status_code=404, detail="Evento non trovato")

    return evento


@event_router.put("/{id}", response_model=Event, status_code=status.HTTP_200_OK)
def update_event(id: int, event_update: Event, session: SessionDep):


    evento_db = session.get(Event, id)  #cerco se levento esiste

    if not evento_db:
        raise HTTPException(status_code=404, detail="Evento non trovato")



    update_data = event_update.model_dump(exclude_unset=True)  # se esiste aggiorniamo i suoi dati con quelli nuovi

    for key, value in update_data.items(): #Serve per aggiornare solo i campi che sono stati modificati
                                            #senza fare il replace dei vari campi uno ad uno

        setattr(evento_db, key, value)

    # salvo le modifiche
    session.add(evento_db)
    session.commit()
    session.refresh(evento_db)

    return evento_db


@event_router.post("/{id}/register", status_code=status.HTTP_200_OK)
def register_user_to_event(id: int, user_data: User, session: SessionDep):


    evento = session.get(Event, id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento non trovato") # Controllo se l'evento esiste


    utente_esistente = session.get(User, user_data.username)  # Controllo se l'utente esiste già

    if not utente_esistente:
        # L'utente non esiste! Le istruzioni dicono di crearlo automaticamente.
        nuovo_utente = User(username=user_data.username, name=user_data.name, email=user_data.email)
        session.add(nuovo_utente)


    # Creo la registrazione
    # Controllo prima che non sia già registrato per evitare doppioni
    registrazione_esistente = session.get(Registration, (user_data.username, id))
    if registrazione_esistente:
        return {"message": "L'utente è già registrato a questo evento"}

    nuova_registrazione = Registration(username=user_data.username, event_id=id)
    session.add(nuova_registrazione)

    # 4. Salvo tutto
    session.commit()

    return {"message": f"Utente {user_data.username} registrato all'evento {id} con successo"}


@event_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_single_event(id: int, session: SessionDep):
    """
    Elimina un evento e tutte le registrazioni ad esso associate.
    """
    evento = session.get(Event, id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    # Trovo tutte le registrazioni per questo evento e le elimino
    registrazioni = session.exec(select(Registration).where(Registration.event_id == id)).all()
    for reg in registrazioni:
        session.delete(reg)

    # Elimino l'evento stesso
    session.delete(evento)
    session.commit()

    return {"message": "Evento e registrazioni associate eliminati con successo"}


@event_router.delete("/", status_code=status.HTTP_200_OK)
def delete_all_events(session: SessionDep):
    """
    Elimina letteralmente tutti gli eventi presenti nel database.
    """
    # Prendo tutti gli eventi
    tutti_gli_eventi = session.exec(select(Event)).all()

    # Elimino uno ad uno
    for evento in tutti_gli_eventi:
        session.delete(evento)

    session.commit()
    return {"message": "Tutti gli eventi sono stati eliminati"}