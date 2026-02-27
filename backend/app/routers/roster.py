"""Roster API endpoints."""

from __future__ import annotations

from typing import Generator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import League
from ..schemas import RosterResponse

router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=RosterResponse)
def read_roster(db: Session = Depends(get_db)) -> RosterResponse:
    """Return the roster for the current league.

    If no league exists in the database this endpoint returns a 404.  The
    roster is nested under the league object along with team and player
    information.
    """
    league = db.query(League).first()
    if not league:
        raise HTTPException(status_code=404, detail="No league found")
    return {"league": league}
