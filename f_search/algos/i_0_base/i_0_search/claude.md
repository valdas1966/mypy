# AlgoSearch - Base Search Algorithm

## Main Class
`AlgoSearch[Problem, Solution]`

## Inheritance
- **Base Classes:** `Generic[Problem, Solution]`, `Algo[Problem, Solution]` (from f_cs.algo)
- **Type Bounds:**
  - `Problem` bounded to `ProblemSearch`
  - `Solution` bounded to `SolutionSearch`

## Purpose
Provides the foundational framework for all search algorithms in the f_search project. This is the abstract base class that establishes the core data structures and lifecycle methods needed by any pathfinding algorithm operating on grid-based search spaces.

## Functionality from Base Classes
From `Algo[Problem, Solution]`:
- Algorithm lifecycle management with run hooks
- Problem instance management
- Generic type system for problem-solution pairs

## Specialized Functionality

### Core Data Structures
This class initializes and manages the essential data structures used by all search algorithms:

- **`_generated`**: Priority queue (`Generated`) of states awaiting exploration (open list)
- **`_explored`**: Set of states that have been fully processed (closed list)
- **`_parent`**: Dictionary mapping each state to its predecessor in the search tree
- **`_g`**: Dictionary of g-values (actual cost from start to each state)
- **`_h`**: Dictionary of h-values (heuristic estimates from state to goal)
- **`_cost`**: Dictionary mapping states to their `Cost` objects (for priority ordering)
- **`_best`**: Reference to the current best state being evaluated
- **`_stats`**: Statistics tracker of type `StatsSearch`

### Key Methods

#### `_run_pre()`
Pre-execution hook that initializes all data structures before the algorithm runs:
- Creates empty `Generated` queue for open states
- Creates empty set for explored states
- Initializes parent tracking dictionary
- Initializes g-value, h-value, and cost dictionaries
- Resets best state to None
- Initializes statistics object

### Design Pattern
This class uses the Template Method pattern, providing the infrastructure while leaving concrete search logic to derived classes. Subclasses like `AlgoSPP` and specific algorithms (A*, Dijkstra) build upon this foundation.

## Usage Context
- Direct instantiation: Not intended (abstract base class)
- Specialization: Extended by `AlgoSPP` for single-goal problems
- Role in hierarchy: Root algorithm class for all grid search implementations
