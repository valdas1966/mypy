# i_1_omspp - One-to-Many Shortest Path Problem Algorithms

## Purpose
Contains all algorithm implementations for OMSPP (One-to-Many Shortest Path Problem) - finding shortest paths from a single start state to multiple goal states on a grid.

## Structure

- **i_0_base/** - `AlgoOMSPP` - Base class for all OMSPP algorithms
- **i_1_kx_astar/** - `KxAStar` - Naive K×A* approach (runs A* independently for each goal)

## Problem Type: OMSPP

**One-to-Many Shortest Path Problem**
- **Start**: Single start state
- **Goals**: Multiple goal states (set of states)
- **Objective**: Find optimal paths from start to each goal
- **Grid context**: 2D grid-based multi-destination pathfinding

## Inheritance Hierarchy

```
AlgoSearch[Problem, Solution]
  │
  └─ AlgoOMSPP[ProblemOMSPP, SolutionOMSPP] (i_0_base)
      │
      └─ KxAStar (i_1_kx_astar)
```

## Base Class: AlgoOMSPP

Provides the foundation for all OMSPP algorithms:

### Type Constraints
- **Problem**: Bounded to `ProblemOMSPP` (has start and multiple goals)
- **Solution**: Bounded to `SolutionOMSPP` (contains multiple paths)
- **Stats**: Uses `StatsOMSPP` for metrics

### Inherited Infrastructure
From `AlgoSearch`:
- Core data structures: `_generated`, `_explored`, `_parent`, `_g`, `_h`, `_cost`
- Lifecycle management: `_run_pre()`, `run()`, `_run_post()`
- Statistics tracking

### Specialization
- Refines stats type from `StatsSearch` to `StatsOMSPP`
- Ensures algorithms work with multi-goal problems

## Implemented Algorithms

### KxAStar (i_1_kx_astar)
**Naive approach: K times A* algorithm**

**Strategy:**
Decomposes the OMSPP into k independent OOSPP sub-problems and solves each separately.

**Algorithm Steps:**
1. **Decomposition**: Convert `ProblemOMSPP` → k × `ProblemOOSPP`
   - For each goal in goals: create OOSPP(grid, start, goal)
2. **Independent Solving**: Run A* autonomously for each sub-problem
   - Each A* instance solves one start→goal path
   - No information sharing between runs
3. **Aggregation**: Combine all sub-solutions into `SolutionOMSPP`
   - Collect all paths: `dict[State, Path]` (goal → path)
   - Aggregate statistics: sum counters, collect per-goal metrics

**Key Features:**
- Simple and straightforward implementation
- Each goal solved independently (no optimization across goals)
- Solution valid only if ALL sub-problems have valid solutions
- Tracks both aggregate and per-goal statistics

**Performance:**
- Time: O(k × AStar_time) where k = number of goals
- Space: O(k × AStar_space)
- **Inefficiency**: Overlapping search spaces explored k times
- **No optimization**: Doesn't exploit shared structure

**Statistics Tracked:**
- **Aggregate metrics**: Total generated/updated/explored/elapsed across all runs
- **Per-goal metrics**: Individual stats for each goal
  - `elapsed_per_goal[goal]`: Time for each A* run
  - `generated_per_goal[goal]`: States generated for each goal
  - `updated_per_goal[goal]`: States updated for each goal
  - `explored_per_goal[goal]`: States explored for each goal

**When to Use:**
- Simple baseline for OMSPP problems
- Benchmarking more sophisticated algorithms
- Small number of goals
- Goals are far apart (less overlap)

**Limitations:**
- **Redundant work**: Explores same states multiple times
- **Not optimal**: Overall computational cost not minimized
- **Scalability**: Linear growth with number of goals
- **No synergy**: Doesn't leverage shared search space

## Future OMSPP Algorithms

Potential sophisticated approaches:
- **Multi-goal A***: Single search tree for all goals
- **Incremental A***: Builds on previous solutions
- **Heuristic adaptation**: Custom heuristics for multi-goal
- **Branch-and-bound**: Prunes unpromising paths

## Solution Type

All OMSPP algorithms return `SolutionOMSPP` containing:
- **is_valid**: Whether ALL goals were reached
- **paths**: Dictionary mapping each goal to its path (`dict[State, Path]`)
- **stats**: `StatsOMSPP` object with aggregate and per-goal metrics

## Design Rationale

### Why Separate OMSPP?
- **Different problem structure**: Multi-goal vs single-goal
- **Different solution format**: Multiple paths vs single path
- **Different statistics**: Per-goal tracking needed
- **Different optimization opportunities**: Can leverage shared structure

### Why KxAStar is Naive?
- Simple decomposition approach
- Provides baseline for comparison
- Easy to implement and understand
- Demonstrates problem conversion (OMSPP → k×OOSPP)

### Why Track Per-Goal Stats?
- Understand performance variation across goals
- Identify difficult goals
- Support debugging and optimization
- Enable fine-grained analysis

## Comparison: OMSPP vs OOSPP

| Aspect | OMSPP | OOSPP |
|--------|-------|-------|
| **Goals** | Multiple (k goals) | Single |
| **Solution** | k paths (dict) | 1 path |
| **Stats** | Per-goal + aggregate | Single set |
| **Validity** | All goals reached | Single goal reached |
| **Complexity** | Higher | Lower |
| **Algorithms** | KxAStar, ... | AStar, Dijkstra |

## Extension Example

To add a new OMSPP algorithm:

```python
class MultiGoalAStar(AlgoOMSPP):
    def run(self) -> SolutionOMSPP:
        # Single search tree for all goals
        # Track which goals found
        # Terminate when all goals reached
        pass

    def _heuristic(self, state: State) -> int:
        # Heuristic to nearest unvisited goal
        pass

    def _can_terminate(self) -> bool:
        # Check if all goals reached
        pass
```

## Related Components

- **Problems**: `ProblemOMSPP` (from problems/i_1_omspp)
- **Solutions**: `SolutionOMSPP` (from solutions/i_1_omspp)
- **Stats**: `StatsOMSPP` (from stats/i_1_omspp)
- **Sub-algorithms**: `AStar` (from algos/i_1_oospp/i_1_astar)
- **Sub-problems**: `ProblemOOSPP` (from problems/i_1_oospp)
- **Data Structures**: `State`, `Cost`, `Path`, `Generated` (from ds/)
