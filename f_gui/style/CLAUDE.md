# f_gui.style

## Purpose

Appearance **value objects** for the GUI layer — the styling vocabulary
shared across scene-graph elements. Unlike `f_gui/elements/` (tree nodes)
these are not nodes; they are attached as element state (e.g.
`Element.border`) or composed into elements (e.g. `Line` holds a
`Stroke`). Pure data — no rendering.

## Package Exports

The `__init__.py` is a **lazy aggregator** (`ULazy` + `TYPE_CHECKING`
mirror block).

```python
from f_gui.style import Stroke, DashPattern, Border, TextStyle
```

| Export      | Source module            | Role                                  |
|-------------|--------------------------|---------------------------------------|
| `Stroke`    | `f_gui.style.stroke`     | `(color, width, pattern)` appearance  |
| `DashPattern` | `f_gui.style.stroke`     | enum: `SOLID` / `DASHED` / `DOTTED`   |
| `Border`    | `f_gui.style.border`     | four edge `Stroke`s (T/L/B/R)         |
| `TextStyle` | `f_gui.style.text` | `(font, size, bold, color)` text look |

## Module Hierarchy

```
f_gui/style/
├── __init__.py     lazy aggregator (Stroke, DashPattern, Border, TextStyle)
├── stroke/         Stroke + DashPattern — shared line/edge appearance
├── border/         Border — four edge Strokes
└── text/           TextStyle — text appearance (font/size/bold/color)
```

## The Reuse Story

```
Stroke  = (color, width, pattern: DashPattern)      the shared appearance
Line    = Stroke + (p1, p2) + arrow               geometry + direction
Border  = { top, left, bottom, right : Stroke? }  four edges
```

`Line` (an element) and `Border` (element state) both consume `Stroke` +
`DashPattern` from here, so the `(color, width, pattern)` triple is defined
exactly once. `DashPattern` (the dash pattern: solid / dashed / dotted) is
used by both lines and borders via `Stroke`, so it lives in the style
package, not the line element. It is `Stroke`'s `pattern` attribute.

## Rendering Map (handled by RenderHtml)

| Model                       | Output                                          |
|-----------------------------|-------------------------------------------------|
| `Stroke` on a `Border` edge | CSS `border-{side}: {width}px {style} {color}`  |
| `Stroke` on a `Line`        | SVG `stroke` / `stroke-width` / `stroke-dasharray` |
| `DashPattern.*`               | CSS `border-style` keyword / SVG dash pattern   |
| `TextStyle` on a `Label`    | CSS `font-family` / `font-size` / `font-weight` / `color` |

## Visual Docs (human-facing)

- `ABOUT.html` (this folder) — **interactive** overview: live Stroke,
  Border, and TextStyle playgrounds (each emitting the real CSS/SVG the
  renderer produces), the reuse story, the rendering map, and a section
  arguing the package placement (peer of `elements/` + `render/`, not
  nested under elements). Links out to each module's page below.
- `stroke/ABOUT.html`, `border/ABOUT.html`, `text/ABOUT.html` — one
  visual explainer per value object. Generated on demand; Claude reads
  `CLAUDE.md`, not these.
