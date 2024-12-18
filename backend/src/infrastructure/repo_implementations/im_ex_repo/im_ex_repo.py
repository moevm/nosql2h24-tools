from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from src.core.entities.category.category import Category, CategoryInDB
from src.core.entities.db_model.db_model import DBModel, DBModelCreate
from src.core.entities.order.order import Order, OrderInDB
from src.core.entities.review.review import Review, ReviewInDB
from src.core.entities.tool.tool import Tool, ToolInDB
from src.core.entities.type.type import Type, TypeInDB
from src.core.entities.users.client.client import Client, ClientInDB
from src.core.entities.users.worker.worker import Worker, WorkerInDB
from src.core.exceptions.server_error import DatabaseError
from src.core.repositories.im_ex_repo.iim_ex_repo import IImExRepository
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId


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
            workers = [WorkerInDB(**worker) for worker in (await self.worker_collection.find().to_list(None))]
            clients = [ClientInDB(**client) for client in (await self.client_collection.find().to_list(None))]
            tools = [ToolInDB(**tool) for tool in (await self.tool_collection.find().to_list(None))]
            orders = [OrderInDB(**order) for order in (await self.order_collection.find().to_list(None))]
            categories = [CategoryInDB(**category) for category in (await self.category_collection.find().to_list(None))]
            types = [TypeInDB(**type) for type in (await self.type_collection.find().to_list(None))]
            reviews = [ReviewInDB(**review)for review in (await self.review_collection.find().to_list(None))]

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

    async def import_data(self, data: DBModelCreate) -> None:
        try:
            if data.workers:
                await self.worker_collection.delete_many({})
                await self.worker_collection.insert_many([worker.model_dump() for worker in data.workers])

            if data.clients:
                await self.client_collection.delete_many({})
                await self.client_collection.insert_many([client.model_dump() for client in data.clients])

            if data.tools:
                await self.tool_collection.delete_many({})
                await self.tool_collection.insert_many([tool.model_dump() for tool in data.tools])

            if data.orders:
                await self.order_collection.delete_many({})
                await self.order_collection.insert_many([order.model_dump() for order in data.orders])

            if data.categories:
                await self.category_collection.delete_many({})
                await self.category_collection.insert_many([category.model_dump() for category in data.categories])

            if data.types:
                await self.type_collection.delete_many({})
                await self.type_collection.insert_many([typee.model_dump() for typee in data.types])

            if data.reviews:
                await self.review_collection.delete_many({})
                await self.review_collection.insert_many([review.model_dump() for review in data.reviews])

        except PyMongoError:
            raise DatabaseError()

