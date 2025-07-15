import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "LangGraph RAG API with Ollama LLM"
    PROJECT_VERSION: str = "1.0.0"
    
    # API Settings
    API_PREFIX: str = ""
    
    # Database Settings
    CHROMA_HOST: str = os.environ.get("CHROMA_HOST", "localhost")
    CHROMA_PORT: int = int(os.environ.get("CHROMA_PORT", "8000"))
    
    # LLM Settings
    OLLAMA_HOST: str = os.environ.get("OLLAMA_HOST", "localhost")
    OLLAMA_PORT: int = int(os.environ.get("OLLAMA_PORT", "11434"))
    DEFAULT_MODEL: str = "tinyllama:latest"
    
    # File Storage Settings
    UPLOAD_DIR: str = "data/uploads"
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

settings = Settings() 