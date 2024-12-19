from bson import ObjectId
from pydantic import Field, BaseModel
from typing import List, Optional


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

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True

class ClientCreateDB(Client):
    id: str = Field(
        ...,
        description="Unique identifier of the client in the db",
        alias="_id",
    )

class ClientForWorker(BaseModel):
    id: Optional[ObjectIdStr] = Field(
        ...,
        default_factory=ObjectIdStr,
        alias="_id",
        description="Unique identifier of the client in the db"
    )
    name: str = Field(
        ...,
        description="Client's first name"
    )
    surname: str = Field(
        ...,
        description="Client's last name",
    )

    class Config:
        json_encoders = {
            ObjectId: str
        }

        allow_population_by_field_name = True

class ClientPrivateSummary(BaseUserPrivateSummary):
    pass

class ClientFullName(BaseModel):
    name: str = Field(
        ...,
        description="Client's first name"
    )
    surname: str = Field(
        ...,
        description="Client's last name",
    )