# RenderHtml

## Purpose

Stateless renderer that emits a self-contained HTML document (no external
CSS, no JS, no images) for an `f_gui` `Element` tree. The `Bounds` model
(`top, left, bottom, right` in a normalized `0-100` space, relative to
parent) maps 1-to-1 onto CSS percentage absolute-positioning — so the
emitter is a ~30-line recursive function.

## Public API

### Class Attributes

```python
Factory: type = None
```

### Static Methods

```python
@staticmethod
def element(elem: Element) -> str
```
Recursively renders a single `Element` (and all its descendants). Most
elements become a single `<div>` string (Label text is HTML-escaped); a
`Line` is special-cased to an inline `<svg>` overlay (see **Line
Rendering** below).

```python
@staticmethod
def page(root: Element, size: int | None = None) -> str
```
Wraps the rendered tree in a full HTML document.
- **`size=None` (default)** — the stage fills the browser **viewport**
  (full-screen, `position:fixed;inset:0`), matching what a `Window`
  models. Bounds map naturally: `left/right` = % of width,
  `top/bottom` = % of height.
- **`size=<int>`** — a fixed `size × size` centered square stage on a
  dark background (e.g. a deterministic thumbnail); keeps the two axes
  pixel-isotropic.

```python
@staticmethod
def to_file(root: Element, path: str, size: int | None = None) -> None
```
Writes `page(root, size)` to `path` as UTF-8 (full-screen by default).

## Convenience — `Window.to_html()`

A thin wrapper lives on `Window` (lazy import to avoid a cycle):

```python
win.to_html(path='/tmp/demo.html')            # full-screen (default)
win.to_html(path='/tmp/demo.html', size=800)  # fixed 800x800 square
```

## Inner-Content Dispatch

| Concrete type | Inner content        |
|---------------|----------------------|
| `Window`      | children (recursive) |
| `Container`   | children (recursive) |
| `Label`       | `html.escape(text)`  |
| `Line`        | — (rendered as `<svg>`, intercepted first) |

`Container` is matched in `_inner()` (Window IS-A Container, so it's
covered). `Line` is intercepted at the top of `element()` and renders as
`<svg>`, not a `<div>`.

**Borders are no longer type-dispatched.** The old per-type default
borders (`_BORDER_WINDOW` etc.) were removed — borders are now opt-in
`Element.border` state (see **Border Rendering** below).

## Border Rendering (CSS)

`_border()` reads `elem.border` (an `f_gui.style.border.Border`) and emits
one declaration per set side:

```
border-{side}: {stroke.width}px {stroke.style.value} {color};
```

- `LineStyle` values (`'solid'`/`'dashed'`/`'dotted'`) are the **exact CSS
  `border-style` keywords** — no translation.
- `stroke.color` → hex; `None` → `_STROKE_DEFAULT` (`#e6edf3`), shared with
  lines via `_stroke_color()`.
- `border is None` (or a side `None`) → that declaration is omitted; an
  Element with no border emits no `border-{side}` CSS (the always-present
  `box-sizing:border-box` is unrelated).
- Duck-typed: `RenderHtml` imports neither `Border` nor `Stroke`.

## Line Rendering (SVG)

`element()` checks `isinstance(elem, Line)` first and delegates to
`_line()`, which emits a **self-contained `<svg>`** filling the parent
(`position:absolute;inset:0;width/height:100%`). This is the only pure
HTML/CSS way to draw a diagonal with dashes and arrowheads (no JS, no
images).

| `Line` attribute    | SVG mapping                                          |
|---------------------|------------------------------------------------------|
| `p1`/`p2`           | `<line x1="p1.x%" y1="p1.y%" x2="p2.x%" y2="p2.y%">` |
| `stroke.color`      | `stroke` (hex); `None` → `_STROKE_DEFAULT` (`#e6edf3`) |
| `stroke.width`      | `stroke-width` (px)                                  |
| `stroke.style`      | `_dash()` → `stroke-dasharray` (`_DASH` map)         |
| `arrow`             | per-`<svg>` `<marker>` + `marker-end="url(#…)"`      |

The line's `color`/`width`/`style` come from its `Stroke` (the same value
object Border edges use) via `_stroke_color()` and `_dash()`.

- **Percent coords, no `viewBox`.** SVG `%` resolves `x` against width and
  `y` against height — so the `0-100` scene-graph coords map 1:1 onto the
  parent box, and `stroke-width` stays a true pixel value (no viewBox
  scale distortion).
- **`_DASH`:** `DASHED → "8 6"`, `DOTTED → "1 6"` (+ `stroke-linecap:round`
  for dots); `SOLID → ''` (omitted).
- **Arrowhead id is content-derived** (`arrow-{color}-{x1}-{y1}-{x2}-{y2}`)
  so it is unique per distinct line — duplicate ids across separate inline
  `<svg>`s would otherwise make `url(#id)` resolve to the wrong marker.
  `orient="auto"` aims the head along `p1→p2`; `markerUnits="strokeWidth"`
  scales it with `width`.
- `Line` carries no `background` and is not bordered.

## Rendering Semantics

- Every element becomes `<div style="position:absolute; top/left/bottom/right: …%;">`.
- `box-sizing:border-box` keeps borders inside the bounds.
- `overflow:hidden` clips descendants that exceed parent bounds.
- `display:flex; align-items:center; justify-content:center` centers
  label text inside its rectangle.
- **Background:** if `elem.background` is set, `_background()` emits
  `background:{color.to.hex()};` (duck-typed — the renderer imports no
  color type). Unset → no `background` declaration (transparent).
- **Border:** `_border()` emits per-side `border-{side}` CSS from
  `elem.border` (see **Border Rendering**). Unset → no border.

## Dependencies

| Import                                   | Purpose                   |
|------------------------------------------|---------------------------|
| `f_gui.elements.i_0_element.Element`     | Base type / element dispatch |
| `f_gui.elements.i_1_container.Container` | Children recursion        |
| `f_gui.elements.i_1_label.Label`         | Text emission             |
| `f_gui.elements.i_1_line.Line`           | SVG line dispatch         |
| `f_gui.style.stroke.LineStyle`           | Dasharray / linecap selection |
| `html.escape` (stdlib)                   | Text safety               |
| `pathlib.Path` (stdlib)                  | File write                |

`Border` and `Stroke` are **duck-typed** (read via `elem.border` /
`line.stroke`) — not imported, keeping the renderer color/style-type free.

## Usage Example

```python
from f_gui.elements.i_2_window    import Window
from f_gui.elements.i_1_container import Container
from f_gui.elements.i_1_label     import Label
from f_ds.geometry.bounds         import Bounds

win   = Window.Factory.default()
panel = Container(bounds=Bounds(top=30, left=50, bottom=50, right=70))
hello = Label(bounds=Bounds(top=20, left=10, bottom=40, right=30),
              text='Hello')
win.add_child(child=panel)
panel.add_child(child=hello)

win.to_html(path='/tmp/demo.html')   # open in a browser
```

Or using the renderer directly:

```python
from f_gui.render.html import RenderHtml
html_string = RenderHtml.page(root=win)
```

## Study Script

`_study.py` — exploratory, not a test. A white `Window` with two yellow
side-by-side `Container`s, plus a dashed blue diagonal `Line` and a solid
red arrow `Line` bridging the containers — exercising the SVG line path.
Its point is to exercise the **emitter directly**
(`RenderHtml.to_file(...)`) rather than the `Window.to_html()` convenience
wrapper, and to leave a *viewable* artifact (the `_tester.py` asserts on
strings and discards its output). Writes `study.html` in the working
directory.

```bash
python -m f_gui.render.html._study   # then open study.html
```

### Per-component studies (`s_<feature>.py`)

Focused galleries, one feature each — run from the repo root, then open
the matching HTML in a browser:

| Script           | Output            | Demonstrates                                   |
|------------------|-------------------|------------------------------------------------|
| `s_bounds.py`    | `bounds.html`     | 0-100 coords: relative-to-parent, concentric scale, corners |
| `s_background.py`| `background.html` | named-color grid, `RGB.Factory.gradient` strip, transparent vs filled |
| `s_border.py`    | `border.html`     | solid/dashed/dotted, per-side, 4-color, width variants |
| `s_line.py`      | `line.html`       | solid/dashed/dotted, arrow, 4 directions, width variants |

```bash
python -m f_gui.render.html.s_border   # then open border.html
```

`s_border.py` and `s_line.py` both place **solid, dashed and dotted side
by side** — dashed renders as segments, dotted as round dots (a 1px dash
with a round linecap; see **Line Rendering** / **Border Rendering**).

## Scope Notes

- **One-shot render.** Updates require re-emitting the file.
- **Not interactive.** No events, no hover handlers — open in a browser
  to visualize scene-graph state. A separate event/renderer layer is
  out of scope.
- **Text sizing is CSS-driven** (not scaled with bounds).
