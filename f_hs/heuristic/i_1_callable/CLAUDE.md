# HCallable

## Purpose
Wrap a `Callable[[State], float]` in an `HBase` so AStar can
treat all heuristic sources uniformly. Preserves the pre-Phase-1
AStar behavior — zero change for callers that still pass raw
lambdas.

## Public API

### Constructor
```python
def __init__(self, fn: Callable[[State], float]) -> None
```

### `__call__(state) -> float`
Delegates to `fn(state)`.

### Inherited Defaults (from HBase)
- `is_perfect(state) -> False`
- `suffix_next(state) -> None`

Because a raw callable carries no per-state perfection info,
the defaults are correct. For cached / bounded / pathmax, see
`HCached` (and Phase 2 `HBounded`).

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `zero()` | `HCallable` | h(s) = 0 — trivial admissible |
| `graph_abc()` | `HCallable` | h(A)=2, h(B)=1, h(C)=0 |

## Inheritance
```
HBase[State]
  └── HCallable[State]
```

## Tests
`_tester.py` — 3 tests:
1. `test_calls_wrapped_fn` — __call__ forwards correctly.
2. `test_unknown_key_falls_back` — unknown-key behavior is fn-defined.
3. `test_inherits_hbase_defaults` — is_perfect/suffix_next defaults.

## Dependencies
- `f_hs.heuristic.i_0_base.HBase`
- `f_hs.state.i_0_base.StateBase`
