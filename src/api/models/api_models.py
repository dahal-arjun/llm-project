from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AskResponse(BaseModel):
    """Response model for the ask endpoint"""
    answer: str
    sources: List[Dict[str, Any]]

class CollectionResponse(BaseModel):
    """Response model for the collections endpoint"""
    collections: List[str]

class CollectionCreateResponse(BaseModel):
    """Response model for the collection creation endpoint"""
    message: str

class FileUploadResponse(BaseModel):
    """Response model for the file upload endpoint"""
    message: str
    collection: str
    chunks_added: int
    file_kept: bool

class ErrorResponse(BaseModel):
    """Response model for errors"""
    detail: str 