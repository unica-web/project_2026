from sqlmodel import SQLModel, Field #impostare modello database
from pydantic import ConfigDict

class CreateUser(SQLModel):
    username: str
    name: str
    email: str

    model_config = ConfigDict(strict=True)

class User(SQLModel, table=True):
    username : str = Field(primary_key=True) #collegamento class user con registration
    name : str
    email: str
    model_config = ConfigDict(strict=True)