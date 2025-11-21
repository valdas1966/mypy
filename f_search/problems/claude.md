# problems - Problem Definitions for Search Algorithms

## Purpose
Contains problem definitions for grid-based pathfinding. Problems specify the search space (grid), initial configuration (start), and objectives (goal/goals). Problems are organized by type and use mixins for compositional design.

## Structure

### Base Classes
- **i_0_base/** - `ProblemSearch` - Base class for all grid search problems

### Problem Types
- **i_1_spp/** - `ProblemSPP` - One-to-One Shortest Path Problem (start → goal)
- **i_1_omspp/** - `ProblemOMSPP` - One-to-Many Shortest Path Problem (start → goals)

### Compositional Mixins
- **mixins/** - Reusable components for problem features
  - `has_start/` - `HasStart` - Provides start state
  - `has_goal/` - `HasGoal` - Provides single goal state
  - `has_goals/` - `HasGoals` - Provides multiple goal states

## Inheritance Hierarchy

```
ProblemSearch (Grid-based base)
  ├─ ProblemSPP (+ HasStart + HasGoal)
  └─ ProblemOMSPP (+ HasStart + HasGoals)
```

## Base Class: ProblemSearch

Provides foundational functionality for all grid search problems:

### Core Functionality
- **Grid management**: Stores and provides access to the GridMap
- **Successor generation**: Computes neighboring states from current state
- **StateBase space**: Defines valid states as grid cells

### Key Method: `successors(state)`
Returns list of valid successor states (neighbors) for a given state:
- Delegates to `grid.neighbors(cell=state.key)`
- Returns neighboring cells as StateBase objects
- Filters out obstacles automatically (via GridMap)

## Problem Types

### ProblemSPP (One-to-One)
**Single start → Single goal**

**Composition:**
- `ProblemSearch` (grid and successors)
- `HasStart` mixin (start state)
- `HasGoal` mixin (goal state)

**Use Case:**
- Classic pathfinding (navigate from A to B)
- Single destination routing
- Point-to-point navigation

**Algorithms:**
- AStar, Dijkstra

### ProblemOMSPP (One-to-Many)
**Single start → Multiple goals**

**Composition:**
- `ProblemSearch` (grid and successors)
- `HasStart` mixin (start state)
- `HasGoals` mixin (multiple goal states)

**Use Case:**
- Multi-destination routing
- Visiting multiple targets
- Pickup/delivery problems

**Algorithms:**
- KxAStar

**Special Method: `to_spps()`**
Converts OMSPP into list of SPP sub-problems:
- For each goal: creates ProblemSPP(grid, start, goal)
- Enables decomposition-based solving (used by KxAStar)

## Mixin Pattern

Problems use **compositional design** via mixins rather than deep inheritance:

### HasStart Mixin
Provides `start` property (single start state):
- Constructor: `__init__(start: StateBase)`
- Property: `start` → returns `_start`
- Used by: ProblemSPP, ProblemOMSPP

### HasGoal Mixin
Provides `goal` property (single goal state):
- Constructor: `__init__(goal: StateBase)`
- Property: `goal` → returns `_goal`
- Used by: ProblemSPP

### HasGoals Mixin
Provides `goals` property (multiple goal states):
- Constructor: `__init__(goals: Iterable[StateBase])`
- Property: `goals` → returns `_goals` (stored as set)
- Used by: ProblemOMSPP

### Mixin Benefits
1. **Reusability**: Same mixin used by different problem types
2. **Composability**: Mix and match features as needed
3. **Single Responsibility**: Each mixin has one clear purpose
4. **Flexibility**: Easy to create new combinations

## Design Philosophy

### Separation of Concerns
- **Grid**: Defines the physical search space
- **Start/Goal(s)**: Defines the search objective
- **Successors**: Defines legal moves
- **Problem**: Combines all three

### Type Safety
Problems use generic types and bounds:
- Ensures algorithms work with compatible problems
- `AlgoSPP` requires `ProblemSPP`
- `AlgoOMSPP` requires `ProblemOMSPP`

### Immutability
Once created, problems are immutable:
- Grid, start, goal(s) cannot be changed
- Ensures consistency during algorithm execution
- Problems can be safely reused

## Relationship to Other Components

```
Problem ─ provides ─→ Algorithm
   ↓
 Contains:
   - Grid (search space)
   - Start (initial state)
   - Goal(s) (objective)
   ↓
 Generates:
   - Successors (via grid.neighbors)
```

## Factory Pattern

Problem classes include `Factory` class attribute:
- Provides static methods for creating test instances
- Example: `ProblemSPP.Factory.without_obstacles()`
- Enables easy testing and experimentation

## Common Operations

### Creating Problems
```python
# SPP
problem_spp = ProblemSPP(
    grid=grid,
    start=StateBase(key=start_cell),
    goal=StateBase(key=goal_cell)
)

# OMSPP
problem_omspp = ProblemOMSPP(
    grid=grid,
    start=StateBase(key=start_cell),
    goals=[StateBase(key=g) for g in goal_cells]
)
```

### Getting Successors
```python
successors = problem.successors(current_state)
# Returns: list[StateBase] of valid neighbors
```

### Accessing Properties
```python
# Common to all problems
grid = problem.grid

# SPP and OMSPP
start = problem.start

# SPP only
goal = problem.goal

# OMSPP only
goals = problem.goals  # set[StateBase]
```

### Converting OMSPP to SPP
```python
omspp = ProblemOMSPP(grid, start, goals)
spps = omspp.to_spps()  # list[ProblemSPP]
```

## External Dependencies

- **f_ds.grids** - GridMap, CellMap (grid representation)
- **f_cs.problem** - ProblemAlgo (generic problem interface)
- **f_search.ds** - StateBase (state representation)

## Extension Example

To add a new problem type (e.g., Many-to-Many):

```python
class ProblemMMSPP(ProblemSearch, HasStarts, HasGoals):
    """Many starts → Many goals"""
    def __init__(self, grid, starts, goals):
        ProblemSearch.__init__(self, grid=grid)
        HasStarts.__init__(self, starts=starts)
        HasGoals.__init__(self, goals=goals)
```

## Key Properties

1. **Grid-based**: All problems operate on GridMap
2. **StateBase-based**: Uses StateBase abstraction for configurations
3. **Neighbor-based**: Successors are grid neighbors
4. **Obstacle-aware**: GridMap filters obstacles automatically
5. **Type-safe**: Generic bounds ensure algorithm compatibility
6. **Immutable**: Problems don't change after creation
7. **Compositional**: Mixins provide flexible feature combination
