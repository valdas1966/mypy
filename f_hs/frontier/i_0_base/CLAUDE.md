# FrontierBase

## Purpose
Abstract base for a search Frontier — the collection of candidate
States awaiting expansion. Holds the narrow interface shared by
every frontier: `push`, `pop`, `decrease`, `__contains__`,
`__bool__`, `__len__`, `clear`.

Owns the always-on **3-counter scaffold** (`cnt_push`,
`cnt_pop`, `cnt_decrease`) via composition with
`f_core.counters.Counters`. Every concrete frontier inherits
the `counters` property; subclasses increment in their concrete
`push` / `pop` / `decrease` overrides where the operation
actually occurs. FIFO ignores `decrease` and does NOT increment
`cnt_decrease` — counts reflect what the frontier actually did,
not what was called.

Priorities are computed by the Algorithm (via `_priority(state)`)
and passed into the Frontier; the Frontier itself is priority-
agnostic.

## Public API

### Constructor
```python
def __init__(self) -> None
```
Creates `self._counters: Counters` from the class-level
`_COUNTER_NAMES = ('cnt_push', 'cnt_pop', 'cnt_decrease')`.
Subclasses MUST call `FrontierBase.__init__(self)` from their
own `__init__`.

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `counters` | `Counters` | Always-on 3-counter scaffold (Mapping; `c == {...}`, `dict(c)`, `c['cnt_pop']` all work). Survives `clear()` — accumulates over the whole run. |

### Methods
| Method | Signature | Default |
|--------|-----------|---------|
| `push` | `(state, priority=None) -> None` | NotImplementedError |
| `pop` | `() -> State` | NotImplementedError |
| `decrease` | `(state, priority=None) -> None` | no-op (does NOT increment `cnt_decrease`) |
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
- `f_core.counters.Counters` — 3-counter scaffold
  (`cnt_push`, `cnt_pop`, `cnt_decrease`).
