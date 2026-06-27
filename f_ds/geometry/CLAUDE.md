# f_ds.geometry

## Purpose

Aggregator package for the framework's geometry primitives — the
coordinate building blocks used by layout, grids and the GUI scene graph.

## Package Exports

The `__init__.py` is a **lazy aggregator** (`ULazy` + `TYPE_CHECKING`
mirror block) — importing one name does not load its siblings, and the
aggregator form resolves in IDEs / mypy.

```python
from f_ds.geometry import Bounds, Point, Side
```

| Export   | Source module           | Role                                   |
|----------|-------------------------|----------------------------------------|
| `Bounds` | `f_ds.geometry.bounds`  | Rectangle `(top, left, bottom, right)` |
| `Point`  | `f_ds.geometry.point`   | 2-D point `(x, y)`                      |
| `Side`   | `f_ds.geometry.side`    | rectangle edge enum `TOP/RIGHT/BOTTOM/LEFT` |

## Module Hierarchy

```
f_ds/geometry/
├── __init__.py     lazy aggregator (Bounds, Point, Side)
├── bounds/         Bounds[T] — generic rectangle primitive; `anchor(side)`; Tupleable
├── point/          Point — (x, y); Tupleable (eq/order/hash/iter via to_tuple)
└── side/           Side — rectangle edge enum (+ outward `normal`, `opposite`)
```

## Conventions

- `Bounds` is `Generic[T]` (int/float) and inherits `Tupleable` — its
  `(top, left, bottom, right)` tuple is its identity (eq/order/hash).
- `Point` is **non-generic** (`float`) and inherits `Tupleable` — a
  deliberate domain choice (coordinates are `0-100` floats, nothing to
  parameterize), not a technical limit; `Generic[T]` composes fine with
  the mixins (cf. `Bounds[T]`).
- Both `Point` and `Bounds` derive identity, ordering, hashing and
  unpacking from a single `to_tuple()` via `Tupleable`.
- `Side` is a plain `Enum` (no `Factory`); its values are the CSS edge
  keywords, shared with `Border` / connection points.
- `Bounds.anchor(side)` returns the mid-point `Point` of an edge — the four
  connection points used by `Element.anchor` and `Connector`.
- All coordinates use the normalized `0-100` space the GUI layer relies on
  (`x` → horizontal/left, `y` → vertical/top).
