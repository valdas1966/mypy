"""
============================================================================
 Shared utility for recording-test golden-reference comparisons.

 `normalize(event)` returns a copy of an Event dict with:
   - `duration` removed (non-deterministic timing field).
   - Any keyed value (State, Cell, ...) rendered to its canonical
     primitive identity via `f_core.canonize.canonize`, recursively
     for tuples / lists.

 The isinstance-based dispatch avoids per-test enumeration of state-
 shaped field names (`state`, `parent`, `goal`, `responsible`,
 `via_parent`, `via_child`, ...) — any new event-type that carries a
 State automatically normalizes the same way.

 Used by every algo's `_tester_recording.py` (oospp + omspp) and
 by future variants. The previous per-package `_utils.py` files
 (each redefining the same logic) have been deleted. The unwrap
 itself is now `f_core.canonize.canonize`, which subsumes the old
 local `_unwrap` + the per-State `event_key()` methods.
============================================================================
"""
from f_core.canonize import canonize


def normalize(event: dict) -> dict:
    """
    ========================================================================
     Return a comparable copy of an Event for golden-reference
     test assertions: `duration` stripped, any keyed value
     canonized to its primitive identity. Non-keyed fields pass
     through unchanged.

     Tuples and lists are walked recursively so collections of
     states (e.g. `via_children: tuple[State, ...]`) canonize
     element-wise.
    ========================================================================
    """
    out = {}
    for k, v in event.items():
        if k == 'duration':
            continue
        out[k] = canonize(v)
    return out
