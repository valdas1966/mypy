# AlgoOOSPP - One-to-One Shortest Path Problem Base Algorithm

## Main Class
`AlgoOOSPP[Problem, Solution]`

## Inheritance
- **Base Classes:** `Generic[Problem, Solution]`, `AlgoSearch[Problem, Solution]`
- **Type Bounds:**
  - `Problem` bounded to `ProblemOOSPP`
  - `Solution` bounded to `SolutionOOSPP`

## Purpose
Specializes the general search algorithm framework for One-to-One Shortest Path Problems (OOSPP). This class serves as the base for all algorithms that find the shortest path from a single start state to a single goal state on a grid.

## Functionality from Base Classes
From `AlgoSearch[Problem, Solution]`:
- Core data structures: `_generated`, `_explored`, `_parent`, `_g`, `_h`, `_cost`, `_best`
- Data structure initialization via `_run_pre()`
- Algorithm lifecycle management
- Generic search framework

## Specialized Functionality

### Statistics Type Refinement
The primary specialization in this class is the refinement of the statistics type:
- Narrows `_stats` from generic `StatsSearch` to `StatsOOSPP`
- Provides type safety for single-goal pathfinding statistics

### Key Methods

#### `_run_pre()`
Extends the parent's initialization:
- Calls `super()._run_pre()` to initialize all base data structures
- Sets `_stats` to `StatsOOSPP` type for OOSPP-specific metrics

### Domain Constraint
By constraining the Problem type to `ProblemOOSPP`, this class ensures that algorithms inheriting from it will work with problems that have:
- A single start state (via `HasStart` mixin)
- A single goal state (via `HasGoal` mixin)
- Grid-based search space (via `ProblemSearch`)

## Usage Context
- Direct instantiation: Not intended (abstract base class)
- Specialization: Extended by concrete OOSPP algorithms like `AStar` and `Dijkstra`
- Role in hierarchy: Bridges the generic search framework and concrete single-goal algorithms

## Design Rationale
This intermediate class provides a clear separation between:
1. Generic search algorithms (any problem type)
2. Single-goal search algorithms (OOSPP problems)
3. Concrete algorithm implementations (A*, Dijkstra, etc.)

This design allows for future expansion to other problem types (e.g., One-to-Many) while maintaining clean type boundaries.
