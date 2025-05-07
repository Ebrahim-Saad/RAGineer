from fastapi import FastAPI, APIRouter
from api.routes.V1.data_router import data_router
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import get_settings
import uvicorn


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn.get_database(settings.MONGODB_DATABASE)


@app.on_event("shutdown")
async def shotdown_db_client():
    app.mongo_conn.close()


app.include_router(data_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
