# RGB

## Purpose
RGB color representation with float values (0-1). Supports construction
from name (matplotlib), hex string, or raw float values. Provides
comparison, hashing, and conversion to tuple/hex/ARGB formats.

## Public API

### Constructor
```python
def __init__(self,
             name: str | None = None,
             r: float | None = None,
             g: float | None = None,
             b: float | None = None) -> None
```
Accepts a color name (matplotlib or custom) or raw r/g/b float values.

### Properties
```python
@property
def r(self) -> float       # Red value (0-1)

@property
def g(self) -> float       # Green value (0-1)

@property
def b(self) -> float       # Blue value (0-1)

@property
def key(self) -> tuple[float, float, float]  # (r, g, b) for comparison
```

### To (instance conversion — rgb.to.*)
```python
rgb.to.tuple(to_int: bool = False) -> tuple[float, float, float]
rgb.to.hex() -> str                    # '#FF0000'
rgb.to.argb(alpha: int = 255) -> str   # 'FFFF0000'
```

### From (static constructors — RGB.From.*)
```python
RGB.From.ints(r: int, g: int, b: int) -> RGB
RGB.From.hex(hex_str: str) -> RGB
```

### Factory (generation — RGB.Factory.*)
```python
RGB.Factory.gradient(a: RGB, b: RGB, n: int) -> list[RGB]
RGB.Factory.gradient_multi(stops: list[RGB], n: int) -> list[RGB]
RGB.Factory.random(n: int) -> list[RGB]
```

## Three-Tier Pattern: From / Factory / To
| Tier | Purpose | Access |
|------|---------|--------|
| `From` | Parse external formats into RGB | `RGB.From.hex('#FF0000')` |
| `Factory` | Generation (gradients, random) | `RGB.Factory.gradient(a, b, n)` |
| `To` | Serialize RGB to external formats | `rgb.to.hex()` |

## Inheritance (Hierarchy)

```
SupportsEquality (Protocol)
 └── Equatable ─── __eq__ via key
      ├── Comparable ─── __lt__, __le__, __gt__, __ge__
      └── Hashable ─── __hash__ via key
           └── HasName ─── string name + str()/repr()
                └── RGB(HasName, Comparable)
                     └── key = (r, g, b)
```

| Base | Responsibility |
|------|----------------|
| `HasName` | String name property |
| `Comparable` | Comparison operators via `key` |

## Internal Files

| File | Purpose |
|------|---------|
| `_colors.py` | Custom color palette dict (`_CUSTOM`) |
| `_from.py` | `From` class (parse external formats) |
| `_to.py` | `To` class (serialize to external formats) |
| `_factory.py` | `Factory` class (presets, gradients, random) |
| `_tester.py` | pytest unit tests |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.comparable.Comparable` | Base — ordering operators |
| `f_core.mixins.has.name.HasName` | Base — name property |
| `f_color.rgb._colors._CUSTOM` | Custom color palette |
| `matplotlib.colors` | Color name -> RGB conversion |
| `numpy` | Gradient generation (Factory) |

## Usage Examples

```python
from f_color.rgb import RGB

# From name or values
red = RGB(name='RED')
gray = RGB(r=0.5, g=0.5, b=0.5)

# From external formats
rgb = RGB.From.hex('#FF0000')
rgb = RGB.From.ints(r=255, g=0, b=0)

# To external formats
red.to.hex()                # '#FF0000'
red.to.tuple(to_int=True)   # (255, 0, 0)
red.to.argb()               # 'FFFF0000'

# Comparison
RGB(name='BLACK') < RGB(name='WHITE')  # True

# Gradient
gradient = RGB.Factory.gradient(
    a=RGB(name='BLACK'),
    b=RGB(name='WHITE'),
    n=5
)
```
