from controllers.base_controller import BaseController
from fastapi import UploadFile, File, HTTPException, status
from core.config import get_settings, Settings
import os
import aiofiles
from typing import Optional
from api.schemas.data_schemas import AddFileSchema, DeleteFileSchema
from integrations.db.models.files import FileModel
from integrations.db.models.text_chunks import ChunkModel
from integrations.db.schemas.file import UploadedFile
import logging

logger = logging.getLogger(__name__)

class DataController(BaseController):
    def __init__(self, db_client):
        super().__init__()
        self.MB_size_scale = 1024 * 1024 # bytes in a megabyte
        self.GB_size_scale = self.MB_size_scale * 1024 # bytes in a gigabyte
        self.KB_size_scale = 1024 # bytes in a kilobyte
        self.db_client = db_client

    async def validate_file(self, file: UploadFile = File(...)):
        """
        Validate the file's content type and size.
        
        Raises:
            HTTPException: If the file is invalid
        """
        if file.content_type not in self.settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type"
            )
        
        if file.size > self.settings.MAXIMUM_FILE_SIZE * self.MB_size_scale:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size is too large"
            )
        
        return True
    
    async def save_file(self, user_id: str, file_extension: str, file: UploadFile = File(...)) -> str:
        """
        Save a file in chunks to prevent memory issues with large files.
        
        Args:
            file: The file to save
            path: The relative path where the file should be saved
            
        Returns:
            str: The path where the file was saved
            
        Raises:
            HTTPException: If the file cannot be saved
        """

        name = await self.generate_random_id(10, False) + "." + file_extension

        file_path = os.path.join(self.users_files_path, user_id)
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        
        file_path = os.path.join(file_path, name)
        
        try:
            async with aiofiles.open(file_path, "wb") as f:
                while chunk := await file.read(self.settings.DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)

            logger.info(f"File saved at {file_path}")

            # Add file to the database
            file_model = await FileModel.create_instance(self.db_client)
            file_data = UploadedFile(
                user_id=user_id,
                file_name=file.filename,
                file_path=file_path,
                file_type=file.content_type,
                file_size_bytes=os.path.getsize(file_path),
            )
            inserted_id = await file_model.create_file(file_data)
            logger.info(f"File data saved in database with ID: {inserted_id}")

            return {"file_path": file_path, "file_db_id": str(inserted_id)}
        except Exception as e:
            # Clean up the file if it was partially written
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
        
    async def delete_file(self, delete_request: DeleteFileSchema):
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
        try:
            file = await FileModel.create_instance(db_client=self.db_client)
            file_data = await file.get_file(file_id=delete_request.file_id)
            file_path = file_data.file_path if file_data else None
            if not file_path:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"file id {delete_request.file_id} not found in database")
            
            # Delete the file from the server
            os.remove(file_data.file_path)
            logger.info(f"File deleted from server: {file_path}")
            
            # Delete the file from the database
            file_model = await FileModel.create_instance(self.db_client)
            chunk_model = await ChunkModel.create_instance(self.db_client)
            file_deleted = await file_model.delete_file(file_id=delete_request.file_id)
            if not file_deleted:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error deleting the file from the database, or it does not exist")
            chunks_deleted = await chunk_model.delete_file_chunks(file_id=delete_request.file_id)
            if not chunks_deleted:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error deleting the file chunks, or they do not exist")
            logger.info(f"File deleted from database with ID: {delete_request.file_id}")
            return {"message": "File deleted successfully"}
        
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
        
