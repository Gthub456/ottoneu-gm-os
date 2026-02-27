"""Projection data connector.

Pull rest‑of‑season projections from public sources and normalise them to
FanGraphs Points.  This is currently a stub that returns made‑up numbers.
"""

from __future__ import annotations

from typing import List, Dict, Any


def fetch_ros_projections() -> List[Dict[str, Any]]:
    """Return a list of fake ROS projections.

    Real implementations might scrape FanGraphs or subscribe to publicly
    available projection feeds.  Each item should include a player ID and
    projected points.
    """
    return [
        {"mlbam_id": 123456, "proj_points": 550.0},
        {"mlbam_id": 789012, "proj_points": 420.0},
    ]
