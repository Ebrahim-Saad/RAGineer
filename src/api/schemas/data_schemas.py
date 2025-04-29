from pydantic import BaseModel
from typing import Literal


class AddFileSchema(BaseModel):
    user_id: str
    file_path: str
    chunk_size: int
    chunk_overlap: int
    file_extension: Literal["pdf", "txt"]


class DeleteFileSchema(BaseModel):
    user_id: str
    file_id: str
