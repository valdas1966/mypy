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
Recursively renders a single `Element` (and all its descendants) as a
single `<div>` string. Label text is HTML-escaped.

```python
@staticmethod
def page(root: Element, size: int = 600) -> str
```
Wraps the rendered tree in a full HTML document with a centered
`size × size` stage on a dark background.

```python
@staticmethod
def to_file(root: Element, path: str, size: int = 600) -> None
```
Writes `page(root, size)` to `path` as UTF-8.

## Convenience — `Window.to_html()`

A thin wrapper lives on `Window` (lazy import to avoid a cycle):

```python
win.to_html(path='/tmp/demo.html', size=800)
```

## Type → Style Dispatch

| Concrete type | Border                  | Inner content           |
|---------------|-------------------------|--------------------------|
| `Window`      | `3px solid #ff8c42`     | children (recursive)     |
| `Container`   | `2px dashed #58a6ff`    | children (recursive)     |
| `Label`       | `2px solid #bc8cff`     | `html.escape(text)`      |
| `Element`     | `1px solid #888` (fallback) | empty                |

`Window` is checked before `Container` because `Window` IS-A `Container`.

## Rendering Semantics

- Every element becomes `<div style="position:absolute; top/left/bottom/right: …%;">`.
- `box-sizing:border-box` keeps borders inside the bounds.
- `overflow:hidden` clips descendants that exceed parent bounds.
- `display:flex; align-items:center; justify-content:center` centers
  label text inside its rectangle.

## Dependencies

| Import                                   | Purpose                   |
|------------------------------------------|---------------------------|
| `f_gui.elements.i_0_element.Element`     | Base type dispatch        |
| `f_gui.elements.i_1_container.Container` | Children recursion        |
| `f_gui.elements.i_1_label.Label`         | Text emission             |
| `f_gui.elements.i_2_window.Window`       | Priority dispatch         |
| `html.escape` (stdlib)                   | Text safety               |
| `pathlib.Path` (stdlib)                  | File write                |

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

## Scope Notes

- **One-shot render.** Updates require re-emitting the file.
- **Not interactive.** No events, no hover handlers — open in a browser
  to visualize scene-graph state. A separate event/renderer layer is
  out of scope.
- **Text sizing is CSS-driven** (not scaled with bounds).
