import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.configs.config import config
from src.core.exceptions.custom_error import CustomError
from src.infrastructure.api.auth_controller import auth_router
from src.infrastructure.api.client_controller import client_router
from src.infrastructure.api.import_export_controller import im_ex_router
from src.infrastructure.api.order_controller import order_router
from src.infrastructure.api.review_controller import review_router
from src.infrastructure.api.tool_controller import tool_router, category_router, type_router
from src.infrastructure.api.worker_contoller import worker_router
from src.infrastructure.db.mongo import MongoDB
from src.infrastructure.api.exceptions.exception_handlers import custom_error_handler, unexpected_error_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect()
    await MongoDB.create_indexes()
    yield
    await MongoDB.close()


app = FastAPI(lifespan=lifespan)

current_dir = os.path.dirname(os.path.abspath(__file__))

img_dir = os.path.join(current_dir, f"../{config.paths.image_dir}")

app.mount("/api/resources/images", StaticFiles(directory=img_dir, html=True), name="images")

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tool_router, prefix="/api/tools", tags=["tool"])
app.include_router(category_router, prefix="/api/categories", tags=["category"])
app.include_router(type_router, prefix="/api/types", tags=["type"])
app.include_router(worker_router, prefix="/api/workers", tags=["worker"])
app.include_router(client_router, prefix="/api/clients", tags=["client"])
app.include_router(order_router, prefix="/api/orders", tags=["order"])
app.include_router(review_router, prefix="/api/reviews", tags=["reviews"])
app.include_router(im_ex_router, prefix="/api/data", tags=["im_ex"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_exception_handler(CustomError, custom_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)

