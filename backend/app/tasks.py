"""Celery tasks for periodic data ingestion.

This module defines Celery tasks that synchronise data from various sources
into the database.  The default schedule is configured via the ``beat_schedule``
dictionary so that tasks run automatically once the worker starts.  You can
adjust the cadence by editing those schedules.
"""

from __future__ import annotations

import os
from datetime import timedelta
from typing import List, Dict, Any

from celery import Celery

from .database import SessionLocal
from .models import League, Team, Player, RosterEntry
from .connectors import (
    ottoneu_connector,
    statcast_connector,
    projections_connector,
    news_connector,
)


# Configure Celery to use Redis as a broker and result backend.  These URLs
# correspond to the docker‑compose services.  You can override them via
# environment variables.
broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
backend_url = os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/1")

celery = Celery(
    "tasks",
    broker=broker_url,
    backend=backend_url,
)

# Periodic task schedule: each entry defines a task, its frequency and
# human‑readable name.  Intervals are in seconds.
celery.conf.beat_schedule = {
    "sync-ottoneu-roster": {
        "task": "tasks.sync_ottoneu_roster",
        "schedule": timedelta(minutes=5),
    },
    "sync-statcast": {
        "task": "tasks.sync_statcast",
        "schedule": timedelta(hours=24),
    },
    "sync-projections": {
        "task": "tasks.sync_projections",
        "schedule": timedelta(hours=24),
    },
    "sync-news": {
        "task": "tasks.sync_news",
        "schedule": timedelta(minutes=10),
    },
}


@celery.task(name="tasks.sync_ottoneu_roster")
def sync_ottoneu_roster() -> None:
    """Synchronise the Ottoneu roster for the configured league.

    If ``OTTONEU_LEAGUE_ID`` is not set the task will simply log and exit.
    The roster export is parsed and merged into the database.  Existing
    players are updated; new players/teams are created as necessary.
    """
    league_id = os.getenv("OTTONEU_LEAGUE_ID")
    if not league_id:
        print("Skipping sync_ottoneu_roster: OTTONEU_LEAGUE_ID not set")
        return
    print(f"Syncing roster for league {league_id}")
    players_data = ottoneu_connector.fetch_roster(league_id)
    db = SessionLocal()
    try:
        # Ensure league exists
        league = db.query(League).filter_by(ottoneu_league_id=int(league_id)).first()
        if not league:
            league = League(ottoneu_league_id=int(league_id), name=f"League {league_id}")
            db.add(league)
            db.commit()
            db.refresh(league)
        # For now, assign all players to a single Team record.  A real system
        # would parse team names/IDs from the export and create one Team per club.
        team = db.query(Team).filter_by(league_id=league.id).first()
        if not team:
            team = Team(league_id=league.id, name="My Team", cap_space=0.0)
            db.add(team)
            db.commit()
            db.refresh(team)
        # Clear existing roster entries
        db.query(RosterEntry).filter(RosterEntry.team_id == team.id).delete()
        db.commit()
        # Insert players and roster entries
        for record in players_data:
            # Determine numeric IDs if present; fields may vary across exports
            mlbam_id = None
            fangraphs_id = None
            ottoneu_player_id = None
            for key in record:
                lk = key.lower()
                if "mlbam" in lk:
                    try:
                        mlbam_id = int(record[key]) if record[key] else None
                    except ValueError:
                        mlbam_id = None
                if "fangraph" in lk:
                    try:
                        fangraphs_id = int(record[key]) if record[key] else None
                    except ValueError:
                        fangraphs_id = None
                if "ottoneu" in lk and "player" in lk:
                    try:
                        ottoneu_player_id = int(record[key]) if record[key] else None
                    except ValueError:
                        ottoneu_player_id = None
            name = record.get("player_name") or record.get("name") or "Unknown"
            position = record.get("position") or record.get("pos")
            try:
                salary = float(record.get("salary", 0))
            except ValueError:
                salary = 0.0
            # Retrieve or create player
            player = None
            if ottoneu_player_id:
                player = db.query(Player).filter_by(ottoneu_player_id=ottoneu_player_id).first()
            if not player and mlbam_id:
                player = db.query(Player).filter_by(mlbam_id=mlbam_id).first()
            if not player:
                player = Player(
                    ottoneu_player_id=ottoneu_player_id,
                    fangraphs_id=fangraphs_id,
                    mlbam_id=mlbam_id,
                    name=name,
                    position=position,
                )
                db.add(player)
                db.commit()
                db.refresh(player)
            # Create roster entry
            roster_entry = RosterEntry(team_id=team.id, player_id=player.id, salary=salary, acquired="import")
            db.add(roster_entry)
        db.commit()
        print(f"Imported {len(players_data)} roster entries")
    finally:
        db.close()


@celery.task(name="tasks.sync_statcast")
def sync_statcast() -> None:
    """Fetch Statcast data and update players with advanced stats (stub)."""
    print("Syncing Statcast data")
    data = statcast_connector.fetch_statcast_leaderboard()
    db = SessionLocal()
    try:
        for item in data:
            mlbam_id = item.get("mlbam_id")
            player = db.query(Player).filter_by(mlbam_id=mlbam_id).first()
            if player:
                # In a real implementation you would store Statcast fields in the database.
                # For demonstration we simply print them.
                print(f"Updating player {player.name} with Statcast metrics {item}")
    finally:
        db.close()


@celery.task(name="tasks.sync_projections")
def sync_projections() -> None:
    """Fetch rest‑of‑season projections and update players (stub)."""
    print("Syncing projections")
    data = projections_connector.fetch_ros_projections()
    db = SessionLocal()
    try:
        for item in data:
            mlbam_id = item.get("mlbam_id")
            proj_points = item.get("proj_points")
            player = db.query(Player).filter_by(mlbam_id=mlbam_id).first()
            if player:
                # TODO: store projections in a separate table or column
                print(f"Updating player {player.name} with projection {proj_points}")
    finally:
        db.close()


@celery.task(name="tasks.sync_news")
def sync_news() -> None:
    """Fetch player news and log it (stub)."""
    print("Syncing news")
    items = news_connector.fetch_player_news()
    for item in items:
        print(f"News for MLBAM {item['mlbam_id']}: {item['headline']} ({item['timestamp']})")
