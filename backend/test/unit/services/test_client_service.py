from unittest.mock import AsyncMock, MagicMock
import pytest
from src.configs.paths import Paths
from src.configs.urls import Urls
from src.core.entities.users.base_user import UpdatedUser, UpdateUser, UpdateUserPassword, UpdatedUserPassword
from src.core.entities.users.client.client import ClientPrivateSummary
from src.core.exceptions.client_error import ResourceNotFoundError, InvalidPasswordProvided
from src.core.services.user_service.client_service import ClientService


@pytest.fixture
def paths_config():
    return Paths()

@pytest.fixture
def urls_config():
    return Urls()

@pytest.fixture
def client_repo():
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
def client_service(client_repo, paths_config, urls_config, img_decoder, password_hasher):
    service = ClientService(client_repo, paths_config, urls_config)
    service.img_decoder = img_decoder
    service.bcrypt_password_hasher = password_hasher
    return service

@pytest.fixture
def client_summaries():
    return [
        ClientPrivateSummary(
            id="1",
            email="test1@example.com",
            name="test_name_1",
            surname="test_surname_1",
            phone="+71111111111"
        ),
        ClientPrivateSummary(
            id="1",
            email="test2@example.com",
            name="test_name_2",
            surname="test_surname_2",
            phone="+72222222222"
        ),
    ]

@pytest.fixture
def client_summary():
    return ClientPrivateSummary(
        id="1",
        email="test1@example.com",
        name="test_name_1",
        surname="test_surname_1",
        phone="+71111111111"
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
async def test_get_all_clients_summary_success(client_service, client_repo, client_summaries):
    client_repo.get_all_clients_summary.return_value = client_summaries

    result = await client_service.get_all_clients_summary()

    assert result == client_summaries

    client_repo.get_all_clients_summary.assert_called_once_with()

@pytest.mark.asyncio
async def test_update_client(client_service, client_repo, update_user_data, updated_user_data, img_decoder):
    client_repo.exists_by_id.return_value = True
    client_repo.update_client.return_value = updated_user_data
    img_decoder.decode_and_save_image.return_value = "image1.jpg"
    img = update_user_data.image
    client_id = "1"

    result = await client_service.update_client(client_id, update_user_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == client_id
    assert result.message == "Update successful"
    assert update_user_data.image == "image1.jpg"

    client_repo.exists_by_id.assert_called_once_with(client_id)
    img_decoder.decode_and_save_image.assert_called_once_with(img, client_id)
    client_repo.update_client.assert_called_once_with(client_id, update_user_data)

@pytest.mark.asyncio
async def test_update_client_not_found(client_service, client_repo, update_user_data):
    client_repo.exists_by_id.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await client_service.update_client("nonexistent_id", update_user_data)

    client_repo.exists_by_id.assert_called_once_with("nonexistent_id")

@pytest.mark.asyncio
async def test_update_password(client_service, client_repo, update_user_password_data, updated_user_password_data, password_hasher):
    client_id = "1"
    old_hashed_password = "old_hashed_password"
    new_hashed_password = "new_hashed_password"
    client_repo.exists_by_id.return_value = True
    password_hasher.verify_password.return_value = True
    client_repo.update_password.return_value = updated_user_password_data
    client_repo.get_password_by_id.return_value = old_hashed_password
    password_hasher.hash_password.return_value = new_hashed_password

    result = await client_service.update_password(client_id, update_user_password_data)

    assert isinstance(result, UpdatedUserPassword)
    assert result.user_id == client_id
    assert result.message == "Password updated successfully"

    client_repo.exists_by_id.assert_called_once_with(client_id)
    client_repo.get_password_by_id.assert_called_once_with(client_id)
    client_repo.update_password.assert_called_once_with(client_id, new_hashed_password)
    password_hasher.verify_password.assert_called_once_with(update_user_password_data.current_password, old_hashed_password)

@pytest.mark.asyncio
async def test_update_password_invalid_current_password(client_service, client_repo, update_user_password_data, updated_user_password_data, password_hasher):
    client_id = "1"
    hashed_password = "hashed_password"
    client_repo.exists_by_id.return_value = True
    password_hasher.verify_password.return_value = False
    client_repo.get_password_by_id.return_value = hashed_password

    with pytest.raises(InvalidPasswordProvided):
        await client_service.update_password(client_id, update_user_password_data)


    client_repo.exists_by_id.assert_called_once_with(client_id)
    client_repo.get_password_by_id.assert_called_once_with(client_id)
    client_repo.update_password.assert_not_called()
    password_hasher.verify_password.assert_called_once_with(update_user_password_data.current_password, hashed_password)

@pytest.mark.asyncio
async def test_update_password_not_found(client_service, client_repo, update_user_password_data, updated_user_password_data, password_hasher):
    client_id = "1"
    client_repo.exists_by_id.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await client_service.update_password(client_id, update_user_password_data)


    client_repo.exists_by_id.assert_called_once_with(client_id)
    client_repo.get_password_by_id.assert_not_called()
    client_repo.update_password.assert_not_called()
    password_hasher.verify_password.assert_not_called()

@pytest.mark.asyncio
async def test_get_private_client_summary(client_service, client_repo, client_summary):
    client_id = "1"
    client_repo.exists_by_id.return_value = True
    client_repo.get_private_summary_by_id.return_value = client_summary

    result = await client_service.get_private_client_summary(client_id)

    assert isinstance(result, ClientPrivateSummary)
    assert result == client_summary

    client_repo.exists_by_id.assert_called_once_with(client_id)
    client_repo.get_private_summary_by_id.assert_called_once_with(client_id)

@pytest.mark.asyncio
async def test_get_private_client_summary_not_found(client_service, client_repo):
    client_id = "nonexistent_id"
    client_repo.exists_by_id.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await client_service.get_private_client_summary(client_id)

    client_repo.exists_by_id.assert_called_once_with(client_id)
    client_repo.get_private_summary_by_id.assert_not_called()