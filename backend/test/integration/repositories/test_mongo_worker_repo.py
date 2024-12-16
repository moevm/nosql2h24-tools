from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock
from bson import ObjectId
import pytest, pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdatedUserPassword
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str, str_to_objectId
from src.core.exceptions.server_error import DatabaseError
from src.infrastructure.repo_implementations.users_repos.worker_repos.mongo_worker_repository import MongoWorkerRepository
from src.core.entities.users.worker.worker import Worker, WorkerInDB, WorkerPrivateSummary
from src.configs.config import config
from pymongo.errors import PyMongoError



@pytest_asyncio.fixture(scope='function')
async def db():
    client = AsyncIOMotorClient(str(config.mongo.mongo_dsn))
    database = client[config.mongo.mongo_db]

    await database.drop_collection(config.collections.worker_collection)

    yield database

    await database.drop_collection(config.collections.worker_collection)

    client.close()


@pytest_asyncio.fixture(scope='function')
async def worker_repo(db):
    return MongoWorkerRepository(db, config.collections.worker_collection)


@pytest.fixture
def worker():
    return Worker(
        email="test_worker@example.com",
        password="hashed_password",
        name="test_name",
        surname="test_surname",
        phone="+71234567890",
        jobTitle="test_job_title",
        date=datetime.now(timezone.utc)
    )


@pytest.mark.asyncio
async def test_create_worker_success(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    assert isinstance(worker_id, str)

    saved_worker = await worker_repo.worker_collection.find_one({"_id": str_to_objectId(worker_id)})

    assert saved_worker is not None
    assert objectId_to_str(saved_worker["_id"]) == worker_id
    assert saved_worker["email"] == worker.email
    assert saved_worker["password"] == worker.password
    assert saved_worker["name"] == worker.name
    assert saved_worker["surname"] == worker.surname
    assert saved_worker["phone"] == worker.phone
    assert saved_worker["jobTitle"] == worker.jobTitle
    assert saved_worker["date"] is not None
    assert isinstance(saved_worker["date"], datetime)
    assert saved_worker["image"] is None

@pytest.mark.asyncio
async def test_create_worker_database_error(worker_repo, worker, monkeypatch):

    async def mock_insert_one(*args, **kwargs):
        raise PyMongoError("Mocked insertion error")

    monkeypatch.setattr(worker_repo.worker_collection, 'insert_one', mock_insert_one)

    with pytest.raises(DatabaseError):
        await worker_repo.create(worker)

@pytest.mark.asyncio
async def test_get_by_email_success(worker_repo, worker):
    await worker_repo.create(worker)

    worker_in_db = await worker_repo.get_by_email(worker.email)

    assert isinstance(worker_in_db, WorkerInDB)

    assert worker_in_db.email == worker.email
    assert worker_in_db.password == worker.password
    assert worker_in_db.name == worker.name
    assert worker_in_db.surname == worker.surname
    assert worker_in_db.phone == worker.phone
    assert worker_in_db.jobTitle == worker.jobTitle
    assert worker_in_db.date is not None
    assert isinstance(worker_in_db.date, datetime)
    assert worker_in_db.image is None

@pytest.mark.asyncio
async def test_get_by_email_database_error(worker_repo, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked find error")

    monkeypatch.setattr(worker_repo.worker_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await worker_repo.get_by_email("test@example.com")

@pytest.mark.asyncio
async def test_exists_true(worker_repo, worker):
    await worker_repo.create(worker)

    exists = await worker_repo.exists_by_email(worker.email)
    assert exists is True

@pytest.mark.asyncio
async def test_exists_false(worker_repo):
    exists = await worker_repo.exists_by_email("nonexistent@example.com")
    assert exists is False


@pytest.mark.asyncio
async def test_exists_database_error(worker_repo, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked exists error")

    monkeypatch.setattr(worker_repo.worker_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await worker_repo.exists_by_email("test@example.com")

@pytest.mark.asyncio
async def test_get_all_workers_summary(worker_repo):
    worker_count = 9

    workers = [
        Worker(
            email=f"test_worker_{i}@example.com",
            password=f"hashed_password{i}",
            name=f"test_user_{i}",
            surname=f"test_surname_{i}",
            phone=f"+7000000000{i}",
            jobTitle=f"test_title_{i}",
            date=datetime.now(timezone.utc)
        ) for i in range(worker_count)
    ]

    for worker in workers:
        await worker_repo.create(worker)

    summaries = await worker_repo.get_all_workers_summary()
    assert len(summaries) == worker_count

    for i in range(worker_count):
        assert summaries[i].email == workers[i].email
        assert summaries[i].name == workers[i].name
        assert summaries[i].surname == workers[i].surname
        assert summaries[i].phone == workers[i].phone
        assert summaries[i].image == workers[i].image
        assert summaries[i].jobTitle == workers[i].jobTitle
        assert abs(summaries[i].date.replace(tzinfo=timezone.utc) - workers[i].date.replace(tzinfo=timezone.utc)) < timedelta(milliseconds=1)


@pytest.mark.asyncio
async def test_get_all_workers_summary_empty(worker_repo):
    summaries = await worker_repo.get_all_workers_summary()
    assert summaries == []

@pytest.mark.asyncio
async def test_get_all_workers_summary_database_error(worker_repo, monkeypatch):
    mock_cursor = AsyncMock()
    mock_cursor.to_list.side_effect = PyMongoError("Mocked to_list error")

    def mock_find(*args, **kwargs):
        return mock_cursor

    monkeypatch.setattr(worker_repo.worker_collection, 'find', mock_find)

    with pytest.raises(DatabaseError):
        await worker_repo.get_all_workers_summary()
        
@pytest.mark.asyncio
async def test_update_worker_all(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    update_data = UpdateUser(
        name="newName",
        surname="newSurname",
        phone="+79876543210",
        image="new_image.jpg"
    )

    result = await worker_repo.update_worker(worker_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == worker_id

    updated_worker = await worker_repo.get_by_email(worker.email)

    assert isinstance(updated_worker, WorkerInDB)
    assert str(updated_worker.id) == worker_id
    assert updated_worker.email == worker.email
    assert updated_worker.name == update_data.name
    assert updated_worker.surname == update_data.surname
    assert updated_worker.phone == update_data.phone
    assert updated_worker.image == update_data.image


@pytest.mark.asyncio
async def test_update_worker_name(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    update_data = UpdateUser(
        name="newName"
    )

    result = await worker_repo.update_worker(worker_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == worker_id

    updated_worker = await worker_repo.get_by_email(worker.email)

    assert isinstance(updated_worker, WorkerInDB)
    assert str(updated_worker.id) == worker_id
    assert updated_worker.email == worker.email
    assert updated_worker.name == update_data.name
    assert updated_worker.surname == worker.surname
    assert updated_worker.phone == worker.phone
    assert updated_worker.image == worker.image

@pytest.mark.asyncio
async def test_update_worker_surname(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    update_data = UpdateUser(
        surname="newSurname"
    )

    result = await worker_repo.update_worker(worker_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == worker_id

    updated_worker = await worker_repo.get_by_email(worker.email)

    assert isinstance(updated_worker, WorkerInDB)
    assert str(updated_worker.id) == worker_id
    assert updated_worker.email == worker.email
    assert updated_worker.name == worker.name
    assert updated_worker.surname == update_data.surname
    assert updated_worker.phone == worker.phone
    assert updated_worker.image == worker.image

@pytest.mark.asyncio
async def test_update_worker_phone(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    update_data = UpdateUser(
        phone="+79876543210"
    )

    result = await worker_repo.update_worker(worker_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == worker_id

    updated_worker = await worker_repo.get_by_email(worker.email)

    assert isinstance(updated_worker, WorkerInDB)
    assert str(updated_worker.id) == worker_id
    assert updated_worker.email == worker.email
    assert updated_worker.name == worker.name
    assert updated_worker.surname == worker.surname
    assert updated_worker.phone == update_data.phone
    assert updated_worker.image == worker.image

@pytest.mark.asyncio
async def test_update_worker_image(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    update_data = UpdateUser(
        image="new_image.jpg"
    )

    result = await worker_repo.update_worker(worker_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == worker_id

    updated_worker = await worker_repo.get_by_email(worker.email)

    assert isinstance(updated_worker, WorkerInDB)
    assert str(updated_worker.id) == worker_id
    assert updated_worker.email == worker.email
    assert updated_worker.name == worker.name
    assert updated_worker.surname == worker.surname
    assert updated_worker.phone == worker.phone
    assert updated_worker.image == update_data.image

@pytest.mark.asyncio
async def test_update_worker_partly(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    update_data = UpdateUser(
        name="newName",
        phone="+79876543210"
    )

    result = await worker_repo.update_worker(worker_id, update_data)

    assert isinstance(result, UpdatedUser)
    assert result.user_id == worker_id

    updated_worker = await worker_repo.get_by_email(worker.email)

    assert isinstance(updated_worker, WorkerInDB)
    assert str(updated_worker.id) == worker_id
    assert updated_worker.email == worker.email
    assert updated_worker.name == update_data.name
    assert updated_worker.surname == worker.surname
    assert updated_worker.phone == update_data.phone
    assert updated_worker.image == worker.image

@pytest.mark.asyncio
async def test_update_worker_database_error(worker_repo, worker, monkeypatch):
    async def mock_update_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(worker_repo.worker_collection, 'update_one', mock_update_one)

    worker_id = await worker_repo.create(worker)

    with pytest.raises(DatabaseError):
        await worker_repo.update_worker(worker_id, UpdateUser(name="newName"))

@pytest.mark.asyncio
async def test_update_password_success(worker_repo, worker):
    worker_id = await worker_repo.create(worker)
    new_password = "new_hashed_pass"

    result = await worker_repo.update_password(worker_id, new_password)

    assert isinstance(result, UpdatedUserPassword)
    assert result.user_id == worker_id

    updated_worker = await worker_repo.get_by_email(worker.email)

    assert isinstance(updated_worker, WorkerInDB)
    assert str(updated_worker.id) == worker_id
    assert updated_worker.email == worker.email
    assert updated_worker.name == worker.name
    assert updated_worker.surname == worker.surname
    assert updated_worker.phone == worker.phone
    assert updated_worker.image == worker.image
    assert updated_worker.password == new_password

@pytest.mark.asyncio
async def test_update_password_database_error(worker_repo, worker, monkeypatch):
    async def mock_update_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(worker_repo.worker_collection, 'update_one', mock_update_one)

    worker_id = await worker_repo.create(worker)

    with pytest.raises(DatabaseError):
        await worker_repo.update_password(worker_id, "new_password")

@pytest.mark.asyncio
async def test_get_password_by_id_success(worker_repo, worker):
    worker_id = await worker_repo.create(worker)
    password = await worker_repo.get_password_by_id(worker_id)

    assert password == worker.password

@pytest.mark.asyncio
async def test_get_password_by_id_database_error(worker_repo, worker, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(worker_repo.worker_collection, 'find_one', mock_find_one)

    worker_id = await worker_repo.create(worker)

    with pytest.raises(DatabaseError):
        await worker_repo.get_password_by_id(worker_id)

@pytest.mark.asyncio
async def test_get_private_summary_by_id_success(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    result = await worker_repo.get_private_summary_by_id(worker_id)

    assert isinstance(result, WorkerPrivateSummary)
    assert str(result.id) == worker_id
    assert result.email == worker.email
    assert result.name == worker.name
    assert result.surname == worker.surname
    assert result.phone == worker.phone
    assert result.image == worker.image

@pytest.mark.asyncio
async def test_get_private_summary_by_id_database_error(worker_repo, worker, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(worker_repo.worker_collection, 'find_one', mock_find_one)

    worker_id = await worker_repo.create(worker)

    with pytest.raises(DatabaseError):
        await worker_repo.get_private_summary_by_id(worker_id)

@pytest.mark.asyncio
async def test_exists_by_id_true(worker_repo, worker):
    worker_id = await worker_repo.create(worker)

    exists = await worker_repo.exists_by_id(worker_id)

    assert exists is True

@pytest.mark.asyncio
async def test_exists_by_id_false(worker_repo, worker):
    exists = await worker_repo.exists_by_id(objectId_to_str(ObjectId()))

    assert exists is False

@pytest.mark.asyncio
async def test_exists_by_id_database_error(worker_repo, worker, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked database error")

    monkeypatch.setattr(worker_repo.worker_collection, 'find_one', mock_find_one)

    worker_id = await worker_repo.create(worker)

    with pytest.raises(DatabaseError):
        await worker_repo.exists_by_id(worker_id)
