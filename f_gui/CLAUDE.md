# f_gui

## Purpose

Lightweight GUI **scene-graph** primitives for the MyPy framework. Provides
four composable classes (`Element`, `Container`, `Label`, `Window`) that model
a tree of rectangular regions in a normalized `0-100` coordinate space.
This package is a *data model* — it does **not** perform rendering.

## Package Exports

The top-level `__init__.py` is a **lazy aggregator** (PEP 562 `__getattr__`)
— importing one class does not trigger loading of its siblings.

```python
from f_gui import Element, Container, Label, Window
```

| Export      | Source module                       | Role                        |
|-------------|-------------------------------------|-----------------------------|
| `Element`   | `f_gui.elements.i_0_element`        | Base: bounds + name + parent|
| `Container` | `f_gui.elements.i_1_container`      | Holds children              |
| `Label`     | `f_gui.elements.i_1_label`          | Leaf with text              |
| `Window`    | `f_gui.elements.i_2_window`         | Root container (full bounds)|

## Module Hierarchy

```
f_gui/
├── __init__.py          lazy aggregator (PEP 562)
├── _run_tests.py        runs every _tester.py under this tree
├── elements/
│   ├── __init__.py      lazy aggregator
│   ├── i_0_element/     Element   (base)
│   ├── i_1_container/   Container (Element + HasChildren)
│   ├── i_1_label/       Label     (Element + text)
│   └── i_2_window/      Window    (Container with implicit full bounds)
└── render/
    ├── __init__.py      lazy aggregator
    └── html/            RenderHtml — emits a self-contained HTML document
```

## Class Hierarchy

```
HasName, HasParent                   (f_core mixins)
 └── Element            i_0_element
      ├── Container     i_1_container (+ HasChildren)
      │    └── Window   i_2_window
      └── Label         i_1_label    (leaf, carries text)
```

## Coordinate System

All bounds are **relative to the parent** in a normalized `0-100` space.

```python
win       = Window.Factory.default()     # (0, 0, 100, 100)
container = Container(bounds=Bounds(top=30, left=50, bottom=50, right=70))
label     = Label(bounds=Bounds(top=20, left=10, bottom=40, right=30),
                  text='Hello')
```
`label.bounds` is relative to `container`, not to `win`.

## Tree-Mutation Semantics

| Operation                          | Result                                         |
|------------------------------------|------------------------------------------------|
| `container.add_child(child)`       | Attaches `child`; auto-detaches from old parent|
| `container.add_child(already_own)` | No-op (no duplication)                         |
| `container.remove_child(child)`    | Detaches and clears `child.parent`             |

Parent-pointer mutation goes through `HasParent._set_parent()` — callers
never touch `child._parent` directly.

## Rendering

```python
win.to_html(path='/tmp/demo.html')      # one-shot HTML file
```
Backed by `f_gui.render.html.RenderHtml` — a stateless emitter. The
`0-100` Bounds model maps 1-to-1 to CSS percentage absolute-positioning,
so the renderer is ~30 lines.

## Running Tests

```bash
python -m f_gui._run_tests
```
Runs every `_tester.py` under `f_gui/` (currently 25 tests, 4 files).

## Dependencies

| Import                                   | Purpose                      |
|------------------------------------------|------------------------------|
| `f_core.mixins.has.name.HasName`         | Name mixin                   |
| `f_core.mixins.has.parent.HasParent`     | Parent-pointer + `_set_parent`|
| `f_core.mixins.has.children.HasChildren` | Children list + add/remove   |
| `f_ds.geometry.bounds.Bounds`            | Rectangular bounds primitive |
| `f_test.TestRunner`                      | Batch test runner            |

## Scope

This package is a **retained-mode scene graph** — it stores structure and
layout metadata only. Rendering, hit-testing, focus management, and input
events are explicitly out of scope.

## See Also

- `ABOUT.html` — full visual architecture overview with diagrams and a
  design review.
