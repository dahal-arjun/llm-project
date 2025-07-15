import os
import shutil
import uuid
from typing import List, Dict, Any, Optional
from fastapi import UploadFile
from src.core.config import settings
from src.db.chroma_client import chroma_client

class FileService:
    def __init__(self):
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    def chunk_text(self, text: str, chunk_size: Optional[int] = 1000) -> List[str]:
        """Split text into chunks of approximately equal size"""
        # Simple chunking by character count
        chunks = []
        
        # Ensure chunk_size is an integer
        if chunk_size is None:
            chunk_size = 1000
        
        # If text is shorter than chunk_size, return it as a single chunk
        if len(text) <= chunk_size:
            return [text]
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size, save current chunk and start a new one
            if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def process_file(self, file: UploadFile, collection_name: str, chunk_size: int = 1000, keep_file: bool = False) -> Dict[str, Any]:
        """
        Process an uploaded file and add its content to the specified collection
        
        Args:
            file: The uploaded file
            collection_name: The name of the collection to add the document to
            chunk_size: The size of chunks to split the document into
            keep_file: Whether to keep the uploaded file
            
        Returns:
            A dictionary with information about the processed file
        """
        # Validate file extension
        if not file.filename or not (file.filename.endswith('.txt') or file.filename.endswith('.md')):
            raise ValueError("Only .txt and .md files are supported")
        
        file_path = ""
        try:
            # Save the file temporarily
            file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Split content into chunks
            chunks = self.chunk_text(content, chunk_size)
            
            # Generate IDs for chunks
            chunk_ids = [str(uuid.uuid4()) for _ in chunks]
            
            # Add chunks to collection with metadata
            chroma_client.add_documents(
                collection_name=collection_name,
                documents=chunks,
                ids=chunk_ids,
                metadatas=[{"source": file.filename, "chunk": i} for i in range(len(chunks))]
            )
            
            # Clean up if not keeping the file
            if not keep_file:
                os.remove(file_path)
            
            return {
                "message": f"File '{file.filename}' processed successfully",
                "collection": collection_name,
                "chunks_added": len(chunks),
                "file_kept": keep_file
            }
            
        except Exception as e:
            # Clean up in case of error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise e

# Create a singleton instance
file_service = FileService() 