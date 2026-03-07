# Color Package

## Purpose
Color representation and visualization utilities. Core class is `RGB`
for float-based (0-1) color values with comparison, hashing, and
format conversion.

## Package Exports

```python
from f_color import RGB
from f_color.rgb import RGB          # same
from f_color.u_color import UColor   # visualization utility
```

## Module Hierarchy

```
f_color/
├── __init__.py        re-exports RGB
├── rgb/               RGB color class (main module)
│   ├── main.py        RGB class + _To helper
│   ├── _from.py       From class (parse external formats)
│   ├── _factory.py    Factory (presets, gradients, random)
│   ├── _tester.py     11 pytest tests
│   └── _study.py      exploratory scripts
└── u_color.py         UColor — matplotlib color visualization
```

## Module Summary

| Module | Class | Key Capability |
|--------|-------|----------------|
| `rgb` | `RGB` | Color representation, comparison, From/To conversion |
| `u_color` | `UColor` | Display colors as matplotlib rectangles |

## Three-Tier Pattern: From / Factory / To

| Tier | Purpose | Example |
|------|---------|---------|
| `From` | Parse external formats | `RGB.From.hex('#FF0000')` |
| `Factory` | Presets + generation | `RGB.Factory.gradient(a, b, n)` |
| `To` | Serialize to external formats | `rgb.to.hex()` |

## Dependencies

| Import | Used By | Purpose |
|--------|---------|---------|
| `f_core.mixins.comparable` | RGB | Ordering operators |
| `f_core.mixins.has.name` | RGB | Name property |
| `matplotlib` | RGB, UColor | Color lookup, visualization |
| `numpy` | Factory | Gradient interpolation |

## Usage Example

```python
from f_color import RGB

# Create
red = RGB(name='RED')

# From external format
rgb = RGB.From.hex('#FF0000')

# Convert
red.to.hex()              # '#FF0000'
red.to.tuple(to_int=True) # (255, 0, 0)

# Gradient
gradient = RGB.Factory.gradient(
    a=RGB(name='BLACK'),
    b=RGB(name='WHITE'),
    n=5
)
```
