# Element

## Purpose

Base class for all GUI elements. Combines `HasName` and `HasParent` mixins to provide identity and tree structure. Each element has rectangular `Bounds` (relative to its parent) that define its position and size within a 0-100 coordinate space.

## Public API

### Class Attributes

```python
Factory: type = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self,
             bounds: Bounds[float] = None,
             name: str = 'Element') -> None
```
Initializes the element with optional bounds (defaults to full `(0, 0, 100, 100)`) and a name.

### Properties

```python
@property
def bounds(self) -> Bounds[float]
```
Returns the bounds of the element (relative to parent).

```python
@property
def parent(self) -> Element | None
```
Inherited from `HasParent`. Returns the parent element, or `None` for root elements.

```python
@property
def name(self) -> str
```
Inherited from `HasName`. Returns the name of the element.

### Methods

```python
def path_from_root(self) -> list[Self]
```
Inherited from `HasParent`. Returns the path from root to this element.

### Dunder Methods

```python
def __str__(self) -> str
```
Returns `'Name(top, left, bottom, right)'` — e.g. `'Element(0, 0, 100, 100)'`.

## Inheritance (Hierarchy)

```
HasName
HasParent
 └── Element
```

| Base | Responsibility |
|------|----------------|
| `HasName` | Provides `name` property and `_name` storage |
| `HasParent` | Provides `parent` property, `_parent` storage, and `path_from_root()` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_core.mixins.has.name.HasName` | Name mixin |
| `f_core.mixins.has.parent.HasParent` | Parent-chain mixin |
| `f_ds.geometry.bounds.Bounds` | Rectangular bounds for positioning |

## Usage Example

```python
from f_gui.elements.i_0_element import Element

# Full-size element (default bounds 0,0,100,100)
full = Element.Factory.full()
print(full.bounds.to_tuple())  # (0, 0, 100, 100)
print(full.name)               # 'Element'
print(full.parent)             # None
print(str(full))               # 'Element(0, 0, 100, 100)'

# Half-size element (centered 25,25,75,75)
half = Element.Factory.half()
print(half.bounds.to_tuple())  # (25, 25, 75, 75)
```
