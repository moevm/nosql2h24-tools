from pydantic import Field
from typing import List, Optional

from src.core.entities.order.order import Order
from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.users.base_user import BaseUser, BaseUserPrivateSummary


class Client(BaseUser):
    name: str = Field(
        ...,
        description="Client's first name"
    )
    surname: str = Field(
        ...,
        description="Client's last name",
    )
    orders: Optional[List[Order]] = Field(
        default_factory=list,
        description="A list of orders made by the client"
    )
    phone: Optional[str] = Field(
        None,
        description="Client's phone number"
    )
    image: Optional[str] = Field(
        None,
        description="Client's image url"
    )

class ClientInDB(Client):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the client in the db"
    )

class ClientPrivateSummary(BaseUserPrivateSummary):
    pass