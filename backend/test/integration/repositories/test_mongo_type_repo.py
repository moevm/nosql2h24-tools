from unittest.mock import AsyncMock
import pytest, pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.configs.config import config
from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.type.type import TypeSignature, Type
from src.core.exceptions.server_error import DatabaseError
from src.infrastructure.repo_implementations.tool_repos.mongo_type_repository import MongoTypeRepository
from pymongo.errors import PyMongoError

@pytest_asyncio.fixture(scope='function')
async def db():
    client = AsyncIOMotorClient(str(config.mongo.mongo_dsn))
    database = client[config.mongo.mongo_db]

    await database.drop_collection(config.collections.type_collection)

    yield database

    await database.drop_collection(config.collections.type_collection)
    client.close()

@pytest_asyncio.fixture(scope='function')
async def type_repo(db):
    return MongoTypeRepository(db, config.collections.type_collection)

@pytest.fixture
def type_signature():
    return TypeSignature(
        name="test-type",
        category_name="test-category"
    )

@pytest.fixture
def type(type_signature):
    tool_ids=[ObjectIdStr(), ObjectIdStr()]
    return Type(
        name=type_signature.name,
        category_name=type_signature.category_name,
        tools=tool_ids
    )

@pytest.mark.asyncio
async def test_create_type_success(type_repo, type):
    type_id = await type_repo.create(type)

    assert isinstance(type_id, str)

    saved_type = await type_repo.type_collection.find_one({"_id": ObjectId(type_id)})

    assert saved_type is not None
    assert saved_type["name"] == type.name
    assert saved_type["category_name"] == type.category_name
    assert saved_type["tools"] == [ObjectId(tool_id) for tool_id in type.tools]

@pytest.mark.asyncio
async def test_create_type_database_error(type_repo, type, monkeypatch):
    async def mock_insert_one(*args, **kwargs):
        raise PyMongoError("Mocked insertion error")

    monkeypatch.setattr(type_repo.type_collection, 'insert_one', mock_insert_one)

    with pytest.raises(DatabaseError):
        await type_repo.create(type)

@pytest.mark.asyncio
async def test_get_id_by_signature_success(type_repo, type, type_signature):
    type_id = await type_repo.create(type)
    retrieved_id = await type_repo.get_id_by_signature(type_signature)
    assert retrieved_id == type_id

@pytest.mark.asyncio
async def test_get_id_by_signature_not_found(type_repo, type_signature):
    retrieved_id = await type_repo.get_id_by_signature(type_signature)
    assert retrieved_id is None

@pytest.mark.asyncio
async def test_get_id_by_signature_database_error(type_repo, type_signature, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked find error")

    monkeypatch.setattr(type_repo.type_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await type_repo.get_id_by_signature(type_signature)

@pytest.mark.asyncio
async def test_delete_by_name_success(type_repo, type, type_signature):
    await type_repo.create(type)
    deleted_count = await type_repo.delete_by_name(type_signature)
    assert deleted_count == 1

    exists = await type_repo.exists(type_signature)
    assert not exists

@pytest.mark.asyncio
async def test_delete_by_name_not_found(type_repo, type_signature):
    deleted_count = await type_repo.delete_by_name(type_signature)
    assert deleted_count == 0

@pytest.mark.asyncio
async def test_delete_by_name_database_error(type_repo, type_signature, monkeypatch):
    async def mock_delete_one(*args, **kwargs):
        raise PyMongoError("Mocked deletion error")

    monkeypatch.setattr(type_repo.type_collection, 'delete_one', mock_delete_one)

    with pytest.raises(DatabaseError):
        await type_repo.delete_by_name(type_signature)

@pytest.mark.asyncio
async def test_add_to_associated_tools_success(type_repo, type, type_signature):
    await type_repo.create(type)
    initial_type = await type_repo.type_collection.find_one({"name": type.name, "category_name": type.category_name})
    initial_tools_count = len(initial_type["tools"])

    new_tool_id = str(ObjectId())
    modified_count = await type_repo.add_to_associated_tools(type_signature, new_tool_id)
    assert modified_count == 1

    updated_type = await type_repo.type_collection.find_one({"name": type.name, "category_name": type.category_name})
    assert updated_type is not None
    assert ObjectId(new_tool_id) in updated_type["tools"]
    assert len(updated_type["tools"]) == initial_tools_count + 1

@pytest.mark.asyncio
async def test_add_to_associated_tools_type_not_found(type_repo, type_signature):
    new_tool_id = str(ObjectId())
    modified_count = await type_repo.add_to_associated_tools(type_signature, new_tool_id)
    assert modified_count == 0

@pytest.mark.asyncio
async def test_add_to_associated_tools_database_error(type_repo, type_signature, monkeypatch):
    async def mock_update_one(*args, **kwargs):
        raise PyMongoError("Mocked update error")

    monkeypatch.setattr(type_repo.type_collection, 'update_one', mock_update_one)

    with pytest.raises(DatabaseError):
        await type_repo.add_to_associated_tools(type_signature, str(ObjectId()))

@pytest.mark.asyncio
async def test_delete_from_associated_tools_success(type_repo, type, type_signature):
    await type_repo.create(type)
    tool_id_to_remove = type.tools[0]
    modified_count = await type_repo.delete_from_associated_tools(type_signature, tool_id_to_remove)
    assert modified_count == 1

    updated_type = await type_repo.type_collection.find_one({"name": type.name, "category_name": type.category_name})
    assert updated_type is not None
    assert ObjectId(tool_id_to_remove) not in updated_type["tools"]
    assert len(updated_type["tools"]) == len(type.tools) - 1

@pytest.mark.asyncio
async def test_delete_from_associated_tools_type_not_found(type_repo, type_signature):
    tool_id = str(ObjectId())
    modified_count = await type_repo.delete_from_associated_tools(type_signature, tool_id)
    assert modified_count == 0

@pytest.mark.asyncio
async def test_delete_from_associated_tools_database_error(type_repo, type_signature, monkeypatch):
    async def mock_update_one(*args, **kwargs):
        raise PyMongoError("Mocked update error")

    monkeypatch.setattr(type_repo.type_collection, 'update_one', mock_update_one)

    with pytest.raises(DatabaseError):
        await type_repo.delete_from_associated_tools(type_signature, str(ObjectId()))

@pytest.mark.asyncio
async def test_exists_true(type_repo, type, type_signature):
    await type_repo.create(type)
    exists = await type_repo.exists(type_signature)
    assert exists is True

@pytest.mark.asyncio
async def test_exists_false(type_repo, type_signature):
    exists = await type_repo.exists(type_signature)
    assert exists is False

@pytest.mark.asyncio
async def test_exists_database_error(type_repo, type_signature, monkeypatch):
    async def mock_count_documents(*args, **kwargs):
        raise PyMongoError("Mocked count error")

    monkeypatch.setattr(type_repo.type_collection, 'count_documents', mock_count_documents)

    with pytest.raises(DatabaseError):
        await type_repo.exists(type_signature)

@pytest.mark.asyncio
async def test_is_associated_tools_empty_false(type_repo, type, type_signature):
    await type_repo.create(type)
    is_empty = await type_repo.is_associated_tools_empty(type_signature)
    assert is_empty is False

@pytest.mark.asyncio
async def test_is_associated_tools_empty_true(type_repo, type, type_signature):
    type.tools = []
    await type_repo.create(type)
    is_empty = await type_repo.is_associated_tools_empty(type_signature)
    assert is_empty is True

@pytest.mark.asyncio
async def test_is_associated_tools_empty_type_not_found(type_repo, type_signature):
    is_empty = await type_repo.is_associated_tools_empty(type_signature)
    assert is_empty is True

@pytest.mark.asyncio
async def test_is_associated_tools_empty_database_error(type_repo, type_signature, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked find error")

    monkeypatch.setattr(type_repo.type_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await type_repo.is_associated_tools_empty(type_signature)