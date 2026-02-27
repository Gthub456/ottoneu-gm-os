"""Database and session configuration.

This module defines the SQLAlchemy engine, session factory and declarative base.  The
connection URL is pulled from the ``DATABASE_URL`` environment variable.  For local
development the default points at the `db` service in docker‑compose.
"""

from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/ottoneu",
)

# Create a synchronous engine.  For simplicity this project uses synchronous
# SQLAlchemy sessions; if you wish to switch to async, adjust accordingly.
engine = create_engine(DATABASE_URL)

# SessionLocal is used in endpoints and tasks to acquire a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models.
Base = declarative_base()

def init_db() -> None:
    """Initialise the database schema.

    During development the API server calls this at startup to ensure tables
    exist.  In production you should instead manage schema via Alembic
    migrations (see ``backend/alembic``).
    """
    import backend.app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
