from abc import ABC, abstractmethod
from typing import List

from src.core.entities.order.order import Order, OrderSummary, OrderForWorker


class IOrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> str:
        pass

    @abstractmethod
    async def get_orders_by_client_id(self, client_id: str) -> List[OrderSummary]:
        pass

    @abstractmethod
    async def get_orders_by_worker_id(self, worker_id: str) -> List[OrderForWorker]:
        pass

    @abstractmethod
    async def get_order_by_id(self, order_id: str) -> Order:
        pass

    @abstractmethod
    async def has_order_with_tool(self, client_id: str, tool_id: str) -> bool:
        pass

    @abstractmethod
    async def paid(self, order_id: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_id(self, order_id: str) -> bool:
        pass