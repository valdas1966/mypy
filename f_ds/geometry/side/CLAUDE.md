# Side

## Purpose

`Side` is an enum naming one edge of a rectangle — `TOP`, `RIGHT`,
`BOTTOM`, `LEFT`. It is the geometry vocabulary for an element's four
**connection points**: `Bounds.anchor(side)` returns the mid-point of the
named edge, and a `Connector` routes between two such anchors.

Values are the **CSS edge keywords** (`'top'`/`'right'`/`'bottom'`/
`'left'`), matching `Border`'s side names — so the GUI uses one side
vocabulary throughout.

## Public API

### Enum members

```python
class Side(Enum):
    TOP    = 'top'
    RIGHT  = 'right'
    BOTTOM = 'bottom'
    LEFT   = 'left'
```

### Properties

```python
@property
def normal(self) -> tuple[int, int]   # outward unit direction (dx, dy)
@property
def opposite(self) -> Side            # TOP<->BOTTOM, LEFT<->RIGHT
```

`normal` is the outward direction in **screen coordinates** (y grows
downward), used by orthogonal connector routing to leave/enter an anchor
perpendicular to its edge:

| Side     | normal   |
|----------|----------|
| `TOP`    | `(0, -1)`|
| `RIGHT`  | `(1, 0)` |
| `BOTTOM` | `(0, 1)` |
| `LEFT`   | `(-1, 0)`|

## Design Notes

- **Plain `Enum`**, no `Factory` (an enum has no manufactured instances).
  Behavior (`normal` / `opposite`) is table-driven via module-level
  `_NORMALS` / `_OPPOSITES` dicts defined after the class.
- **No existing direction enum** in the repo — grid neighbours use raw
  `(row, col)` deltas — so `Side` is the first one; kept in `f_ds/geometry`
  as foundational geometry, not in `f_gui`.

## Used By

| Consumer | Relationship |
|----------|--------------|
| `Bounds.anchor(side)` (`f_ds.geometry.bounds`) | side -> mid-point `PointXY` |
| `Element.anchor(side)` (`f_gui`)               | delegates to its `Bounds` |
| `Connector` (`f_gui.elements.i_1_connector`)   | attach sides + routing normals |

## Dependencies

| Import | Purpose |
|--------|---------|
| `enum.Enum` (stdlib) | Enum base |

## Usage Example

```python
from f_ds.geometry.side import Side

Side.RIGHT.normal      # (1, 0)
Side.TOP.opposite      # Side.BOTTOM
Side.LEFT.value        # 'left'
```
