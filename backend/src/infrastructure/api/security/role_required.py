from functools import wraps
from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.configs.config import config
from src.core.exceptions.client_error import JWTTokenMissing, InsufficientPermissionsError
from src.core.exceptions.server_error import ServerError
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

            if role == 'self':
                client_id = kwargs.get('user_id')
                if client_id != payload["sub"]:
                    raise InsufficientPermissionsError(details={"role_required": 'self'})
            elif role == 'worker':
                if payload["role"] != role:
                    raise InsufficientPermissionsError(details={"role_provided": payload["role"] ,"role_required": role})
            else:
                raise ServerError("Internal server error")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def is_worker(token: str):
    if token is None:
        raise JWTTokenMissing()

    token_manager = JWTTokenManager(config.jwt)
    payload = token_manager.decode_access_token(token)

    if payload["role"] != "worker":
        raise InsufficientPermissionsError(
            details={"role_provided": payload["role"],
                     "role_required": "worker"}
        )

def is_self(token: str, user_id: str):
    if token is None:
        raise JWTTokenMissing()

    token_manager = JWTTokenManager(config.jwt)
    payload = token_manager.decode_access_token(token)

    if payload["sub"] != user_id:
        raise InsufficientPermissionsError(details={"role_required": 'self'})

