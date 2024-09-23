from pydantic import BaseModel, Field


class Text(BaseModel):
    text: str

class TextInDB(BaseModel):
    id: str
    text: str

    @classmethod
    def from_mongo(cls, doc):
        return cls(id=str(doc["_id"]), text=doc["text"])


class TextUpdate(BaseModel):
    id: str
    text: str