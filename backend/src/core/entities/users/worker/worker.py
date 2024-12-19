from bson import ObjectId
from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

from src.core.entities.object_id_str import ObjectIdStr
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

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True

class WorkerCreateDB(Worker):
    id: str = Field(
        ...,
        description="Unique identifier of the client in the db",
        alias="_id",
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

class WorkerPaginated(BaseModel):
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
    email: EmailStr = Field(
        ...,
        description="User's email",
        min_length=1,
        max_length=100,
    )
    jobTitle: str = Field(
        ...,
        description="Worker's job title"
    )
    date: datetime = Field(
        default=None,
        description="Employee start date",
    )

class PaginatedWorkersResponse(BaseModel):
    workers: List[WorkerPaginated] = Field(
        ...
    )
    totalNumber: int = Field(
        ...
    )