from pydantic import BaseModel, EmailStr, field_validator, Field

class ClientRegistrationForm(BaseModel):
    name: str = Field(
        ...,
        title="User's first name",
        min_length=1,
        max_length=100,
        description="The first name of the user, required for registration"
    )
    surname: str = Field(
        ...,
        title="User's last name",
        min_length=1,
        max_length=100,
        description="The last name of the user, required for registration"
    )
    email: EmailStr = Field(
        ...,
        title="User's email",
        min_length=1,
        max_length=100,
        description="The email of the user, must be in a valid email format, required for registration"
    )
    password: str = Field(
        ...,
        title="User's password",
        min_length=8,
        max_length=100,
        description="The password of the user, must be at least 8 characters long, required for registration"
    )

class WorkerRegistrationForm(ClientRegistrationForm):
    jobTitle: str = Field(
        ...,
        title="Worker's job title",
        description="The job title of the worker, required"
    )
    phone: str = Field(
        ...,
        title="Worker's phone number",
        pattern=r'^\+?[1-9]\d{1,14}$',
        description="The phone number of the worker, must be in international format"
    )

class RegisteredUser(BaseModel):
    message: str = Field(
        default="Registration successful"
    )
    user_id: str = Field(
        ...,
        title="User id of registered user"
    )