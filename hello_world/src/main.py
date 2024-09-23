from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import MONGO_URI
from src.database.database import connect_to_database
from src.reposiroties.mongo_text_repository import MongoTextRepository
from src.api.text_router import router
from src.services.text_service import TextService

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo_client, app.mongodb = await connect_to_database(MONGO_URI)
    repository = MongoTextRepository(app.mongodb)
    app.text_service = TextService(repository)
    yield

    if app.mongo_client:
        app.mongo_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router)

