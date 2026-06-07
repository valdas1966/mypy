# Window

## Purpose

Root `Container` of a scene graph, with **implicit full bounds**
`(0, 0, 100, 100)` — it models the whole screen / viewport. Adds a
convenience `to_html()` for one-shot rendering.

## Public API

### Class Attributes

```python
Factory: type = None
```

### Constructor

```python
def __init__(self,
             name: str = 'Window',
             background: RGB | None = None,
             border: Border | None = None) -> None
```
Takes no `bounds` (always full). `background` (`f_color.rgb.RGB`) and
`border` (`f_gui.style.border.Border`) are forwarded to `Container` →
`Element`.

### Methods

```python
def to_html(self, path: str, size: int | None = None) -> None
```
Renders this Window (and descendants) to a standalone HTML file via
`RenderHtml` (lazy import to avoid a cycle). `size=None` (default) →
full-screen stage; `size=<int>` → fixed `size × size` square.

### Inherited

`add_child()`, `remove_child()`, `children`, `bounds`, `name`, `parent`,
`background`, `border`, `path_from_root()`.

## Inheritance (Hierarchy)

```
Element (HasName, HasParent)   abstract
 └── Container   i_1_container   (+ HasChildren)
      └── Window   i_2_window    (root, full bounds 0-100)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_gui.elements.i_1_container.Container` | Parent class (children + bounds) |
| `f_gui.render.html.RenderHtml` (lazy, in `to_html`) | Rendering |
| `f_color.rgb.RGB` (TYPE_CHECKING) | Background color type |
| `f_gui.style.border.Border` (TYPE_CHECKING) | Border type |

## Factory Presets

| Method      | Result            |
|-------------|-------------------|
| `default()` | `Window()` (full) |

## Usage Example

```python
from f_gui.elements.i_2_window import Window
from f_gui.elements.i_1_label  import Label

win = Window.Factory.default()
win.add_child(child=Label(text='Hello'))
win.to_html(path='/tmp/demo.html')      # full-screen
```
