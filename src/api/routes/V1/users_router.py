from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from core.config import get_settings, Settings
from api.schemas.users_api_schemas import UserResponse
from integrations.db.models.users import UserModel
from integrations.db.schemas.user import User
from controllers.users_controller import UserController

import logging

logger = logging.getLogger(__name__)

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@users_router.post("/create_user", response_model=UserResponse)
async def create_user(request: Request, user: User):
    """
    Create a new user.
    
    Args:
        user (UserSchema): The user data to create.
        
    Returns:
        JSONResponse: The response containing the created user data.
        
    Raises:
        HTTPException: If the user already exists or if there is an error during creation.
    """
    logger.info("Creating a new user...")
    
    user_controller = UserController(db_client=request.app.db_client)
    user_controller.create_user(user)

@users_router.get("/get_user", response_model=UserResponse)
async def get_user(request: Request, user_email: str):
    """
    Get user by email.
    
    Args:
        user_email (str): The email of the user to retrieve.
        
    Returns:
        JSONResponse: The response containing the user data.
        
    Raises:
        HTTPException: If the user does not exist or if there is an error during retrieval.
    """
    logger.info("Retrieving user...")
    
    user_controller = UserController(db_client=request.app.db_client)
    
    try:
        user_data = await user_controller.get_user_by_email(user_email)
        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=user_data.dict())
    
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@users_router.post("/delete_user", response_model=UserResponse)
async def delete_user(request: Request, user_email: str = None, user_id: str = None):
    """
    delete user by email or id.
    
    Args:
        user_email (str): The email of the user to retrieve.
        
    Returns:
        JSONResponse: The response containing the operation signal and details.
        
    Raises:
        HTTPException: If the user does not exist or if there is an error during deletion.
    """
    logger.info("Retrieving user...")
    
    user_controller = UserController(db_client=request.app.db_client)
    
    try:
        response = await user_controller.delete_user(user_email=user_email, user_id=user_id)
        return response
    
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))