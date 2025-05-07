from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException, Request
from fastapi.responses import JSONResponse
from core.config import get_keys, get_settings, Settings
from controllers.data_controller import DataController
from controllers.process_controller import ProcessController
from api.schemas.data_schemas import AddFileSchema, DeleteFileSchema
from integrations.db.models.files import FileModel
from integrations.db.schemas.file import UploadedFile
import logging
import os

logger = logging.getLogger(__name__)

data_router = APIRouter(
    prefix="/data",
    tags=["data"],
)


@data_router.post("/upload_file/{user_id}")
async def upload_file(request: Request, user_id: str, file: UploadFile = File(...),
                       settings: Settings = Depends(get_settings)):
    logger.info("Uploading file...")

    file_extension = file.filename.split(".")[-1]
    data_controller = DataController(db_client=request.app.db_client)
    process_controller = ProcessController(db_client=request.app.db_client)
    try:
        await data_controller.validate_file(file)
        save_ret = await data_controller.save_file(user_id=user_id,
                                                    file_extension=file_extension, 
                                                    file=file)

        logger.info(f"File saved at {save_ret['file_path']}")
        # Add file to the database


        chunk_ids = await process_controller.add_file(file_id = save_ret['file_db_id'],add_file_args=
            AddFileSchema(  file_path=save_ret['file_path'],
                            user_id=user_id,
                            file_extension=file_extension,
                            chunk_size=data_controller.settings.DEFAULT_CHUNK_SIZE, 
                            chunk_overlap=data_controller.settings.DEFAULT_CHUNK_OVERLAP))
        logger.info(f"{len(chunk_ids)} chunks added to the database with IDs: {chunk_ids}")
        # Return the response
        return JSONResponse({'signal': status.HTTP_200_OK, 'message': 'File uploaded successfully', 
                             **save_ret, 'chunk_ids': chunk_ids})
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        if os.path.exists(save_ret['file_path']):
            os.remove(save_ret['file_path'])
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
     

@data_router.delete("/delete_file")
async def delete_file(request: Request, user_id: str, file_id: str, 
                      settings: Settings = Depends(get_settings)):
    """
    Delete a file from the server and the database.
    
    Args:
        user_id (str): The ID of the user.
        file (DeleteFileSchema): The file data to delete.
        
    Returns:
        JSONResponse: The response containing the status of the deletion.
        
    Raises:
        HTTPException: If the file does not exist or if there is an error during deletion.
    """
    logger.info("Deleting file...")
    
    data_controller = DataController(db_client=request.app.db_client)
    
    try:
        # Delete the file from the server
        delete_request = DeleteFileSchema(
            user_id=user_id,
            file_id=file_id
        )
        await data_controller.delete_file(delete_request)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "File deleted successfully"})
    
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


