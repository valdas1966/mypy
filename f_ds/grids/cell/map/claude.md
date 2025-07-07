# Cell Map Module

## Overview
The `f_ds/grids/cell/map` module provides a specialized cell implementation for 2D grid maps. It extends the base cell functionality with validation capabilities.

## Components

### CellMap Class
- **Purpose**: Represents a cell in a 2D grid map with validation support
- **Inheritance**: Inherits from `CellBase` and `ValidatablePublic`
- **Key Features**:
  - Position tracking (row, col)
  - Validity state management
  - Customizable naming

### Factory Class
- **Purpose**: Factory class for creating CellMap instances
- **Methods**:
  - `zero()`: Creates a CellMap at position (0, 0)

## Usage

```python
from f_ds.grids.cell.map import CellMap

# Create a cell at specific position
cell = CellMap(row=5, col=3, is_valid=True, name="MyCell")

# Create a cell at origin using factory
origin_cell = CellMap.Factory.zero()
```

## Architecture
- Follows the factory pattern for object creation
- Implements validation through mixins
- Part of the larger grid system architecture