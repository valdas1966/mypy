# f_hs/state — Search States

## Purpose
State classes representing configurations in a search space.

## Module Structure
```
state/
├── __init__.py         StateBase, StateCell
├── i_0_base/           StateBase[Key] — generic base
└── i_1_cell/           StateCell — CellMap for 2D grids
```

## Inheritance
```
HasKey[Key]
  └── StateBase[Key]
        └── StateCell (Key=CellMap)
```
