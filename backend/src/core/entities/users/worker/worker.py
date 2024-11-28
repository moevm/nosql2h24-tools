from email.policy import default

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import List, Optional

from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.order.order import Order
from src.core.entities.users.base_user import BaseUser, BaseUserSummary


class Worker(BaseUser):
    name: str = Field(
        ...,
        description="Worker's first name"
    )
    surname: str = Field(
        ...,
        description="Worker's last name"
    )
    phone: str = Field(
        ...,
        description="Worker's phone number",
        pattern=r'^\+?[1-9]\d{1,14}$'
    )
    jobTitle: str = Field(
        ...,
        description="Worker's job title"
    )
    date: datetime = Field(
        default=None,
        description="Employee start date"
    )
    orders: Optional[List[Order]] = Field(
        default_factory=list,
        description="The orders of the worker"
    )
    image: Optional[str] = Field(
        default=None,
        description="Worker's image url",
    )

class WorkerInDB(Worker):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the client in the db"
    )

class WorkerSummary(BaseUserSummary):
    jobTitle: str = Field(
        ...,
        description="Worker's job title",
    )
    date: datetime = Field(
        default=None,
        description="Employee start date",
    )