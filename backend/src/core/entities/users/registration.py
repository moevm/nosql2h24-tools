from pydantic import BaseModel, EmailStr, field_validator, Field

class ClientRegistrationForm(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ]+$",
        description="User's first name. Must be between 2 and 50 characters and contain only letters"
    )
    surname: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ]+$",
        description="User's last name. Must be between 2 and 50 characters and contain only letters"
    )
    email: EmailStr = Field(
        ...,
        description="User's email"
    )
    password: str = Field(
        ...,
        min_length=5,
        max_length=128,
        description="User's password. Must be at least 5 characters long and include a mix of letters, numbers, and special characters."
    )

class WorkerRegistrationForm(ClientRegistrationForm):
    jobTitle: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Worker's job title. Must be between 3 and 50 characters."
    )
    phone: str = Field(
        ...,
        pattern=r"^\+?[1-9]\d{1,14}$",
        description="Worker's phone number in international format (e.g., +123456789)."
    )

class RegisteredUser(BaseModel):
    message: str = Field(
        default="Registration successful"
    )
    user_id: str = Field(
        ...,
        description="id of registered user"
    )