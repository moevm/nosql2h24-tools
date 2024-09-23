from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi.params import Depends
from src.reposiroties.text_repository import TextRepository
from src.schemas.text import TextInDB, Text, TextUpdate
from src.services.text_service import TextService

router = APIRouter(
    prefix="/texts",
    tags=["Text"]
)

@router.get("/", response_model=list[TextInDB])
async def get_texts(request: Request) -> list[TextInDB]:
    text_service: TextService = request.app.text_service
    result = await text_service.get_all_texts()
    return result

@router.post("/", response_model=TextInDB)
async def create_text(request: Request, text: Text) -> TextInDB:
    text_service: TextService = request.app.text_service
    result = await text_service.create_text(text)
    return result

@router.get("/{text_id}", response_model=TextInDB)
async def get_text_by_id(request: Request, text_id: str) -> TextInDB:
    text_service: TextService = request.app.text_service
    result = await text_service.get_text_by_id(text_id)

    if not result:
        raise HTTPException(status_code=404, detail="Text not found")

    return result

@router.delete("/{text_id}", response_model=TextInDB)
async def delete_text(request: Request, text_id: str) -> TextInDB:
    text_service: TextService = request.app.text_service
    result = await text_service.delete_text(text_id)

    if not result:
        raise HTTPException(status_code=404, detail="Text not found")

    return result

@router.put("/", response_model=TextInDB)
async def update_text(request: Request, text: TextUpdate) -> TextInDB:
    text_service: TextService = request.app.text_service
    result = await text_service.update_text(text)

    if not result:
        raise HTTPException(status_code=404, detail="Text not found")

    return result
