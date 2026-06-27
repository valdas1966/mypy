# Stroke

## Purpose

`Stroke` is the **shared visual appearance of a line**: `(color, width,
pattern)` with no geometry. It is the single reuse point between a `Line`
(geometry + appearance + arrow) and a `Border` edge (just appearance), so
the two never duplicate the color/width/pattern triple.

This module also defines the **`DashPattern`** enum (relocated here from the
line element, since both Line and Border now use it).

## `DashPattern` Enum

```python
class DashPattern(Enum):
    SOLID  = 'solid'
    DASHED = 'dashed'
    DOTTED = 'dotted'
```
Values are the **exact CSS keywords** — `border-style: solid/dashed/dotted`
and the SVG dash family — so the renderer translates with zero mapping.

## `Stroke` — Public API

### Constructor

```python
def __init__(self,
             color: RGB | None = None,
             width: float = 1,
             pattern: DashPattern = DashPattern.SOLID) -> None
```
`RGB` is imported only under `TYPE_CHECKING`, so a plain `Stroke` never
pulls in `matplotlib`.

### Properties

```python
@property
def color(self) -> RGB | None      # None = renderer default
@property
def width(self) -> float           # pixels
@property
def pattern(self) -> DashPattern
```

### Dunder Methods

```python
def __str__(self) -> str    # '(2px dashed RED(255, 0, 0))' / '... default'
```

## Design Notes

- **Plain value object** (manual `__init__` + properties + `=`-docstrings),
  matching `Bounds` / `PointXY` / `RGB`. Not a dataclass, not `Equatable`
  (no current need).
- **No rendering here.** `f_gui` stores appearance; `RenderHtml` turns a
  `Stroke` into CSS (`border-{side}: {width}px {style} {color}`) or an SVG
  stroke. The renderer supplies the fallback color for `color is None`.

## Used By

| Consumer | Relationship |
|----------|--------------|
| `Line` (`f_gui.elements.i_1_line`) | `Line` = `Stroke` + endpoints + arrow |
| `Border` (`f_gui.style.border`)    | each edge is a `Stroke` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_color.rgb.RGB` (TYPE_CHECKING) | Stroke color type only |

## Factory Presets

| Method      | Stroke                          |
|-------------|---------------------------------|
| `default()` | `Stroke()` (1px, solid, no color)|
| `dashed()`  | `Stroke(width=2, pattern=DASHED)` |

## Usage Example

```python
from f_gui.style.stroke import Stroke, DashPattern
from f_color.rgb import RGB

s = Stroke(color=RGB('RED'), width=3, pattern=DashPattern.DASHED)
print(s)   # (3px dashed RED(255, 0, 0))
```
