from pydantic import BaseModel, EmailStr, Field


class LoginForm(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's email",
    )
    password: str = Field(
        ...,
        description="User's password"
    )

class JWTTokens(BaseModel):
    access_token: str = Field(
        ...
    )
    refresh_token: str = Field(
        ...
    )
    token_type: str = Field(
        default="bearer"
    )

class JWTAccessToken(BaseModel):
    access_token: str = Field(
        ...
    )
    token_type: str = Field(
        default="bearer"
    )

class JWTRefreshToken(BaseModel):
    refresh_token: str = Field(
        ...
    )