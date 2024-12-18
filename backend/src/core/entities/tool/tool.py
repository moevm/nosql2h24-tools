from datetime import datetime, timezone
from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Optional
from bson import ObjectId
from src.core.entities.object_id_str import ObjectIdStr


class Tool(BaseModel):
    name: str = Field(
        ...,
        description="tool name"
    )
    dailyPrice: float = Field(
        default=None,
        description="Rental price per day"
    )
    totalPrice: float = Field(
        default=None,
        description="Tool type"
    )
    images: List[str] = Field(
        default=None,
        description="Tool image list"
    )
    features: Dict[str, str] = Field(
        default=None,
        description="Tool features dictionary"
    )
    rating: float = Field(
        default=0.0,
        description="Average tool rating"
    )
    reviews_count: int = Field(
        default=0
    )
    ordersNumber: int = Field(
        default=0,
        description="Total number of orders"
    )
    category: str = Field(
        default=None,
        description="Tool category"
    )
    type: str = Field(
        default=None,
        title="Tool type"
    )
    description: str = Field(
        default=None,
        title="Tool description"
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Client Creation Date"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Client Last Update Date"
    )

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

        allow_population_by_field_name = True


class ToolInDB(Tool):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the tool in the db"
    )

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True

class ToolCreateDB(Tool):
    id: str = Field(
        ...,
        description="Unique identifier of the tool in the db",
        alias="_id",
    )

class ToolSummary(BaseModel):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the tool in the db"
    )
    name: str = Field(
        ...,
        description="tool name"
    )
    dailyPrice: float = Field(
        ...,
        description="Rental price per day"
    )
    images: List[str] = Field(
        ...,
        description="Tool image list"
    )
    rating: float = Field(
        ...,
        description="Average tool rating"
    )
    description: str = Field(
        ...,
        description="Tool description"
    )

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True


class ToolDetails(ToolSummary):
    features: Dict[str, str] = Field(
        ...,
        description="Tool features dictionary"
    )
    category: str = Field(
        ...,
        description="Tool category"
    )
    type: str = Field(
        ...,
        description="Tool type"
    )


class ToolCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$",
        description="Tool name. Must be between 3 and 100 characters, and contain only letters (Latin or Cyrillic), numbers, spaces, and hyphens."
    )
    dailyPrice: float = Field(
        ...,
        gt=0,
        description="Rental price per day. Must be greater than 0."
    )
    totalPrice: float = Field(
        ...,
        gt=0,
        description="Total price. Must be greater than 0."
    )
    images: List[str] = Field(
        default_factory=list,
        description="Tool image list in base64 strings. Maximum of 10 images."
    )
    features: Dict[str, str] = Field(
        ...,
        description="Tool features dictionary. Keys and values must be non-empty strings."
    )
    category: str = Field(
        ...,
        description="Tool category. Must be one of the predefined categories."
    )
    type: str = Field(
        ...,
        description="Tool type. Must be one of the predefined types."
    )
    description: str = Field(
        ...,
        description="Tool description"
    )

    @model_validator(mode="before")
    def validate_images(cls, values):
        images = values.get('images')
        if images:
            if len(images) > 10:
                raise ValueError("No more than 10 images are allowed.")
        return values

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True

class ToolCreated(BaseModel):
    message: str = Field(
        default="Tool created successfully"
    )
    tool_id: str = Field(
        ...,
        description="Created tool id"
    )

class ToolPages(BaseModel):
    pages: int = Field(
        ...,
        description="count of pages"
    )

class PaginatedToolsResponse(BaseModel):
    tools: List[ToolSummary] = Field(
        ...
    )
    totalNumber: int = Field(
        ...
    )

