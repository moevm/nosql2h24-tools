from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from src.core.entities.db_model.db_model import DBModel
from src.core.exceptions.server_error import DatabaseError
from src.core.repositories.im_ex_repo.iim_ex_repo import IImExRepository


class MongoImExRepository(IImExRepository):
    def __init__(
            self,
            db: AsyncIOMotorDatabase,
            order_collection: str,
            tool_collection: str,
            client_collection: str,
            worker_collection: str,
            review_collection: str,
            category_collection: str,
            type_collection: str):
        self.order_collection = db[order_collection]
        self.tool_collection = db[tool_collection]
        self.client_collection = db[client_collection]
        self.worker_collection = db[worker_collection]
        self.review_collection = db[review_collection]
        self.category_collection = db[category_collection]
        self.type_collection = db[type_collection]

    async def export_data(self) -> DBModel:
        try:
            workers = await self.worker_collection.find().to_list(None)
            clients = await self.client_collection.find().to_list(None)
            tools = await self.tool_collection.find().to_list(None)
            orders = await self.order_collection.find().to_list(None)
            categories = await self.category_collection.find().to_list(None)
            types = await self.type_collection.find().to_list(None)
            reviews = await self.review_collection.find().to_list(None)

            return DBModel(
                workers=workers,
                clients=clients,
                tools=tools,
                orders=orders,
                categories=categories,
                types=types,
                reviews=reviews
            )
        except PyMongoError:
            raise DatabaseError()

    async def import_data(self, data: DBModel) -> None:
        try:
            if data.workers:
                await self.worker_collection.delete_many({})
                await self.worker_collection.insert_many(data.workers)

            if data.clients:
                await self.client_collection.delete_many({})
                await self.client_collection.insert_many(data.clients)

            if data.tools:
                await self.tool_collection.delete_many({})
                await self.tool_collection.insert_many(data.tools)

            if data.orders:
                await self.order_collection.delete_many({})
                await self.order_collection.insert_many(data.orders)

            if data.categories:
                await self.category_collection.delete_many({})
                await self.category_collection.insert_many(data.categories)

            if data.types:
                await self.type_collection.delete_many({})
                await self.type_collection.insert_many(data.types)

            if data.reviews:
                await self.review_collection.delete_many({})
                await self.review_collection.insert_many(data.reviews)

        except PyMongoError:
            raise DatabaseError()

