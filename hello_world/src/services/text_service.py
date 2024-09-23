from typing import Optional

from src.reposiroties.text_repository import TextRepository
from src.schemas.text import TextInDB, Text, TextUpdate


class TextService:
    def __init__(self, repository: TextRepository):
        self.repository = repository

    async def create_text(self, text: Text) -> TextInDB:
        return await self.repository.create_text(text)

    async def get_text_by_id(self, text_id: str) -> Optional[TextInDB]:
        return await self.repository.get_text_by_id(text_id)

    async def get_all_texts(self) -> list[TextInDB]:
        return await self.repository.get_all_texts()

    async def update_text(self, text: TextUpdate) -> Optional[TextInDB]:
        return await self.repository.update_text(text)

    async def delete_text(self, text_id: str) -> Optional[TextInDB]:
        return await self.repository.delete_text(text_id)