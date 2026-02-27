"""Router package for API endpoints."""

from fastapi import APIRouter

from . import roster

api_router = APIRouter()

# Roster endpoints
api_router.include_router(roster.router, prefix="/roster", tags=["Roster"])
