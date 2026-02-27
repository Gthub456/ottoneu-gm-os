"""Seed the database with demo data.

This script populates the database with a sample league, team and a few
players so that the frontend can render realistic data even when no
Ottoneu account has been connected.  Run this via ``make seed`` or
``python -m backend.app.seed_data``.

The demo dataset is intentionally small; feel free to modify or extend it
to suit your needs.  If the database already contains a league this
script will do nothing.
"""

from __future__ import annotations

from typing import Optional

from .database import SessionLocal, init_db
from .models import League, Team, Player, RosterEntry


def seed_demo() -> None:
    """Insert a demo league, team and roster into the database."""
    init_db()
    db = SessionLocal()
    try:
        # Only seed if no league exists
        if db.query(League).first():
            print("Demo data already exists; skipping seed.")
            return
        # Create league and team
        league = League(ottoneu_league_id=0, name="Demo League")
        db.add(league)
        db.commit()
        db.refresh(league)
        team = Team(league_id=league.id, name="Demo Team", cap_space=400.0)
        db.add(team)
        db.commit()
        db.refresh(team)
        # Sample players
        players = [
            {
                "name": "Ronald Acuña Jr.",
                "position": "OF",
                "ottoneu_player_id": 1,
                "fangraphs_id": 12816,
                "mlbam_id": 660670,
                "salary": 62.0,
            },
            {
                "name": "Gerrit Cole",
                "position": "SP",
                "ottoneu_player_id": 2,
                "fangraphs_id": 21522,
                "mlbam_id": 543037,
                "salary": 44.0,
            },
            {
                "name": "Juan Soto",
                "position": "OF",
                "ottoneu_player_id": 3,
                "fangraphs_id": 19783,
                "mlbam_id": 665742,
                "salary": 51.0,
            },
        ]
        for p in players:
            player = Player(
                ottoneu_player_id=p["ottoneu_player_id"],
                fangraphs_id=p["fangraphs_id"],
                mlbam_id=p["mlbam_id"],
                name=p["name"],
                position=p["position"],
            )
            db.add(player)
            db.commit()
            db.refresh(player)
            roster_entry = RosterEntry(
                team_id=team.id,
                player_id=player.id,
                salary=p["salary"],
                acquired="demo",
            )
            db.add(roster_entry)
        db.commit()
        print("Seeded demo data successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()