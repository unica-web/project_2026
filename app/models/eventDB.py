from sqlmodel import SQLModel, Field
from datetime import datetime

#Struttura dati di Event (Improved by jj)

class Event(SQLModel, table=True):
    id: int | None=Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str
