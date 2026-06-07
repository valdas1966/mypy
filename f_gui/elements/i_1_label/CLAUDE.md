# Label

## Purpose

Leaf `Element` that carries a string of `text`. Renders as a `<div>` with
the text centered and HTML-escaped. Holds no children.

## Public API

### Class Attributes

```python
Factory: type = None
```

### Constructor

```python
def __init__(self,
             bounds: Bounds[float] = None,
             text: str = '',
             name: str = 'Label',
             background: RGB | None = None,
             border: Border | None = None) -> None
```
Bounds default to full `(0, 0, 100, 100)`. `background`
(`f_color.rgb.RGB`, `None` = transparent) and `border`
(`f_gui.style.border.Border`, `None` = no border) are forwarded to
`Element`.

### Properties

```python
@property
def text(self) -> str
```
Plus inherited `bounds`, `name`, `parent`, `background`, `border`,
`path_from_root()`.

### Dunder Methods

```python
def __str__(self) -> str    # 'Label[text](top, left, bottom, right)'
```

## Inheritance (Hierarchy)

```
Element (HasName, HasParent)   abstract
 └── Label   i_1_label   (leaf, carries text)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_gui.elements.i_0_element.Element` | Base: name + parent + bounds |
| `f_ds.geometry.bounds.Bounds` | Rectangular bounds |
| `f_color.rgb.RGB` (TYPE_CHECKING) | Background color type |
| `f_gui.style.border.Border` (TYPE_CHECKING) | Border type |

## Rendering

Text is HTML-escaped and centered (`display:flex; align-items/justify:
center`) inside the label's box. See `f_gui/render/html/CLAUDE.md`.

## Factory Presets

| Method    | Result                                          |
|-----------|-------------------------------------------------|
| `hello()` | `Label(text='Hello')` (full bounds)             |
| `title()` | title bar `Label` at `(0, 0, 10, 100)`          |

## Usage Example

```python
from f_gui.elements.i_1_label import Label
from f_ds.geometry.bounds import Bounds

label = Label(bounds=Bounds(top=20, left=10, bottom=40, right=30),
              text='Hello')
print(label.text)    # Hello
```
