from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional

from src.api.models.api_models import FileUploadResponse
from src.api.dependencies.dependencies import get_file_service, get_chroma_client
from src.services.file_service import FileService
from src.db.chroma_client import ChromaDBClient

router = APIRouter(tags=["Files"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    collection_name: str = Form(...),
    chunk_size: Optional[int] = Form(1000),
    keep_file: bool = Form(False),
    file_service: FileService = Depends(get_file_service),
    chroma_client: ChromaDBClient = Depends(get_chroma_client)
):
    """
    Upload a .txt or .md file and add its content to the specified collection
    
    Parameters:
    - file: The file to upload (.txt or .md)
    - collection_name: The name of the collection to add the document to
    - chunk_size: The size of chunks to split the document into (default: 1000)
    - keep_file: Whether to keep the uploaded file in the data/uploads directory (default: False)
    """
    try:
        # Ensure chunk_size is an integer
        chunk_size_value = 1000 if chunk_size is None else chunk_size
        
        result = await file_service.process_file(
            file=file,
            collection_name=collection_name,
            chunk_size=chunk_size_value,
            keep_file=keep_file
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 