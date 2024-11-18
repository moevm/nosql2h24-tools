from pydantic import BaseModel


class RegisteredUserResponse(BaseModel):
    message: str
    user_id: str
