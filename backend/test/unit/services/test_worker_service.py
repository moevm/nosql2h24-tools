from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from src.configs.paths import Paths
from src.configs.urls import Urls
import pytest
from src.core.entities.users.base_user import UpdateUser, UpdateUserPassword, UpdatedUser, UpdatedUserPassword
from src.core.entities.users.worker.worker import WorkerPrivateSummary
from src.core.exceptions.client_error import ResourceNotFoundError, InvalidPasswordProvided
from src.core.services.worker_service.worker_service import WorkerService



@pytest.fixture
def paths_config():
    return Paths()

@pytest.fixture
def urls_config():
    return Urls()

@pytest.fixture
def worker_repo():
    return AsyncMock()

@pytest.fixture
def img_decoder():
    mock_decoder = MagicMock()
    mock_decoder.decode_and_save_image.return_value = "image1.jpg"
    return mock_decoder

@pytest.fixture
def password_hasher():
    mock_hasher = MagicMock()
    return mock_hasher


@pytest.fixture
def worker_service(worker_repo, paths_config, urls_config, img_decoder, password_hasher):
    service = WorkerService(worker_repo, paths_config, urls_config)
    service.img_decoder = img_decoder
    service.bcrypt_password_hasher = password_hasher
    return service

@pytest.fixture
def worker_summaries():
    return [
        WorkerPrivateSummary(
            id="1",
            email="test1@example.com",
            name="test_name_1",
            surname="test_surname_1",
            phone="+71111111111",
            jobTitle="test_title_1",
            date=datetime.now(timezone.utc)
        ),
        WorkerPrivateSummary(
            id="2",
            email="test2@example.com",
            name="test_name_2",
            surname="test_surname_2",
            phone="+72222222222",
            jobTitle="test_title_2",
            date=datetime.now(timezone.utc)
        )
    ]

@pytest.fixture
def worker_summary():
    return WorkerPrivateSummary(
        id="1",
        email="test1@example.com",
        name="test_name_1",
        surname="test_surname_1",
        phone="+71111111111",
        jobTitle="test_title_1",
        date=datetime.now(timezone.utc)
    )

@pytest.fixture
def update_user_data():
    return UpdateUser(
        name="testName",
        surname="testSurname",
        phone="+72222222222",
        image="test_image"
    )

@pytest.fixture
def update_user_password_data():
    return UpdateUserPassword(
        current_password="123456789",
        new_password="987654321"
    )

@pytest.fixture
def updated_user_data():
    return UpdatedUser(
        user_id="1"
    )

@pytest.fixture
def updated_user_password_data():
    return UpdatedUserPassword(
        user_id="1"
    )

@pytest.mark.asyncio
async def test_get_all_workers_summary_success(worker_service, worker_repo, worker_summaries):
    worker_repo.get_all_workers_summary.return_value = worker_summaries

    result = await worker_service.get_all_workers_summary()

    assert result == worker_summaries

    worker_repo.get_all_workers_summary.assert_called_once_with()
    
@pytest.mark.asyncio
async def test_update_worker(worker_service, worker_repo, update_user_data, updated_user_data, img_decoder):
    worker_repo.exists_by_id.return_value = True
    worker_repo.update_worker.return_value = updated_user_data
    img_decoder.decode_and_save_image.return_value = "image1.jpg"
    img = update_user_data.image
    worker_id = "1"

    result = await worker_service.update_worker(worker_id, update_user_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == worker_id
    assert result.message == "Update successful"
    assert update_user_data.image == "image1.jpg"

    worker_repo.exists_by_id.assert_called_once_with(worker_id)
    img_decoder.decode_and_save_image.assert_called_once_with(img, worker_id)
    worker_repo.update_worker.assert_called_once_with(worker_id, update_user_data)

@pytest.mark.asyncio
async def test_update_worker_not_found(worker_service, worker_repo, update_user_data):
    worker_repo.exists_by_id.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await worker_service.update_worker("nonexistent_id", update_user_data)

    worker_repo.exists_by_id.assert_called_once_with("nonexistent_id")

@pytest.mark.asyncio
async def test_update_password(worker_service, worker_repo, update_user_password_data, updated_user_password_data, password_hasher):
    worker_id = "1"
    old_hashed_password = "old_hashed_password"
    new_hashed_password = "new_hashed_password"
    worker_repo.exists_by_id.return_value = True
    password_hasher.verify_password.return_value = True
    worker_repo.update_password.return_value = updated_user_password_data
    worker_repo.get_password_by_id.return_value = old_hashed_password
    password_hasher.hash_password.return_value = new_hashed_password

    result = await worker_service.update_password(worker_id, update_user_password_data)

    assert isinstance(result, UpdatedUserPassword)
    assert result.user_id == worker_id
    assert result.message == "Password updated successfully"

    worker_repo.exists_by_id.assert_called_once_with(worker_id)
    worker_repo.get_password_by_id.assert_called_once_with(worker_id)
    worker_repo.update_password.assert_called_once_with(worker_id, new_hashed_password)
    password_hasher.verify_password.assert_called_once_with(update_user_password_data.current_password, old_hashed_password)

@pytest.mark.asyncio
async def test_update_password_invalid_current_password(worker_service, worker_repo, update_user_password_data, updated_user_password_data, password_hasher):
    worker_id = "1"
    hashed_password = "hashed_password"
    worker_repo.exists_by_id.return_value = True
    password_hasher.verify_password.return_value = False
    worker_repo.get_password_by_id.return_value = hashed_password

    with pytest.raises(InvalidPasswordProvided):
        await worker_service.update_password(worker_id, update_user_password_data)


    worker_repo.exists_by_id.assert_called_once_with(worker_id)
    worker_repo.get_password_by_id.assert_called_once_with(worker_id)
    worker_repo.update_password.assert_not_called()
    password_hasher.verify_password.assert_called_once_with(update_user_password_data.current_password, hashed_password)

@pytest.mark.asyncio
async def test_update_password_not_found(worker_service, worker_repo, update_user_password_data, updated_user_password_data, password_hasher):
    worker_id = "1"
    worker_repo.exists_by_id.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await worker_service.update_password(worker_id, update_user_password_data)


    worker_repo.exists_by_id.assert_called_once_with(worker_id)
    worker_repo.get_password_by_id.assert_not_called()
    worker_repo.update_password.assert_not_called()
    password_hasher.verify_password.assert_not_called()

@pytest.mark.asyncio
async def test_get_private_worker_summary(worker_service, worker_repo, worker_summary):
    worker_id = "1"
    worker_repo.exists_by_id.return_value = True
    worker_repo.get_private_summary_by_id.return_value = worker_summary

    result = await worker_service.get_private_worker_summary(worker_id)

    assert isinstance(result, WorkerPrivateSummary)
    assert result == worker_summary

    worker_repo.exists_by_id.assert_called_once_with(worker_id)
    worker_repo.get_private_summary_by_id.assert_called_once_with(worker_id)

@pytest.mark.asyncio
async def test_get_private_worker_summary_not_found(worker_service, worker_repo):
    worker_id = "nonexistent_id"
    worker_repo.exists_by_id.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await worker_service.get_private_worker_summary(worker_id)

    worker_repo.exists_by_id.assert_called_once_with(worker_id)
    worker_repo.get_private_summary_by_id.assert_not_called()