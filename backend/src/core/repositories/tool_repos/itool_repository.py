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