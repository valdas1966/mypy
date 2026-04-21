"""
============================================================================
 Shared test utilities for AStarLookup recording tests. Private to this
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
     - state / parent / via_parent / via_child unwrapped to
       their keys (when present). via_parent fires on
       bpmx_forward; via_child fires on bpmx_lift.
     - state-less meta-events (e.g. `propagate_wave`) pass
       through unchanged; no state field expected.
    ========================================================================
    """
    out = {k: v for k, v in event.items() if k != 'duration'}
    if 'state' in event:
        out['state'] = key_of(event['state'])
    if 'parent' in event:
        p = event['parent']
        out['parent'] = key_of(p) if p is not None else None
    if 'via_parent' in event:
        out['via_parent'] = key_of(event['via_parent'])
    if 'via_child' in event:
        out['via_child'] = key_of(event['via_child'])
    return out
