from unittest.mock import AsyncMock
from bson import ObjectId
import pytest, pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.configs.config import config
from pymongo.errors import PyMongoError
from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdateUserPassword, UpdatedUserPassword
from src.core.entities.users.client.client import Client, ClientInDB, ClientPrivateSummary
from src.core.exceptions.server_error import DatabaseError
from src.infrastructure.api.client_controller import update_client
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId, objectId_to_str
from src.infrastructure.repo_implementations.users_repos.client_repos.mongo_client_repository import \
    MongoClientRepository


@pytest_asyncio.fixture(scope='function')
async def db():
    client = AsyncIOMotorClient(str(config.mongo.mongo_dsn))
    database = client[config.mongo.mongo_db]

    await database.drop_collection(config.collections.client_collection)

    yield database

    await database.drop_collection(config.collections.client_collection)
    client.close()

@pytest_asyncio.fixture(scope='function')
async def client_repo(db):
    return MongoClientRepository(db, config.collections.client_collection)

@pytest.fixture
def client():
    return Client(
        email="test_client@example.com",
        password="hashed_password",
        name="testName",
        surname="testSurname",
        phone="+71234567890"
    )

@pytest.mark.asyncio
async def test_create_client_success(client_repo, client):
    client_id = await client_repo.create(client)

    assert isinstance(client_id, str)

    saved_client = await client_repo.client_collection.find_one({"_id": str_to_objectId(client_id)})

    assert saved_client is not None
    assert objectId_to_str(saved_client["_id"]) == client_id
    assert saved_client["email"] == client.email
    assert saved_client["password"] == client.password
    assert saved_client["name"] == client.name
    assert saved_client["surname"] == client.surname
    assert saved_client["phone"] == client.phone
    assert saved_client["image"] is None

@pytest.mark.asyncio
async def test_create_client_database_error(client_repo, client, monkeypatch):
    async def mock_insert_one(*args, **kwargs):
        raise PyMongoError("Mocked insertion error")

    monkeypatch.setattr(client_repo.client_collection, 'insert_one', mock_insert_one)

    with pytest.raises(DatabaseError):
        await client_repo.create(client)

@pytest.mark.asyncio
async def test_get_by_email_success(client_repo, client):
    await client_repo.create(client)

    client_in_db = await client_repo.get_by_email(client.email)

    assert isinstance(client_in_db, ClientInDB)

    assert client_in_db.email == client.email
    assert client_in_db.password == client.password
    assert client_in_db.name == client.name
    assert client_in_db.surname == client.surname
    assert client_in_db.phone == client.phone
    assert client_in_db.image is None


@pytest.mark.asyncio
async def test_get_by_email_database_error(client_repo, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked find error")

    monkeypatch.setattr(client_repo.client_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await client_repo.get_by_email("test@example.com")

@pytest.mark.asyncio
async def test_exists_true(client_repo, client):
    await client_repo.create(client)
    exists = await client_repo.exists_by_email(client.email)
    assert exists is True

@pytest.mark.asyncio
async def test_exists_false(client_repo):
    exists = await client_repo.exists_by_email("nonexistent@example.com")
    assert exists is False

@pytest.mark.asyncio
async def test_exists_database_error(client_repo, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked exists error")

    monkeypatch.setattr(client_repo.client_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await client_repo.exists_by_email("test@example.com")

@pytest.mark.asyncio
async def test_get_all_clients_summary(client_repo):
    client_count = 9

    clients = [
        Client(
            email=f"test_worker_{i}@example.com",
            password=f"hashed_password{i}",
            name=f"test_user_{i}",
            surname=f"test_surname_{i}",
            phone=f"+7000000000{i}",
        ) for i in range(client_count)
    ]

    for client in clients:
        await client_repo.create(client)

    summaries = await client_repo.get_all_clients_summary()
    assert len(summaries) == client_count

    for i in range(client_count):
        assert summaries[i].email == clients[i].email
        assert summaries[i].name == clients[i].name
        assert summaries[i].surname == clients[i].surname
        assert summaries[i].phone == clients[i].phone
        assert summaries[i].image == clients[i].image


@pytest.mark.asyncio
async def test_get_all_clients_summary_empty(client_repo):
    summaries = await client_repo.get_all_clients_summary()
    assert summaries == []

@pytest.mark.asyncio
async def test_get_all_clients_summary_database_error(client_repo, monkeypatch):
    mock_cursor = AsyncMock()
    mock_cursor.to_list.side_effect = PyMongoError("Mocked to_list error")

    def mock_find(*args, **kwargs):
        return mock_cursor

    monkeypatch.setattr(client_repo.client_collection, 'find', mock_find)

    with pytest.raises(DatabaseError):
        await client_repo.get_all_clients_summary()

@pytest.mark.asyncio
async def test_update_client_all(client_repo, client):
    client_id = await client_repo.create(client)

    update_data = UpdateUser(
        name="newName",
        surname="newSurname",
        phone="+79876543210",
        image="new_image.jpg"
    )

    result = await client_repo.update_client(client_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == client_id

    updated_client = await client_repo.get_by_email(client.email)

    assert isinstance(updated_client, ClientInDB)
    assert str(updated_client.id) == client_id
    assert updated_client.email == client.email
    assert updated_client.name == update_data.name
    assert updated_client.surname == update_data.surname
    assert updated_client.phone == update_data.phone
    assert updated_client.image == update_data.image


@pytest.mark.asyncio
async def test_update_client_name(client_repo, client):
    client_id = await client_repo.create(client)

    update_data = UpdateUser(
        name="newName"
    )

    result = await client_repo.update_client(client_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == client_id

    updated_client = await client_repo.get_by_email(client.email)

    assert isinstance(updated_client, ClientInDB)
    assert str(updated_client.id) == client_id
    assert updated_client.email == client.email
    assert updated_client.name == update_data.name
    assert updated_client.surname == client.surname
    assert updated_client.phone == client.phone
    assert updated_client.image == client.image

@pytest.mark.asyncio
async def test_update_client_surname(client_repo, client):
    client_id = await client_repo.create(client)

    update_data = UpdateUser(
        surname="newSurname"
    )

    result = await client_repo.update_client(client_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == client_id

    updated_client = await client_repo.get_by_email(client.email)

    assert isinstance(updated_client, ClientInDB)
    assert str(updated_client.id) == client_id
    assert updated_client.email == client.email
    assert updated_client.name == client.name
    assert updated_client.surname == update_data.surname
    assert updated_client.phone == client.phone
    assert updated_client.image == client.image

@pytest.mark.asyncio
async def test_update_client_phone(client_repo, client):
    client_id = await client_repo.create(client)

    update_data = UpdateUser(
        phone="+79876543210"
    )

    result = await client_repo.update_client(client_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == client_id

    updated_client = await client_repo.get_by_email(client.email)

    assert isinstance(updated_client, ClientInDB)
    assert str(updated_client.id) == client_id
    assert updated_client.email == client.email
    assert updated_client.name == client.name
    assert updated_client.surname == client.surname
    assert updated_client.phone == update_data.phone
    assert updated_client.image == client.image

@pytest.mark.asyncio
async def test_update_client_image(client_repo, client):
    client_id = await client_repo.create(client)

    update_data = UpdateUser(
        image="new_image.jpg"
    )

    result = await client_repo.update_client(client_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == client_id

    updated_client = await client_repo.get_by_email(client.email)

    assert isinstance(updated_client, ClientInDB)
    assert str(updated_client.id) == client_id
    assert updated_client.email == client.email
    assert updated_client.name == client.name
    assert updated_client.surname == client.surname
    assert updated_client.phone == client.phone
    assert updated_client.image == update_data.image

@pytest.mark.asyncio
async def test_update_client_partly(client_repo, client):
    client_id = await client_repo.create(client)

    update_data = UpdateUser(
        name="newName",
        phone="+79876543210"
    )

    result = await client_repo.update_client(client_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == client_id

    updated_client = await client_repo.get_by_email(client.email)

    assert isinstance(updated_client, ClientInDB)
    assert str(updated_client.id) == client_id
    assert updated_client.email == client.email
    assert updated_client.name == update_data.name
    assert updated_client.surname == client.surname
    assert updated_client.phone == update_data.phone
    assert updated_client.image == client.image

@pytest.mark.asyncio
async def test_update_client_database_error(client_repo, client, monkeypatch):
    async def mock_update_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(client_repo.client_collection, 'update_one', mock_update_one)

    client_id = await client_repo.create(client)

    with pytest.raises(DatabaseError):
        await client_repo.update_client(client_id, UpdateUser(name="newName"))

@pytest.mark.asyncio
async def test_update_password_success(client_repo, client):
    client_id = await client_repo.create(client)
    new_password = "new_hashed_pass"

    result = await client_repo.update_password(client_id, new_password)

    assert isinstance(result, UpdatedUserPassword)
    assert result.user_id == client_id

    updated_client = await client_repo.get_by_email(client.email)

    assert isinstance(updated_client, ClientInDB)
    assert str(updated_client.id) == client_id
    assert updated_client.email == client.email
    assert updated_client.name == client.name
    assert updated_client.surname == client.surname
    assert updated_client.phone == client.phone
    assert updated_client.image == client.image
    assert updated_client.password == new_password

@pytest.mark.asyncio
async def test_update_password_database_error(client_repo, client, monkeypatch):
    async def mock_update_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(client_repo.client_collection, 'update_one', mock_update_one)

    client_id = await client_repo.create(client)

    with pytest.raises(DatabaseError):
        await client_repo.update_password(client_id, "new_password")

@pytest.mark.asyncio
async def test_get_password_by_id_success(client_repo, client):
    client_id = await client_repo.create(client)
    password = await client_repo.get_password_by_id(client_id)

    assert password == client.password

@pytest.mark.asyncio
async def test_get_password_by_id_database_error(client_repo, client, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(client_repo.client_collection, 'find_one', mock_find_one)

    client_id = await client_repo.create(client)

    with pytest.raises(DatabaseError):
        await client_repo.get_password_by_id(client_id)

@pytest.mark.asyncio
async def test_get_private_summary_by_id_success(client_repo, client):
    client_id = await client_repo.create(client)

    result = await client_repo.get_private_summary_by_id(client_id)

    assert isinstance(result, ClientPrivateSummary)
    assert str(result.id) == client_id
    assert result.email == client.email
    assert result.name == client.name
    assert result.surname == client.surname
    assert result.phone == client.phone
    assert result.image == client.image

@pytest.mark.asyncio
async def test_get_private_summary_by_id_database_error(client_repo, client, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(client_repo.client_collection, 'find_one', mock_find_one)

    client_id = await client_repo.create(client)

    with pytest.raises(DatabaseError):
        await client_repo.get_private_summary_by_id(client_id)

@pytest.mark.asyncio
async def test_exists_by_id_true(client_repo, client):
    client_id = await client_repo.create(client)

    exists = await client_repo.exists_by_id(client_id)

    assert exists is True

@pytest.mark.asyncio
async def test_exists_by_id_false(client_repo, client):
    exists = await client_repo.exists_by_id(objectId_to_str(ObjectId()))

    assert exists is False

@pytest.mark.asyncio
async def test_exists_by_id_database_error(client_repo, client, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(client_repo.client_collection, 'find_one', mock_find_one)

    client_id = await client_repo.create(client)

    with pytest.raises(DatabaseError):
        await client_repo.exists_by_id(client_id)
