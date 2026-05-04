"""
============================================================================
 Shared utility for recording-test golden-reference comparisons.

 `normalize(event)` returns a copy of an Event dict with:
   - `duration` removed (non-deterministic timing field).
   - Any `StateBase`-typed value unwrapped via `state.event_key()`,
     recursively for tuples / lists.

 The isinstance-based dispatch avoids per-test enumeration of state-
 shaped field names (`state`, `parent`, `goal`, `responsible`,
 `via_parent`, `via_child`, ...) — any new event-type that carries a
 State automatically normalizes the same way.

 Used by every algo's `_tester_recording.py` (oospp + omspp) and
 by future variants. The previous per-package `_utils.py` files
 (each redefining the same logic) have been deleted.
============================================================================
"""
from f_hs.state.i_0_base.main import StateBase


def normalize(event: dict) -> dict:
    """
    ========================================================================
     Return a comparable copy of an Event for golden-reference
     test assertions: `duration` stripped, any `StateBase` value
     unwrapped via `state.event_key()`. Non-state fields pass
     through unchanged.

     Tuples and lists are walked recursively so collections of
     states (e.g. `via_children: tuple[State, ...]`) unwrap
     element-wise.
    ========================================================================
    """
    out = {}
    for k, v in event.items():
        if k == 'duration':
            continue
        out[k] = _unwrap(v)
    return out


def _unwrap(v: object) -> object:
    """
    ========================================================================
     If `v` is a `StateBase`, return its `event_key()`; if it's a
     tuple or list, recurse element-wise; otherwise pass through.
    ========================================================================
    """
    if isinstance(v, StateBase):
        return v.event_key()
    if isinstance(v, tuple):
        return tuple(_unwrap(x) for x in v)
    if isinstance(v, list):
        return [_unwrap(x) for x in v]
    return v
