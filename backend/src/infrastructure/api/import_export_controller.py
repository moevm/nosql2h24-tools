from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.core.entities.db_model.db_model import DBModel
from src.core.services.im_ex_service.im_ex_service import ImExService
from src.infrastructure.api.client_controller import oauth2_scheme
from src.infrastructure.api.security.role_required import is_worker
from src.infrastructure.services_instances import get_im_ex_service

im_ex_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@im_ex_router.get(path="/export", status_code=201, response_model=DBModel)
async def export(
        im_ex_service: ImExService = Depends(get_im_ex_service),

):
    return await im_ex_service.export()


@im_ex_router.post(path="/import", status_code=201, response_model=None)
async def import_data(
        data: DBModel,
        im_ex_service: ImExService = Depends(get_im_ex_service),
):
    return await im_ex_service.import_data(data)
