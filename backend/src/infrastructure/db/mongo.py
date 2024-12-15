from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.configs.config import config
from src.configs.mongo_config import MongoConfig

mongo_config = config.mongo
collections_config = config.collections

class MongoDB:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None

    @staticmethod
    async def connect() -> None:
        print("Connecting to MongoDB...")
        print(mongo_config.mongo_dsn)
        MongoDB.client = AsyncIOMotorClient(str(mongo_config.mongo_dsn))
        MongoDB.db = MongoDB.client[mongo_config.mongo_db]
        print("Connected to MongoDB:", MongoDB.db)

    @staticmethod
    async def close() -> None:
        if MongoDB.client:
            MongoDB.client.close()
        else:
            raise ConnectionError("Client not connected")

    @staticmethod
    async def create_indexes()  -> None:
        await MongoDB.db[collections_config.tool_collection].create_index(
            [
                ("name", "text"),
                ("description", "text"),
                ("category", "text"),
                ("type", "text")
            ],
            weights={
                "name": 10,
                "description": 5,
                "category": 2,
                "type": 2
            },
            default_language="russian"
        )

    @staticmethod
    def get_db_instance() -> AsyncIOMotorDatabase:
        if MongoDB.db is not None:
            return MongoDB.db
        else:
            raise ConnectionError("Database not connected")


def get_db() -> AsyncIOMotorDatabase:
    return MongoDB.get_db_instance()