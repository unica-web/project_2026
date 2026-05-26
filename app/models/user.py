from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Modello ORM che rappresenta un utente del sistema.
    """

    username: str = Field(primary_key=True)
    name: str
    email: str