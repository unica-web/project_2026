from sqlmodel import SQLModel, Field #impostare modello database
from pydantic import ConfigDict

# 1. Modello usato per validare i dati in INGRESSO (Request Body)
class CreateUser(SQLModel):
    username: str
    name: str
    email: str

    # Questo blocca la conversione automatica dei tipi (es. rifiuta username=0)
    # e garantisce che se manca un campo obbligatorio scatti l'errore 422
    model_config = ConfigDict(strict=True)

class User(SQLModel, table=True):
    username : str = Field(primary_key=True) #collegamento class user con registration
    name : str
    email: str
    model_config = ConfigDict(strict=True)