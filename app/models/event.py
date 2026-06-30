from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
#from pydantic import ConfigDict

class CreateEvent(SQLModel):
    title : str
    description : str
    date: datetime
    location : str

    #model_config = ConfigDict(strict=True)

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str

    #model_config = ConfigDict(strict=True)