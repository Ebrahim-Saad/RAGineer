from core.config import get_settings, Settings
from fastapi import Depends
import os

class BaseController:
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = os.path.dirname(os.getcwd())
        self.assets_path = os.path.join(self.base_dir,"assets")

    async def get_settings(self):
        return self.settings
