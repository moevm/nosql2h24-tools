from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from bson import ObjectId
from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.type.type import TypeName


class CategoryName(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$",
        description="Category name. Must be between 3 and 50 characters, and contain only letters (Latin or Cyrillic), numbers, and spaces."
    )

    class Config:
        json_encoders = {
            ObjectId: str,
        }

        allow_population_by_field_name = True

class Category(CategoryName):
    types: List[ObjectIdStr] = Field(
        default_factory=list,
        description="List of type ids associated with this category"
    )

class CategoryInDB(Category):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the category in the db"
    )

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True

class CategoryCreateDB(Category):
    id: str = Field(
        ...,
        description="Unique identifier of the order in the db",
        alias="_id",
    )

    types: List[str] = Field(
        ...,
        description="Unique identifier of the order in the db"
    )

class CategoryCreated(BaseModel):
    message: str = Field(
        default="Category created successfully"
    )
    id: str = Field(
        ...,
        description="id of created category"
    )

class CategoryWithTypes(BaseModel):
    name: str
    types: List[TypeName]