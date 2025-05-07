#enums for database
from enum import Enum


class DataBaseEnum(Enum):
    """Enum for database collections."""
    USERS_DB_NAME = "users"
    FILES_DB_NAME = "files"
    CHUNKS_DB_NAME = "chunks"
    SESSIONS_DB_NAME = "sessions"
