"""
============================================================================
 Memory-counter finalization helper for `f_hs/algo`.

 Single rule, applied uniformly across every `f_hs/algo` algo:

     mem_total := Σ_{k != 'mem_total'} mem_k

 i.e., `mem_total` is the conservative upper-bound sum of every
 per-region `mem_*` value (each of which is itself the right
 reading for its region — peak for non-monotone OPEN, final-on-
 owner for monotone CLOSED/cache/bounds, max-across-sub-searches
 for disjoint-in-time orchestrator scopes). Component peaks need
 not coincide in time, so the sum is an *upper bound* on the
 true coincident peak; this bias is shared across every algo,
 so cross-algo deltas (Inc - Rep) largely cancel it out.

 `finalize_mem_total` is called LAST in each algo's memory-
 snapshot routine, after every other `mem_*` has been assigned.
 New `mem_*` keys (e.g., `mem_aux`, `mem_cache`, `mem_bounds`)
 are auto-absorbed without each algo being patched — the rule
 is encoded once, here.

 Accepts either a `Counters` instance (uses `.assign`) or a
 plain `dict[str, int]` (`AlgoSPP._memory_snapshot` returns
 a dict; `AlgoOMSPP._sync_memory_snapshot` mutates a Counters
 in-place).
============================================================================
"""
from typing import Any


def finalize_mem_total(target: Any) -> None:
    """
    ========================================================================
     Write `mem_total = Σ mem_k` (excluding `mem_total` itself)
     into `target`. `target` is either a `Counters` instance
     (uses `target.assign(name, value)`) or a plain
     `dict[str, int]` (uses `target[name] = value`).

     Must be called LAST in the algo's memory-snapshot routine
     — after every other `mem_*` key has been assigned — so the
     sum sees the fully populated set.
    ========================================================================
    """
    total = 0
    for k in list(target.keys()):
        if k.startswith('mem_') and k != 'mem_total':
            total += target[k]
    if hasattr(target, 'assign'):
        target.assign('mem_total', total)
    else:
        target['mem_total'] = total
