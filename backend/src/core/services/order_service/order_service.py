import datetime
from typing import List, Optional

from src.core.entities.order.order import Order, OrderCreate, OrderCreated, OrderSummary, OrderForWorker, \
    PaginatedOrdersResponseForWorker, PaginatedOrdersResponseForClient
from src.core.entities.users.client.client import Client, ClientInDB, ClientForWorker
from src.core.exceptions.client_error import ResourceNotFoundError
from src.core.repositories.order_repos.iorder_repository import IOrderRepository
from src.core.repositories.tool_repos.itool_repository import IToolRepository
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str, str_to_objectId


class OrderService:
    def __init__(self, order_repo: IOrderRepository, tool_repo: IToolRepository, worker_repo: IWorkerRepository, client_repo: IClientRepository):
        self.order_repo = order_repo
        self.tool_repo = tool_repo
        self.worker_repo = worker_repo
        self.client_repo = client_repo

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
            create_order_time=datetime.datetime.now()
        )

        created_order_id = await self.order_repo.create(new_order)
        return OrderCreated(order_id=created_order_id)

    async def get_paginated_orders_for_client(
            self,
            user_id: str,
            page: int,
            page_size: int,
            tool_name: Optional[List[str]] = None,
            status: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> PaginatedOrdersResponseForClient:
        tool_ids = None
        if tool_name:
            tool_ids = await self.tool_repo.get_ids_by_names(tool_name)

        orders_raw = await self.order_repo.get_paginated_orders(
            page=page,
            page_size=page_size,
            customer_ids=[user_id],
            tool_ids=tool_ids,
            status=status,
            start_date=start_date,
            end_date=end_date,
            min_price=min_price,
            max_price=max_price
        )

        total_count = await self.order_repo.count_orders(
            min_price=min_price,
            max_price=max_price,
            start_date=start_date,
            end_date=end_date,
            status=status,
            tool_ids=tool_ids,
            customer_ids=[user_id]
        )

        orders = []
        for order in orders_raw:
            tool_summaries = await self.tool_repo.get_tools_summaries_by_ids(
                [objectId_to_str(tool) for tool in order.tools])

            orders.append(OrderSummary(
                id=str(order.id),
                price=order.price,
                tools=tool_summaries,
                start_leasing=order.start_leasing,
                end_leasing=order.end_leasing,
                delivery_type=order.delivery_type,
                delivery_state=order.delivery_state,
                payment_type=order.payment_type,
                payment_state=order.payment_state,
                create_order_time=order.create_order_time
            ))

        return PaginatedOrdersResponseForClient(
            orders=orders,
            totalNumber=total_count
        )


    async def get_paginated_orders_for_worker(
            self,
            page: int,
            page_size: int,
            customer_name: Optional[str] = None,
            customer_surname: Optional[str] = None,
            tool_name: Optional[List[str]] = None,
            status: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> PaginatedOrdersResponseForWorker:
        tool_ids = None
        if tool_name:
            tool_ids = await self.tool_repo.get_ids_by_names(tool_name)

        customer_ids = None
        if customer_name or customer_surname:
            customer_ids = await self.client_repo.get_ids_by_fullname(customer_name, customer_surname)

        orders_raw = await self.order_repo.get_paginated_orders(
            page=page,
            page_size=page_size,
            customer_ids=customer_ids,
            tool_ids=tool_ids,
            status=status,
            start_date=start_date,
            end_date=end_date,
            min_price=min_price,
            max_price=max_price
        )

        total_count = await self.order_repo.count_orders(
            min_price=min_price,
            max_price=max_price,
            start_date=start_date,
            end_date=end_date,
            status=status,
            tool_ids=tool_ids,
            customer_ids=customer_ids
        )

        orders = []
        for order in orders_raw:
            tool_summaries = await self.tool_repo.get_tools_summaries_by_ids([objectId_to_str(tool) for tool in order.tools])
            client_summary = await self.client_repo.get_private_summary_by_id(objectId_to_str(order.client))

            orders.append(OrderForWorker(
                id=str(order.id),
                price=order.price,
                tools=tool_summaries,
                start_leasing=order.start_leasing,
                end_leasing=order.end_leasing,
                delivery_type=order.delivery_type,
                delivery_state=order.delivery_state,
                payment_type=order.payment_type,
                payment_state=order.payment_state,
                create_order_time=order.create_order_time,
                client=ClientForWorker(
                    id=client_summary.id,
                    name=client_summary.name,
                    surname=client_summary.surname
                )
            ))

        return PaginatedOrdersResponseForWorker(
            orders=orders,
            totalNumber=total_count
        )


    async def get_order_by_id(self, order_id: str) -> Optional[OrderSummary]:
        return await self.order_repo.get_order_by_id(order_id)
