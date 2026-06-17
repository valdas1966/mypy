# Line

## Purpose

A **directed segment** GUI element: a leaf `Element` defined by two
endpoints `p1 -> p2` (each a `Point` in the normalized `0-100` space,
relative to the parent). Unlike the rectangle-based `Container`/`Label`,
a `Line` is a two-point primitive, so it renders as an inline **`<svg>`**
overlay (not a `<div>`) — the only pure-HTML way to draw a diagonal with
dashes and arrowheads.

## Appearance — `Stroke`

`Line` holds a **`Stroke`** (`f_gui.style.stroke`) = `(color, width,
style)`. This is the same value object a `Border` edge uses, so the
appearance triple lives in one place:

```
Line = Stroke + (p1, p2) + arrow
```

`DashPattern` (`SOLID`/`DASHED`/`DOTTED`) also lives in `f_gui.style.stroke`
(it is shared with borders) — import it from there, not from this module.

| Aspect    | Source                       | Renders as            |
|-----------|------------------------------|-----------------------|
| `stroke.color` | `RGB \| None` (→ default)| SVG `stroke`          |
| `stroke.width` | `float` (px)             | `stroke-width`        |
| `stroke.pattern` | `DashPattern`              | `stroke-dasharray`    |
| `arrow`        | `bool`                   | `marker-end` at `p2`  |

## Public API

### Constructor

```python
def __init__(self,
             p1: Point,
             p2: Point,
             stroke: Stroke | None = None,   # None -> Stroke() default
             arrow: bool = False,
             name: str = 'Line') -> None
```
The `Element.bounds` are computed as the **bounding box** of `p1`/`p2`
(`min`/`max` of each axis) — keeping the "rectangular extent" invariant
meaningful for future hit-testing.

### Properties

```python
@property
def p1(self) -> Point          # start
@property
def p2(self) -> Point          # end (arrowhead sits here)
@property
def stroke(self) -> Stroke     # color / width / style
@property
def arrow(self) -> bool
```
Plus inherited `bounds`, `name`, `parent`, `background`, `border`,
`path_from_root()`.

### Dunder Methods

```python
def __str__(self) -> str    # 'Line(x1, y1)->(x2, y2)'
```

## Inherited `border` is ignored

`Line` inherits `Element.border` but renders as `<svg>` (not a bordered
`<div>`), so a border set on a `Line` has no visual effect. `Line`'s own
constructor does not expose `border`.

## Inheritance (Hierarchy)

```
Element (HasName, HasParent)   abstract
 └── Line   i_1_line   (leaf; two Points + Stroke + arrow)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_gui.elements.i_0_element.Element` | Base: name + parent + bounds |
| `f_gui.style.stroke.Stroke` | Appearance (color/width/style) |
| `f_ds.geometry.bounds.Bounds` | Bounding box for `Element.bounds` |
| `f_ds.geometry.point.Point` | Endpoint primitive |

## Rendering

`RenderHtml` special-cases `Line` (see `f_gui/render/html/CLAUDE.md`):
each `Line` emits a self-contained `<svg>` filling its parent, with the
endpoints as SVG percentages (`x1="40%"` …), so the `0-100` coords map
1:1 onto the parent box. The arrowhead is a per-`<svg>` `<marker>` with a
content-derived id (unique per distinct line).

## Factory Presets

| Method       | Result                                          |
|--------------|-------------------------------------------------|
| `diagonal()` | solid `(0,0) -> (100,100)`                       |
| `arrow()`    | horizontal `(10,50) -> (90,50)`, `arrow=True`   |
| `dashed()`   | dashed `(0,0) -> (100,100)`                      |

## Usage Example

```python
from f_gui.elements.i_1_line import Line
from f_gui.style.stroke import Stroke, DashPattern
from f_ds.geometry.point import Point
from f_color.rgb import RGB

arrow = Line(p1=Point(x=10, y=50), p2=Point(x=90, y=50),
             stroke=Stroke(color=RGB('RED'), width=3), arrow=True)
dashed = Line(p1=Point(x=0, y=0), p2=Point(x=100, y=100),
              stroke=Stroke(pattern=DashPattern.DASHED))
```
