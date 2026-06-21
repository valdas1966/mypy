# f_ds/grids/cell — Grid Cells

## Purpose
Cell classes used as the atoms of 2D grids: a positional base, a
map cell with a validity flag, and a GUI-bearing cell.

## Package Exports
```python
from f_ds.grids.cell import CellBase, CellMap
```
(`CellGui` lives in `gui/` and is imported directly, not via the
aggregator.)

## Module Structure
```
cell/
├── __init__.py     CellBase, CellMap  (lazy ULazy exports)
├── i_0_base/       CellBase — positional + named base
├── i_1_map/        CellMap  — CellBase + mutable validity
└── gui/            CellGui  — CellBase + a GUI widget
```

## Inheritance
```
HasRowCol, HasName
    └── CellBase
          ├── CellMap (+ ValidatableMutable)
          └── CellGui (+ widget: Component)
```

## Dependencies
- `f_core.mixins.has.row_col.HasRowCol`,
  `f_core.mixins.has.name.HasName`
- `f_core.mixins.validatable_mutable.ValidatableMutable` (CellMap)
- `f_gui_old.components.component.Component` (CellGui, legacy GUI)
