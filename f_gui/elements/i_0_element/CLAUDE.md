# Element

## Purpose

**Abstract** base class for all GUI elements. Combines `HasName` and
`HasParent` mixins to provide identity and tree structure. Each element
has rectangular `Bounds` (relative to its parent) in a 0-100 coordinate
space.

`Element` is **not instantiable directly** — `Element()` raises
`TypeError`. Create a concrete subclass instead (`Container`, `Label`,
`Window`).

## Why Abstract (and how)

There is no natural abstract method: `bounds` / `name` / `parent` are
fully implemented here, and the only candidate hook (rendering) is
deliberately kept **out** of this pure data model (`f_gui` stores
structure; `RenderHtml` renders). Since `abc.ABC` without an
`@abstractmethod` does **not** block instantiation, abstractness is
enforced with a `__new__` guard:

```python
def __new__(cls, *args, **kwargs) -> 'Element':
    if cls is Element:
        raise TypeError('Element is abstract; instantiate a concrete '
                        'subclass (Container, Label, Window).')
    return super().__new__(cls)
```

The guard blocks `Element()` while allowing every subclass — no
metaclass, no fake abstract method.

## Public API

### Constructor (subclasses only)

```python
def __init__(self,
             bounds: Bounds[float] = None,
             name: str = 'Element',
             background: RGB | None = None) -> None
```
Called by subclasses via `Element.__init__(self, ...)`. Bounds default
to full `(0, 0, 100, 100)`; `background` defaults to `None`
(transparent). All four element types accept and forward `background`.

### Properties

```python
@property
def bounds(self) -> Bounds[float]      # relative to parent
@property
def background(self) -> RGB | None     # fill color; None = transparent
@property
def parent(self) -> Element | None     # from HasParent; None for roots
@property
def name(self) -> str                  # from HasName
```

### Visual style — `background`

The first visual feature on the data model. Stored as a **loose
attribute** (not a `Style` object) and typed as `f_color.rgb.RGB`. To
keep `f_gui` light, `RGB` is imported only under `TYPE_CHECKING` — a
plain `Element`/`Label` never pulls in `matplotlib`; only *passing* an
`RGB` does. The renderer reads `elem.background` and emits
`background:{rgb.to.hex()}` (duck-typed; `RenderHtml` imports no color
type). Border is still type-dispatched in the renderer — a future step.

### Methods

```python
def path_from_root(self) -> list[Self]   # from HasParent
```

### Dunder Methods

```python
def __str__(self) -> str    # 'Name(top, left, bottom, right)'
```

## No Factory

`Element` has **no** `Factory` — an abstract class has no canonical
instances to manufacture, and a factory would itself be a way to create
bare elements (the thing abstractness forbids). Concrete subclasses
carry their own factories (`Container.Factory`, `Window.Factory`, …).

## Inheritance (Hierarchy)

```
HasName
HasParent
 └── Element  (abstract)
      ├── Container
      │    └── Window
      └── Label
```

| Base | Responsibility |
|------|----------------|
| `HasName` | Provides `name` property and `_name` storage |
| `HasParent` | Provides `parent`, `_parent`, and `path_from_root()` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.has.name.HasName` | Name mixin |
| `f_core.mixins.has.parent.HasParent` | Parent-chain mixin |
| `f_ds.geometry.bounds.Bounds` | Rectangular bounds for positioning |

## Usage Example

```python
from f_gui.elements.i_0_element.main import Element
from f_gui.elements.i_1_label.main     import Label
from f_ds.geometry.bounds              import Bounds

Element()                       # TypeError — abstract

label = Label(bounds=Bounds(top=10, left=10, bottom=40, right=40),
              text='Hi')        # OK — concrete subclass
print(label.bounds.to_tuple())  # (10, 10, 40, 40)
print(label.parent)             # None

# Testing the abstract base uses a minimal local concrete subclass:
class _Concrete(Element):
    pass
print(_Concrete().bounds.to_tuple())   # (0, 0, 100, 100)
```

## Testing Note

`_tester.py` tests inherited behavior through a local `_Concrete(Element)`
subclass and asserts that `Element()` raises `TypeError`. The
`i_1_container` tests use `Label` as their neutral leaf child (previously
a bare `Element`).
