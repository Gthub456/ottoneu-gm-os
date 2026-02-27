"""Player news aggregator.

Aggregate player news from multiple feeds.  This connector currently returns
static data; replace with real API calls or RSS feed parsing.
"""

from __future__ import annotations

from typing import List, Dict, Any


def fetch_player_news() -> List[Dict[str, Any]]:
    """Return a list of fake news items.

    Each news item should include a timestamp, player identifier and a
    headline.  Real implementations would normalise MLBAM/FanGraphs/Ottoneu IDs.
    """
    return [
        {
            "mlbam_id": 123456,
            "headline": "Player A placed on injured list with elbow soreness",
            "timestamp": "2026-02-27T10:00:00Z",
        },
        {
            "mlbam_id": 789012,
            "headline": "Player B homers twice in spring training debut",
            "timestamp": "2026-02-26T15:30:00Z",
        },
    ]
