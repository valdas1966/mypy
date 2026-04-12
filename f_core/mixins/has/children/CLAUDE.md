# HasChildren

## Purpose
1. Mixin for objects that have children, forming a one-to-many relationship.
2. Provides a children list and `add_child()` method.
3. Generic and reusable across any domain (GUI, trees, org structures, etc.).

## Public API

### Class Attribute
```python
Factory: type = None
```
1. Factory for creating test instances. Wired via `__init__.py`.

### Constructor
```python
def __init__(self) -> None
```
1. Initializes an empty `_children` list.

### Properties
```python
@property
def children(self) -> list[Self]
```
1. Returns the list of children.

### Methods
```python
def add_child(self, child: Self) -> None
```
1. Appends a child to the children list.

```python
def remove_child(self, child: Self) -> None
```
1. Removes the child from the children list.
2. Raises `ValueError` if the child is not present.

## Inheritance (Hierarchy)

```
HasChildren (plain class, no mixin bases)
```

## Dependencies

| Import                   | Purpose                            |
|--------------------------|------------------------------------|
| `__future__.annotations` | Postponed annotation evaluation    |
| `typing.Self`            | Self-type for children and add_child |

## Usage Example

```python
from f_core.mixins.has.children import HasChildren

empty = HasChildren.Factory.empty()
print(empty.children)           # []

parent = HasChildren.Factory.with_two()
print(len(parent.children))     # 2

child = HasChildren()
empty.add_child(child=child)
print(len(empty.children))      # 1
```
