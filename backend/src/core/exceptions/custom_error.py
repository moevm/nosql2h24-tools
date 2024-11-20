from typing import Any

class CustomError(Exception):
    def __init__(self, message: str, status_code: int, details: Any = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details