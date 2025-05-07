from core.config import get_settings


class BaseDataModel:
    """
    Base class for all data models.
    """

    def __init__(self, db_client: object):
        self.settings = get_settings()
        self.db_client = db_client
            

