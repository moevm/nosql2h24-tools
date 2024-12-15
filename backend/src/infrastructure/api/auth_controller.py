from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from src.core.entities.users.login import LoginForm, JWTTokens, JWTRefreshToken
from src.core.services.authentication.jwt.jwt_auth import JWTAuthentication
from src.core.services.registration.registration import RegistrationService
from src.core.entities.users.login import JWTAccessToken
from src.core.entities.users.registration import ClientRegistrationForm, WorkerRegistrationForm, RegisteredUser
from src.infrastructure.api.security.role_required import is_worker
from src.infrastructure.services_instances import get_jwt_authenticator, get_registration_service

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@auth_router.post(
    "/token",
    status_code=200,
    response_model=JWTAccessToken
)
async def login(
        data: LoginForm,
        auth_service: JWTAuthentication = Depends(get_jwt_authenticator)
):
        result = await auth_service.login(login_request=data)
        response = JSONResponse(content={
            "access_token": result.access_token,
            "token_type": result.token_type
        })

        response.set_cookie(
            key="refresh_token",
            value=result.refresh_token,
            httponly=True,
            samesite="strict"
        )

        return response


@auth_router.post(
    "/token/refresh",
    status_code=200,
    response_model=JWTAccessToken
)
async def refresh_access_token(
        refresh_token: JWTRefreshToken,
        auth_service: JWTAuthentication = Depends(get_jwt_authenticator)
):
        return auth_service.refresh_access_token(refresh_token.refresh_token)


@auth_router.post(
    "/register/client",
    status_code=201,
    response_model=RegisteredUser
)
async def registrate_client(
        registration_data: ClientRegistrationForm,
        registration_service: RegistrationService = Depends(get_registration_service)
):
        return await registration_service.register_client(registration_data)


@auth_router.post(
    "/register/worker",
    status_code=201,
    response_model=RegisteredUser
)
async def registrate_worker(
        registration_data: WorkerRegistrationForm,
        registration_service: RegistrationService = Depends(get_registration_service),
        token: str = Depends(oauth2_scheme)
):
        is_worker(token)
        return await registration_service.register_worker(registration_data)