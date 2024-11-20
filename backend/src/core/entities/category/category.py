from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from bson import ObjectId
from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.type.type import TypeName


class CategoryName(BaseModel):
    name: str = Field(
        ...,
        title="Category name"
    ),

    class Config:
        json_encoders = {
            ObjectId: str,
        }

        allow_population_by_field_name = True

class Category(CategoryName):
    types: List[ObjectIdStr] = Field(
        default_factory=list,
        title="List of type ids associated with this category"
    )

class CategoryInDB(Category):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the category in the db"
    )

class CategoryCreated(BaseModel):
    message: str = Field(
        default="Category created successfully"
    )
    id: str = Field(
        ...,
        title="id of created category"
    )

class CategoryWithTypes(BaseModel):
    name: str
    types: List[TypeName]