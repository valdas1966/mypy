# `f_ds/rates/counter_rates` — `CounterRates`

## 1) Purpose
Per-item positive-rate table built from a positive and a
negative `collections.Counter`. Instance data structure,
`Equatable`.

## 2) Public API
- `CounterRates(positive: Counter, negative: Counter)` —
  one `ItemRate` per key in the **union** of both counters.
  **Binary by construction** (rate is a two-class quantity).
  Zero guard: total `0` → rate `None` (no raise); assumes
  non-negative counts.
- Rows kept **sorted**: rate desc; ties by larger total
  (`pos+neg`); `None`-rate rows last.
- `.rows -> tuple[ItemRate, ...]`,
  `.top(n) -> list[ItemRate]`, `len(cr)`, `iter(cr)`.
- Equality: same rows in the same order.
- `CounterRates.Factory`: `a()` (canonical), `empty()`.

## 3) Inheritance
`CounterRates` → `Equatable`. `key` surrogate = the ordered
row tuple. **No `Generic` base** (Protocol-mixin MRO
conflict).

## 4) Dependencies
`collections.Counter`, `f_core.mixins.equatable.main`,
`f_core.protocols.equality.main`,
`f_ds.rates.item_rate.main.ItemRate`.

## 5) Usage Example
```python
from collections import Counter
from f_ds.rates.counter_rates import CounterRates
cr = CounterRates(positive=Counter(a=3, b=1),
                  negative=Counter(a=1, b=3))
cr.top(1)   # [<ItemRate 'a': +3/-1 -> 0.750>]
```

## Notes
- **Name history.** Folder was `f_ds/collections/counter_rates/`
  until 2026-05-25; rows held `KeyRate` (now `ItemRate`).
  See `f_ds/rates/CLAUDE.md` Notes for why.

## Files
| File | Purpose |
|------|---------|
| `main.py` | `CounterRates` class. |
| `_factory.py` | `Factory` (`a`, `empty`). |
| `__init__.py` | Wires `CounterRates.Factory`. |
| `_tester.py` | pytest; rows / len / top / eq, 4-line structural. |
