# f_ds.geometry

## Purpose

Aggregator package for the framework's geometry primitives — the
coordinate building blocks used by layout, grids and the GUI scene graph.

## Package Exports

The `__init__.py` is a **lazy aggregator** (`ULazy` + `TYPE_CHECKING`
mirror block) — importing one name does not load its siblings, and the
aggregator form resolves in IDEs / mypy.

```python
from f_ds.geometry import Bounds, PointXY, Point2D, Side
```

| Export   | Source module           | Role                                   |
|----------|-------------------------|----------------------------------------|
| `Bounds` | `f_ds.geometry.bounds`  | Rectangle `(top, left, bottom, right)` |
| `PointXY`  | `f_ds.geometry.pointxy`   | 2-D point `(x, y)` — `float`, GUI/render |
| `Point2D`| `f_ds.geometry.point2d` | 2-D lattice point `(row, col)` — `int`, grid |
| `Side`   | `f_ds.geometry.side`    | rectangle edge enum `TOP/RIGHT/BOTTOM/LEFT` |

## Module Hierarchy

```
f_ds/geometry/
├── __init__.py     lazy aggregator (Bounds, PointXY, Point2D, Side)
├── bounds/         Bounds[T] — generic rectangle primitive; `anchor(side)`; Tupleable
├── pointxy/          PointXY — (x, y) float; Tupleable (eq/order/hash/iter via to_tuple)
├── point2d/        Point2D — (row, col) int lattice coord; Tupleable; grid Connectivity
└── side/           Side — rectangle edge enum (+ outward `normal`, `opposite`)
```

## Conventions

- `Bounds` is `Generic[T]` (int/float) and inherits `Tupleable` — its
  `(top, left, bottom, right)` tuple is its identity (eq/order/hash).
- `PointXY` is **non-generic** (`float`) and inherits `Tupleable` — a
  deliberate domain choice (a coordinate is a real-valued scalar, nothing
  to parameterize), not a technical limit; `Generic[T]` composes fine
  with the mixins (cf. `Bounds[T]`).
- Both `PointXY` and `Bounds` derive identity, ordering, hashing and
  unpacking from a single `to_tuple()` via `Tupleable`.
- `PointXY` (`float` `x, y`, GUI/render) and `Point2D` (`int` `row, col`,
  grid lattice) are **distinct** value objects — same Tupleable base,
  different domains; do not conflate. `Point2D` is the footgun-free
  coordinate the grid Connectivity policy consumes (it has no Manhattan
  `distance`, unlike the `HasRowCol` cell mixin).
- `Side` is a plain `Enum` (no `Factory`); its values are the CSS edge
  keywords, shared with `Border` / connection points.
- `Bounds.anchor(side)` returns the mid-point `PointXY` of an edge — the four
  connection points used by `Element.anchor` and `Connector`.
- `PointXY` and `Bounds` are **frame-agnostic** — they impose no coordinate
  domain. The normalized `0-100` space (`x` → horizontal/left, `y` →
  vertical/top) is an **`f_gui` canvas policy** that consumers apply; it
  surfaces here only as `Factory` presets (`PointXY.zero` is the lone
  frame-agnostic one; `Bounds.full/half/quarter` are `0-100` presets).
