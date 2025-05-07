from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId


class TextChunk(BaseModel):
    _id: Optional[ObjectId]
    user_id: str
    file_id: str
    chunk_embedding: Optional[list[float]] = Field(default=None)
    chunk_text: str
    chunk_metadata: Optional[dict] = Field(default={})

    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {
        #     ObjectId: lambda v: str(v)
        # }

    @classmethod
    def get_indexes(cls):
        return [{
            "key": [
                ("file_id", 1),
            ],
            "name": "chunk_file_id_index",
            "unique": False,
        }
        ]