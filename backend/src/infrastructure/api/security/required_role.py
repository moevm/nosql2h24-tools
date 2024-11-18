from functools import wraps
from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.configs.config import config
from src.core.services.authentication.jwt.jwt_token_manager import JWTTokenManager



def role_required(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.get('token')
            print(token)
            if token is None:
                raise HTTPException(status_code=403, detail="Token is missing")

            token_manager = JWTTokenManager(config.jwt)

            try:
                payload = token_manager.decode_access_token(token)
                print(payload)
            except ValueError as e:
                raise HTTPException(status_code=403, detail=str(e))

            if payload["role"] != role:
                raise HTTPException(status_code=403, detail="Forbidden: insufficient permissions")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

