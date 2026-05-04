"""
============================================================================
 Heuristic aggregation functions for kA*_agg.

 Each aggregation takes a list of per-goal h values (over the ACTIVE
 goal subset) and returns an int. Internal; users pass the string
 name ('MIN', 'MAX', 'AVG', 'RND', 'PROJECTION') OR a custom Callable
 to the AStarLookup / KAStarAgg constructor.

 Semantic properties (per Stern et al. 2021):
   MIN / AVG / PROJECTION : antitone (removing a goal never decreases Φ).
   MAX                    : isotone  (removing a goal never increases Φ).
   RND                    : inconsistent (each call picks randomly);
                            included for research comparison.
============================================================================
"""
import random
from typing import Callable


def _min(hs: list[int]) -> int:
    return min(hs) if hs else 0


def _max(hs: list[int]) -> int:
    return max(hs) if hs else 0


def _avg(hs: list[int]) -> int:
    # Integer floor — preserves the framework's int-everywhere
    # convention. Slight admissibility drift acceptable for research.
    return sum(hs) // len(hs) if hs else 0


def _rnd(hs: list[int]) -> int:
    return random.choice(hs) if hs else 0


def _projection(hs: list[int]) -> int:
    # Pick the first goal's h. Order determined by `problem.goals`.
    return hs[0] if hs else 0


_AGG_FNS: dict[str, Callable[[list[int]], int]] = {
    'MIN': _min,
    'MAX': _max,
    'AVG': _avg,
    'RND': _rnd,
    'PROJECTION': _projection,
}


def resolve_agg(
        agg: str | Callable[[list[int]], int],
        ) -> tuple[Callable[[list[int]], int], str]:
    """
    ========================================================================
     Resolve the `agg` argument to a (function, display-name) pair.

     Accepts either:
       - A string in {'MIN', 'MAX', 'AVG', 'RND', 'PROJECTION'}.
       - A custom Callable[[list[int]], int] — display name 'CUSTOM'.

     Raises ValueError on unknown strings.
    ========================================================================
    """
    if callable(agg):
        return agg, 'CUSTOM'
    if isinstance(agg, str) and agg in _AGG_FNS:
        return _AGG_FNS[agg], agg
    raise ValueError(
        f"agg must be one of {sorted(_AGG_FNS)} or a Callable; "
        f"got {agg!r}.")
