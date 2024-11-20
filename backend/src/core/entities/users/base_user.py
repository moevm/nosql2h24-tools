from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from bson import ObjectId
from typing import List, Optional
from src.core.entities.object_id_str import ObjectIdStr


class BaseUser(BaseModel):
    email: EmailStr = Field(
        ...,
        title="Client's email",
        min_length=1,
        max_length=100,
        description="The email of the client, must be in a valid email format, required"
    )
    password: str = Field(
        ...,
        title="Worker's password",
        min_length=1,
        max_length=100,
        description="The password of the worker, must be at least 1 characters long, required"
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Client Creation Date", description="The timestamp when the client record was created"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Client Last Update Date",
        description="The timestamp when the client record was last updated"
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
        description="Unique identifier of the client in the db"
    )