from datetime import datetime, timezone
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from src.core.entities.object_id_str import ObjectIdStr


class Order(BaseModel):
    tools: List[ObjectIdStr] = Field(
        default=None,
        description="list of ids of tools"
    )
    start_leasing: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="start of leasing tools"
    )
    end_leasing: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="end of leasing"
    )
    price: float = Field(
        default=None,
        description="price of leasing"
    )
    client: ObjectIdStr = Field(
        default=None,
        description="client who ordered"
    )
    delivery_type: str = Field(
        default=None,
        description="delivery type (to door, at pickup point)"
    )
    delivery_state: str = Field(
        default=None,
        description="delivery state (accepted, on the way, delivered)"
    )
    payment_type: str = Field(
        default=None,
        description="payment type (cash, card)"
    )
    payment_state: str = Field(
        default=None,
        description="payment state (paid, not paid)"
    )
    create_order_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="create order time"
    )
    related_worker: ObjectIdStr = Field(
        default=None, 
        description="related worker id"
    )

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

        allow_population_by_field_name = True

class OrderCreate(BaseModel):
    tools: List[ObjectIdStr] = Field(
        ...,
        max_length=50,
        min_length=1,
        description="Order tools, must contain at least 1 tool"
    )
    start_leasing: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="start of leasing tools"
    )
    end_leasing: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="end of leasing"
    )
    client: ObjectIdStr = Field(
        ...,
        description="client who ordered"
    )
    delivery_type: str = Field(
        ...,
        description="delivery type (to door, at pickup point)"
    )
    delivery_state: str = Field(
        ...,
        description="delivery state (accepted, on the way, delivered)"
    )
    payment_type: str = Field(
        ...,
        description="payment type (cash, card)"
    )
    payment_state: str = Field(
        ...,
        description="payment state (paid, not paid)"
    )
    

class OrderCreated(BaseModel):
    message: str = Field(
        default="Order created successfully"
    )
    order_id: str = Field(
        ...,
        description="ID of created order"
    )