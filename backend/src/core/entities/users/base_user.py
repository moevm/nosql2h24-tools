from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from bson import ObjectId
from typing import List, Optional
from src.core.entities.object_id_str import ObjectIdStr


class BaseUser(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's email",
    )
    password: str = Field(
        ...,
        description="User's password",
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="User Creation Date"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="User Last Update Date",
    )

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

        allow_population_by_field_name = True

class BaseUserInDB(BaseUser):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the user in the db"
    )

class BaseUserSummary(BaseModel):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the user in the db"
    )
    email: EmailStr = Field(
        ...,
        description="User's email",
        min_length=1,
        max_length=100,
    )
    name: str = Field(
        ...,
        description="User's first name"
    )
    surname: str = Field(
        ...,
        description="User's last name",
    )
    phone: str = Field(
        ...,
        description="User's phone number",
    )
    image: Optional[str] = Field(
        default=None,
        description="User's image url",
    )

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True

