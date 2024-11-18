from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        title="User's email",
        description="The email of the user, must be in a valid email format, required"
    )
    password: str = Field(
        ...,
        title="User's password",
        min_length=8,
        max_length=100,
        description="The password of the user, must be at least 8 characters long, required for login"
    )
