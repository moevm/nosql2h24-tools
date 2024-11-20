from typing import Any
from .custom_error import CustomError

class ClientError(CustomError):
    def __init__(self, message: str, status_code: int = 400, details: Any = None):
        super().__init__(message, status_code, details)

class ResourceAlreadyExistsError(ClientError):
    def __init__(self, message: str, details: Any = None):
        super().__init__(message, status_code=409, details=details)

class ResourceNotFoundError(ClientError):
    def __init__(self, message: str, details: Any = None):
        super().__init__(message, status_code=404, details=details)

class JWTTokenExpiredError(ClientError):
    def __init__(self, message: str = "Token has expired", details: Any = None):
        super().__init__(message, status_code=401, details=details)

class JWTTokenInvalidError(ClientError):
    def __init__(self, message: str = "Invalid token", details: Any = None):
        super().__init__(message, status_code=401, details=details)

class JWTTokenDecodeError(ClientError):
    def __init__(self, message: str = "Failed to decode token", details: Any = None):
        super().__init__(message, status_code=400, details=details)

class JWTTokenMissing(ClientError):
    def __init__(self, message: str = "Token missing", details: Any = None):
        super().__init__(message, status_code=401, details=details)

class InsufficientPermissionsError(ClientError):
    def __init__(self, message: str = "Forbidden: insufficient permissions", details: Any = None):
        super().__init__(message, status_code=403, details=details)