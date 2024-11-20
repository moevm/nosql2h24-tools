from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from bson import ObjectId
from src.core.entities.object_id_str import ObjectIdStr


class Tool(BaseModel):
    name: str = Field(
        ...,
        title="tool name"
    )
    dailyPrice: float = Field(
        default=None,
        title="Rental price per day"
    )
    totalPrice: float = Field(
        default=None,
        title="Tool type"
    )
    images: List[str] = Field(
        default=None,
        title="Tool image list"
    )
    features: Dict[str, str] = Field(
        default=None,
        title="Tool features dictionary"
    )
    reviews: List[ObjectIdStr] = Field(
        default=None,
        title="List of review identifiers for this tool from the review collection"
    )
    rating: float = Field(
        default=0.0,
        title="Average tool rating"
    )
    ordersNumber: int = Field(
        default=0,
        title="Total number of orders"
    )
    category: str = Field(
        default=None,
        title="Tool category"
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
        title="tool name"
    )
    dailyPrice: float = Field(
        ...,
        title="Rental price per day"
    )
    images: List[str] = Field(
        ...,
        title="Tool image list"
    )
    rating: float = Field(
        ...,
        title="Average tool rating"
    )

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True


class ToolDetails(ToolSummary):
    features: Dict[str, str] = Field(
        ...,
        title="Tool features dictionary"
    )
    category: str = Field(
        ...,
        title="Tool category"
    )
    type: str = Field(
        ...,
        title="Tool type"
    )
    description: str = Field(
        ...,
        title="Tool description"
    )

class ToolCreate(BaseModel):
    name: str = Field(
        ...,
        title="tool name"
    )
    dailyPrice: float = Field(
        ...,
        title="Rental price per day"
    )
    totalPrice: float = Field(
        ...,
        title="Tool type"
    )
    images: List[str] = Field(
        default_factory=list,
        title="Tool image list in base64 strings"
    )
    features: Dict[str, str] = Field(
        ...,
        title="Tool features dictionary"
    )
    category: str = Field(
        ...,
        title="Tool category"
    )
    type: str = Field(
        ...,
        title="Tool type"
    )
    description: str = Field(
        ...,
        title="Tool description"
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
        title="Created tool id"
    )

class ToolPages(BaseModel):
    pages: int = Field(
        ...,
        title="count of pages"
    )



