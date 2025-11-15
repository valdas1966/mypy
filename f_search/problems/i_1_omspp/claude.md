# ProblemOMSPP - One-to-Many Shortest Path Problem

## Main Class
`ProblemOMSPP(ProblemSearch, HasStart, HasGoals)`

## Inheritance
- **Base Classes:**
  - `ProblemSearch` - Grid-based search problem
  - `HasStart` - Provides start state
  - `HasGoals` - Provides multiple goal states (set)

## Purpose
Defines the One-to-Many Shortest Path Problem: finding optimal paths from a single start state to multiple goal states on a grid. This represents multi-destination routing scenarios.

## Functionality from Base Classes

### From ProblemSearch
- `grid` property - Access to GridMap
- `successors(state)` - Generate neighbor states

### From HasStart
- `start` property - Access to start state
- `_start` attribute - Start state storage

### From HasGoals
- `goals` property - Access to goal states (set)
- `_goals` attribute - Goal states storage (set[State])

## Specialized Functionality

### Constructor (`__init__`)
**Parameters:**
- **grid**: `Grid` - The 2D grid map
- **start**: `State` - The single start state
- **goals**: `Iterable[State]` - Multiple goal states

**Implementation:**
```python
ProblemSearch.__init__(self, grid=grid)
HasStart.__init__(self, start=start)
HasGoals.__init__(self, goals=goals)
```

**Note:** Goals are converted to a set by HasGoals mixin

### Problem Decomposition

#### `to_oospps()` → `list[ProblemOOSPP]`
Converts the OMSPP into multiple OOSPP sub-problems.

**Purpose:** Enables decomposition-based solving strategies

**Implementation:**
- For each goal in `self.goals`:
  - Creates `ProblemOOSPP(grid, start, goal)`
  - Appends to list
- Returns list of k sub-problems (k = number of goals)

**Usage:**
```python
omspp = ProblemOMSPP(grid, start, {goal1, goal2, goal3})
oospps = omspp.to_oospps()  # [OOSPP(→goal1), OOSPP(→goal2), OOSPP(→goal3)]
```

**Used by:** KxAStar algorithm for naive decomposition approach

## Problem Specification

### Complete Definition
A ProblemOMSPP fully specifies a multi-goal pathfinding problem:
1. **Search Space**: GridMap with obstacles
2. **Initial State**: Single start state
3. **Goal Condition**: Reach all goal states
4. **Actions**: Move to neighboring cells
5. **Objective**: Find optimal paths to all goals

### Problem Instance
```python
problem = ProblemOMSPP(
    grid=grid_map,
    start=State(key=(0, 0)),
    goals=[State(key=(5, 5)), State(key=(10, 10)), State(key=(15, 15))]
)
```

## Mixin Composition

Uses **compositional inheritance** via multiple mixins:

```
ProblemOMSPP
    ├─ ProblemSearch (grid + successors)
    ├─ HasStart (start property)
    └─ HasGoals (goals property - plural, set-based)
```

## Usage with Algorithms

### Compatible Algorithms
- **KxAStar**: Naive K×A* decomposition approach
- Any `AlgoOMSPP` subclass

### Algorithm Integration
```python
problem = ProblemOMSPP(grid, start, goals)
algorithm = KxAStar(problem=problem)
solution = algorithm.run()
```

### Algorithm Queries
Algorithms interact with problem via:
- `problem.grid` - Access grid structure
- `problem.start` - Get initial state
- `problem.goals` - Get all goal states (set)
- `problem.successors(state)` - Get neighbors
- `problem.to_oospps()` - Decompose into OOSPP (KxAStar)

## Goals as Set

### Why Set Instead of List?
- **No duplicates**: Each goal appears once
- **Order-independent**: Goals have no inherent order
- **Fast membership**: O(1) goal checking
- **Set semantics**: Matches mathematical definition

### Goal Operations
```python
# Check if state is a goal
if state in problem.goals:
    # Goal reached

# Iterate goals
for goal in problem.goals:
    # Process each goal

# Number of goals
k = len(problem.goals)
```

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## Relationship to Other Components

- **Algorithms**: `AlgoOMSPP` (KxAStar)
- **Solutions**: `SolutionOMSPP` (multiple paths)
- **Sub-problems**: Can convert to `ProblemOOSPP` list
- **Grid**: `GridMap` (search space)
- **States**: `State` (start, goals, path nodes)

## Comparison with ProblemOOSPP

| Aspect | ProblemOMSPP | ProblemOOSPP |
|--------|-------------|-------------|
| **Goals** | Multiple (set) | Single |
| **Mixin** | HasGoals | HasGoal |
| **Property** | goals (set[State]) | goal (State) |
| **Algorithms** | KxAStar | AStar, Dijkstra |
| **Solutions** | SolutionOMSPP | SolutionOOSPP |
| **Decomposition** | to_oospps() | N/A |
| **Complexity** | Higher | Lower |

## Problem Challenges

OMSPP introduces unique challenges:
1. **Multiple objectives**: Must reach all goals
2. **Exploration redundancy**: Paths may overlap
3. **Solution structure**: Multiple paths vs single path
4. **Algorithm complexity**: More states to explore

## Problem Invariants

Valid ProblemOMSPP instances satisfy:
1. Start state is valid (not obstacle, within bounds)
2. All goal states are valid
3. Goals set is non-empty
4. Grid is properly formed
5. No goal equals start (typically)

## Example Usage

```python
from f_ds.grids import GridMap
from f_search.ds import State
from f_search.problems import ProblemOMSPP
from f_search.algos import KxAStar

# Create grid
grid = GridMap(width=20, height=20)

# Define start and multiple goals
start = State(key=(0, 0))
goals = [
    State(key=(5, 5)),
    State(key=(15, 5)),
    State(key=(10, 15))
]

# Create problem
problem = ProblemOMSPP(grid=grid, start=start, goals=goals)

# Solve with KxAStar
kx_astar = KxAStar(problem=problem)
solution = kx_astar.run()

if solution.is_valid:
    for goal, path in solution.paths.items():
        print(f"Path to {goal}: {path}")
```

## Decomposition Example

```python
# Convert to multiple OOSPP
omspp = ProblemOMSPP(grid, start, {g1, g2, g3})
oospps = omspp.to_oospps()

# oospps[0] = ProblemOOSPP(grid, start, g1)
# oospps[1] = ProblemOOSPP(grid, start, g2)
# oospps[2] = ProblemOOSPP(grid, start, g3)

# Can solve each independently
for oospp in oospps:
    astar = AStar(problem=oospp)
    solution = astar.run()
```

## Design Rationale

### Why Separate OMSPP?
- **Different structure**: Multiple goals fundamentally different
- **Different algorithms**: Require specialized approaches
- **Different solutions**: Multiple paths vs single path
- **Type safety**: Algorithms can require OMSPP specifically

### Why Provide to_oospps()?
- **Enables decomposition**: Supports naive solving strategies
- **Reuses OOSPP algorithms**: Leverage existing A* implementation
- **Simplifies KxAStar**: Provides sub-problems directly
- **Explicit conversion**: Clear transformation from OMSPP to OOSPP

### Future Algorithm Opportunities
- **Multi-goal A***: Single search tree for all goals
- **Incremental search**: Build on previous solutions
- **Cluster-based**: Group nearby goals
- **Priority-based**: Visit important goals first
