from fastapi import FastAPI, APIRouter
from api.routes.V1.data_router import data_router
import uvicorn
app = FastAPI()


app.include_router(data_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
