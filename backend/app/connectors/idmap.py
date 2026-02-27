"""Identity resolution service.

The IdMap stores associations between player identifiers across Ottoneu,
FanGraphs and MLBAM.  In a production system you might maintain this in
the database with unique constraints and update it when new mappings are
discovered.  For demonstration purposes this module exposes a simple in‑memory
lookup table and a function to seed it from roster exports or other sources.
"""

from __future__ import annotations

from typing import Optional, Dict, Tuple


class IdMap:
    """In‑memory mapping between Ottoneu, FanGraphs and MLBAM IDs."""

    def __init__(self) -> None:
        # Use dictionaries keyed by one ID type mapping to a tuple of the others
        self._ottoneu_to_other: Dict[int, Tuple[Optional[int], Optional[int]]] = {}
        self._fangraphs_to_other: Dict[int, Tuple[Optional[int], Optional[int]]] = {}
        self._mlbam_to_other: Dict[int, Tuple[Optional[int], Optional[int]]] = {}

    def add_mapping(
        self, *, ottoneu_id: Optional[int], fangraphs_id: Optional[int], mlbam_id: Optional[int]
    ) -> None:
        # Store each mapping for each key if provided
        value = (fangraphs_id, mlbam_id)
        if ottoneu_id is not None:
            self._ottoneu_to_other[ottoneu_id] = value
        if fangraphs_id is not None:
            self._fangraphs_to_other[fangraphs_id] = (ottoneu_id, mlbam_id)
        if mlbam_id is not None:
            self._mlbam_to_other[mlbam_id] = (ottoneu_id, fangraphs_id)

    def resolve_from_ottoneu(self, ottoneu_id: int) -> Tuple[Optional[int], Optional[int]]:
        return self._ottoneu_to_other.get(ottoneu_id, (None, None))

    def resolve_from_fangraphs(self, fangraphs_id: int) -> Tuple[Optional[int], Optional[int]]:
        return self._fangraphs_to_other.get(fangraphs_id, (None, None))

    def resolve_from_mlbam(self, mlbam_id: int) -> Tuple[Optional[int], Optional[int]]:
        return self._mlbam_to_other.get(mlbam_id, (None, None))


# Initialise a global IdMap.  In a real system you would persist this in the DB.
id_map = IdMap()
