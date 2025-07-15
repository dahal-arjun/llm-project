from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from src.api.models.api_models import AskResponse
from src.api.dependencies.dependencies import get_langgraph_service, get_ollama_service, get_chroma_client
from src.services.langgraph_service import LangGraphService
from src.services.ollama_service import OllamaService
from src.db.chroma_client import ChromaDBClient
from src.core.config import settings

router = APIRouter(tags=["Queries"])

@router.get("/ask", response_model=AskResponse)
async def ask(
    query: str,
    collection_name: str,
    model_name: str = Query(default=settings.DEFAULT_MODEL),
    langgraph_service: LangGraphService = Depends(get_langgraph_service),
    ollama_service: OllamaService = Depends(get_ollama_service),
    chroma_client: ChromaDBClient = Depends(get_chroma_client)
):
    """
    Ask a question and get an answer with sources using the LangGraph agent
    
    Parameters:
    - query: The question to ask
    - collection_name: The name of the collection to search in
    - model_name: The name of the Ollama model to use (default: tinyllama:latest)
    """
    try:
        # Update the model name if different from default
        if model_name != ollama_service.model_name:
            ollama_service.model_name = model_name
        
        # Run the LangGraph agent
        result = langgraph_service.run_agent(
            query=query,
            collection_name=collection_name
        )
        
        # Return the result
        return {
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        import traceback
        print(f"Error in ask endpoint: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e)) 