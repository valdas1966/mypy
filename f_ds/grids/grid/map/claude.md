# GridMap

## Purpose

2D grid of `CellMap` cells where each cell can be valid or invalid (obstacles). Extends `GridBase[CellMap]` with map-specific operations: valid-cell filtering, neighbor queries respecting validity, random cell selection, obstacle invalidation, and analytic reporting.

## Public API

### Class Attributes

```python
Factory: type = None
From: type = None
```
Factory and From classes for creating instances. Attached via `__init__.py`.

### Constructor

```python
def __init__(self,
             rows: int,
             cols: int = None,
             name: str = 'GridMap',
             domain: str = None) -> None
```
Creates a grid with the given dimensions. If `cols` is `None`, the grid is square. Optionally assigns a domain label.

### Properties

```python
@property
def domain(self) -> str
```
Returns the domain label of the grid.

```python
@property
def random(self) -> Random
```
Returns the `Random` helper object for sampling cells.

### Methods

```python
def cells_valid(self) -> list[Cell]
```
Returns a list of all valid (truthy) cells in the grid.

```python
def neighbors(self, cell: Cell) -> list[Cell]
```
Returns valid neighbors of the given cell (filters out invalid cells).

```python
def invalidate(self, cells: list[Cell]) -> None
```
Marks the given cells as invalid (obstacles).

```python
def to_analytics(self) -> dict
```
Returns a dict of analytic values for reporting: `domain`, `map` (name), `rows`, `cols`, `cells` (count of valid cells).

```python
def print(self) -> str
```
Returns a string representation of the grid in `[0,1]` 2D-bool format with a title header.

### Dunder Methods

```python
def __len__(self) -> int
```
Returns the total number of valid cells in the grid.

```python
def __str__(self) -> str
```
Returns `'GridMap(3x3, 5)'` — name, dimensions, valid cell count.

```python
def __repr__(self) -> str
```
Returns `'<GridMap: Name=GridMap, Shape=3x3, Cells=5>'`.

```python
def __iter__(self) -> Iterator[Cell]
```
Iterates over valid cells only.

## Inheritance (Hierarchy)

```
HasName, HasRowsCols, Iterable, Generic[Cell]
 └── GridBase[Cell]
      └── GridMap  (Cell = CellMap)
```

| Base | Responsibility |
|------|----------------|
| `HasName` | Provides `name` property |
| `HasRowsCols` | Provides `rows`, `cols` properties |
| `Iterable` | Makes the grid iterable |
| `GridBase[Cell]` | 2D cell storage, indexing (`grid[r][c]`), base neighbor logic, `shape()`, `select` |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_ds.grids.grid.base.main.GridBase` | Base grid implementation |
| `f_ds.grids.cell.CellMap` | Cell type with valid/invalid state |
| `f_ds.grids.grid.map._random.Random` | Random cell sampling helper |
| `typing.Iterator` | Type hint for `__iter__` |

## Usage Examples

### Create and query

```python
from f_ds.grids.grid.map import GridMap

grid = GridMap(rows=3, name='Tel-Aviv', domain='city')
print(len(grid))           # 9 (all valid)
print(grid.cells_valid())  # list of 9 CellMap objects
```

### Using the Factory

```python
from f_ds.grids.grid.map import GridMap

grid = GridMap.Factory.x()        # 3x3 X-shaped grid (5 valid)
print(str(grid))                  # GridMap(3x3, 5)
print(grid.neighbors(grid[1][1])) # valid neighbors of center cell
```

### Analytics reporting

```python
from f_ds.grids.grid.map import GridMap

grid = GridMap(rows=4, cols=4, name='Arena', domain='game')
analytics = grid.to_analytics()
# {'domain': 'game', 'map': 'Arena', 'rows': 4, 'cols': 4, 'cells': 16}
```

### From file or array

```python
from f_ds.grids.grid.map import GridMap
import numpy as np

array = np.array([[True, False], [True, True]])
grid = GridMap.From.array(array, name='small')
print(len(grid))  # 3
```
