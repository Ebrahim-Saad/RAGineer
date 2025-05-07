from motor.motor_asyncio import AsyncIOMotorClient
from core.enums.db_enums import DataBaseEnum
from .base_model import BaseDataModel
from integrations.db.schemas.text_chunk import TextChunk
from bson import ObjectId

class ChunkModel(BaseDataModel):
    """
    Text chunks model for interacting with the chunks collection in the database.
    """

    def __init__(self, db_client: AsyncIOMotorClient):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.CHUNKS_DB_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: AsyncIOMotorClient):
        instance = cls(db_client)
        await instance.create_index()
        return instance

    async def create_index(self):
        """
        Create indexes for the chunks collection.
        """
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.CHUNKS_DB_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.CHUNKS_DB_NAME.value]
            indexes = TextChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"],
                )

    async def add_chunk(self, chunk: TextChunk):
        """
        Add a new chunk to the database.
        """
        chunk_dict = chunk.model_dump()
        result = await self.collection.insert_one(chunk_dict)
        return str(result.inserted_id)
    
    
    async def get_chunk(self, chunk_id: str):
        """
        Get a chunk by its ID.
        """
        chunk = await self.collection.find_one({"_id": chunk_id})
        if chunk:
            return TextChunk(**chunk)
        return None
    
    
    async def update_chunk(self, chunk_id: str, chunk: TextChunk):
        """
        Update a chunk by its ID.
        """
        chunk_dict = chunk.dict()
        result = await self.collection.update_one({"_id": ObjectId(chunk_id)}, {"$set": chunk_dict})
        return result.modified_count > 0
    

    async def delete_chunk(self, chunk_id: str):
        """
        Delete a chunk by its ID.
        """
        result = await self.collection.delete_one({"_id": ObjectId(chunk_id)})
        return result.deleted_count > 0
    
    async def delete_file_chunks(self, file_id: str):
        """
        Delete all chunks associated with a specific file.
        """
        result = await self.collection.delete_many({"file_id": file_id})
        return result.deleted_count > 0
    

    async def get_user_chunks(self, user_id: str, page: int = 0, limit: int = 100):
        """
        Get all chunks for a specific user.
        """
        chunks = []
        cursor = self.collection.find({"user_id": user_id}).skip(page * limit).limit(limit)
        async for chunk in cursor:
            chunks.append(TextChunk(**chunk))
        return chunks
    

    async def get_chunks_by_file_id(self, file_id: str):
        """
        Get all chunks for a specific file.
        """
        chunks = []
        cursor = self.collection.find({"file_id": file_id})
        async for chunk in cursor:
            chunks.append(TextChunk(**chunk))
        return chunks
    