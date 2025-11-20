# AStar - A* Pathfinding Algorithm

## Main Class
`AStar(AlgoSPP)`

## Inheritance
- **Base Classes:** `AlgoSPP[ProblemSPP, SolutionSPP]`
- **Inherits From:**
  - `AlgoSPP`: SPP-specific algorithm base
  - `AlgoSearch`: Core search data structures and lifecycle
  - `Algo`: Generic algorithm framework

## Purpose
Implements the A* (A-star) pathfinding algorithm, one of the most widely-used informed search algorithms. A* finds the optimal shortest path from a start state to a goal state by using both actual cost (g-value) and heuristic estimation (h-value) to guide the search.

## Functionality from Base Classes
From `AlgoSPP` and `AlgoSearch`:
- `_generated`: Priority queue of open states
- `_explored`: Set of closed states
- `_parent`: Parent pointers for path reconstruction
- `_g`: Actual costs from start
- `_h`: Heuristic estimates to goal
- `_cost`: Combined Cost objects for priority ordering
- `_best`: Current state being processed
- `_stats`: StatsSPP metrics tracker

## Specialized Functionality

### Algorithm Implementation

#### Core Algorithm Loop (`run()`)
The main execution method implementing the A* algorithm:
1. **Initialization:**
   - Calls `_run_pre()` to set up data structures
   - Adds start state to generated queue with g=0, h=heuristic(start)
2. **Search Loop:**
   - Pops state with lowest f-value (g+h) from generated queue
   - Checks termination condition via `_can_terminate()`
   - If goal found: reconstructs path and creates solution
   - If not goal: explores state by generating successors
3. **Post-processing:**
   - Calls `_run_post()` to finalize statistics
   - Returns `SolutionSPP` with validity flag, path, and stats

#### State Exploration (`_explore()`)
Expands the current best state:
- Increments EXPLORED counter in stats
- Adds state to explored set
- Gets successors from problem instance
- For each successor, calls `_generate()`

#### State Generation (`_generate()`)
Handles new or updated states:
- Skips states in explored set
- Calculates new g-value: `g[best] + cost(best, successor)`
- **If state not in generated queue:**
  - Increments GENERATED counter
  - Updates parent, g, h, and cost
  - Adds to generated queue
- **If state already in generated queue with higher cost:**
  - Increments UPDATED counter
  - Updates parent, g, h, and cost
  - Updates state in generated queue

#### Heuristic Function (`_heuristic()`)
Returns Manhattan distance to goal:
- Formula: `|x1 - x2| + |y1 - y2|`
- Admissible and consistent heuristic for grid-based pathfinding
- Ensures optimality of found path

#### Cost Update (`_update_cost()`)
Updates all cost-related data for a state:
- Sets parent pointer
- Sets g-value
- Calculates and sets h-value via `_heuristic()`
- Creates Cost object with (key, g, h, is_cached=False, is_bounded=False)
- Stores Cost in `_cost` dictionary

#### Termination Check (`_can_terminate()`)
Returns True if current best state is the goal state

#### Path Reconstruction (`_reconstruct_path()`)
Traces path from goal back to start:
- Follows parent pointers from best (goal) state
- Creates Path object from reversed state sequence
- Returns Path wrapped in list

#### Post-processing (`_run_post()`)
Finalizes statistics after algorithm completion

#### Solution Creation (`_create_solution()`)
Creates the final solution object:
- Combines validity flag, statistics, and path
- Returns `SolutionSPP` instance

### Metrics Tracked
Uses counter system to track:
- **GENERATED**: Number of new states added to open queue
- **UPDATED**: Number of states re-added with better cost
- **EXPLORED**: Number of states fully expanded

## Specialties of A* Algorithm

1. **Informed Search:** Uses heuristic to guide search toward goal
2. **Optimality:** Guarantees shortest path when heuristic is admissible
3. **Efficiency:** Explores fewer states than uninformed search (e.g., Dijkstra)
4. **Best-First Strategy:** Always expands most promising state (lowest f-value)
5. **Dynamic Programming:** Maintains optimal costs and updates when better paths found

## Algorithm Complexity
- **Time:** O(b^d) where b is branching factor, d is solution depth
- **Space:** O(b^d) for storing generated and explored sets
- **Practical Performance:** Depends heavily on heuristic quality

## Usage Context
- Primary use: Finding optimal shortest paths on 2D grids
- Problem type: Single start, single goal (SPP)
- Heuristic: Manhattan distance (L1 norm)
- Optimality: Guaranteed for grid-based pathfinding

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)
