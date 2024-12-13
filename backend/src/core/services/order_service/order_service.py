import datetime
from src.core.entities.order.order import Order, OrderCreate, OrderCreated
from src.core.exceptions.client_error import ResourceNotFoundError
from src.core.repositories.order_repos.iorder_repository import IOrderRepository
from src.core.repositories.tool_repos.itool_repository import IToolRepository
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str, str_to_objectId


class OrderService:
    def __init__(self, order_repo: IOrderRepository, tool_repo: IToolRepository, worker_repo: IWorkerRepository):
        self.order_repo = order_repo
        self.tool_repo = tool_repo
        self.worker_repo = worker_repo

    async def create_order(self, order: OrderCreate) -> OrderCreated:
        for tool_id in order.tools:
            tool = await self.tool_repo.get_tool_by_id(tool_id)
            if not await self.tool_repo.exists(tool.name):
                raise ResourceNotFoundError("Provided tool doesn't exist", details={"tool name": tool.name})
        tools = [await self.tool_repo.get_tool_by_id(tool_id) for tool_id in order.tools]
        new_order = Order(
            tools=list(map(str_to_objectId, order.tools)),
            start_leasing=order.start_leasing,
            end_leasing=order.end_leasing,
            price=sum([tool.dailyPrice * (order.end_leasing - order.start_leasing).days for tool in tools]),
            client=str_to_objectId(order.client),
            delivery_type=order.delivery_type,
            delivery_state=order.delivery_state,
            payment_type=order.payment_type,
            payment_state=order.payment_state,
            create_order_time=datetime.datetime.now(),
            related_worker=await self.worker_repo.get_random_worker()
        )

        created_order_id = await self.order_repo.create(new_order)
        return OrderCreated(order_id=created_order_id)
