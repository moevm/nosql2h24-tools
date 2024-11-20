from contextlib import asynccontextmanager
from sys import prefix

from fastapi import FastAPI
from src.core.exceptions.custom_error import CustomError
from src.infrastructure.api.auth_controller import auth_router
from src.infrastructure.api.tool_controller import tool_router, category_router, type_router
from src.infrastructure.db.mongo import MongoDB
from src.infrastructure.api.exceptions.exception_handlers import custom_error_handler, unexpected_error_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect()
    yield
    await MongoDB.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tool_router, prefix="/api/tools", tags=["tool"])
app.include_router(category_router, prefix="/api/categories", tags=["category"])
app.include_router(type_router, prefix="/api/types", tags=["type"])

app.add_exception_handler(CustomError, custom_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)

