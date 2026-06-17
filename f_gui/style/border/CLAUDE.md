# Border

## Purpose

`Border` groups **up to four edge `Stroke`s** around an Element's box —
`top`, `left`, `bottom`, `right` — each independently a `Stroke` or `None`
(no edge on that side). Because a border edge and a line share the same
appearance vocabulary (`Stroke`), a `Border` is simply four of them.

`Border` is carried as opt-in Element state (`Element.border`); it is
*not* a scene-graph node.

## Public API

### Constructor

```python
def __init__(self,
             top: Stroke | None = None,
             left: Stroke | None = None,
             bottom: Stroke | None = None,
             right: Stroke | None = None) -> None
```
`Stroke` is imported only under `TYPE_CHECKING`.

### Properties

```python
@property
def top(self)    -> Stroke | None
@property
def left(self)   -> Stroke | None
@property
def bottom(self) -> Stroke | None
@property
def right(self)  -> Stroke | None
```

### Dunder Methods

```python
def __str__(self) -> str    # 'Border[T=(2px solid default)]' (set sides only)
```

## Rendering

`RenderHtml._border()` reads `Element.border` and emits one
`border-{side}: {width}px {style} {color}` declaration per set side —
`DashPattern` values are the exact CSS `border-style` keywords, so the map
is 1:1. An Element with `border is None` emits nothing (borders are fully
opt-in; the old per-type default borders were removed).

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_gui.style.stroke.Stroke` | Per-edge appearance (TYPE_CHECKING in main; eager in factory) |

## Factory Presets

| Method         | Result                                  |
|----------------|-----------------------------------------|
| `all(stroke)`  | the same `Stroke` on all four sides     |
| `solid()`      | uniform default (1px solid) on all sides|

## Usage Example

```python
from f_gui.style.border import Border
from f_gui.style.stroke import Stroke, DashPattern
from f_color.rgb import RGB

# Uniform red 2px border
uniform = Border.Factory.all(stroke=Stroke(color=RGB('RED'), width=2))

# Dashed blue top + bottom only
edge = Stroke(color=RGB('BLUE'), width=3, pattern=DashPattern.DASHED)
partial = Border(top=edge, bottom=edge)
```
