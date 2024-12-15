from .custom_error import CustomError
from typing import Any

class ServerError(CustomError):
    def __init__(self, message: str, status_code: int = 500, details: Any = None):
        super().__init__(message, status_code, details)

class DatabaseError(ServerError):
    def __init__(self, message: str = "A database error occurred", details: Any = None):
        super().__init__(message, status_code=500, details=details)

class MappingToStrError(ServerError):
    def __init__(self, message: str = "Internal server error", details: Any = None):
        super().__init__(message, status_code=500, details=details)

class ImageProcessingError(ServerError):
    def __init__(self, message: str = "Error processing image", details: Any = None):
        super().__init__(message, status_code=500, details=details)

class DirectoryCreationError(ServerError):
    def __init__(self, message: str = "Error creating directory", details: Any = None):
        super().__init__(message, status_code=500, details=details)