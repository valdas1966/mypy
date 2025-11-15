# AlgoOMSPP - One-to-Many Shortest Path Problem Base Algorithm

## Main Class
`AlgoOMSPP[Problem, Solution]`

## Inheritance
- **Base Classes:** `Generic[Problem, Solution]`, `AlgoSearch[Problem, Solution]`
- **Type Bounds:**
  - `Problem` bounded to `ProblemOMSPP`
  - `Solution` bounded to `SolutionOMSPP`

## Purpose
Specializes the general search algorithm framework for One-to-Many Shortest Path Problems (OMSPP). This class serves as the base for all algorithms that find shortest paths from a single start state to multiple goal states on a grid.

## Functionality from Base Classes
From `AlgoSearch[Problem, Solution]`:
- Core data structures: `_generated`, `_explored`, `_parent`, `_g`, `_h`, `_cost`, `_best`
- Data structure initialization via `_run_pre()`
- Algorithm lifecycle management
- Generic search framework

## Specialized Functionality

### Statistics Type Refinement
The primary specialization in this class is the refinement of the statistics type:
- Narrows `_stats` from generic `StatsSearch` to `StatsOMSPP`
- Provides type safety for multi-goal pathfinding statistics
- Enables per-goal metric tracking

### Key Methods

#### `_run_pre()`
Extends the parent's initialization:
- Calls `super()._run_pre()` to initialize all base data structures
- Sets `_stats` to `StatsOMSPP` type for OMSPP-specific metrics

### Domain Constraint
By constraining the Problem type to `ProblemOMSPP`, this class ensures that algorithms inheriting from it will work with problems that have:
- A single start state (via `HasStart` mixin)
- Multiple goal states (via `HasGoals` mixin)
- Grid-based search space (via `ProblemSearch`)

## Multi-Goal Challenges

OMSPP algorithms must address unique challenges:

1. **Multiple Termination Conditions**: When to stop searching?
   - All goals found? (exhaustive)
   - First goal found? (satisficing)
   - Timeout reached?

2. **Exploration Redundancy**: How to avoid re-exploring shared regions?
   - Naive approach: Independent searches (KxAStar)
   - Sophisticated: Unified search tree

3. **Statistics Tracking**: How to measure performance?
   - Aggregate metrics (total across all goals)
   - Per-goal metrics (individual goal performance)

4. **Solution Validity**: What constitutes success?
   - All goals reached (strict validity)
   - Some goals reached (partial validity)
   - Best-effort results

## Usage Context
- Direct instantiation: Not intended (abstract base class)
- Specialization: Extended by concrete OMSPP algorithms like `KxAStar`
- Role in hierarchy: Bridges the generic search framework and concrete multi-goal algorithms

## Design Rationale
This intermediate class provides a clear separation between:
1. Generic search algorithms (any problem type)
2. Multi-goal search algorithms (OMSPP problems)
3. Concrete algorithm implementations (KxAStar, MultiGoalAStar, etc.)

This design allows for future expansion while maintaining clean type boundaries and enabling algorithm-specific optimizations for multi-goal scenarios.

## Comparison with AlgoOOSPP

| Aspect | AlgoOMSPP (this class) | AlgoOOSPP |
|--------|------------------------|-----------|
| **Goals** | Multiple | Single |
| **Problem Type** | ProblemOMSPP | ProblemOOSPP |
| **Solution Type** | SolutionOMSPP | SolutionOOSPP |
| **Stats Type** | StatsOMSPP | StatsOOSPP |
| **Complexity** | Higher (k goals) | Lower (1 goal) |
| **Per-goal tracking** | Yes | N/A |

## Extension Points

Subclasses should implement:
- **run()**: Main algorithm logic for multi-goal search
- **_heuristic()**: Heuristic function (may need adaptation for multiple goals)
- **_can_terminate()**: Termination condition (e.g., all goals found)
- **_create_solution()**: Aggregate paths and stats into SolutionOMSPP

Optional overrides:
- **_explore()**: Custom exploration for multi-goal
- **_generate()**: Custom generation logic
- **_update_cost()**: Custom cost updates
- **_run_post()**: Custom statistics calculation
