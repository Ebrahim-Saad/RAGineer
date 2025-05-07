from controllers.base_controller import BaseController
from fastapi import UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from core.config import get_settings, Settings
import os
import aiofiles
from typing import Optional
from integrations.db.models.users import UserModel
from integrations.db.schemas.user import User
import logging

logger = logging.getLogger(__name__)

class UserController(BaseController):
    def __init__(self, db_client):
        super().__init__()
        self.db_client = db_client

    async def create_user(self, user: User):
        """
        Create a new user.
        
        Args:
            user (User): The user data to create.
            
        Returns:
            JSONResponse: The response containing the created user data.
            
        Raises:
            HTTPException: If the user already exists or if there is an error during creation.
        """
        logger.info("Creating a new user...")
        
        user_model = UserModel(db_client=self.db_client)
        
        try:
            existing_user = await user_model.get_user_by_email(user.email)
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
            
            new_user_id = await user_model.create_user(user)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                 content={"detail": "User created successfully", "user_id": new_user_id})
        
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    async def get_user_by_email(user_email: str):
        """
        Get user by email.
        
        Args:
            user_email (str): The email of the user to retrieve.
            
        Returns:
            JSONResponse: The response containing the user data.
            
        Raises:
            HTTPException: If the user does not exist or if there is an error during retrieval.
        """
        logger.info("Retrieving user by email...")
        
        user_model = UserModel(db_client=self.db_client)
        
        try:
            user = await user_model.get_user_by_email(user_email)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            return JSONResponse(status_code=status.HTTP_200_OK, content={
                'detail'="User retrieved successfully",
                "user_id": user.user_id,
                "user_email": user.email,
            })
        
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def delete_user(user_id: Optional[str] = None, user_email: Optional[str] = None):
        """
        Delete a user by ID or email.
        
        Args:
            user_id (str): The ID of the user to delete.
            user_email (str): The email of the user to delete.
            
        Returns:
            JSONResponse: The response containing the status of the deletion.
            
        Raises:
            HTTPException: If the user does not exist or if there is an error during deletion.
        """
        logger.info("Deleting user...")
        
        user_model = UserModel(db_client=self.db_client)
        
        try:
            if user_id:
                deleted = await user_model.delete_user(user_id)
            elif user_email != None:
                user = await user_model.get_user_by_email(user_email)
                user_id = user.user_id if user else None
                if not user_id:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                deleted = await user_model.delete_user(user.user_id)
            
            if not deleted:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="error deleting the user, or it does not exist")
            
            return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "User deleted successfully",
                                                                          "user_id": user_id})
        
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))