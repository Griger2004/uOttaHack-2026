"""
Health check and status endpoints.
"""

from fastapi import APIRouter
from config import settings

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    """
    Root endpoint - API health check and information.
    """
    return {
        "message": f"{settings.app_name} API",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "POST /verify": "Verify an article for fake news",
            "GET /health": "Detailed health check",
        },
    }


@router.get("/health")
async def health_check():
    """
    Detailed health check endpoint.
    """
    return {
        "status": "healthy",
        "services": {
            "gemini": "configured" if settings.gemini_api_key else "not configured",
            "serper": "configured" if settings.serper_api_key else "not configured",
            "yellowcake": "configured" if settings.yellowcake_api_key else "not configured",
        },
    }
