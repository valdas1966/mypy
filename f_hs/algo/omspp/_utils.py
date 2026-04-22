"""
============================================================================
 Shared test utilities for OMSPP recording tests. Private to this
 package (leading underscore); not part of the public API.
============================================================================
"""


def key_of(state) -> object:
    """
    ========================================================================
     Return a comparable Key for a State.
     Graph states (key=str) return the string as-is.
     Grid states (key=CellMap) return a (row, col) tuple.
    ========================================================================
    """
    k = state.key
    if hasattr(k, 'row') and hasattr(k, 'col'):
        return (k.row, k.col)
    return k


def normalize(event: dict) -> dict:
    """
    ========================================================================
     Return a comparable copy of an Event:
     - duration removed (non-deterministic timing).
     - state / parent unwrapped to their keys (when present).
     - state-less meta-events (e.g. `update_frontier`) pass
       through unchanged; no state field expected.
    ========================================================================
    """
    out = {k: v for k, v in event.items() if k != 'duration'}
    if 'state' in event:
        out['state'] = key_of(event['state'])
    if 'parent' in event:
        p = event['parent']
        out['parent'] = key_of(p) if p is not None else None
    return out
