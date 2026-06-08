# Connector

## Purpose

A **Connector** is an auto-routing line/arrow that attaches to **two
Elements** (PowerPoint-style). It stores references to a *source* and a
*destination* element plus the `Side` of each to attach to, and on every
render it pulls the two connection points **live** from the elements'
`bounds` — so the connector **follows automatically** when an element
moves (no event system; the path is recomputed on each access).

Unlike `Line` (two fixed `Point`s), a Connector's endpoints are derived,
and it can bend: `Routing.DIRECT` is a straight segment, `Routing.
ORTHOGONAL` is a 90-degree elbow.

```
Connector = (src, dst : Element) + (src_side, dst_side : Side?)
            + Stroke + arrow + Routing
```

## Coordinate-Frame Constraint

A Connector renders as an SVG overlay filling **its parent**, with the
path points as percentages of that parent. So the **source, destination
and Connector must share a parent** (the same 0-100 frame) — typically
added as siblings to one `Container`. Cross-container connectors (elements
at different tree depths) would need an absolute-coordinate transform and
are out of scope.

## `Routing` Enum

```python
class Routing(Enum):
    DIRECT     = 'direct'      # straight: [anchor_src, anchor_dst]
    ORTHOGONAL = 'orthogonal'  # 90-degree elbow (axis-aligned polyline)
```

**Orthogonal algorithm:** each anchor steps out by `_STUB` (6 units) along
its side's outward `normal`, then the two stubs are joined — a vertical
mid-line for two horizontal normals, a horizontal mid-line for two
vertical normals, or a single corner for a mixed pair — and collinear
points are dropped (`_simplify`). Obstacle avoidance is **not** done.

## Public API

### Constructor

```python
def __init__(self,
             src: Element,
             dst: Element,
             src_side: Side | None = None,   # None -> auto-pick nearest
             dst_side: Side | None = None,   # None -> auto-pick nearest
             stroke: Stroke | None = None,   # None -> Stroke() default
             arrow: bool = True,             # arrowhead at dst end
             routing: Routing = Routing.DIRECT,
             name: str = 'Connector') -> None
```

### Properties

```python
@property
def src / dst -> Element
@property
def src_side / dst_side -> Side | None
@property
def stroke -> Stroke
@property
def arrow -> bool
@property
def routing -> Routing
@property
def path -> list[Point]      # live polyline vertices (>= 2)
@property
def bounds -> Bounds[float]  # live bbox of the path (overrides Element)
```

`bounds` is **computed** (not stored) — overriding `Element.bounds` keeps
it in sync as the connected elements move.

### Auto Side-Selection

When a side is `None`, it is auto-picked from the elements' relative
centers: horizontal gap dominates -> `RIGHT`/`LEFT`; vertical gap
dominates -> `BOTTOM`/`TOP`. Explicit `src_side`/`dst_side` override this.

## Inheritance (Hierarchy)

```
Element (HasName, HasParent)   abstract
 └── Connector   i_1_connector   (leaf; two Element refs + routing)
```

## Rendering

`RenderHtml` special-cases `Connector` (like `Line`): `_connector()` emits
a self-contained `<svg>` overlay whose `path` becomes a chain of `<line>`
segments in percent coordinates (the same distortion-free model as a
single `Line`). The arrowhead sits on the **last** segment via a per-svg
`<marker>` with a content-derived id. See `f_gui/render/html/CLAUDE.md`.

> 90-degree corners use butt-capped `<line>` segments, so a thin
> sub-pixel notch can appear at the outer corner — cosmetically
> negligible at typical widths.

## Factory Presets

| Method         | Result                                              |
|----------------|-----------------------------------------------------|
| `direct()`     | straight arrow between a top-left and bottom-right box|
| `orthogonal()` | 90-degree elbow arrow between the same two boxes    |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_gui.elements.i_0_element.Element` | Base + the two endpoint refs |
| `f_gui.style.stroke.Stroke`          | Appearance (color/width/style) |
| `f_ds.geometry.bounds.Bounds`        | Live bounding box |
| `f_ds.geometry.point.Point`          | Path vertices |
| `f_ds.geometry.side.Side`            | Attach sides + routing normals |

## Usage Example

```python
from f_gui.elements.i_1_container import Container
from f_gui.elements.i_1_connector import Connector, Routing
from f_ds.geometry.bounds import Bounds
from f_ds.geometry.side   import Side

a = Container(bounds=Bounds(top=20, left=10, bottom=40, right=30))
b = Container(bounds=Bounds(top=60, left=70, bottom=80, right=90))

direct = Connector(src=a, dst=b)                       # auto sides, arrow
elbow  = Connector(src=a, dst=b, routing=Routing.ORTHOGONAL)
fixed  = Connector(src=a, dst=b, src_side=Side.TOP, dst_side=Side.TOP)

# a, b and the connector must be added to the SAME container before render.
```

## Possible Extensions

- Obstacle-aware orthogonal routing (avoid crossing the boxes).
- Cross-container connectors via absolute-coordinate resolution.
- Corner radius on elbows; mid-path labels; a `Routing.CURVED` (bezier).
