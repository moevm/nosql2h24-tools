from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from src.core.entities.object_id_str import ObjectIdStr
from bson import ObjectId


class TypeSignature(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Zа-яА-Я0-9\s\-]+$",
        description="Type name. Must be between 3 and 50 characters, and contain only letters (Latin or Cyrillic), numbers, spaces, and hyphens."
    )
    category_name: str = Field(
        ...,
        description="Category name associated with this type "
    )

class Type(TypeSignature):
    tools: List[ObjectIdStr] = Field(
        default_factory=list,
        description="List of tools ids associated with this type"
    )

class TypeInDB(Type):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the type in the db"
    )

    class Config:
        json_encoders = {
            ObjectId: str,
        }

        allow_population_by_field_name = True

class TypeCreateDB(Type):
    id: str = Field(
        ...,
        description="Unique identifier of the order in the db",
        alias="_id",
    )

    tools: List[str] = Field(
        ...,
        description="List of tools ids associated with this type"
    )

class TypeCreated(BaseModel):
    message: str = Field(
        default="Type created successfully"
    )
    id: str = Field(
        ...,
        description="id of created type"
    )

class TypeName(BaseModel):
    name: str = Field(
        ...,
        description="Type name",
    )