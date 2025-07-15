import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.core.config import settings
from src.api.routes import router
from src.db.chroma_client import chroma_client
from src.services.ollama_service import ollama_service

# Configure logger
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include API router
app.include_router(router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    logger.info("Starting application initialization")
    
    # Initialize database connection
    try:
        chroma_client.connect()
        logger.info("Successfully connected to ChromaDB")
    except Exception as e:
        logger.error(f"Failed to connect to ChromaDB: {e}")
    
    # Initialize LLM
    try:
        ollama_service.connect()
        logger.info(f"Successfully connected to Ollama using model: {ollama_service.model_name}")
    except Exception as e:
        logger.error(f"Failed to connect to Ollama: {e}")
    
    # Create upload directory if it doesn't exist
    try:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        logger.info(f"Created uploads directory at {settings.UPLOAD_DIR}")
    except Exception as e:
        logger.error(f"Failed to create uploads directory: {e}")
    
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down application")

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": f"{settings.PROJECT_NAME} is running"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "services": {
            "chroma": chroma_client.client is not None,
            "ollama": ollama_service.is_connected
        }
    }
    
    # If any service is down, return unhealthy status
    if not all(health_status["services"].values()):
        health_status["status"] = "unhealthy"
        logger.warning(f"Health check failed: {health_status}")
        return health_status, 503
    
    logger.debug("Health check passed")
    return health_status

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8081, reload=True) 