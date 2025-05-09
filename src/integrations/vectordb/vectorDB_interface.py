from abc import ABC, abstractmethod

from typing import Dict, List
class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def list_all_collections(self)-> List:
        pass
    
    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> Dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass
    @abstractmethod
    def create_collection(self, collection_name: str, 
                          embedding_size: int,
                          do_reset: bool = False,):
        pass
    
    @abstractmethod
    def insert(self, collection_name: str,
               vector: List[float],
               metadata: Dict,
               id: str = None,):
        pass

    @abstractmethod
    def insert_many(self, collection_name: str,
                    vectors: List[List[float]],
                    metadatas: List[Dict],
                    ids: List[str] = None, 
                    batch_size: int = 50):
        pass

    @abstractmethod
    def query_vector(self, collection_name: str,
                     query_vector: List[float],
                     limit: int = 10,):
        pass

    @abstractmethod
    def delete_chunk(self, collection_name : str, id: str):
        pass

