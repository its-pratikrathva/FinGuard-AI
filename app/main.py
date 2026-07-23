"""
FinGuard AI - FastAPI Application Entry Point

This module bootstraps the FastAPI application, configures middleware,
registers API routers, and exposes health-check endpoints.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.database.database import init_db

from app.api.scan import router as scan_router
from app.api.history import router as history_router
# from app.api.auth import router as auth_router
# from app.api.report import router as report_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler.

    Startup: initialize database connections, load data files, etc.
    Shutdown: clean up resources gracefully.
    """
    init_db()
    yield


def create_app() -> FastAPI:
    """
    Application factory — creates and configures the FastAPI instance.

    Using a factory pattern keeps the app testable and modular.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "AI-powered Financial Scam Detection System. "
            "Analyzes SMS, WhatsApp messages, and emails for phishing, "
            "OTP scams, fake KYC updates, and other fraud patterns."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS — allow React frontend to communicate with the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware will be registered here as modules are built
    # app.add_middleware(LoggingMiddleware)

    # Register API routers
    app.include_router(scan_router)
    app.include_router(history_router)
    # app.include_router(auth_router)
    # app.include_router(report_router)

    @app.get("/", tags=["Health"])
    async def root() -> dict[str, str]:
        """Root endpoint — confirms the API is running."""
        return {
            "message": "FinGuard AI API is running",
            "version": settings.APP_VERSION,
            "docs": "/docs",
        }

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict[str, str | list[str]]:
        """Health check endpoint for monitoring and load balancers."""
        from sqlalchemy import inspect

        from app.database.database import engine

        tables = inspect(engine).get_table_names()
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "database": "connected",
            "tables": tables,
        }

    return app


# Uvicorn entry point: uvicorn app.main:app --reload
app = create_app()
