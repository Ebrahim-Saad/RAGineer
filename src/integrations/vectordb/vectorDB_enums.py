from enum import Enum


class VectorDBType(Enum):
    """Enum for different types of vector databases."""

    QDRANT = "qdrant"

    # to be added in the future
    FAISS = "faiss"
    MILVUS = "milvus"
    WEAVIATE = "weaviate"



class DistanceMethods(Enum):
    """Enum for different distance methods."""

    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT = "dot"


