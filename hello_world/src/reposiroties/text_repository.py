from abc import ABC, abstractmethod
from typing import Optional

from src.schemas.text import Text, TextInDB, TextUpdate


class TextRepository(ABC):
    @abstractmethod
    async def create_text(self, text: Text) -> TextInDB:
        pass

    @abstractmethod
    async def get_text_by_id(self, text_id: str) -> Optional[TextInDB]:
        pass

    @abstractmethod
    async def get_all_texts(self) -> list[TextInDB]:
        pass

    @abstractmethod
    async def update_text(self, text: TextUpdate) -> Optional[TextInDB]:
        pass

    @abstractmethod
    async def delete_text(self, text_id: str) -> Optional[TextInDB]:
        pass
