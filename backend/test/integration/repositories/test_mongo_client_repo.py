from multiprocessing.context import assert_spawning
from unittest.mock import AsyncMock

import pytest, pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.configs.config import config
from pymongo.errors import PyMongoError
from src.core.entities.users.client.client import Client, ClientInDB
from src.core.exceptions.server_error import DatabaseError
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
        name="test_name",
        surname="test_surname",
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
    assert saved_client["orders"] == []

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
    assert client_in_db.orders == []

@pytest.mark.asyncio
async def test_get_by_email_not_found(client_repo):
    retrieved_client = await client_repo.get_by_email("nonexistent@example.com")
    assert retrieved_client is None

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
    exists = await client_repo.exists(client.email)
    assert exists is True

@pytest.mark.asyncio
async def test_exists_false(client_repo):
    exists = await client_repo.exists("nonexistent@example.com")
    assert exists is False

@pytest.mark.asyncio
async def test_exists_database_error(client_repo, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked exists error")

    monkeypatch.setattr(client_repo.client_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await client_repo.exists("test@example.com")

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
