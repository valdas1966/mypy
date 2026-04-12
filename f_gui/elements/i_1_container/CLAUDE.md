# Container

## Purpose

Element that can hold child `Element`s. Owns the parent/children
invariants: adding a child auto-detaches it from its previous parent;
removing a child clears its parent pointer.

## Public API

### Class Attributes

```python
Factory: type = None
```

### Constructor

```python
def __init__(self,
             bounds: Bounds[float] = None,
             name: str = 'Container') -> None
```
Bounds default to full `(0, 0, 100, 100)`.

### Methods

```python
def add_child(self, child: Element) -> None
```
Attaches `child` to this container.
- If `child` already has another parent, it is detached from that parent first.
- If `child` is already owned by `self`, the call is a no-op (no duplication).
- Sets `child.parent = self` via `HasParent._set_parent()`.

```python
def remove_child(self, child: Element) -> None
```
Removes `child` from this container's children and clears
`child.parent` (via `_set_parent(None)`). Raises `ValueError` if `child`
is not in the list.

### Inherited

`children`, `bounds`, `name`, `parent`, `path_from_root()`, `__str__`.

## Inheritance (Hierarchy)

```
Element (HasName, HasParent)
 └── Container (+ HasChildren)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_gui.elements.i_0_element.Element` | Parent class |
| `f_core.mixins.has.children.HasChildren` | Children list + add/remove |
| `f_ds.geometry.bounds.Bounds` | Rectangular bounds |

## Usage Example

```python
from f_gui.elements.i_1_container import Container
from f_gui.elements.i_1_label     import Label
from f_ds.geometry.bounds         import Bounds

panel = Container.Factory.full()
label = Label(bounds=Bounds(top=10, left=10, bottom=30, right=40),
              text='Hi')

panel.add_child(child=label)
assert label.parent is panel
assert panel.children == [label]

# Reparent to another container — old link is cleaned up automatically.
other = Container.Factory.half()
other.add_child(child=label)
assert label.parent is other
assert panel.children == []

# Remove explicitly — parent pointer is cleared.
other.remove_child(child=label)
assert label.parent is None
```

## Factory Presets

| Method   | Bounds            | Notes                                  |
|----------|-------------------|----------------------------------------|
| `full()` | `(0, 0, 100, 100)`| Spans entire parent                    |
| `half()` | `(25,25,75,75)`   | Reuses `Bounds.Factory.half()`         |
