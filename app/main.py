from app.config import config

# NB: do not add imports here!

from pathlib import Path
import os



# ...and here!!

if Path(__file__).parent == Path(os.getcwd()):
    config.root_dir = "."

# You can add imports from here...

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from app.routers import frontend, events, users
from app.models import user
from contextlib import asynccontextmanager
from app.data.db import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on start
    init_database()
    yield
    # on close


app = FastAPI(lifespan=lifespan)
app.mount(
    "/static",
    StaticFiles(directory=config.root_dir / "static"),
    name="static"
)
app.include_router(frontend.router)

app.include_router(events.events_router) #implementazione file events

app.include_router(users.user_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
