# f_gui.elements

## Purpose

Aggregator package holding the four GUI element classes. Organized with
`i_X_` folders that encode inheritance depth:

| Folder           | Class       | Depth | Role                                |
|------------------|-------------|-------|-------------------------------------|
| `i_0_element/`   | `Element`   | 0     | Base: bounds + name + parent        |
| `i_1_container/` | `Container` | 1     | Element + `HasChildren`             |
| `i_1_label/`     | `Label`     | 1     | Element + text (leaf)               |
| `i_2_window/`    | `Window`    | 2     | Container with implicit full bounds |

## Package Exports

The `__init__.py` is a **lazy aggregator** (PEP 562 `__getattr__`).
Importing one class does not trigger loading of its siblings.

```python
from f_gui.elements import Element, Container, Label, Window
```

Equivalent direct imports (preferred — bypass the aggregator entirely):

```python
from f_gui.elements.i_0_element   import Element
from f_gui.elements.i_1_container import Container
from f_gui.elements.i_1_label     import Label
from f_gui.elements.i_2_window    import Window
```

## Inheritance Graph

```
Element                  i_0_element      (HasName, HasParent)
 ├── Container           i_1_container    (+ HasChildren)
 │    └── Window         i_2_window       (root, full bounds 0-100)
 └── Label               i_1_label        (leaf, text)
```

## Tree-Mutation Contract

`Container` owns the parent/children invariants:

- `add_child(child)` — if `child` already has a parent, detaches it from
  the old parent before attaching to `self`. Re-adding a child already
  owned by `self` is a no-op.
- `remove_child(child)` — removes from children list and clears
  `child.parent`.
- Parent pointer is mutated via `HasParent._set_parent()` — never by
  direct attribute assignment.

## Dependencies

| Import                                   | Purpose                   |
|------------------------------------------|---------------------------|
| `f_core.mixins.has.name.HasName`         | Name mixin                |
| `f_core.mixins.has.parent.HasParent`     | Parent pointer + helper   |
| `f_core.mixins.has.children.HasChildren` | Children list + add/remove|
| `f_ds.geometry.bounds.Bounds`            | Rectangular bounds        |

## Usage Example

```python
from f_gui.elements.i_2_window    import Window
from f_gui.elements.i_1_container import Container
from f_gui.elements.i_1_label     import Label
from f_ds.geometry.bounds         import Bounds

win   = Window.Factory.default()
panel = Container(bounds=Bounds(top=30, left=50, bottom=50, right=70))
hello = Label(bounds=Bounds(top=20, left=10, bottom=40, right=30),
              text='Hello')

win.add_child(child=panel)
panel.add_child(child=hello)

# Reparent: moves hello from panel to win, detaches cleanly.
win.add_child(child=hello)
assert hello.parent is win
assert panel.children == []
```
