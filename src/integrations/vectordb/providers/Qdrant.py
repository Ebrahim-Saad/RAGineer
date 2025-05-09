from ..vectorDB_interface import VectorDBInterface
from ..vectorDB_enums import VectorDBType, DistanceMethods
from qdrant_client import QdrantClient, models
from typing import List, Dict

import logging



class QdrantDB(VectorDBInterface):

    def __init__(self, 
                 db_path: str,
                 distance_method: str,
                 embedding_size: int = 1536):
        self.client = None
        self.distance_method = None
        self.db_path = db_path
        self.embedding_size = embedding_size

        if distance_method == DistanceMethods.COSINE:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethods.EUCLIDEAN:
            self.distance_method = models.Distance.EUCLIDEAN
        else:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)
        
    def connect(self):
        """Connect to the Qdrant database."""
        self.client = QdrantClient(path=self.db_path)
        self.logger.info("Connected to Qdrant database.")
    
    def disconnect(self):
        """Sets the client to None because there is no disconnect metod in QDrant."""
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in the Qdrant database."""
        return self.client.get_collection(collection_name) is not None
    
    def list_all_collections(self) -> List:
        """List all collections in the Qdrant database."""
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> Dict:
        """Get information about a specific collection in the Qdrant database."""
        return self.client.get_collection(collection_name)
    
    def create_collection(self, collection_name: str,
                            embedding_size: int = self.embedding_size,
                            do_reset: bool = False):
          """Create a new collection in the Qdrant database."""
          if self.is_collection_exists(collection_name) and do_reset:
                self.logger.info(f"Collection {collection_name} already exists. Resetting...")
                self.client.delete_collection(collection_name)
          
          if self.is_collection_exists(collection_name):
                self.logger.error(f"Collection {collection_name} already exists.")
                return False
          
          try:
                self.logger.info(f"Creating Qdrant collection {collection_name}...")
                self.client.create_collection(
                 collection_name=collection_name,
                 vector_config = models.VectorParams(
                     size=embedding_size,
                     distance=self.distance_method
                 ),
                 
                )
                self.logger.info(f"Collection {collection_name} created successfully.")
                return True
          except Exception as e:
                self.logger.error(f"Error creating Qdrant collection {collection_name}: {e}")
                return False

    def delete_collection(self, collection_name: str):
        """Delete a collection from the Qdrant database."""
        if(self.is_collection_exists(collection_name) == False):
            self.logger.error(f"Collection {collection_name} does not exist.")
            return False
        try:
            self.logger.info(f"Deleting Qdrant collection {collection_name}...")
            self.client.delete_collection(collection_name)
            self.logger.info(f"Collection {collection_name} deleted succesfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting Qdrant collection {collection_name}: {e}")
            return False


    def insert(self, collection_name: str,
                vector: List[float],
                metadata: Dict,
                id: str = None):
        """Insert a single vector into the Qdrant database."""
        if self.is_collection_exists(collection_name) == False:
            self.logger.error(f"Collection {collection_name} does not exist.")
            return False
        try:
            self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=id,
                        vector=vector,
                        payload=metadata
                    )
                ]
            ) 
            self.logger.info(f"Vector inserted into collection {collection_name}.")
            return True
        except Exception as e:
            self.logger.error(f"Error inserting vector into Qdrant collection {collection_name}: {e}")
            return False

    def insert_many(self, collection_name: str,
                    vectors: List[List[float]],
                    metadatas: List[Dict],
                    ids: List[str] = None,
                    batch_size: int = 50):
        """Insert multiple vectors into the Qdrant database in batches."""
        if self.is_collection_exists(collection_name) == False:
            self.logger.error(f"Collection {collection_name} does not exist.")
            return False
        try:
            self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=id,
                        vector=vector,
                        payload=metadata
                    )
                    for id, vector, metadata in zip(ids, vectors, metadatas)
                ],
                batch_size=batch_size
            )
            self.logger.info(f"Vectors inserted into collection {collection_name}.")
            return True
        except Exception as e:
            self.logger.error(f"Error inserting vectors into Qdrant collection {collection_name}: {e}")
            return False
        
    def query_vector(self, collection_name: str,
                    query_vector: List[float],
                    limit: int = 5):
        """Query the Qdrant database for similar vectors."""
        if self.is_collection_exists(collection_name) == False:
            self.logger.error(f"Collection {collection_name} does not exist.")
            return None
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
            self.logger.info(f"Query executed on collection {collection_name}.")
            return results
        except Exception as e:
            self.logger.error(f"Error querying Qdrant collection {collection_name}: {e}")
            return None