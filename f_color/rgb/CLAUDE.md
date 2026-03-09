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
Accepts a color name (matplotlib or custom palette) or raw r/g/b float values (0-1).

### Properties
```python
@property
def r(self) -> float       # Red channel (0-1)

@property
def g(self) -> float       # Green channel (0-1)

@property
def b(self) -> float       # Blue channel (0-1)

@property
def key(self) -> tuple[float, float, float]  # (r, g, b) — used for eq/lt/hash
```

### Dunder Methods
```python
def __str__(self) -> str
```
- Named: `'RED(255, 0, 0)'`
- Unnamed: `'(127, 127, 127)'`

```python
def __eq__(self, other) -> bool   # via Equatable (compares key)
def __lt__(self, other) -> bool   # via Comparable (compares key)
def __hash__(self) -> int         # via Hashable (hashes key)
```

### To (instance conversion — `rgb.to.*`)
```python
rgb.to.tuple(to_int: bool = False) -> tuple[float, float, float]
rgb.to.hex() -> str                    # '#FF0000'
rgb.to.argb(alpha: int = 255) -> str   # 'FFFF0000'
rgb.to.ansi() -> str                   # '\033[38;2;255;0;0m'
```

### From (static constructors — `RGB.From.*`)
```python
RGB.From.ints(r: int, g: int, b: int) -> RGB
RGB.From.hex(hex_str: str) -> RGB
```

### Factory (generation — `RGB.Factory.*`)
```python
RGB.Factory.gradient(a: RGB, b: RGB, n: int) -> list[RGB]
RGB.Factory.gradient_multi(stops: list[RGB], n: int) -> list[RGB]
RGB.Factory.random(n: int) -> list[RGB]
```

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
| `HasName` | String name property, `__str__`/`__repr__` |
| `Comparable` | Ordering operators via `key` |
| `Hashable` | `__hash__` via `key` |
| `Equatable` | `__eq__` via `key` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.comparable.Comparable` | Base — ordering operators |
| `f_core.mixins.has.name.HasName` | Base — name property |
| `f_color.rgb._colors._CUSTOM` | Custom color palette (13 colors) |
| `matplotlib.colors` | Color name → RGB float conversion |
| `numpy` | Gradient interpolation (Factory) |

## Usage Examples

```python
from f_color.rgb import RGB

# From name or raw values
red = RGB(name='RED')
gray = RGB(r=0.5, g=0.5, b=0.5)

# From external formats
rgb = RGB.From.hex('#FF0000')
rgb = RGB.From.ints(r=255, g=0, b=0)

# To external formats
red.to.hex()                # '#FF0000'
red.to.tuple(to_int=True)   # (255, 0, 0)
red.to.argb()               # 'FFFF0000'
red.to.ansi()               # '\033[38;2;255;0;0m'

# Comparison
assert RGB(name='BLACK') < RGB(name='WHITE')
assert RGB(name='BLACK') == RGB(r=0, g=0, b=0)

# Gradient
gradient = RGB.Factory.gradient(
    a=RGB(name='WHITE'),
    b=RGB(name='BLACK'),
    n=5
)
assert gradient[2] == RGB(r=0.5, g=0.5, b=0.5)
```
