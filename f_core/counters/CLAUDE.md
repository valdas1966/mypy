# Counters

## Purpose
Always-on operation counters for algorithms. A small,
problem-agnostic observability primitive — sibling of
`Recorder` under `f_core/`.

Where `Recorder` is **opt-in** structured-trace capture (off
by default for cost reasons), `Counters` is **always-on** O(1)
per-run metric accumulation. They are complementary, not
duplicates: counters survive `is_recording=False` benchmark
runs that cannot afford the recorder's per-event dict
allocations.

## Public API

### Constructor
```python
def __init__(self,
             names: tuple[str, ...]
                    | tuple[tuple[str, ...], ...]) -> None
```

`names` accepts two forms (auto-detected by inspecting the
first element):

- **Flat** `tuple[str, ...]` — single un-grouped block.
- **Grouped** `tuple[tuple[str, ...], ...]` — produces a
  blank-line separator between groups in `__repr__`. Group
  structure is **display-only**; equality and dict snapshot
  are flat.

Duplicate names raise `ValueError` at construction.

### Methods
| Method | Signature | Description |
|---|---|---|
| `inc(name, n=1)` | `(str, int) -> None` | Increment counter `name`. `KeyError` on undeclared name (typo guard). |
| `assign(name, value)` | `(str, int) -> None` | Overwrite counter `name` with absolute `value`. Use for ownership-handoff (another component owns the count; this Counters mirrors the final tally). `KeyError` on undeclared name. |
| `absorb(source, names=None, default=0)` | `(Mapping, tuple[str,...] \| None, int) -> None` | Mirror counters from a `source` Mapping by absolute `assign`. For each name in `names` (default: full schema), copy `source[name]` if present else write `default`. Centralizes the structural-default policy for cross-component handoff — synthesizes `cnt_decrease=0` for a FIFO frontier, replacing a per-call-site `'cnt_decrease' in fc` guard. Undeclared target name → `KeyError`. |
| `reset()` | `() -> None` | Zero all counters in place. |
| `as_dict()` | `() -> dict[str, int]` | Plain-dict copy in declaration order. |

### Mapping protocol (read-only mutation guarded)
- `c[name]` — current value.
- `name in c` — declared?
- `iter(c)`, `len(c)`, `c.keys()`, `c.values()`, `c.items()`.
- `dict(c)` — flat dict in declaration order.
- `c == other` — True for any `Mapping` (incl. plain `dict`)
  with the same name→value map. Group structure is **not**
  part of identity.

`Counters` is **mutable**, hence **unhashable** (`__hash__ = None`).

### `__repr__`
Multi-line aligned block; blank lines between groups when
constructed grouped:

```
Counters(
  cnt_h_search   =   25
  cnt_h_update   =   21

  cnt_phi_search =   13
  cnt_phi_update =   13

  cnt_push       =   16
  cnt_pop        =   13
  cnt_pop_stale  =    3
  cnt_decrease   =    0
)
```

## Why `Counters` alongside `Recorder`?

Counters mirror some event types (push, pop, decrease) that
are also derivable from a full event log. Why keep both?

1. **Always-on vs. opt-in.** `Recorder` defaults to inactive;
   benchmarks that disable recording for performance still
   need accurate counters.
2. **O(1) snapshot vs. O(N) replay.** Counters give an
   immediate per-run summary; deriving the same number from
   a recorder log requires walking N events.
3. **Schema decoupling.** Counters cover semantic increments
   that don't have an event (e.g., `cnt_h_search` /
   `cnt_h_update` route the same h-call to different
   counters based on phase tag).

## Inheritance
`Counters(collections.abc.Mapping)` — read-only Mapping
contract. Mutation goes through `inc()` / `reset()`.

## Dependencies
None (stdlib `collections.abc.Mapping` only).

## Usage

### Flat
```python
from f_core.counters import Counters

c = Counters(names=('cnt_push', 'cnt_pop', 'cnt_decrease'))
c.inc('cnt_push')
c.inc('cnt_push', n=4)
c.inc('cnt_pop')
print(c['cnt_push'])         # 5
print(c.as_dict())           # {'cnt_push': 5, 'cnt_pop': 1, ...}
print(c == {'cnt_push': 5,   # True (Mapping equality)
            'cnt_pop': 1,
            'cnt_decrease': 0})
```

### Grouped (visual scanning in `__repr__`)
```python
c = Counters(names=(
    ('cnt_h_search', 'cnt_h_update'),
    ('cnt_phi_search', 'cnt_phi_update'),
    ('cnt_push', 'cnt_pop',
     'cnt_pop_stale', 'cnt_decrease'),
))
c.inc('cnt_h_search', n=25)
print(c)   # aligned block with blank lines between groups
```

### Composition into an Algorithm
```python
class MyAlgo:
    _COUNTER_NAMES: tuple[str, ...] = (
        'cnt_push', 'cnt_pop', 'cnt_decrease',
    )

    def __init__(self) -> None:
        self._counters = Counters(names=self._COUNTER_NAMES)

    @property
    def counters(self) -> Counters:
        return self._counters

    def _run_pre(self) -> None:
        self._counters.reset()

    def _push(self, ...) -> None:
        self._counters.inc('cnt_push')
        ...
```

### Absorbing a sub-component's tally
At end-of-run an algorithm mirrors its frontier's heap-op
counts into its own wider scaffold. `absorb` copies the named
subset and synthesizes the structural default for names the
frontier does not track (a FIFO frontier has no
`cnt_decrease`), so there is no `'cnt_decrease' in fc` guard
at the call site:
```python
fc = self._search.frontier.counters          # source Mapping
self._counters.absorb(
    fc, names=('cnt_push', 'cnt_pop', 'cnt_decrease'))
# FIFO frontier → cnt_decrease defaults to 0; priority
# frontier → its real count is mirrored.
```

Runnable toy examples (priority vs FIFO mirror, default
fill): `_study.py` (`python -m f_core.counters._study`),
built on the `Factory.frontier_priority/frontier_fifo/algo`
fixtures.
