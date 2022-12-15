from fastapi import FastAPI
from . import models
from .database import engine
from .routers import playlist, channel, user, video, auth, edits
from .config import settings

# if you're not using alembic  , use this to created tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(channel.router)
app.include_router(playlist.router)
app.include_router(user.router)
app.include_router(video.router)
app.include_router(auth.router)
app.include_router(edits.router)
