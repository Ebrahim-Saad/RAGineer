from controllers.base_controller import BaseController
from api.schemas.data_schemas import AddFileSchema, DeleteFileSchema
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class ProcessController(BaseController):
    def __init__(self):
        super().__init__()
        
    async def process_pdf(self, add_file_args: AddFileSchema):
        """
        Process a PDF file and return the documents.

        Future work:
        - add image processing
        """
        loader = PyMuPDFLoader(add_file_args.file_path)
        docs = loader.load()
        return docs
    


    async def add_file(self, add_file_args: AddFileSchema):
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

            return chunks
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    def delete_file(self, delete_file_args: DeleteFileSchema):
        pass

