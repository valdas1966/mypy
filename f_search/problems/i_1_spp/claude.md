# ProblemSPP - One-to-One Shortest Path Problem

## Main Class
`ProblemSPP(ProblemSearch, HasStart, HasGoal)`

## Inheritance
- **Base Classes:**
  - `ProblemSearch` - Grid-based search problem
  - `HasStart` - Provides start state
  - `HasGoal` - Provides goal state

## Purpose
Defines the One-to-One Shortest Path Problem: finding the optimal path from a single start state to a single goal state on a grid. This is the classic pathfinding problem.

## Functionality from Base Classes

### From ProblemSearch
- `grid` property - Access to GridMap
- `successors(state)` - Generate neighbor states

### From HasStart
- `start` property - Access to start state
- `_start` attribute - Start state storage

### From HasGoal
- `goal` property - Access to goal state
- `_goal` attribute - Goal state storage

## Specialized Functionality

### Constructor (`__init__`)
**Parameters:**
- **grid**: `Grid` - The 2D grid map
- **start**: `State` - The start state
- **goal**: `State` - The goal state

**Implementation:**
```python
ProblemSearch.__init__(self, grid=grid)
HasStart.__init__(self, start=start)
HasGoal.__init__(self, goal=goal)
```

**Initializes:**
1. Grid search space (via ProblemSearch)
2. Start state (via HasStart)
3. Goal state (via HasGoal)

## Problem Specification

### Complete Definition
A ProblemSPP fully specifies a pathfinding problem:
1. **Search Space**: GridMap with obstacles
2. **Initial State**: Single start state
3. **Goal Condition**: Reach specific goal state
4. **Actions**: Move to neighboring cells
5. **Objective**: Find optimal (shortest) path

### Problem Instance
```python
problem = ProblemSPP(
    grid=grid_map,
    start=State(key=(0, 0)),
    goal=State(key=(10, 10))
)
```

## Mixin Composition

Uses **compositional inheritance** via multiple mixins:

```
ProblemSPP
    ├─ ProblemSearch (grid + successors)
    ├─ HasStart (start property)
    └─ HasGoal (goal property)
```

This design provides:
- Clean separation of concerns
- Reusable components
- Flexible composition

## Usage with Algorithms

### Compatible Algorithms
- **AStar**: Optimal informed search
- **Dijkstra**: Optimal uninformed search
- Any `AlgoSPP` subclass

### Algorithm Integration
```python
problem = ProblemSPP(grid, start, goal)
algorithm = AStar(problem=problem)
solution = algorithm.run()
```

### Algorithm Queries
Algorithms interact with problem via:
- `problem.grid` - Access grid structure
- `problem.start` - Get initial state
- `problem.goal` - Get target state
- `problem.successors(state)` - Get neighbors

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## Factory Methods

The Factory class provides methods for creating test problems:
- `Factory.without_obstacles()` - Empty grid problems
- `Factory.with_obstacles()` - Problems with obstacles
- Other test case generators

## Relationship to Other Components

- **Algorithms**: `AlgoSPP` (AStar, Dijkstra)
- **Solutions**: `SolutionSPP` (single path)
- **Grid**: `GridMap` (search space)
- **States**: `State` (start, goal, path nodes)

## Comparison with ProblemOMSPP

| Aspect | ProblemSPP | ProblemOMSPP |
|--------|-------------|-------------|
| **Goals** | Single | Multiple |
| **Mixin** | HasGoal | HasGoals |
| **Property** | goal (State) | goals (set[State]) |
| **Algorithms** | AStar, Dijkstra | KxAStar |
| **Solutions** | SolutionSPP | SolutionOMSPP |
| **Complexity** | Simpler | More complex |

## Problem Invariants

Valid ProblemSPP instances satisfy:
1. Start state is valid (not obstacle, within bounds)
2. Goal state is valid (not obstacle, within bounds)
3. Grid is properly formed
4. Start and goal are reachable (not guaranteed, but typical)

## Example Usage

```python
from f_ds.grids import GridMap
from f_search.ds import State
from f_search.problems import ProblemSPP
from f_search.algos import AStar

# Create grid
grid = GridMap(width=20, height=20)

# Define start and goal
start = State(key=(0, 0))
goal = State(key=(19, 19))

# Create problem
problem = ProblemSPP(grid=grid, start=start, goal=goal)

# Solve with A*
astar = AStar(problem=problem)
solution = astar.run()

if solution.is_valid:
    path = solution.path
    print(f"Path found: {path}")
```

## Design Rationale

### Why Separate SPP?
- Type safety: Algorithms can require specific problem type
- Clarity: Distinct from multi-goal problems
- Optimization: Algorithms can exploit single-goal structure
- Simplicity: Simpler interface than multi-goal

### Why Use Mixins?
- Reusability: HasStart/HasGoal used by multiple problem types
- Composition: Flexible feature combination
- Single Responsibility: Each mixin has one purpose
- Extensibility: Easy to add new mixins (e.g., HasConstraints)
