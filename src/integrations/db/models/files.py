from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from core.enums.db_enums import DataBaseEnum
from .base_model import BaseDataModel
from integrations.db.schemas.file import UploadedFile

class FileModel(BaseDataModel):
    """
    File model for interacting with the files collection in the database.
    """

    def __init__(self, db_client: AsyncIOMotorClient):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.FILES_DB_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: AsyncIOMotorClient):
        instance = cls(db_client)
        await instance.create_index()
        return instance
    
    async def create_index(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.FILES_DB_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.FILES_DB_NAME.value]
            indexes = UploadedFile.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"],
                )

    async def create_file(self, file: UploadedFile):
        """
        Create a new file in the database.
        """
        file_dict = file.dict()
        result = await self.collection.insert_one(file_dict)
        return str(result.inserted_id)
    
    
    async def get_file(self, file_id: str):
        """
        Get a file by its ID.
        """
        file = await self.collection.find_one({"_id": ObjectId(file_id)})
        if file:
            return UploadedFile(**file)
        return None
    
    async def update_file(self, file_id: str, file: UploadedFile):
        """
        Update a file by its ID.
        """
        file_dict = file.dict()
        result = await self.collection.update_one({"_id": ObjectId(file_id)}, {"$set": file_dict})
        return result.modified_count > 0
    
    async def delete_file(self, file_id: str):
        """
        Delete a file chunks by its ID.
        """
        result = await self.collection.delete_one({"_id": ObjectId(file_id)})
        return result.deleted_count > 0
    
    async def get_user_files(self, user_id: str, page: int = 0, limit: int = 10):
        """
        Get all files for a specific user.
        """
        files = []
        cursor = self.collection.find({"user_id": ObjectId(user_id)}).skip(page * limit).limit(limit)
        async for file in cursor:
            files.append(UploadedFile(**file))
        return files