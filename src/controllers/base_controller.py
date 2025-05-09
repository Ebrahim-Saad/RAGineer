from core.config import get_settings, Settings
from fastapi import Depends
import os
import random
import string

class BaseController:
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = os.path.dirname(os.getcwd())
        self.assets_path = os.path.join(self.base_dir,"assets")
        self.users_files_path = os.path.join(self.assets_path, "users_files")
    async def get_settings(self):
        return self.settings
    


    async def generate_random_id(self, length: int =10, number_only: bool = False):
        if number_only:
            return ''.join(random.choices(string.digits, k=length))
        else:
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
    async def get_vector_db_path(self):
        return self.base_dir + self.settings.VECTOR_DB_PATH
