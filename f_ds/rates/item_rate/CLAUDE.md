# `f_ds/rates/item_rate` — `ItemRate`

## 1) Purpose
One item's positive/negative tally and derived positive
rate. Instance data structure (a row), `Comparable`.

## 2) Public API
- `ItemRate(item, pos, neg)` — `rate = pos/(pos+neg)`
  derived in `__init__`; `None` when `pos+neg == 0`.
- `.item` — the counter key. Named `item` (not `key`)
  because `key` is the Equatable/Comparable surrogate.
- `.pos`, `.neg`, `.total` (`pos+neg`),
  `.rate -> float | None`.
- `.key` — comparison surrogate `(has-rate, rate, total,
  repr(item))`.
- Ordering: higher rate, then larger total; `None` rate
  lowest. Equality: same rate, total, item.
- `ItemRate.Factory`: `a()` (0.75), `b()` (0.25),
  `none_rate()` (`None`).

## 3) Inheritance
`ItemRate` → `Comparable` → `Equatable`. **No `Generic`
base** (Protocol-mixin MRO conflict; not subscriptable).

## 4) Dependencies
`f_core.mixins.comparable.main`,
`f_core.protocols.comparison.main` (direct-module imports,
not the lazy aggregator).

## 5) Usage Example
```python
from f_ds.rates.item_rate import ItemRate
ItemRate(item='good', pos=4, neg=0).rate   # 1.0
ItemRate(item='z', pos=0, neg=0).rate      # None
```

## Notes
- **Name history.** Class was `KeyRate` (folder
  `key_rate/`) until 2026-05-25. Renamed because
  `KeyRate.key` is the Equatable/Comparable surrogate, not
  the counter key — the old name suggested otherwise.
  `ItemRate` matches the public `.item` field.

## Files
| File | Purpose |
|------|---------|
| `main.py` | `ItemRate` class. |
| `_factory.py` | `Factory` (`a`, `b`, `none_rate`). |
| `__init__.py` | Wires `ItemRate.Factory`. |
| `_tester.py` | pytest; rate / eq / order, 4-line structural. |
