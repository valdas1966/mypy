# ProblemSearch - Base Class for Grid Search Problems

## Main Class
`ProblemSearch(ProblemAlgo)`

## Inheritance
- **Base Classes:** `ProblemAlgo` (from f_cs.problem)

## Purpose
Provides the foundational framework for all search problems operating on 2D grid maps. Defines the search space (grid) and the fundamental operation of generating successor states (neighbors) for pathfinding algorithms.

## Functionality from Base Classes
From `ProblemAlgo`:
- Generic problem interface for algorithms
- Problem lifecycle management
- Abstract problem structure

## Specialized Functionality

### Constructor (`__init__`)
**Parameters:**
- **grid**: `GridMap` - The 2D grid defining the search space

**Storage:**
- `_grid`: Internal reference to the GridMap

**Purpose:** Establishes the physical search space for pathfinding

### Grid Access

#### `grid` property → `Grid`
Returns the problem's GridMap.

**Usage:** Algorithms access the grid to query structure, check obstacles, etc.

### Successor Generation

#### `successors(state: StateBase)` → `list[StateBase]`
Core method that defines the search space connectivity.

**Purpose:** Returns all valid successor states from a given state

**Implementation:**
1. Extracts cell from state: `cell = state.key`
2. Gets neighbors from grid: `cells = grid.neighbors(cell)`
3. Wraps neighbors as States: `states = [StateBase(key=cell) for cell in cells]`
4. Returns list of successor states

**Behavior:**
- Delegates to `GridMap.neighbors()` for actual neighbor computation
- GridMap automatically filters out obstacles
- Typically returns 4 neighbors (up, down, left, right) for 2D grids
- Fewer neighbors at grid boundaries or near obstacles

**Usage:**
```python
current_state = StateBase(key=cell_5_3)
successors = problem.successors(current_state)
# Returns: [StateBase((4,3)), StateBase((6,3)), StateBase((5,2)), StateBase((5,4))]
```

## Grid-Based Search Space

### Search Space Definition
- **States**: Grid cells wrapped as StateBase objects
- **Actions**: Moves to neighboring cells
- **Transitions**: StateBase → List[StateBase] via successors()
- **Obstacles**: Automatically filtered by GridMap

### StateBase Representation
States are grid positions:
- **Key**: Cell coordinates (e.g., (x, y))
- **Validity**: Determined by GridMap (not obstacles)
- **Connectivity**: Defined by grid neighbor structure

## Design Philosophy

### Minimal Base Class
ProblemSearch provides only essential grid functionality:
- Grid storage and access
- Successor generation
- Leaves start/goal specification to subclasses

### Delegation Pattern
Core operations delegate to GridMap:
- **Neighbor finding**: `grid.neighbors()`
- **Obstacle checking**: Handled by GridMap
- **Boundary checking**: Handled by GridMap

This keeps ProblemSearch simple and focused.

### Template for Specialization
Subclasses add specific problem structure:
- SPP: adds start + goal
- OMSPP: adds start + goals
- Future: could add starts + goals, constraints, etc.

## Relationship to Other Classes

- **GridMap**: Provides the physical search space
- **StateBase**: Represents configurations (grid cells)
- **AlgoSearch**: Consumes problems, calls successors()
- **ProblemSPP/OMSPP**: Extend with start/goal(s)

## Usage Context

- **Direct instantiation**: Not typical (too generic)
- **Specialization**: Extended by ProblemSPP, ProblemOMSPP
- **Role in hierarchy**: Root problem class for grid search

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## External Dependencies

- **f_ds.grids**:
  - `GridMap` (alias `Grid`) - 2D grid structure
  - `CellMap` (alias `Cell`) - Grid cell coordinates
- **f_cs.problem**:
  - `ProblemAlgo` - Generic problem interface
- **f_search.ds**:
  - `StateBase` - StateBase wrapper

## Key Properties

1. **Grid-centric**: Everything revolves around the GridMap
2. **StateBase abstraction**: Uses StateBase wrapper for grid cells
3. **Neighbor-based**: Successors are grid neighbors
4. **Obstacle-aware**: Invalid cells automatically filtered
5. **Generic base**: Doesn't specify start/goal
6. **Simple delegation**: Relies on GridMap for core operations
