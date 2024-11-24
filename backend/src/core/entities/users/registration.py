from pydantic import BaseModel, EmailStr, field_validator, Field

class ClientRegistrationForm(BaseModel):
    name: str = Field(
        ...,
        description="User's first name"
    )
    surname: str = Field(
        ...,
        description="User's last name"
    )
    email: EmailStr = Field(
        ...,
        description="User's email"
    )
    password: str = Field(
        ...,
        description="User's password"
    )

class WorkerRegistrationForm(ClientRegistrationForm):
    jobTitle: str = Field(
        ...,
        description="Worker's job title"
    )
    phone: str = Field(
        ...,
        description="Worker's phone number"
    )

class RegisteredUser(BaseModel):
    message: str = Field(
        default="Registration successful"
    )
    user_id: str = Field(
        ...,
        description="id of registered user"
    )