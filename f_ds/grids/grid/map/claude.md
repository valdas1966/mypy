# GridMap Module

## Overview
The GridMap module provides a 2D grid implementation that uses CellMap objects as its underlying cell type. This module extends the base GridBase class to create grids specifically designed for mapping operations.

## Main Components

### GridMap Class
- **Purpose**: A 2D grid container that holds CellMap cells
- **Base Class**: GridBase[CellMap]
- **Key Features**:
  - Configurable rows and columns
  - Default name "GridMap"
  - Uses CellMap as the cell type
  - Provides valid cell filtering functionality

### Key Methods
- `__init__(rows, cols=None, name='GridMap')`: Initialize grid with specified dimensions
- `cells_valid()`: Returns a View of valid (truthy) cells in the grid

## Dependencies
- `f_ds.grids.grid.base.main.GridBase`: Base grid implementation
- `f_ds.grids.cell.CellMap`: Cell type used in this grid
- `f_ds.groups.view.View`: For filtered cell collections

## Usage
GridMap is typically used when you need a 2D grid structure where each cell can hold mapping data and you need to filter for valid/active cells.