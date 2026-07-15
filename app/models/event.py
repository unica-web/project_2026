from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class CreateEvent(SQLModel):
    title : str
    description : str
    date: datetime
    location : str


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str
