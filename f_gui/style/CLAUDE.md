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
from f_gui.style import Stroke, LineStyle, Border, TextStyle
```

| Export      | Source module            | Role                                  |
|-------------|--------------------------|---------------------------------------|
| `Stroke`    | `f_gui.style.stroke`     | `(color, width, style)` appearance    |
| `LineStyle` | `f_gui.style.stroke`     | enum: `SOLID` / `DASHED` / `DOTTED`   |
| `Border`    | `f_gui.style.border`     | four edge `Stroke`s (T/L/B/R)         |
| `TextStyle` | `f_gui.style.text` | `(font, size, bold, color)` text look |

## Module Hierarchy

```
f_gui/style/
├── __init__.py     lazy aggregator (Stroke, LineStyle, Border, TextStyle)
├── stroke/         Stroke + LineStyle — shared line/edge appearance
├── border/         Border — four edge Strokes
└── text/           TextStyle — text appearance (font/size/bold/color)
```

## The Reuse Story

```
Stroke  = (color, width, style: LineStyle)        the shared appearance
Line    = Stroke + (p1, p2) + arrow               geometry + direction
Border  = { top, left, bottom, right : Stroke? }  four edges
```

`Line` (an element) and `Border` (element state) both consume `Stroke` +
`LineStyle` from here, so the `(color, width, style)` triple is defined
exactly once. `LineStyle` keeps its name (used by both lines and borders)
even though it now lives in the style package, not the line element.

## Rendering Map (handled by RenderHtml)

| Model                       | Output                                          |
|-----------------------------|-------------------------------------------------|
| `Stroke` on a `Border` edge | CSS `border-{side}: {width}px {style} {color}`  |
| `Stroke` on a `Line`        | SVG `stroke` / `stroke-width` / `stroke-dasharray` |
| `LineStyle.*`               | CSS `border-style` keyword / SVG dash pattern   |
| `TextStyle` on a `Label`    | CSS `font-family` / `font-size` / `font-weight` / `color` |
