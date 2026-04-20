# FrontierBase

## Purpose
Abstract base for a search Frontier — the collection of candidate
States awaiting expansion. Holds the narrow interface shared by
every frontier: `push`, `pop`, `decrease`, `__contains__`,
`__bool__`, `__len__`, `clear`.

Priorities are computed by the Algorithm (via `_priority(state)`)
and passed into the Frontier; the Frontier itself is priority-
agnostic.

## Public API

### Methods
| Method | Signature | Default |
|--------|-----------|---------|
| `push` | `(state, priority=None) -> None` | NotImplementedError |
| `pop` | `() -> State` | NotImplementedError |
| `decrease` | `(state, priority=None) -> None` | no-op |
| `clear` | `() -> None` | NotImplementedError |
| `__contains__` | `(state) -> bool` | NotImplementedError |
| `__bool__` | `() -> bool` | NotImplementedError |
| `__len__` | `() -> int` | NotImplementedError |
| `__iter__` | `() -> Iterator[State]` | NotImplementedError |

### Design Notes
- `priority` is kept `Any` — FIFO frontiers ignore it,
  priority-ordered frontiers use it.
- `decrease` has a no-op default so BFS-style frontiers can
  safely inherit without extra boilerplate.
- No `Factory` — the class is abstract.

## Dependencies
None (stdlib only).
