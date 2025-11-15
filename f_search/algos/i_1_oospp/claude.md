# i_1_oospp - One-to-One Shortest Path Problem Algorithms

## Purpose
Contains all algorithm implementations for OOSPP (One-to-One Shortest Path Problem) - finding the shortest path from a single start state to a single goal state on a grid.

## Structure

- **i_0_base/** - `AlgoOOSPP` - Base class for all OOSPP algorithms
- **i_1_astar/** - `AStar` - A* algorithm with Manhattan distance heuristic
- **i_2_dijkstra/** - `Dijkstra` - Dijkstra's algorithm (special case of A* with h=0)

## Problem Type: OOSPP

**One-to-One Shortest Path Problem**
- **Start**: Single start state
- **Goal**: Single goal state
- **Objective**: Find optimal path from start to goal
- **Grid context**: 2D grid-based pathfinding

## Inheritance Hierarchy

```
AlgoSearch[Problem, Solution]
  │
  └─ AlgoOOSPP[ProblemOOSPP, SolutionOOSPP] (i_0_base)
      │
      ├─ AStar (i_1_astar)
      │
      └─ Dijkstra (i_2_dijkstra)
```

## Base Class: AlgoOOSPP

Provides the foundation for all OOSPP algorithms:

### Type Constraints
- **Problem**: Bounded to `ProblemOOSPP` (has start and goal)
- **Solution**: Bounded to `SolutionOOSPP` (contains single path)
- **Stats**: Uses `StatsOOSPP` for metrics

### Inherited Infrastructure
From `AlgoSearch`:
- Core data structures: `_generated`, `_explored`, `_parent`, `_g`, `_h`, `_cost`
- Lifecycle management: `_run_pre()`, `run()`, `_run_post()`
- Statistics tracking

### Specialization
- Refines stats type from `StatsSearch` to `StatsOOSPP`
- Ensures algorithms work with single-goal problems

## Implemented Algorithms

### 1. AStar (i_1_astar)
**Informed search algorithm using heuristic guidance**

**Key Features:**
- Uses Manhattan distance heuristic: |x₁-x₂| + |y₁-y₂|
- Best-first strategy: always expands most promising state (lowest f-value)
- f-value = g + h (actual cost + estimated remaining cost)
- Guaranteed optimal path (heuristic is admissible)

**Performance:**
- Explores fewer states than uninformed search
- Efficiency depends on heuristic quality
- Time: O(b^d), Space: O(b^d) where b=branching factor, d=depth

**When to Use:**
- Goal location is known
- Good heuristic is available
- Want optimal path with minimal exploration

### 2. Dijkstra (i_2_dijkstra)
**Uninformed search algorithm (special case of A*)**

**Key Features:**
- Heuristic always returns 0: h(n) = 0
- f-value = g + 0 = g (pure cost-based)
- Explores states in concentric waves from start
- Guaranteed optimal path (h=0 is admissible)

**Performance:**
- Explores more states than A*
- Time: O(E + V log V), Space: O(V)
- Uniform exploration in all directions

**When to Use:**
- No reliable heuristic available
- Need guaranteed optimal path without heuristic design
- Benchmarking informed search algorithms
- Small search spaces

## Algorithm Comparison

| Aspect | AStar | Dijkstra |
|--------|-------|----------|
| **Heuristic** | Manhattan distance | h = 0 |
| **f-value** | f = g + h | f = g |
| **Search Type** | Informed | Uninformed |
| **States Explored** | Fewer (typically) | More |
| **Optimality** | Yes (if h admissible) | Yes (always) |
| **Heuristic Design** | Required | Not needed |
| **Performance** | Fast with good h | Slower but reliable |

## Common Algorithm Pattern

All OOSPP algorithms follow this pattern:

1. **Initialize**: Add start to Generated with g=0, h=heuristic(start)
2. **Loop**: While Generated not empty:
   - Pop state with lowest f-value
   - If state is goal: reconstruct path, return solution
   - Else: explore state (generate successors)
3. **Explore**: For each successor:
   - Skip if in Explored
   - Calculate g_new = g_current + cost(current, successor)
   - If new or better: update parent, g, h, cost; add/update in Generated
4. **Return**: Solution with path and statistics

## Statistics Tracked

All OOSPP algorithms track:
- **generated**: Total states added to open queue
- **updated**: Total states updated with better cost
- **explored**: Total states fully expanded
- **elapsed**: Algorithm execution time (seconds)

## Solution Type

All algorithms return `SolutionOOSPP` containing:
- **is_valid**: Whether goal was reached
- **path**: Single `Path` object (sequence of states from start to goal)
- **stats**: `StatsOOSPP` object with performance metrics

## Design Rationale

### Why Separate OOSPP?
- **Type Safety**: Ensures algorithms work with single-goal problems
- **Clarity**: Clear distinction from multi-goal algorithms (OMSPP)
- **Optimization**: Can optimize for single-goal case
- **Extensibility**: Easy to add new single-goal algorithms

### Why Dijkstra Extends AStar?
- Code reuse: Dijkstra is literally A* with h=0
- Demonstrates strategy pattern
- Single method override: `_heuristic()` returns 0
- Clean inheritance hierarchy

## Extension Example

To add a new OOSPP algorithm:

```python
class NewAlgo(AlgoOOSPP):
    def run(self) -> SolutionOOSPP:
        # Implement algorithm logic
        pass

    def _heuristic(self, state: State) -> int:
        # Implement heuristic function
        pass

    def _can_terminate(self) -> bool:
        # Implement termination check
        pass
```

## Related Components

- **Problems**: `ProblemOOSPP` (from problems/i_1_oospp)
- **Solutions**: `SolutionOOSPP` (from solutions/i_1_oospp)
- **Stats**: `StatsOOSPP` (from stats/i_1_oospp)
- **Data Structures**: `State`, `Cost`, `Path`, `Generated` (from ds/)
