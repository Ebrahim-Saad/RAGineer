from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    ALLOWED_FILE_TYPES: list[str]
    MAXIMUM_FILE_SIZE: int
    DEFAULT_CHUNK_SIZE: int
    class Config:
        env_file = ".env"

class keys:
    TAVILY_API_KEY: str
    TOGETHER_API_KEY: str

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()

def get_keys() -> keys:
    return keys()
