from abc import ABC, abstractmethod
from optparse import Option
from typing import List, Optional

from src.core.entities.order.order import Order, OrderSummary, OrderForWorker, OrderInDB
from datetime import datetime

class IOrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> str:
        pass

    @abstractmethod
    async def get_orders_by_client_id(self, client_id: str) -> List[OrderSummary]:
        pass

    @abstractmethod
    async def get_order_by_id(self, order_id: str) -> Optional[OrderSummary]:
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

    @abstractmethod
    async def get_paginated_orders(
            self,
            page: int,
            page_size: int,
            customer_ids: Optional[List[str]] = None,
            tool_ids: Optional[List[str]] = None,
            status: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> List[OrderInDB]:
        pass

    @abstractmethod
    async def count_orders(
            self,
            customer_ids: Optional[List[str]] = None,
            tool_ids: Optional[List[str]] = None,
            status: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> int:
        pass