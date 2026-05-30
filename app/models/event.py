from datetime import datetime
from sqlmodel import SQLModel, Field


class EventBase(SQLModel):
    title: str
    description: str
    date: datetime
    location: str


class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class EventCreate(EventBase):
    pass


class EventPublic(EventBase):
    id: int