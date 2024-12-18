from typing import List, Optional

from pydantic import BaseModel, Field

from src.core.entities.category.category import Category
from src.core.entities.order.order import Order
from src.core.entities.review.review import Review
from src.core.entities.tool.tool import Tool
from src.core.entities.type.type import Type
from src.core.entities.users.client.client import Client
from src.core.entities.users.worker.worker import Worker


class DBModel(BaseModel):
    workers: Optional[List[Worker]] = Field(
        ...
    )
    clients: Optional[List[Client]] = Field(
        ...,
    )
    tools: Optional[List[Tool]] = Field(
        ...,
    )
    orders: Optional[List[Order]] = Field(
        ...,
    )
    categories: Optional[List[Category]] = Field(
        ...,
    )
    types: Optional[List[Type]] = Field(
        ...,
    )
    reviews: Optional[List[Review]] = Field(
        ...,
    )