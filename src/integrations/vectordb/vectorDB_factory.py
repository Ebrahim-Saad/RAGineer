from providers import QdrantDB
from vectorDB_enums import VectorDBType
from ...core.config import get_settings
from ...controllers.base_controller import BaseController
class VectorDBFactory:
    def __init__(self):
        self.base_controller = BaseController()
        self.config = {
            "provider_name": self.base_controller.settings.VECTOR_DB_PROVIDER,
            "distance_method": self.base_controller.settings.VECTOR_DB_DISTANCE_METHOD,
            "embedding_size": self.base_controller.settings.VECTOR_DB_EMBEDDING_SIZE,
            "vector_db_path": self.base_controller.get_vector_db_path()
        }

    def create_vector_db(self):
        """
        Create a vector database client based on the config defined in the enviroment variables (.env).
        
        Returns:
            An instance of the vector database client.
        """
        if self.config['provider_name'] == VectorDBType.QDRANT.value:
            return QdrantDB(
                db_path=self.config["vector_db_path"],
                embedding_size=self.config["embedding_size"],
                distance_method=self.config["distance_method"]
            )
        else:
            raise ValueError(f"Unsupported vector database provider: {self.config['provider_name']}")