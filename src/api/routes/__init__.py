from fastapi import APIRouter
from src.api.routes.collection_routes import router as collection_router
from src.api.routes.file_routes import router as file_router
from src.api.routes.query_routes import router as query_router

# Create a router that includes all routes
router = APIRouter()

# Include all routers
router.include_router(collection_router)
router.include_router(file_router)
router.include_router(query_router) 