# algos - Search Algorithm Implementations

## Purpose
Contains all search algorithm implementations for solving pathfinding problems on 2D grids. Algorithms are organized hierarchically by problem type (OOSPP vs OMSPP) with shared base classes providing common infrastructure.

## Structure

### Base Classes
- **i_0_base/** - `AlgoSearch` - Root algorithm class with core data structures and lifecycle

### OOSPP Algorithms (One-to-One)
- **i_1_oospp/** - Algorithms for single start, single goal problems
  - `i_0_base/` - `AlgoOOSPP` - Base for OOSPP algorithms
  - `i_1_astar/` - `AStar` - A* with Manhattan heuristic
  - `i_2_dijkstra/` - `Dijkstra` - Uninformed search (h=0)

### OMSPP Algorithms (One-to-Many)
- **i_1_omspp/** - Algorithms for single start, multiple goals problems
  - `i_0_base/` - `AlgoOMSPP` - Base for OMSPP algorithms
  - `i_1_kx_astar/` - `KxAStar` - Naive approach (runs A* k times)

## Inheritance Hierarchy

```
AlgoSearch (Generic base - i_0_base)
  │
  ├─ AlgoOOSPP (One-to-One base - i_1_oospp/i_0_base)
  │   ├─ AStar (A* algorithm - i_1_oospp/i_1_astar)
  │   └─ Dijkstra (Dijkstra algorithm - i_1_oospp/i_2_dijkstra)
  │
  └─ AlgoOMSPP (One-to-Many base - i_1_omspp/i_0_base)
      └─ KxAStar (K times A* - i_1_omspp/i_1_kx_astar)
```

## Core Algorithm Infrastructure (AlgoSearch)

All algorithms inherit from `AlgoSearch` which provides:

### Data Structures
- **_generated**: Priority queue (`Generated`) of states awaiting exploration (open list)
- **_explored**: Set of states that have been fully processed (closed list)
- **_parent**: Dictionary mapping each state to its predecessor
- **_g**: Dictionary of g-values (actual cost from start)
- **_h**: Dictionary of h-values (heuristic estimates to goal)
- **_cost**: Dictionary mapping states to `Cost` objects (for priority ordering)
- **_best**: Reference to current state being evaluated
- **_stats**: Statistics tracker (`StatsSearch`)

### Lifecycle Methods
- **_run_pre()**: Initialize all data structures before execution
- **run()**: Main algorithm logic (implemented by subclasses)
- **_run_post()**: Finalize statistics after completion
- **_create_solution()**: Build solution object

## Algorithm Comparison

| Algorithm | Type | Heuristic | Completeness | Optimality | Use Case |
|-----------|------|-----------|--------------|------------|----------|
| AStar | Informed | Manhattan | Yes | Yes | Known goal location |
| Dijkstra | Uninformed | h=0 | Yes | Yes | No heuristic available |
| KxAStar | Composite | Manhattan | Yes | Yes | Multiple goals (naive) |

## Common Algorithm Flow

1. **Initialization** (_run_pre):
   - Create empty Generated queue
   - Create empty Explored set
   - Initialize parent, g, h, cost dictionaries
   - Add start state to Generated with g=0, h=heuristic(start)

2. **Main Loop** (run):
   - Pop state with lowest f-value from Generated
   - Check if goal reached (termination condition)
   - If goal: reconstruct path, create solution
   - If not goal: explore state (generate successors)

3. **State Exploration** (_explore):
   - Add state to Explored set
   - Get successors from problem
   - For each successor, call _generate()

4. **State Generation** (_generate):
   - Skip if in Explored
   - Calculate new g-value: g[parent] + cost(parent, successor)
   - If new state: add to Generated
   - If existing state with worse cost: update in Generated

5. **Finalization** (_run_post):
   - Calculate final statistics
   - Return solution with path(s) and stats

## Performance Metrics

All algorithms track:
- **GENERATED**: Number of states added to open queue
- **UPDATED**: Number of states updated with better cost
- **EXPLORED**: Number of states fully expanded
- **Elapsed time**: Algorithm execution duration

## Design Patterns

### Template Method Pattern
Base classes define the algorithm structure; subclasses fill in specific steps:
- `AlgoSearch` provides infrastructure
- `AlgoOOSPP`/`AlgoOMSPP` specialize for problem types
- Concrete algorithms implement specific logic (heuristics, termination, etc.)

### Strategy Pattern
Different algorithms implement the same interface with different strategies:
- AStar uses Manhattan heuristic
- Dijkstra uses zero heuristic
- KxAStar decomposes into multiple AStar runs

## Type Safety

Algorithms use generic type parameters for compile-time safety:
- `AlgoSearch[Problem, Solution]`
- `AlgoOOSPP[ProblemOOSPP, SolutionOOSPP]`
- `AlgoOMSPP[ProblemOMSPP, SolutionOMSPP]`

## Extension Points

To add a new algorithm:
1. Determine problem type (OOSPP or OMSPP)
2. Extend appropriate base class (`AlgoOOSPP` or `AlgoOMSPP`)
3. Implement required methods:
   - `run()` - Main algorithm logic
   - `_heuristic()` - Heuristic function (if applicable)
   - `_can_terminate()` - Goal check (if applicable)
4. Override optional methods as needed:
   - `_explore()` - Custom exploration logic
   - `_generate()` - Custom generation logic
   - `_update_cost()` - Custom cost updates

## File Organization

Each algorithm folder contains:
- `__init__.py` - Exports main class
- `main.py` - Algorithm implementation
- `_factory.py` - Factory methods for testing (optional)
- `_tester.py` - Unit tests (optional)
- `claude.md` - Documentation
