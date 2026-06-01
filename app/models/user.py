from pydantic import StrictStr
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    """
    Attributi comuni dell'utente.
    """

    username: str
    name: str
    email: str


class User(UserBase, table=True):
    """
    Modello ORM che rappresenta un utente del sistema nel database.
    """

    username: str = Field(primary_key=True)


class UserCreate(SQLModel):
    """
    Modello usato per creare un utente tramite API.
    Serve per validare correttamente i dati in input.
    """

    username: StrictStr
    name: StrictStr
    email: StrictStr


class UserPublic(UserBase):
    """
    Modello usato per restituire un utente tramite API.
    """

    pass