from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import List, Optional

from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.order.order import Order
from src.core.entities.users.BaseUser import BaseUser


class Worker(BaseUser):
    name: str = Field(
        ...,
        title="Worker's first name",
        min_length=1, max_length=100,
        description="The first name of the worker, required"
    )
    surname: str = Field(
        ...,
        title="Worker's last name",
        min_length=1,
        max_length=100,
        description="The last name of the worker, required"
    )
    phone: str = Field(
        ...,
        title="Worker's phone number",
        pattern=r'^\+?[1-9]\d{1,14}$',
        description="The phone number of the worker, must be in international format"
    )
    jobTitle: str = Field(
        ...,
        title="Worker's job title",
        description="The job title of the worker, required"
    )
    date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Employee start date",
        description="The start date of the employee"
    )
    orders: Optional[List[Order]] = Field(
        default_factory=list,
        description="The orders of the worker"
    )
    image: Optional[bytes] = Field(
        default=None,
        title="Worker's image",
        description="The image of the worker in binary format"
    )

class WorkerInDB(Worker):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the client in the db"
    )