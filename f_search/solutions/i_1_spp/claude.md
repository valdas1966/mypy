# SolutionSPP - Solution for One-to-One Shortest Path Problem

## Main Class
`SolutionSPP(SolutionSearch[StatsSPP])`

## Inheritance
- **Base Classes:** `SolutionSearch[StatsSPP]`
- **Type Parameter:** `StatsSPP` (statistics for SPP)

## Purpose
Encapsulates the complete result of solving a One-to-One Shortest Path Problem. Contains validity status, performance statistics, and the solution path from start to goal.

## Functionality from Base Classes

### From SolutionSearch
- `is_valid` property - Solution validity flag
- `stats` property - Performance statistics (StatsSPP)

## Specialized Functionality

### Constructor (`__init__`)
**Parameters:**
- **is_valid**: `bool` - Whether goal was reached
- **stats**: `StatsSPP` - Performance metrics
- **path**: `Path` - Solution path from start to goal

**Implementation:**
```python
SolutionSearch.__init__(self, is_valid=is_valid, stats=stats)
self._path = path
```

**Initializes:**
1. Validity and statistics (via SolutionSearch)
2. Solution path (SPP-specific)

### Path Access

#### `path` property → `Path`
Returns the solution path.

**Type:** `Path` (sequence of states from start to goal)

**Availability:**
- Valid solutions: Contains actual path
- Invalid solutions: May be empty or None

**Usage:**
```python
if solution.is_valid:
    path = solution.path
    states = path.to_iterable()
    print(f"Path length: {len(states)} states")
    print(f"Start: {path.head()}")
    print(f"Goal: {path.tail()}")
```

## Complete Solution Structure

A SolutionSPP contains:

1. **is_valid** (bool): Did we reach the goal?
2. **stats** (StatsSPP): How did we perform?
   - `elapsed`: Total time
   - `generated`: States generated
   - `updated`: States updated
   - `explored`: States explored
3. **path** (Path): What's the route?
   - Sequence of states from start to goal
   - Empty or None if invalid

## Solution Validity

### Valid Solution
```python
SolutionSPP(
    is_valid=True,
    stats=StatsSPP(...),
    path=Path([start, ..., goal])
)
```

**Characteristics:**
- Goal was reached
- Path exists and is complete
- Statistics reflect successful search

### Invalid Solution
```python
SolutionSPP(
    is_valid=False,
    stats=StatsSPP(...),
    path=Path([])  # or None
)
```

**Characteristics:**
- Goal was not reached
- Path is empty or partial
- Statistics reflect failed search attempt

## Usage with Algorithms

### Algorithm Returns Solution
```python
from f_search.algos import AStar
from f_search.problems import ProblemSPP

problem = ProblemSPP(grid, start, goal)
astar = AStar(problem=problem)
solution = astar.run()  # Returns SolutionSPP
```

### Processing Solution
```python
solution: SolutionSPP = astar.run()

if solution.is_valid:
    # Success - process path
    path = solution.path
    print(f"Found path with {len(path.to_iterable())} states")

    # Access specific states
    start_state = path.head()
    goal_state = path.tail()

    # Iterate path
    for state in path.to_iterable():
        print(f"Visit: {state}")

    # Performance metrics
    print(f"Time: {solution.stats.elapsed}s")
    print(f"Generated: {solution.stats.generated} states")
    print(f"Explored: {solution.stats.explored} states")
else:
    # Failure - handle error
    print("No path found!")
    print(f"Explored: {solution.stats.explored} states before giving up")
```

## Path Properties

The path in a valid solution:
- **Starts** at problem's start state: `path.head() == problem.start`
- **Ends** at problem's goal state: `path.tail() == problem.goal`
- **Connected**: Adjacent states are neighbors
- **Valid**: All states are on grid, not obstacles
- **Optimal**: Shortest path (for A*, Dijkstra)

## Statistics (StatsSPP)

Performance metrics included:
- **elapsed**: Algorithm execution time (seconds)
- **generated**: Total states added to open queue
- **updated**: Total states updated with better cost
- **explored**: Total states fully expanded

## Immutability

Solutions are immutable:
- Cannot change `is_valid` after creation
- Cannot modify `stats` after creation
- Cannot replace `path` after creation

Represents final, unchanging result.

## Comparison with SolutionOMSPP

| Aspect | SolutionSPP | SolutionOMSPP |
|--------|--------------|--------------|
| **Problem Type** | One-to-One | One-to-Many |
| **Path(s)** | Single Path | dict[StateBase, Path] |
| **Property** | path | paths |
| **Stats** | StatsSPP | StatsOMSPP |
| **Validity** | Goal reached | All goals reached |

## Example Output

```python
solution = astar.run()

# Valid solution
SolutionSPP(
    is_valid=True,
    stats=StatsSPP(
        elapsed=0.042,
        generated=156,
        updated=23,
        explored=134
    ),
    path=Path([
        StateBase((0,0)), StateBase((1,0)), StateBase((2,0)),
        ...,
        StateBase((10,10))
    ])
)
```

## Common Patterns

### Check Validity First
```python
if solution.is_valid:
    path = solution.path
else:
    print("No solution")
```

### Extract Path Length
```python
if solution.is_valid:
    num_states = len(solution.path.to_iterable())
    num_steps = num_states - 1
```

### Compare Algorithms
```python
sol_astar = AStar(problem).run()
sol_dijkstra = Dijkstra(problem).run()

print(f"A* explored: {sol_astar.stats.explored}")
print(f"Dijkstra explored: {sol_dijkstra.stats.explored}")
```

## Relationship to Other Components

- **Algorithms**: AStar, Dijkstra produce SolutionSPP
- **Problems**: Solve ProblemSPP
- **Statistics**: Contains StatsSPP
- **Path**: Contains Path object
- **States**: Path contains sequence of States

## Design Rationale

### Why Single Path Property?
- SPP has single goal → single path
- Simple, direct interface
- Type-appropriate (Path vs dict[StateBase, Path])

### Why Include Invalid Solutions?
- Algorithms can fail (unreachable goal)
- Statistics useful even for failures
- Explicit failure handling
- Debugging information preserved
