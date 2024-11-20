from datetime import datetime, timezone, timedelta
import jwt
from src.configs.jwt_config import JWTConfig
from typing import Dict, Union
from src.core.exceptions.client_error import JWTTokenExpiredError, JWTTokenInvalidError, JWTTokenDecodeError

class JWTTokenManager:
    def __init__(self, config: JWTConfig):
        self.config = config

    def create_access_token(self, payload: Dict) -> str:
        to_encode = payload.copy()
        expires_delta = timedelta(minutes=self.config.jwt_access_token_expire_minutes)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.config.jwt_access_secret_key, algorithm=self.config.jwt_algorithm)

    def create_refresh_token(self, payload: Dict) -> str:
        to_encode = payload.copy()
        expires_delta = timedelta(days=self.config.jwt_refresh_token_expire_days)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.config.jwt_refresh_secret_key, algorithm=self.config.jwt_algorithm)

    def decode_refresh_token(self, token: str) -> Dict:
        try:
            payload = jwt.decode(token, self.config.jwt_refresh_secret_key,
                                 algorithms=[self.config.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise JWTTokenExpiredError("Refresh token has expired")
        except jwt.InvalidTokenError:
            raise JWTTokenInvalidError("Invalid refresh token")
        except jwt.PyJWTError:
            raise JWTTokenDecodeError("Failed to decode the refresh token")

    def decode_access_token(self, token: str) -> Dict:
        try:
            payload = jwt.decode(token, self.config.jwt_access_secret_key, algorithms=[self.config.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise JWTTokenExpiredError("Access token has expired")
        except jwt.InvalidTokenError:
            raise JWTTokenInvalidError("Invalid access token")
        except jwt.PyJWTError:
            raise JWTTokenDecodeError("Failed to decode the access token")

    def refresh_access_token(self, refresh_token: str) -> str:
        payload = self.decode_refresh_token(refresh_token)
        user_data = {"sub": payload["sub"], "role": payload["role"]}
        return self.create_access_token(payload=user_data)