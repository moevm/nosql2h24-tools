
from pydantic import Field
from datetime import datetime
from typing import List, Optional

from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.order.order import Order
from src.core.entities.users.base_user import BaseUser, BaseUserPrivateSummary


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

class WorkerPrivateSummary(BaseUserPrivateSummary):
    jobTitle: str = Field(
        ...,
        description="Worker's job title",
    )
    date: datetime = Field(
        default=None,
        description="Employee start date",
    )