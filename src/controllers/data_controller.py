from controllers.base_controller import BaseController
from fastapi import UploadFile, File, HTTPException, status
from core.config import get_settings, Settings
import os
import aiofiles
from typing import Optional

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.MB_size_scale = 1024 * 1024 # bytes in a megabyte
        self.GB_size_scale = self.MB_size_scale * 1024 # bytes in a gigabyte
        self.KB_size_scale = 1024 # bytes in a kilobyte

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
    
    async def save_file(self, file: UploadFile = File(...), path: str = "uploads") -> str:
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
        file_path = os.path.join(self.base_dir, "assets", path)
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        
        file_path = os.path.join(file_path, file.filename)
        
        try:
            async with aiofiles.open(file_path, "wb") as f:
                while chunk := await file.read(self.settings.DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)
            return file_path
        except Exception as e:
            # Clean up the file if it was partially written
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
