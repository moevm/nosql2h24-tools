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

class BaseUserPrivateSummary(BaseModel):
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
    phone: Optional[str] = Field(
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



class UpdateUser(BaseModel):
    name: str = Field(
        None,
        description="User's first name. Must be between 2 and 20 characters and contain only letters",
        pattern=r"^[a-zA-Zа-яА-ЯёЁ]+$",
        min_length=2,
        max_length=20

    )
    surname: str = Field(
        None,
        description="User's last name. Must be between 2 and 20 characters and contain only letters",
        pattern=r"^[a-zA-Zа-яА-ЯёЁ]+$",
        min_length=2,
        max_length=20
    )
    phone: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{1,14}$",
        description="User's phone number in international format (e.g., +123456789)."
    )
    image: str = Field(
        None,
        description="User's image, base64 string."
    )


class UpdatedUser(BaseModel):
    message: str = Field(
        default="Update successful"
    )
    user_id: str = Field(
        ...,
        description="id of updated user"
    )


class UpdateUserPassword(BaseModel):
    current_password: str = Field(
        ...,
        description="Current user's password"
    )
    new_password: str = Field(
        ...,
        description="New user's password"
    )


class UpdatedUserPassword(BaseModel):
    message: str = Field(
        default="Password updated successfully"
    )
    user_id: str = Field(
        ...,
        description="id of updated user"
    )