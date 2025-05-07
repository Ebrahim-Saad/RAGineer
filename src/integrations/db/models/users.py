from .base_model import BaseDataModel
from schemas.user import User
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.enums.db_enums import DataBaseEnum

class UserModel(BaseDataModel):
    
    def __init__(self, db_client: AsyncIOMotorClient):
        super().__init__(db_client)
    
        self.collection = self.db_client[DataBaseEnum.USERS_DB_NAME.value]
        self.collection.create_index("username", unique=True)

    async def create_user(self, user: User):
        """
        Create a new user in the database.
        """
        user_dict = user.dict()
        result = await self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    async def get_user(self, user_email: str):
        """ get user by id"""

        user = await self.collection.find_ond({"email": user_email})
        if user:
            return User(**user)
        return None
    
    async def get_user_by_email(self, user_email: str):
        """ get user by email"""
        user = await self.collection.find_one({"email": user_email})
        if user:
            return User(**user)
        return None
    
    async def update_user(self, user_id: str, user: User):
        """ update user by id"""
        user_dict = user.dict()
        result = await self.collection.update_one({"_id": user_id}, {"$set": user_dict})
        return result.modified_count > 0

    async def delete_user(self, user_id: str):
        """ delete user by id"""
        result = await self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0
    