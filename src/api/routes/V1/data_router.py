from fastapi import APIRouter, Depends, UploadFile, File, status
from core.config import get_keys, get_settings, Settings
from controllers.data_controller import DataController
from controllers.process_controller import ProcessController
from api.schemas.data_schemas import AddFileSchema, DeleteFileSchema
import logging
import os

logger = logging.getLogger(__name__)

data_router = APIRouter(
    prefix="/data",
    tags=["data"],
)


@data_router.post("/upload_file/{user_id}")
async def upload_file(user_id: str, file: UploadFile = File(...),
                       settings: Settings = Depends(get_settings)):
    logger.info("Uploading file...")

    file_extension = file.filename.split(".")[-1]
    data_controller = DataController()
    process_controller = ProcessController()
    try:
        await data_controller.validate_file(file)
        file_path = await data_controller.save_file(user_id=user_id,
                                                    file_extension=file_extension, 
                                                    file=file)

        chunks = await process_controller.add_file(add_file_args=
            AddFileSchema(  file_path=file_path,
                            user_id=user_id,
                            file_extension=file_extension,
                            chunk_size=data_controller.settings.DEFAULT_CHUNK_SIZE, 
                            chunk_overlap=data_controller.settings.DEFAULT_CHUNK_OVERLAP))
        print(chunks)
        return {'signal': status.HTTP_200_OK, 'message': 'File uploaded successfully'}
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))
     




