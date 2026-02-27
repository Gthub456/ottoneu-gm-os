"""Ottoneu data connector.

This module fetches roster and league information from Ottoneu.  The public
roster export does not require authentication and can be accessed via the
`rosterexport` endpoint.  For private data (such as transaction history or
free agent lists) you will need to implement authenticated scraping using a
headless browser (e.g. Playwright) and store session cookies server‑side.

For now this connector focuses on retrieving roster data from the public
export.  Use the Celery tasks in ``backend/app/tasks.py`` to invoke these
functions on a schedule.
"""

from __future__ import annotations

import csv
import io
import os
from typing import Dict, List, Any

import requests


def roster_export_url(league_id: str) -> str:
    """Return the roster export URL for a given league ID."""
    return f"https://ottoneu.fangraphs.com/{league_id}/rosterexport?csv=1"


def parse_csv(text: str) -> Dict[str, List[str]]:
    """Parse a CSV string into a dict of columns mapping to lists.

    The roster export contains quoted fields and embedded commas.  This
    function uses Python's built‑in CSV reader to handle quoting.
    """
    reader = csv.DictReader(io.StringIO(text))
    columns: Dict[str, List[str]] = {}
    for field in reader.fieldnames or []:
        columns[field] = []
    for row in reader:
        for field in reader.fieldnames or []:
            columns[field].append(row.get(field, ""))
    return columns


def fetch_roster(league_id: str) -> List[Dict[str, Any]]:
    """Fetch the roster export for a league and return a list of player records.

    Each record contains keys matching the CSV header names.  Example fields
    include ``player_name``, ``position``, ``salary``, and ``mlbam_id``.
    """
    url = roster_export_url(league_id)
    resp = requests.get(url)
    resp.raise_for_status()
    data = parse_csv(resp.text)
    # Transform the columnar dict into a list of row dicts
    players: List[Dict[str, Any]] = []
    headers = list(data.keys())
    row_count = len(next(iter(data.values()), []))
    for i in range(row_count):
        entry: Dict[str, Any] = {}
        for header in headers:
            entry[header] = data[header][i]
        players.append(entry)
    return players
