from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.entities.users.registration import ClientRegistrationForm, WorkerRegistrationForm, RegisteredUser
from src.core.exceptions.client_error import ResourceAlreadyExistsError
from src.core.services.registration.registration import RegistrationService


@pytest.fixture
def client_repo():
    return AsyncMock()

@pytest.fixture
def worker_repo():
    return AsyncMock()

@pytest.fixture
def registration_service(client_repo, worker_repo):
    service = RegistrationService(client_repo, worker_repo)
    service.password_hasher = MagicMock()
    return service

@pytest.fixture
def client_registration_form():
    return ClientRegistrationForm(
        email="client@test.com",
        password="client_password",
        name="Иван",
        surname="Иванов"
    )

@pytest.fixture
def worker_registration_form():
    return WorkerRegistrationForm(
        email="worker@test.com",
        password="worker_password",
        name="Иван",
        surname="Иванов",
        phone="+71234567890",
        jobTitle="test"
    )

@pytest.mark.asyncio
async def test_register_client_success(registration_service, client_repo, client_registration_form):
    client_repo.exists_by_email.return_value = False
    client_repo.create.return_value = "new_client_id"
    registration_service.password_hasher.hash_password.return_value = "hashed_password"

    registered_user = await registration_service.register_client(client_registration_form)

    assert isinstance(registered_user, RegisteredUser)
    assert registered_user.user_id == "new_client_id"
    client_repo.exists_by_email.assert_called_once_with(client_registration_form.email)
    client_repo.create.assert_called_once()
    registration_service.password_hasher.hash_password.assert_called_once_with(password=client_registration_form.password)

@pytest.mark.asyncio
async def test_register_worker_success(registration_service, worker_repo, worker_registration_form):
    worker_repo.exists_by_email.return_value = False
    worker_repo.create.return_value = "new_worker_id"
    registration_service.password_hasher.hash_password.return_value = "hashed_password"

    registered_user = await registration_service.register_worker(worker_registration_form)

    assert isinstance(registered_user, RegisteredUser)
    assert registered_user.user_id == "new_worker_id"
    worker_repo.exists_by_email.assert_called_once_with(worker_registration_form.email)
    worker_repo.create.assert_called_once()
    registration_service.password_hasher.hash_password.assert_called_once_with(password=worker_registration_form.password)

@pytest.mark.asyncio
async def test_register_client_email_already_exists(registration_service, client_repo, client_registration_form):
    client_repo.exists_by_email.return_value = True

    with pytest.raises(ResourceAlreadyExistsError):
        await registration_service.register_client(client_registration_form)

    client_repo.exists_by_email.assert_called_once_with(client_registration_form.email)
    client_repo.create.assert_not_called()

@pytest.mark.asyncio
async def test_register_worker_email_already_exists(registration_service, worker_repo, worker_registration_form):
    worker_repo.exists_by_email.return_value = True

    with pytest.raises(ResourceAlreadyExistsError):
        await registration_service.register_worker(worker_registration_form)

    worker_repo.exists_by_email.assert_called_once_with(worker_registration_form.email)
    worker_repo.create.assert_not_called()
