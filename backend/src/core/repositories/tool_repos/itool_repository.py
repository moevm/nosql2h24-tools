from abc import ABC, abstractmethod
from src.core.entities.tool.tool import Tool, ToolSummary, ToolDetails, ToolPages
from typing import List, Optional

class IToolRepository(ABC):
    @abstractmethod
    async def create(self, tool: Tool) -> str:
        pass

    @abstractmethod
    async def get_paginated_summary(self, page: int, page_size: int) -> List[ToolSummary]:
        pass

    @abstractmethod
    async def get_details(self, tool_id: str) -> Optional[ToolDetails]:
        pass

    @abstractmethod
    async def get_total_count(self) -> ToolPages:
        pass

    @abstractmethod
    async def exists(self, tool_name: str) -> bool:
        pass

    @abstractmethod
    async def get_tool_by_id(self, tool_id: str) -> Optional[Tool]:
        pass
  
    @abstractmethod
    async def search(
            self,
            query: str,
            page: int,
            page_size: int,
            category: Optional[List[str]] = None,
            type: Optional[List[str]] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> List[ToolSummary]:
        pass

    @abstractmethod
    async def exists_by_id(self, tool_id: str) -> bool:
        pass

    @abstractmethod
    async def get_name_by_id(self, tool_id: str) -> Optional[str]:
        pass

    @abstractmethod
    async def get_ids_by_names(self, names: List[str]) -> List[str]:
        pass

    @abstractmethod
    async def get_ids_by_name(self, name: str) -> List[str]:
        pass

    @abstractmethod
    async def count_tools(
            self,
            query: str,
            category: Optional[List[str]] = None,
            type: Optional[List[str]] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> int:
        pass

    @abstractmethod
    async def get_tools_summaries_by_ids(self, tool_ids: List[str]) -> List[ToolSummary]:
        pass

    @abstractmethod
    async def update_rating(self, tool_id: str, new_rating: float) -> None:
        pass