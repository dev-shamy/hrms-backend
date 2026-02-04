from fastapi import APIRouter
from src.routes.admin_routes.admin_endpoints import router as admin_router
api_router = APIRouter()

api_router.include_router(admin_router, prefix="/admin")
