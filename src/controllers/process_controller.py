from controllers.base_controller import BaseController
from api.schemas.data_schemas import AddFileSchema, DeleteFileSchema
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter
from integrations.db.models.text_chunks import ChunkModel
from integrations.db.schemas.text_chunk import TextChunk
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class ProcessController(BaseController):
    def __init__(self, db_client):
        super().__init__()
        self.db_client = db_client
        
    async def process_pdf(self, add_file_args: AddFileSchema):
        """
        Process a PDF file and return the documents.

        Future work:
        - add image processing
        """
        loader = PyMuPDFLoader(add_file_args.file_path)
        docs = loader.load()
        return docs
    


    async def add_file(self, add_file_args: AddFileSchema, file_id: str):
        try:
            if(add_file_args.file_extension == "pdf"):
                docs = await self.process_pdf(add_file_args)
            else:
                loader = TextLoader(add_file_args.file_path)
                docs = loader.load()
        
            logger.info(f"Loaded {len(docs)} documents from {add_file_args.file_path}")

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=add_file_args.chunk_size, 
                chunk_overlap=add_file_args.chunk_overlap)
            chunks = text_splitter.split_documents(docs)

            logger.info(f"Split {len(docs)} documents into {len(chunks)} chunks")
            # Save chunks to the database
            chunk_model = await ChunkModel.create_instance(self.db_client)
            ids = []
            # Save each chunk to the database
            for chunk in chunks:
                chunk_dict = {
                    "user_id": add_file_args.user_id,
                    "file_id": file_id,
                    "chunk_text": chunk.page_content,
                    "chunk_metadata": chunk.metadata,
                }
                ids.append(await chunk_model.add_chunk(TextChunk(**chunk_dict)))
            return ids
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    

