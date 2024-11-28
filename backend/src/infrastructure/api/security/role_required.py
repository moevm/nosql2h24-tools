from functools import wraps
from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.configs.config import config
from src.core.exceptions.client_error import JWTTokenMissing, InsufficientPermissionsError
from src.core.services.authentication.jwt.jwt_token_manager import JWTTokenManager



def role_required(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.get('token')

            if token is None:
                raise JWTTokenMissing()

            token_manager = JWTTokenManager(config.jwt)
            payload = token_manager.decode_access_token(token)

            if payload["role"] != role:
                raise InsufficientPermissionsError(details={"role_provided": payload["role"] ,"role_required": role})

            return await func(*args, **kwargs)
        return wrapper
    return decorator

