"""FastAPI application entrypoint.

This module configures the FastAPI instance, mounts all routers and performs
basic initialisation such as creating tables.  When run in production the
database should be managed via Alembic migrations instead of auto‑creating
tables on startup.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Ottoneu GM OS API", version="0.1.0")
    # Enable CORS for the frontend development server
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Initialise DB (only for dev; use migrations in prod)
    init_db()
    # Mount API routes under /api
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
