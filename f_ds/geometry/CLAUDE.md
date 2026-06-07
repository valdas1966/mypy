# f_ds.geometry

## Purpose

Aggregator package for the framework's geometry primitives — the
coordinate building blocks used by layout, grids and the GUI scene graph.

## Package Exports

The `__init__.py` is a **lazy aggregator** (`ULazy` + `TYPE_CHECKING`
mirror block) — importing one name does not load its siblings, and the
aggregator form resolves in IDEs / mypy.

```python
from f_ds.geometry import Bounds, Point
```

| Export   | Source module           | Role                                   |
|----------|-------------------------|----------------------------------------|
| `Bounds` | `f_ds.geometry.bounds`  | Rectangle `(top, left, bottom, right)` |
| `Point`  | `f_ds.geometry.point`   | 2-D point `(x, y)`                      |

## Module Hierarchy

```
f_ds/geometry/
├── __init__.py     lazy aggregator (Bounds, Point)
├── bounds/         Bounds[T] — generic rectangle primitive
└── point/          Point — (x, y), Hashable (eq + hash via key)
```

## Conventions

- `Bounds` is `Generic[T]` (int/float) with no mixins.
- `Point` is **non-generic** (`float`) and inherits `Hashable` — combining
  `Generic[T]` with a mixin raises a metaclass `TypeError` here.
- All coordinates use the normalized `0-100` space the GUI layer relies on
  (`x` → horizontal/left, `y` → vertical/top).
