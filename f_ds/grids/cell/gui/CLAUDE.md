# CellGui

## Purpose
A grid cell that carries a GUI widget for rendering. Extends
`CellBase` with a `widget`; the cell's `name` is taken from the
widget's name.

## Public API

### Constructor
```python
def __init__(self, row: int, col: int, widget: Component) -> None
```
`name` is set to `widget.name`.

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `widget` | `Component` | The displayed widget |

### Inherited from `CellBase`
`key` (`(row, col)`), `row`, `col`, `rc`, `distance`, `name`,
`__str__`, `__repr__`, and the `HasRowCol`/`HasName` surface.

## Inheritance
```
CellBase
    └── CellGui
```

## Dependencies
- `f_ds.grids.cell.i_0_base.CellBase`
- `f_gui_old.components.component.Component` (legacy GUI layer)

## Usage
```python
from f_ds.grids.cell.gui.gui import CellGui

cell = CellGui(row=0, col=0, widget=some_component)
cell.widget   # -> Component
```
