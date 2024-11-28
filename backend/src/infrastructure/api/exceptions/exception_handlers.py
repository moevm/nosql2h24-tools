from src.core.exceptions.custom_error import CustomError
from fastapi import Request
from fastapi.responses import JSONResponse, Response

def custom_error_handler(request: Request, exception: CustomError) -> Response:
    return JSONResponse(
        status_code=exception.status_code,
        content={"message": exception.message, "details": exception.details or {}}
    )

def unexpected_error_handler(request: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"}
    )