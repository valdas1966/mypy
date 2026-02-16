# HasParent

## Purpose

Mixin for objects that have a parent reference, forming a chain/tree. Provides parent traversal to reconstruct the path from root to the current node.

## Public API

### Class Attributes

```python
Factory = None
```
Factory class for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self, parent: HasParent = None) -> None
```
Stores `parent` as `_parent`.

### Properties

```python
@property
def parent(self) -> HasParent
```
Returns the parent of the object (can be `None`).

### Methods

```python
def path_from_root(self) -> list[HasParent]
```
Walks up the parent chain, then reverses to return root-first order. Returns `[root, ..., self]`.

## Inheritance (Hierarchy)

```
HasParent (plain class, no mixin bases)
```

## Dependencies

| Import | Purpose |
|--------|---------|
| `__future__.annotations` | Postponed evaluation of annotations |

## Usage Example

```python
from f_core.mixins.has.parent import HasParent

a = HasParent.Factory.a()   # ParentWithName(name='A')
b = HasParent.Factory.b()   # ParentWithName(name='B', parent=a)

print(b.parent.name)        # 'A'
print(len(b.path_from_root()))  # 2  (a -> b)
```
