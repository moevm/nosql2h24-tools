from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional
from src.core.entities.object_id_str import ObjectIdStr


class Review(BaseModel):
    toolId: ObjectIdStr = Field(
        ...,
        description="Reviewed tool id"
    )
    reviewerId: ObjectIdStr = Field(
        ...,
        description="Reviewer tool id"
    )
    rating: int = Field(
        ...,
        description="rating (from 1 to 5)",
        ge=1,
        le=5
    )
    date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Review creation date"
    )
    text: str = Field(
        ...,
        description="Review text",
        min_length=4,
        max_length=300
    )

class ReviewInDB(Review):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the review in the db"
    )

class ReviewCreate(Review):
    orderId: str = Field(
        ...,
        description="Order id"
    )
    toolId: str = Field(
        ...,
        description="Reviewed tool id"
    )
    reviewerId: str = Field(
        ...,
        description="Reviewer tool id"
    )
    rating: int = Field(
        ...,
        description="rating (from 1 to 5)",
        ge=1,
        le=5
    )
    date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Review creation date"
    )
    text: str = Field(
        ...,
        description="Review text",
        min_length=4,
        max_length=300
    )

class ReviewCreated(BaseModel):
    message: str = Field(
        default="Review created successfully"
    )
    review_id: str = Field(
        ...,
        description="Created review id"
    )

class ReviewSummary(BaseModel):
    reviewer_name: str = Field(
        ...,
        description="Reviewer name"
    )
    reviewer_surname: str = Field(
        ...,
        description="Reviewer surname"
    )
    rating: int = Field(
        ...,
        description="rating (from 1 to 5)",
        ge=1,
        le=5
    )
    date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Review creation date"
    )
    text: str = Field(
        ...,
        description="Review text",
        min_length=4,
        max_length=300
    )

class ReviewPaginated(ReviewSummary):
    tool_name: str = Field(
        ...,
        description="Tool name"
    )
