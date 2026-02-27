"""Pydantic schemas used for API responses and requests."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PlayerBase(BaseModel):
    id: int
    name: str
    position: Optional[str] = None
    ottoneu_player_id: Optional[int] = None
    fangraphs_id: Optional[int] = None
    mlbam_id: Optional[int] = None

    class Config:
        orm_mode = True


class RosterEntryBase(BaseModel):
    id: int
    salary: Optional[float] = None
    acquired: Optional[str] = None
    player: PlayerBase

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    id: int
    name: Optional[str] = None
    cap_space: Optional[float] = None
    roster_entries: List[RosterEntryBase] = []

    class Config:
        orm_mode = True


class LeagueBase(BaseModel):
    id: int
    ottoneu_league_id: int
    name: Optional[str] = None
    teams: List[TeamBase] = []

    class Config:
        orm_mode = True


class RosterResponse(BaseModel):
    league: LeagueBase
