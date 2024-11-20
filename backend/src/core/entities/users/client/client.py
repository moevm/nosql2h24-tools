from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.order.order import Order
from src.core.entities.users.base_user import BaseUser


class Client(BaseUser):
    name: str = Field(
        ...,
        title="Client's first name",
        min_length=1,
        max_length=100,
        description="The first name of the client, required"
    )
    surname: str = Field(
        ...,
        title="Client's last name",
        min_length=1,
        max_length=100,
        description="The last name of the client, required"
    )
    orders: Optional[List[Order]] = Field(
        default_factory=list,
        description="A list of orders made by the client"
    )
    phone: Optional[str] = Field(
        None,
        title="Client's phone number",
        pattern=r'^\+?[1-9]\d{1,14}$',
        description="The phone number of the client, must be in international format"
    )
    image: Optional[str] = Field(
        None,
        title="Client's image url",
        description="The image of the client in"
    )

class ClientInDB(Client):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the client in the db"
    )