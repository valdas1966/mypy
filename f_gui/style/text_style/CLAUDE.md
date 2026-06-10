# TextStyle

## Purpose

Appearance **value object** for text — `(font, size, bold, color)`. Pure
presentation, no content: the text *string* stays on the `Label` (its
content), a `TextStyle` is *how it looks*. Attached the same opt-in way as
`background` / `border` (separate, reusable across many Labels), and sits
beside `Stroke` / `Border` in `f_gui.style`.

The defaults reproduce the renderer's historical hard-coded text CSS
(`monospace`, `12px`, not bold, no color → inherits the page color), so a
`Label` with `style=None` renders byte-identically to before this object
existed.

## Public API

### Class Attributes

```python
Factory: type = None
```

### Constructor

```python
def __init__(self,
             font: str = 'monospace',
             size: float = 12,
             bold: bool = False,
             color: RGB | None = None) -> None
```

### Properties

```python
@property
def font(self) -> str           # CSS font-family value
@property
def size(self) -> float         # pixels
@property
def bold(self) -> bool
@property
def color(self) -> RGB | None   # None = inherit the page color
```

### Dunder Methods

```python
def __str__(self) -> str   # '(monospace 12px normal default)'
```

## Factory Presets

| Method      | Result                                              |
|-------------|-----------------------------------------------------|
| `default()` | `TextStyle()` — monospace, 12px (the baseline look) |
| `title()`   | `TextStyle(size=18, bold=True)`                     |
| `body()`    | `TextStyle(font='sans-serif', size=14)`            |
| `code()`    | `TextStyle(font='monospace', size=12)`             |

## Rendering Map (handled by RenderHtml)

`RenderHtml._text_style()` reads a `Label`'s `style` and emits inline CSS:

| Model        | Output                              |
|--------------|-------------------------------------|
| `font`       | `font-family:{font};`               |
| `size`       | `font-size:{size}px;`               |
| `bold`       | `font-weight:bold;` (only if True)  |
| `color`      | `color:{color.to.hex()};` (opt-in)  |
| `style=None` | `font-family:monospace;font-size:12px;` (baseline) |

Color is duck-typed (`color.to.hex()`); `RenderHtml` imports no
`TextStyle` type (like `Border` / `Stroke`).

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_color.rgb.RGB` (TYPE_CHECKING) | Text color type |

## Usage Example

```python
from f_gui.elements.i_1_label import Label
from f_gui.style.text_style import TextStyle
from f_color.rgb import RGB

Label(text='Title', style=TextStyle.Factory.title())
Label(text='note', style=TextStyle(size=14, color=RGB(name='RED')))
Label(text='plain')   # style=None -> baseline monospace 12px
```
