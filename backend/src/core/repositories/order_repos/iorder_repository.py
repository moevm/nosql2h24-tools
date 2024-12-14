from abc import ABC, abstractmethod
from typing import List

from src.core.entities.order.order import Order, OrderSummary


class IOrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> str:
        pass

    @abstractmethod
    async def get_orders_by_client_id(self, client_id: str) -> List[OrderSummary]:
        pass

    @abstractmethod
    async def get_order_by_id(self, order_id: str) -> Order:
        pass