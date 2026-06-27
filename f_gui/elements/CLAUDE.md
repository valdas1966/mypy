# f_gui.elements

## Purpose

Aggregator package holding the four GUI element classes. Organized with
`i_X_` folders that encode inheritance depth:

| Folder           | Class       | Depth | Role                                |
|------------------|-------------|-------|-------------------------------------|
| `i_0_element/`   | `Element`   | 0     | **Abstract** base: bounds+name+parent; `anchor(side)`|
| `i_1_container/` | `Container` | 1     | Element + `HasChildren`             |
| `i_1_label/`     | `Label`     | 1     | Element + text (leaf)               |
| `i_1_line/`      | `Line`      | 1     | Element + two `PointXY`s + `Stroke` (leaf, SVG)|
| `i_1_connector/` | `Connector` | 1     | Element + two element refs + routing (leaf, SVG)|
| `i_2_window/`    | `Window`    | 2     | Container with implicit full bounds |

`Line` holds a `Stroke`; the `Stroke` / `DashPattern` / `Border` styling
value objects live in **`f_gui.style`** (not here).

## Package Exports

The `__init__.py` is a **lazy aggregator** (PEP 562 `__getattr__` via
`ULazy`). Importing one class does not trigger loading of its siblings.
A `TYPE_CHECKING` mirror block makes the aggregator form resolve in
IDEs / mypy (autocomplete + go-to-definition) while staying lazy at
runtime — so this form is now static-clean, no "unresolved reference":

```python
from f_gui.elements import Element, Container, Label, Line, Connector, Window
```

`Routing` (the connector's `DIRECT`/`ORTHOGONAL` enum) is also exported
from the aggregator. Equivalent direct imports (also valid — bypass the
aggregator entirely):

```python
from f_gui.elements.i_0_element   import Element
from f_gui.elements.i_1_container import Container
from f_gui.elements.i_1_label     import Label
from f_gui.elements.i_1_line      import Line
from f_gui.elements.i_1_connector import Connector, Routing
from f_gui.elements.i_2_window    import Window
```

Styling value objects (`Stroke`, `DashPattern`, `Border`) come from
`f_gui.style`, not from here.

## Inheritance Graph

```
Element                  i_0_element      (HasName, HasParent; anchor(side))
 ├── Container           i_1_container    (+ HasChildren)
 │    └── Window         i_2_window       (root, full bounds 0-100)
 ├── Label               i_1_label        (leaf, text)
 ├── Line                i_1_line         (leaf, two Points; SVG stroke)
 └── Connector           i_1_connector    (leaf, two element refs; SVG, auto-routed)
```

`Connector` attaches to two elements by their `Side` anchors and routes a
straight (`DIRECT`) or 90-degree elbow (`ORTHOGONAL`) path between them,
recomputed live from their bounds. See `i_1_connector/CLAUDE.md`.

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

## Visual Docs (human-facing)

- `ABOUT.html` (this folder) — **interactive** overview: a live, draggable
  scene-graph playground (anchors, DIRECT/ORTHOGONAL routing, connector
  "follow", reparenting) plus the hierarchy, coordinate model, interaction
  matrix, and render pipeline. Links out to each element's page below.
- `i_*/ABOUT.html` — one visual explainer per element (Element, Container,
  Label, Line, Connector, Window). Dark-theme, concept-first ("what is a
  …?"). Generated on demand; Claude reads `CLAUDE.md`, not these.

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
