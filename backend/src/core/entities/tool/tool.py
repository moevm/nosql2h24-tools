from datetime import datetime, timezone
from pydantic import BaseModel, Field
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
    reviews: List[ObjectIdStr] = Field(
        default=None,
        description="List of review identifiers for this tool from the review collection"
    )
    rating: float = Field(
        default=0.0,
        description="Average tool rating"
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
        description="tool name"
    )
    dailyPrice: float = Field(
        ...,
        description="Rental price per day"
    )
    totalPrice: float = Field(
        ...,
        description="Tool type"
    )
    images: List[str] = Field(
        default_factory=list,
        description="Tool image list in base64 strings"
    )
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
    description: str = Field(
        ...,
        description="Tool description"
    )


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



