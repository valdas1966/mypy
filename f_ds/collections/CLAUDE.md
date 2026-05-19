# `f_ds/collections` — collections-derived Data Structures

## 1) Purpose
Reusable data structures derived from Python `collections`
types. Currently the positive/negative **rate** family built
from two `collections.Counter` tallies.

Distinct from `f_core/counters/Counters` (an always-on
operation-counter scaffold) — unrelated, not a
`collections.Counter` consumer.

## 2) Public API

### `KeyRate` (`key_rate/`)
One key's two-class tally — instance class, `Comparable`.
- `KeyRate(item, pos, neg)` — `rate` is **derived**
  (`pos/(pos+neg)`, `None` when total `0`); an inconsistent
  triple cannot be constructed.
- `.item` — the key from the counters. (Named `item`, **not**
  `key`, because `key` is reserved by the Equatable/Comparable
  mixins for the comparison surrogate.)
- `.pos`, `.neg`, `.total` (`pos+neg`), `.rate` (`float | None`).
- Ordering: higher rate first; ties by larger total
  (`pos+neg`); `None` rate lowest. Equality: same rate,
  total, item.

### `CounterRates` (`counter_rates/`)
Per-key rate table from two counters — instance class,
`Equatable`.
- `CounterRates(positive: Counter, negative: Counter)` —
  builds one `KeyRate` per key in the **union**; rows kept
  sorted (rate desc, ties total desc, `None` last). **Binary
  by construction.** Zero guard: total `0` → rate `None`
  (no raise); assumes non-negative counts.
- `.rows -> tuple[KeyRate, ...]`, `.top(n)`, `len()`,
  iteration. Equality: same rows in the same order.

Both have a `Factory` (standard class-module shape).

## 3) Inheritance (Hierarchy)
`KeyRate` → `Comparable` → `Equatable`. `CounterRates` →
`Equatable`. Both use the `key` property as the mixin
surrogate. **No explicit `Generic[...]` base** — see Notes.

## 4) Dependencies
- `collections.Counter`, `typing.Iterator`,
  `f_core.mixins.comparable` / `equatable`,
  `f_core.protocols`. Standard library + `f_core`.

## 5) Usage Example
```python
from collections import Counter
from f_ds.collections import CounterRates

cr = CounterRates(positive=Counter(good=4, ok=3, bad=1),
                  negative=Counter(ok=3, bad=5))
[(r.item, r.rate) for r in cr.top(2)]
# [('good', 1.0), ('ok', 0.5)]
```

## Notes
- **No `Generic[Key]` base.** Under `f_core`'s Protocol-based
  mixins, `class X(Generic[T], Equatable/Comparable)` raises
  an MRO `TypeError` (Generic is already in the MRO via
  `Protocol`). The classes are therefore not subscriptable
  (`KeyRate[str]` fails); annotate plainly. `f_ds/pair/Pair`
  has this latent bug and must not be copied as precedent.

## Files
| Path | Purpose |
|------|---------|
| `key_rate/` | `KeyRate` class module. |
| `counter_rates/` | `CounterRates` class module. |
| `__init__.py` | Re-exports `KeyRate`, `CounterRates`. |
