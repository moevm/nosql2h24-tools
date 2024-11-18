from contextlib import asynccontextmanager
from multiprocessing.managers import Token

from fastapi import FastAPI
from src.infrastructure.api.auth_controller import auth_router
from src.infrastructure.db.mongo import MongoDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect()
    yield
    await MongoDB.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


