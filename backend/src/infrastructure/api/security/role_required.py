from src.configs.config import config
from src.core.exceptions.client_error import JWTTokenMissing, InsufficientPermissionsError
from src.core.services.authentication.jwt.jwt_token_manager import JWTTokenManager


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

