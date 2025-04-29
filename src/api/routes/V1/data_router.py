from fastapi import APIRouter, Depends, UploadFile, File, status
from core.config import get_keys, get_settings, Settings
from controllers.data_controller import DataController
import os
data_router = APIRouter(
    prefix="/data",
    tags=["data"],
)


@data_router.post("/upload_file/{user_id}")
async def upload_file(user_id: str, file: UploadFile = File(...),
                       settings: Settings = Depends(get_settings)):
    print("Uploading file...")
    data_controller = DataController()
    await data_controller.validate_file(file)
    await data_controller.save_file(file, os.path.join("users_files", user_id))
    return {'signal': status.HTTP_200_OK, 'message': 'File uploaded successfully'}

     




