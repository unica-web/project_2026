from datetime import datetime
from sqlmodel import SQLModel, Field


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str