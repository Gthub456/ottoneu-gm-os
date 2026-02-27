"""Database models for the Ottoneu GM OS.

These SQLAlchemy models represent the core entities of the system.  They are
designed to be simple but extensible.  Additional fields and tables can be
added as your analytics engine grows.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from .database import Base


class League(Base):
    __tablename__ = "leagues"
    id = Column(Integer, primary_key=True, index=True)
    ottoneu_league_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    teams = relationship("Team", back_populates="league")


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    ottoneu_team_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    cap_space = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    league = relationship("League", back_populates="teams")
    roster_entries = relationship("RosterEntry", back_populates="team")


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    ottoneu_player_id = Column(Integer, unique=True, index=True, nullable=True)
    fangraphs_id = Column(Integer, unique=True, index=True, nullable=True)
    mlbam_id = Column(Integer, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    roster_entries = relationship("RosterEntry", back_populates="player")


class RosterEntry(Base):
    __tablename__ = "roster_entries"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    salary = Column(Float, nullable=True)
    acquired = Column(String, nullable=True)  # e.g. 'draft', 'auction', etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    team = relationship("Team", back_populates="roster_entries")
    player = relationship("Player", back_populates="roster_entries")
