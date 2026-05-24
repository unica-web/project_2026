from sqlmodel import create_engine, SQLModel, Session, select
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
# TODO: remember to import all the DB models here
from app.models.registration import Registration  # NOQA
from app.models.userDB import User # NOQA
from app.models.eventDB import Event  # NOQA


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")        
        with Session(engine) as session:
            
            utenti=[]
            eventi=[]

            for i in range(10):
                user = User(username=f.user_name(), name=f.name(), email=f.email())
                session.add(user)
                
                # TODO: Aggiungere la parte di creazione dell'event ID
                evento = Event(
                    title=f.sentence(nb_words=3),  # Titolo di 3 parole
                    description=f.sentence(),  # Una frase casuale
                    date=f.date_time_this_year(),  # Una data casuale di quest'anno
                    location=f.city()  # Una città casuale
                )
                session.add(evento)
                session.commit()

                session.refresh(user)
                session.refresh(evento)
                eventi.append(evento)
                utenti.append(user)
            import random

            for user in utenti:
                eventi_scelti= random.sample(eventi, k=random.randint(1,3))
                for evento in eventi_scelti:
                    registrazione= Registration(
                        username=user.username,
                        event_id=evento.id
                    )
                    session.add(registrazione)
            
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
