from lib2to3.btm_utils import tokens

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.core.entities.users.client.client import ClientInDB
from src.core.entities.users.login import LoginForm, JWTTokens
from src.core.entities.users.worker.worker import WorkerInDB
from src.core.services.authentication.jwt.jwt_auth import JWTAuthentication
from src.core.exceptions.client_error import ResourceNotFoundError


@pytest.fixture
def mock_client_repo():
    client_repo = AsyncMock()
    client_repo.get_by_email.return_value = ClientInDB(
        id="1",
        email="client@test.com",
        password="hashed_password",
        name="test_name",
        surname="test_surname",
        phone=None,
        image=None
    )
    return client_repo

@pytest.fixture
def mock_worker_repo():
    worker_repo = AsyncMock()
    worker_repo.get_by_email.return_value = WorkerInDB(
        id="1",
        email="worker@test.com",
        password="hashed_password",
        name="test_name",
        surname="test_surname",
        phone="+71234567890",
        image=None,
        jobTitle="test_title"
    )
    return worker_repo

@pytest.fixture
def mock_jwt_manager():
    jwt_manager = MagicMock()
    jwt_manager.create_access_token.return_value = "mock_access_token"
    jwt_manager.create_refresh_token.return_value = "mock_refresh_token"
    return jwt_manager

@pytest.fixture
def mock_password_hasher():
    password_hasher = MagicMock()
    return password_hasher

@pytest.mark.asyncio
async def test_login_success_client(mock_client_repo, mock_worker_repo, mock_jwt_manager, mock_password_hasher):
    mock_client_repo.exists_by_email.return_value = True
    mock_password_hasher.verify_password.return_value = True

    jwt_auth = JWTAuthentication(mock_client_repo, mock_worker_repo, MagicMock())
    jwt_auth.password_hasher = mock_password_hasher
    jwt_auth.token_manager = mock_jwt_manager

    login_form = LoginForm(email="client@test.com", password="password")

    tokens = await jwt_auth.login(login_form)
    assert isinstance(tokens, JWTTokens)
    assert tokens.access_token == "mock_access_token"
    assert tokens.refresh_token == "mock_refresh_token"
    assert tokens.token_type == "bearer"

    mock_client_repo.exists_by_email.assert_called_once_with("client@test.com")
    mock_client_repo.get_by_email.assert_called_once_with("client@test.com")
    mock_worker_repo.exists_by_email.assert_not_called()
    mock_worker_repo.get_by_email.assert_not_called()

@pytest.mark.asyncio
async def test_login_success_worker(mock_client_repo, mock_worker_repo, mock_jwt_manager, mock_password_hasher):
    mock_client_repo.exists_by_email.return_value = False
    mock_worker_repo.exists_by_email.return_value = True
    mock_password_hasher.verify_password.return_value = True

    jwt_auth = JWTAuthentication(mock_client_repo, mock_worker_repo, MagicMock())
    jwt_auth.password_hasher = mock_password_hasher
    jwt_auth.token_manager = mock_jwt_manager

    login_form = LoginForm(email="worker@test.com", password="password")

    tokens = await jwt_auth.login(login_form)
    assert isinstance(tokens, JWTTokens)
    assert tokens.access_token == "mock_access_token"
    assert tokens.refresh_token == "mock_refresh_token"
    assert tokens.token_type == "bearer"

    mock_client_repo.exists_by_email.assert_called_once_with("worker@test.com")
    mock_client_repo.get_by_email.asser_not_called()
    mock_worker_repo.exists_by_email.assert_called_once_with("worker@test.com")
    mock_worker_repo.get_by_email.assert_called_once_with("worker@test.com")

@pytest.mark.asyncio
async def test_login_invalid_password_client(mock_client_repo, mock_worker_repo, mock_jwt_manager, mock_password_hasher):
    mock_client_repo.exists_by_email.return_value = True
    mock_password_hasher.verify_password.return_value = False

    jwt_auth = JWTAuthentication(mock_client_repo, mock_worker_repo, MagicMock())
    jwt_auth.password_hasher = mock_password_hasher
    jwt_auth.token_manager = mock_jwt_manager

    login_form = LoginForm(email="client@test.com", password="wrong_password")

    with pytest.raises(ResourceNotFoundError):
        await jwt_auth.login(login_form)

    mock_client_repo.exists_by_email.assert_called_once_with("client@test.com")
    mock_client_repo.get_by_email.assert_called_once_with("client@test.com")
    mock_worker_repo.exists_by_email.assert_not_called()

@pytest.mark.asyncio
async def test_login_invalid_password_worker(mock_client_repo, mock_worker_repo, mock_jwt_manager, mock_password_hasher):
    mock_client_repo.exists_by_email.return_value = False
    mock_worker_repo.exists_by_email.return_value = True
    mock_password_hasher.verify_password.return_value = False

    jwt_auth = JWTAuthentication(mock_client_repo, mock_worker_repo, MagicMock())
    jwt_auth.password_hasher = mock_password_hasher
    jwt_auth.token_manager = mock_jwt_manager

    login_form = LoginForm(email="worker@test.com", password="wrong_password")

    with pytest.raises(ResourceNotFoundError):
        await jwt_auth.login(login_form)

    mock_client_repo.exists_by_email.assert_called_once_with("worker@test.com")
    mock_client_repo.get_by_email.assert_not_called()
    mock_worker_repo.exists_by_email.assert_called_once_with("worker@test.com")
    mock_worker_repo.get_by_email.assert_called_once_with("worker@test.com")



@pytest.mark.asyncio
async def test_login_non_existent_credentials(mock_client_repo, mock_worker_repo):
    mock_client_repo.exists_by_email.return_value = False
    mock_worker_repo.exists_by_email.return_value = False

    jwt_auth = JWTAuthentication(mock_client_repo, mock_worker_repo, MagicMock())
    login_form = LoginForm(email="invalid@test.com", password="wrong_password")

    with pytest.raises(ResourceNotFoundError):
        await jwt_auth.login(login_form)

    mock_client_repo.exists_by_email.assert_called_once_with("invalid@test.com")
    mock_worker_repo.exists_by_email.assert_called_once_with("invalid@test.com")
    mock_client_repo.get_by_email.assert_not_called()
    mock_worker_repo.get_by_email.assert_not_called()