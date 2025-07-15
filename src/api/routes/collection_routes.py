from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.api.models.api_models import CollectionResponse, CollectionCreateResponse
from src.api.dependencies.dependencies import get_chroma_client
from src.db.chroma_client import ChromaDBClient

router = APIRouter(prefix="/collections", tags=["Collections"])

@router.get("", response_model=CollectionResponse)
async def get_collections(chroma_client: ChromaDBClient = Depends(get_chroma_client)):
    """List all collections in the database"""
    collections = chroma_client.list_collections()
    return {"collections": collections}

@router.post("/{collection_name}", response_model=CollectionCreateResponse)
async def create_collection(collection_name: str, chroma_client: ChromaDBClient = Depends(get_chroma_client)):
    """Create a new collection"""
    try:
        chroma_client.create_collection(name=collection_name)
        return {"message": f"Collection '{collection_name}' created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 