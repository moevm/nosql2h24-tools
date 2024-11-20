from bson import ObjectId
from src.core.exceptions.server_error import MappingError


def str_to_objectId(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except Exception:
        raise MappingError()

def objectId_to_str(id: ObjectId) -> str:
    try:
        return str(id)
    except Exception:
        raise MappingError()
