# Grid Base Module

This module provides the foundational `GridBase` class - a generic 2D grid data structure that can hold any type of cell.

## Key Components

### GridBase Class (`main.py`)
- **Purpose**: Generic 2D grid container that holds cells in a rows×cols structure
- **Type**: Generic class `GridBase[Cell]` where `Cell` must inherit from `CellBase`
- **Key Features**:
  - Iterable (flattens grid when iterating)
  - Indexable via `grid[row][col]` syntax
  - Can be converted to Group via `to_group()`
  - Supports naming and has rows/cols properties
  - Uses Factory pattern for common configurations

### FactoryGridBase (`_factory.py`)
- **Purpose**: Factory class for creating common grid configurations
- **Current Methods**: 
  - `grid_3x3()` - creates a 3×3 grid
- **Usage**: `GridBase.Factory.grid_3x3()`

### Tests (`_tester.py`)
- Comprehensive unit tests covering length, iteration, grouping, and indexing functionality

## Usage Examples

```python
# Create a custom grid
grid = GridBase(rows=5, cols=5, name="my_grid")

# Create using factory
grid = GridBase.Factory.grid_3x3()

# Access cells
cell = grid[1][2]  # row 1, col 2

# Iterate over all cells
for cell in grid:
    print(f"Cell at {cell.row}, {cell.col}")

# Convert to group
group = grid.to_group("grid_cells")
```

## Dependencies
- `f_core.mixins.has_name.HasName` - for naming capability
- `f_core.mixins.has_rows_cols.HasRowsCols` - for dimension management
- `f_ds.mixins.groupable.Groupable` - for grouping functionality
- `f_ds.grids.cell.CellBase` - base cell type

## Architecture Notes
- This is a foundational class in the grid system hierarchy
- Uses composition pattern with mixins for functionality
- Generic design allows for different cell types while maintaining type safety
- Factory pattern provides convenient constructors for common configurations