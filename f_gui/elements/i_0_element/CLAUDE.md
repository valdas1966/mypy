# Element

## Purpose

**Abstract** base class for all GUI elements. Combines `HasName` and
`HasParent` mixins to provide identity and tree structure. Each element
has rectangular `Bounds` (relative to its parent) in a 0-100 coordinate
space.

`Element` is **abstract by convention** — it inherits from `abc.ABC` as
an explicit marker, but is meant to be subclassed (`Container`, `Label`,
`Window`), not used directly.

## Why Abstract (and how)

There is no natural abstract method: `bounds` / `name` / `parent` are
fully implemented here, and the only candidate hook (rendering) is
deliberately kept **out** of this pure data model (`f_gui` stores
structure; `RenderHtml` renders).

Abstractness is therefore declared with an `ABC` marker:

```python
class Element(HasName, HasParent, ABC):
    ...
```

This matches the framework's convention-only abstract bases (e.g.
`StateBase`): the class is **marked** abstract, not runtime-enforced.
Note that `abc.ABC` **without** an `@abstractmethod` does *not* block
instantiation — `Element()` does not raise. Enforcement was previously
done with a `__new__` guard; that was removed for consistency with the
rest of the framework (we do not invent a fake abstract method, and
runtime blocking was the lone outlier among the `i_0_*` bases). No
metaclass conflict arises — `HasName`/`HasParent` use the plain `type`
metaclass, so `ABCMeta` composes cleanly.

## Public API

### Constructor (subclasses only)

```python
def __init__(self,
             bounds: Bounds[float] = None,
             name: str = 'Element',
             background: RGB | None = None,
             border: Border | None = None) -> None
```
Called by subclasses via `Element.__init__(self, ...)`. Bounds default
to full `(0, 0, 100, 100)`; `background` defaults to `None`
(transparent); `border` defaults to `None` (no border). `Container`,
`Label` and `Window` accept and forward both `background` and `border`.
(`Line` forwards neither — it carries a `Stroke` and renders as SVG.)

### Properties

```python
@property
def bounds(self) -> Bounds[float]      # relative to parent
@property
def background(self) -> RGB | None     # fill color; None = transparent
@property
def border(self) -> Border | None      # 4 edge Strokes; None = no border
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
type).

### Visual style — `border`

`border` is a `f_gui.style.border.Border` — four optional edge `Stroke`s
(top/left/bottom/right). Opt-in: `None` means no border. The renderer
emits per-side CSS (`border-{side}: {width}px {style} {color}`); the old
per-type default borders were removed (appearance is element state, not a
renderer-imposed default). Imported under `TYPE_CHECKING` to keep
`Element` light.

### Methods

```python
def anchor(self, side: Side) -> Point     # connection point on an edge
def path_from_root(self) -> list[Self]    # from HasParent
```

`anchor(side)` returns the mid-point of the named edge (`TOP`/`RIGHT`/
`BOTTOM`/`LEFT`) — the connection point a `Connector` attaches to. It
delegates to `self.bounds.anchor(side)` and reads the `bounds` **property**
(not `_bounds`), so subclasses that compute bounds dynamically (e.g.
`Connector`) stay correct. `Side` is imported under `TYPE_CHECKING` to keep
`Element` light.

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
| `abc.ABC` | Abstract-base marker (declares Element abstract) |
| `f_core.mixins.has.name.HasName` | Name mixin |
| `f_core.mixins.has.parent.HasParent` | Parent-chain mixin |
| `f_ds.geometry.bounds.Bounds` | Rectangular bounds for positioning |

## Usage Example

```python
from f_gui.elements.i_0_element.main import Element
from f_gui.elements.i_1_label.main     import Label
from f_ds.geometry.bounds              import Bounds

issubclass(Element, ABC)        # True — marked abstract

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
subclass and asserts that `Element` is marked abstract
(`issubclass(Element, ABC)`). The `i_1_container` tests use `Label` as
their neutral leaf child (previously a bare `Element`).
