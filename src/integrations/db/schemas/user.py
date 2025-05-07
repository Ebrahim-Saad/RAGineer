from pydantic import BaseModel, Field, EmailStr
from bson.objectid import ObjectId
from typing import Optional
from datetime import datetime


class AgentConfig(BaseModel):
    custom_instructions: Optional[str] = Field(default=None, max_length=500)
    preferred_model: Optional[str] = Field(default=None)

class User(BaseModel):
    _id: ObjectId
    user_email: EmailStr # Unique identifier for the user, should be indexed
    user_first_name: str
    user_last_name: str
    user_rule: Optional[str] = Field(default="user") # Role of the user, default is "user"
    user_hashed_password: str
    user_agent_config: AgentConfig

