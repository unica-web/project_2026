from sqlmodel import SQLModel, Field

#Struttura dati di User

class Event(SQLModel, table=True):
    id : int = Field(primary_key=True)