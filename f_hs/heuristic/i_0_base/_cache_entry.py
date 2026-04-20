from dataclasses import dataclass
from typing import Generic, TypeVar

from f_hs.state.i_0_base.main import StateBase

State = TypeVar('State', bound=StateBase)


@dataclass(frozen=True)
class CacheEntry(Generic[State]):
    """
    ============================================================================
     One harvested cache row.

     h_perfect    — provably tight h*(state -> goal).
     suffix_next  — next State on the optimal suffix, or None
                    when this entry IS the goal itself.

     Frozen: mutation after construction is prevented. Matches
     the static-cache decision from 2026-04-20.
    ============================================================================
    """
    h_perfect:   float
    suffix_next: State | None
