# Dijkstra - Dijkstra's Shortest Path Algorithm

## Main Class
`Dijkstra(AStar)`

## Inheritance
- **Base Classes:** `AStar`
- **Inherits From:**
  - `AStar`: A* algorithm implementation
  - `AlgoSPP`: SPP-specific algorithm base
  - `AlgoSearch`: Core search data structures
  - `Algo`: Generic algorithm framework

## Purpose
Implements Dijkstra's shortest path algorithm, which is a special case of A* where the heuristic function always returns zero. This makes Dijkstra an uninformed search algorithm that guarantees finding the shortest path by exploring states in order of their actual cost from the start.

## Functionality from Base Classes
From `AStar`:
- Complete A* algorithm implementation
- Core algorithm loop in `run()`
- StateBase exploration via `_explore()`
- StateBase generation via `_generate()`
- Cost updates via `_update_cost()`
- Path reconstruction via `_reconstruct_path()`
- Termination checking via `_can_terminate()`
- All data structures: `_generated`, `_explored`, `_parent`, `_g`, `_h`, `_cost`
- Statistics tracking with GENERATED, UPDATED, EXPLORED counters

## Specialized Functionality

### Heuristic Override

#### `_heuristic(state)` → `0`
The **only** method overridden in this class:
- **Returns:** Always returns 0 (zero heuristic)
- **Effect:** Transforms A* into Dijkstra's algorithm
- **Consequence:** f-value equals g-value (f = g + 0)

### Algorithm Behavior

With h(n) = 0, the algorithm behavior changes:
1. **Priority Queue Ordering:**
   - States ordered purely by actual cost g(n)
   - No heuristic guidance toward goal
2. **Search Pattern:**
   - Explores states in concentric waves from start
   - Uniform expansion in all directions
   - More thorough exploration than A*
3. **Optimality:**
   - Still guarantees shortest path (h=0 is admissible)
   - Explores more states than A* with good heuristic
4. **Completeness:**
   - Will find goal if reachable
   - No risk of heuristic misleading search

## Specialties of Dijkstra's Algorithm

1. **Uninformed Search:** No domain knowledge used (h=0)
2. **Guaranteed Optimality:** Always finds shortest path
3. **Cost-Based Expansion:** Explores in order of increasing cost from start
4. **Uniform Exploration:** Explores all directions equally
5. **Benchmark Algorithm:** Often used as baseline for comparison with informed search

## Comparison with A*

| Aspect | Dijkstra (this class) | A* (parent class) |
|--------|----------------------|-------------------|
| Heuristic | h(n) = 0 | h(n) = Manhattan distance |
| f-value | f(n) = g(n) | f(n) = g(n) + h(n) |
| Search strategy | Uninformed | Informed |
| States explored | More | Fewer (typically) |
| Optimality | Guaranteed | Guaranteed (if h admissible) |
| Use case | Unknown/complex goal | Known single goal |

## Algorithm Complexity
- **Time:** O(E + V log V) with efficient priority queue, O(V²) with simple array
  - V = number of vertices (states)
  - E = number of edges (transitions)
- **Space:** O(V) for storing all states
- **Practical Performance:** Explores more states than A*, but requires no heuristic design

## Usage Context
- **Primary use:** Shortest path when no good heuristic available
- **Problem type:** Single start, single goal (SPP)
- **Grid context:** Works on any weighted graph, including 2D grids
- **Optimality:** Guaranteed for any non-negative edge weights

## Design Pattern
This class demonstrates the **Strategy Pattern** - by simply changing the heuristic function, the entire algorithm behavior changes from informed (A*) to uninformed (Dijkstra) search.

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## When to Use
- No reliable heuristic available for the domain
- Need guaranteed shortest path without heuristic design
- Benchmarking informed search algorithms
- Small search spaces where exploration cost is acceptable
