from dataclasses import dataclass, field
from typing import Any


@dataclass
class Batch:
    """
    ============================================================================
     Pagination-State for FetchMulti.
    ============================================================================
    """
    # Items fetched from the API (list of dicts)
    items: list[dict[str, Any]] = field(default_factory=list)
    # Whether there is more data to fetch
    has_more: bool = field(default=True)
    # Cursor to fetch the next batch
    cursor: str = field(default='0')
