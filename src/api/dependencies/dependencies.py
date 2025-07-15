from fastapi import Depends, HTTPException, status
from typing import Callable

from src.db.chroma_client import chroma_client
from src.services.ollama_service import ollama_service
from src.services.langgraph_service import langgraph_service
from src.services.file_service import file_service

def get_chroma_client():
    """Dependency for ChromaDB client"""
    if not chroma_client.client:
        success = chroma_client.connect()
        if not success:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not connect to ChromaDB"
            )
    return chroma_client

def get_ollama_service():
    """Dependency for Ollama service"""
    if not ollama_service.is_connected:
        success = ollama_service.connect()
        if not success:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not connect to Ollama service"
            )
    return ollama_service

def get_langgraph_service():
    """Dependency for LangGraph service"""
    return langgraph_service

def get_file_service():
    """Dependency for File service"""
    return file_service 