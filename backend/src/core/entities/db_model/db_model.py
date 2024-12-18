from typing import List, Optional

from pydantic import BaseModel, Field

from src.core.entities.category.category import Category, CategoryInDB, CategoryCreateDB
from src.core.entities.order.order import Order, OrderInDB, OrderCreateDB
from src.core.entities.review.review import Review, ReviewInDB, ReviewCreateDB
from src.core.entities.tool.tool import Tool, ToolInDB, ToolCreateDB
from src.core.entities.type.type import Type, TypeInDB, TypeCreateDB
from src.core.entities.users.client.client import Client, ClientInDB, ClientCreateDB
from src.core.entities.users.worker.worker import Worker, WorkerInDB, WorkerCreateDB


class DBModel(BaseModel):
    workers: Optional[List[WorkerInDB]] = Field(
        ...
    )
    clients: Optional[List[ClientInDB]] = Field(
        ...,
    )
    tools: Optional[List[ToolInDB]] = Field(
        ...,
    )
    orders: Optional[List[OrderInDB]] = Field(
        ...,
    )
    categories: Optional[List[CategoryInDB]] = Field(
        ...,
    )
    types: Optional[List[TypeInDB]] = Field(
        ...,
    )
    reviews: Optional[List[ReviewInDB]] = Field(
        ...,
    )

class DBModelCreate(BaseModel):
    workers: Optional[List[WorkerCreateDB]] = Field(
        ...
    )
    clients: Optional[List[ClientCreateDB]] = Field(
        ...,
    )
    tools: Optional[List[ToolCreateDB]] = Field(
        ...,
    )
    orders: Optional[List[OrderCreateDB]] = Field(
        ...,
    )
    categories: Optional[List[CategoryCreateDB]] = Field(
        ...,
    )
    types: Optional[List[TypeCreateDB]] = Field(
        ...,
    )
    reviews: Optional[List[ReviewCreateDB]] = Field(
        ...,
    )