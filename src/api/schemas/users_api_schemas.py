from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson.objectid import ObjectId
from integrations.db.schemas.user import AgentConfig

class UserResponse(BaseModel):
    _id: Optional[ObjectId] = Field(default=None) # Unique identifier for the user, should be indexed
    user_email: Optional[EmailStr] = Field(default=None)# Unique identifier for the user, should be indexed
    signal: str # Signal for the operation
    detail: Optional[str] = Field(default=None) # Details about the operation