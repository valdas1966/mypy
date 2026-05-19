# `f_ds/collections/key_rate` — `KeyRate`

## 1) Purpose
One key's positive/negative tally and derived positive rate.
Instance data structure (a row), `Comparable`.

## 2) Public API
- `KeyRate(item, pos, neg)` — `rate = pos/(pos+neg)` derived
  in `__init__`; `None` when `pos+neg == 0`.
- `.item` — the counter key. Named `item` (not `key`) because
  `key` is the Equatable/Comparable surrogate.
- `.pos`, `.neg`, `.total` (`pos+neg`), `.rate -> float | None`.
- `.key` — comparison surrogate `(has-rate, rate, total,
  repr(item))`.
- Ordering: higher rate, then larger total; `None` rate
  lowest. Equality: same rate, total, item.
- `KeyRate.Factory`: `a()` (0.75), `b()` (0.25),
  `none_rate()` (`None`).

## 3) Inheritance
`KeyRate` → `Comparable` → `Equatable`. **No `Generic`
base** (Protocol-mixin MRO conflict; not subscriptable).

## 4) Dependencies
`f_core.mixins.comparable`, `f_core.protocols.comparison`.

## 5) Usage Example
```python
from f_ds.collections.key_rate import KeyRate
KeyRate(item='good', pos=4, neg=0).rate   # 1.0
KeyRate(item='z', pos=0, neg=0).rate      # None
```

## Files
| File | Purpose |
|------|---------|
| `main.py` | `KeyRate` class. |
| `_factory.py` | `Factory` (`a`, `b`, `none_rate`). |
| `__init__.py` | Wires `KeyRate.Factory`. |
| `_tester.py` | pytest; rate / eq / order, 4-line structural. |
