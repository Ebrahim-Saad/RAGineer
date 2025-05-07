from typing import Optional
from pydantic import BaseModel, Field, validator
from bson.objectid import ObjectId

class UploadedFile(BaseModel):
    _id: ObjectId # unique identifier for the file
    user_id: str   # user id of the person who uploaded the file
    file_name: str # original file name uploaded by the user
    file_path: str # path to the file in the storage
    file_type: str # type of the file (application/pdf, plain/txt)
    file_size_bytes: int # size of the file in bytes
    file_desciption: Optional[str] = Field(default=None, max_length=500) # description of the file
    file_metadata: Optional[dict] = Field(default=None) # metadata of the file


    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [{
            "key": [
                ("user_id", 1),
            ],
            "name": "file_user_id_index",
            "unique": False,
        }
        ]