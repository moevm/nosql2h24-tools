from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.core.entities.auth.login_request import LoginRequest
from src.core.entities.auth.registration_request import ClientRegistrationRequest, WorkerRegistrationRequest
from src.core.services.authentication.jwt.jwt_auth import JWTAuthentication
from src.core.services.registration.registration import RegistrationService
from src.infrastructure.api.response_models.registered_user_response import RegisteredUserResponse
from src.infrastructure.api.response_models.token_response import TokenResponse
from src.infrastructure.api.security.required_role import role_required
from src.infrastructure.factories import get_jwt_authenticator, get_registration_service

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@auth_router.post(
    "/token",
    status_code=200,
    response_model=TokenResponse
)
async def login(
        data: LoginRequest,
        auth_service: JWTAuthentication = Depends(get_jwt_authenticator)
):
    try:
        result = await auth_service.login(login_request=data)
        response = JSONResponse(content={
            "access_token": result["access_token"],
            "token_type": result["token_type"]
        })
        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            samesite="strict"
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post(
    "/token/refresh",
    status_code=200,
    response_model=TokenResponse
)
async def refresh_access_token(
        refresh_token: str,
        auth_service: JWTAuthentication = Depends(get_jwt_authenticator)
):
    try:
        new_access_token = auth_service.refresh_access_token(refresh_token)
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post(
    "/register/client",
    status_code=201,
    response_model=RegisteredUserResponse
)
async def registrate_client(
        registration_data: ClientRegistrationRequest,
        registration_service: RegistrationService = Depends(get_registration_service)
):
    try:
        new_client_id = await registration_service.register_client(registration_data)
        return {
            "message": "Registration successful",
            "user_id": new_client_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post(
    "register/worker",
    status_code=201,
    response_model=RegisteredUserResponse
)
@role_required('worker')
async def registrate_worker(
        registration_data: WorkerRegistrationRequest,
        registration_service: RegistrationService = Depends(get_registration_service),
        token: str = Depends(oauth2_scheme)
):
    try:
        new_worker_id = await registration_service.register_worker(registration_data)
        return {
            "message": "Registration successful",
            "user_id": new_worker_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))