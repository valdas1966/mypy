# FrontierBase

## Purpose
Abstract base for a search Frontier — the collection of candidate
States awaiting expansion. **True ABC** (metaclass `ABCMeta` via
`Sizable`): `push`, `pop`, `clear`, `__contains__`, `__len__`,
`__iter__` are all `@abstractmethod`, so `FrontierBase` is
NON-instantiable (`FrontierBase()` raises `TypeError: Can't
instantiate abstract class ...`) and any subclass that omits one
of them fails at CONSTRUCTION, not at first call. Holds the
narrow interface shared by
every frontier: `push`, `pop`, `__contains__`, `__len__`,
`__iter__`, `clear`. Inherits `f_core.mixins.Sizable`, which
supplies `__bool__` (emptiness) derived from the subclass
`__len__` — size is declared in one place. `decrease` is NOT
part of the base interface — it lives only on `FrontierPriority`.

Owns the always-on **2-counter scaffold** (`cnt_push`,
`cnt_pop`) via composition with `f_core.counters.Counters`.
Every concrete frontier inherits the `counters` property;
subclasses increment in their concrete `push` / `pop`
overrides where the operation actually occurs. Priority
frontiers add `cnt_decrease` via a `_COUNTER_NAMES` override —
the decrease op and its counter live only where the op does.

Priorities are computed by the Algorithm (via `_priority(state)`)
and passed into the Frontier; the Frontier itself is priority-
agnostic.

## Public API

### Constructor
```python
def __init__(self) -> None
```
Creates `self._counters: Counters` from the class-level
`_COUNTER_NAMES = ('cnt_push', 'cnt_pop')`. Subclasses MUST
call `FrontierBase.__init__(self)` from their own `__init__`.

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `counters` | `Counters` | Always-on 2-counter scaffold `cnt_push`, `cnt_pop` (Mapping; `c == {...}`, `dict(c)`, `c['cnt_pop']` all work). Survives `clear()` — accumulates over the whole run. Priority frontiers extend it with `cnt_decrease` via a `_COUNTER_NAMES` override. |
| `max_size` | `int` | Lifetime high-water mark of `len(frontier)` across the whole run. Used by `f_hs/algo`'s `mem_open` reading (rule-2: OPEN is non-monotone, so end-of-run `len()` understates the peak). Survives `clear()` — a drain-and-rebuild (`AlgoSPP.refresh_priorities`) does not reset the peak. |

### Methods
| Method | Signature | Default |
|--------|-----------|---------|
| `push` | `(state, priority=None) -> None` | **`@abstractmethod`** — abstract; subclass MUST implement. Overrides MUST call `self._track_max_size()` at the end (after the actual insertion). |
| `pop` | `() -> State` | **`@abstractmethod`** — abstract; subclass MUST implement |
| `clear` | `() -> None` | **`@abstractmethod`** — abstract; subclass MUST implement |
| `__contains__` | `(state) -> bool` | **`@abstractmethod`** — abstract; subclass MUST implement |
| `__bool__` | `() -> bool` | **inherited from `Sizable`** — `bool(len(self) != 0)`; not declared on the base (unchanged) |
| `__len__` | `() -> int` | **`@abstractmethod`** — abstract; subclass MUST implement (also satisfies `Sizable`'s abstract `__len__`; no longer a concrete stub) |
| `__iter__` | `() -> Iterator[State]` | **`@abstractmethod`** — abstract; subclass MUST implement |
| `_track_max_size` | `() -> None` | Bumps `_max_size` to `len(self)` if it grew. Called by each subclass's `push` after the actual insertion. O(1); does NOT call `getsizeof` (per-push hot path). |

All six abstract bodies still `raise NotImplementedError`
(belt-and-suspenders behind the `@abstractmethod` guard), but
enforcement is now at construction time, not call time.

### Design Notes
- `priority` is kept `Any` — FIFO frontiers ignore it,
  priority-ordered frontiers use it.
- `decrease` is NOT on the base. FIFO has no decrease op (and
  no `cnt_decrease`); `FrontierPriority` owns both the
  `decrease` method and the `cnt_decrease` counter. Hierarchy
  honesty — each frontier visibly carries only the ops it has.
- No `Factory` — the class is abstract.

## Dependencies
- `f_core.counters.Counters` — 2-counter scaffold
  (`cnt_push`, `cnt_pop`).
- `f_core.mixins.Sizable` (base class) — supplies `__bool__`
  derived from `__len__` AND the `ABCMeta` metaclass that makes
  `FrontierBase`'s `@abstractmethod`s construction-enforced; the
  base declares `__len__` as `@abstractmethod` (subclasses
  implement it), so size is declared once and `bool()` follows.
  Only `__bool__`/`Sized`
  come from the mixin; `__contains__` / `__iter__` stay
  hand-declared (the frontier keeps a separate O(1) membership
  index, so it is not a single-iterable wrapper).
