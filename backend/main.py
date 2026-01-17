"""
Agentic Fake News Detector API

A FastAPI application that uses a 3-step agentic pipeline to detect fake news:
1. Reader - Extracts core claims from articles
2. Researcher - Searches and scrapes trusted sources
3. Judge - Compares and renders a verdict

Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import verify_router, health_router


def create_app() -> FastAPI:
    """
    Application factory for creating the FastAPI app.
    """
    app = FastAPI(
        title=settings.app_name,
        description="An AI-powered fake news detection API using a 3-step agentic pipeline.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(verify_router)

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
