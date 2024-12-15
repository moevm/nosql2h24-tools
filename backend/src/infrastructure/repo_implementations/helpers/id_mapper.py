from bson import ObjectId

from src.core.exceptions.client_error import MappingToObjectIDError
from src.core.exceptions.server_error import MappingToStrError


def str_to_objectId(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except Exception:
        raise MappingToObjectIDError()

def objectId_to_str(id: ObjectId) -> str:
    try:
        return str(id)
    except Exception:
        raise MappingToStrError()
