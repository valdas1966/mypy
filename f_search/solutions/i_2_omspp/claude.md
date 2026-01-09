# SolutionOMSPP - Solution for One-to-Many Shortest Path Problem

## Main Class
`SolutionOMSPP(SolutionSearch[StatsOMSPP])`

## Inheritance
- **Base Classes:** `SolutionSearch[StatsOMSPP]`
- **Type Parameter:** `StatsOMSPP` (statistics for OMSPP)

## Purpose
Encapsulates the complete result of solving a One-to-Many Shortest Path Problem. Contains validity status, performance statistics, and solution paths from start to each goal.

## Functionality from Base Classes

### From SolutionSearch
- `is_valid` property - Solution validity flag
- `stats` property - Performance statistics (StatsOMSPP)

## Specialized Functionality

### Constructor (`__init__`)
**Parameters:**
- **is_valid**: `bool` - Whether ALL goals were reached
- **stats**: `StatsOMSPP` - Performance metrics (aggregate + per-goal)
- **paths**: `dict[StateBase, Path]` - Mapping from each goal to its path

**Implementation:**
```python
SolutionSearch.__init__(self, is_valid=is_valid, stats=stats)
self._paths = paths
```

**Initializes:**
1. Validity and statistics (via SolutionSearch)
2. Paths dictionary (OMSPP-specific)

### Paths Access

#### `paths` property → `dict[StateBase, Path]`
Returns the dictionary of paths.

**Type:** `dict[StateBase, Path]` where:
- **Key**: Goal state
- **Value**: Path from start to that goal

**Availability:**
- Valid solutions: Contains paths for all goals
- Invalid solutions: May contain partial paths or be empty

**Usage:**
```python
if solution.is_valid:
    for goal, path in solution.paths.items():
        states = path.to_iterable()
        print(f"Path to {goal}: {len(states)} states")
```

## Complete Solution Structure

A SolutionOMSPP contains:

1. **is_valid** (bool): Did we reach ALL goals?
2. **stats** (StatsOMSPP): How did we perform?
   - **Aggregate**: Total elapsed, generated, updated, explored
   - **Per-goal**: Individual metrics for each goal
3. **paths** (dict[StateBase, Path]): What are the routes?
   - One path for each goal
   - Each path: start → specific goal

## Solution Validity

### Valid Solution
```python
SolutionOMSPP(
    is_valid=True,
    stats=StatsOMSPP(...),
    paths={
        goal1: Path([start, ..., goal1]),
        goal2: Path([start, ..., goal2]),
        goal3: Path([start, ..., goal3])
    }
)
```

**Characteristics:**
- ALL goals were reached
- Paths exist for all goals
- `len(paths) == len(problem.goals)`
- Statistics include per-goal breakdown

### Invalid Solution
```python
SolutionOMSPP(
    is_valid=False,
    stats=StatsOMSPP(...),
    paths={
        goal1: Path([start, ..., goal1])
        # goal2, goal3 missing - unreachable
    }
)
```

**Characteristics:**
- Not all goals were reached
- Paths dictionary may be incomplete
- Statistics reflect partial search

## Usage with Algorithms

### Algorithm Returns Solution

```python
from f_search.algos import AStarRepeated
from f_search.problems import ProblemOMSPP

problem = ProblemOMSPP(grid, start, goals)
kx_astar = AStarRepeated(problem=problem)
solution = kx_astar.run()  # Returns SolutionOMSPP
```

### Processing Solution
```python
solution: SolutionOMSPP = kx_astar.run()

if solution.is_valid:
    # Success - process all paths
    print(f"Found paths to {len(solution.paths)} goals")

    for goal, path in solution.paths.items():
        print(f"\nGoal {goal}:")
        print(f"  Path length: {len(path.to_iterable())} states")
        print(f"  Generated: {solution.stats.generated_per_goal[goal]}")
        print(f"  Explored: {solution.stats.explored_per_goal[goal]}")
        print(f"  Time: {solution.stats.elapsed_per_goal[goal]}s")

    # Aggregate metrics
    print(f"\nTotal generated: {solution.stats.generated}")
    print(f"Total explored: {solution.stats.explored}")
    print(f"Total time: {solution.stats.elapsed}s")
else:
    # Failure - not all goals reached
    print(f"Only {len(solution.paths)} of {num_goals} goals reached")
```

## Paths Dictionary Structure

**Key**: Goal state
**Value**: Path from start to that goal

**Properties:**
- Each path starts at `problem.start`
- Each path ends at its corresponding goal
- Paths are independent (may overlap in space)
- Dictionary may be partial (invalid solutions)

**Access Patterns:**
```python
# Iterate all paths
for goal, path in solution.paths.items():
    # Process goal and its path

# Get specific path
goal_x = StateBase(key=(10, 10))
if goal_x in solution.paths:
    path_to_x = solution.paths[goal_x]

# Count paths
num_paths_found = len(solution.paths)
```

## Statistics (StatsOMSPP)

Performance metrics included:

### Aggregate Metrics
- **elapsed**: Total algorithm execution time
- **generated**: Total states generated across all sub-problems
- **updated**: Total states updated
- **explored**: Total states explored

### Per-Goal Metrics
- **elapsed_per_goal[goal]**: Time for this goal's search
- **generated_per_goal[goal]**: States generated for this goal
- **updated_per_goal[goal]**: States updated for this goal
- **explored_per_goal[goal]**: States explored for this goal

**Usage:**
```python
for goal in solution.paths.keys():
    time = solution.stats.elapsed_per_goal[goal]
    explored = solution.stats.explored_per_goal[goal]
    print(f"Goal {goal}: {explored} explored in {time}s")
```

## Path Properties

Each path in a valid solution:
- **Starts** at problem's start state
- **Ends** at the corresponding goal state
- **Connected**: Adjacent states are neighbors
- **Valid**: All states are on grid, not obstacles
- **Optimal**: Shortest path (for KxAStar using A*)

## Validity Semantics

**Valid** means:
- ALL goals in `problem.goals` were reached
- Paths exist for all goals
- Each path is valid and complete

**Invalid** means:
- At least one goal was unreachable
- Paths dictionary is incomplete
- Solution is partial or failed

## Immutability

Solutions are immutable:
- Cannot change `is_valid`
- Cannot modify `stats`
- Cannot alter `paths` dictionary

Represents final, unchanging result.

## Comparison with SolutionSPP

| Aspect | SolutionOMSPP | SolutionSPP |
|--------|--------------|--------------|
| **Problem Type** | One-to-Many | One-to-One |
| **Path(s)** | dict[StateBase, Path] | Single Path |
| **Property** | paths (dict) | path (Path) |
| **Stats** | StatsOMSPP | StatsSPP |
| **Validity** | All goals reached | Goal reached |
| **Per-goal metrics** | Yes | No |

## Example Output

```python
solution = kx_astar.run()

# Valid solution for 3 goals
SolutionOMSPP(
    is_valid=True,
    stats=StatsOMSPP(
        elapsed=0.156,
        generated=487,
        updated=72,
        explored=412,
        elapsed_per_goal={
            StateBase((5,5)): 0.048,
            StateBase((10,10)): 0.051,
            StateBase((15,5)): 0.057
        },
        generated_per_goal={
            StateBase((5,5)): 142,
            StateBase((10,10)): 165,
            StateBase((15,5)): 180
        },
        # ... other per-goal metrics
    ),
    paths={
        StateBase((5,5)): Path([StateBase((0,0)), ..., StateBase((5,5))]),
        StateBase((10,10)): Path([StateBase((0,0)), ..., StateBase((10,10))]),
        StateBase((15,5)): Path([StateBase((0,0)), ..., StateBase((15,5))])
    }
)
```

## Common Patterns

### Iterate All Goal Paths
```python
if solution.is_valid:
    for goal, path in solution.paths.items():
        print(f"Path to {goal}: {len(path.to_iterable())} states")
```

### Check Specific Goal
```python
goal_x = StateBase(key=(10, 10))
if goal_x in solution.paths:
    path = solution.paths[goal_x]
    print(f"Found path to {goal_x}")
```

### Compare Goal Difficulties
```python
for goal in solution.paths.keys():
    explored = solution.stats.explored_per_goal[goal]
    time = solution.stats.elapsed_per_goal[goal]
    print(f"{goal}: {explored} explored, {time}s")
```

### Aggregate Analysis
```python
total_path_length = sum(
    len(path.to_iterable())
    for path in solution.paths.values()
)
avg_explored = solution.stats.explored / len(solution.paths)
```

## Relationship to Other Components

- **Algorithms**: KxAStar produces SolutionOMSPP
- **Problems**: Solve ProblemOMSPP
- **Statistics**: Contains StatsOMSPP
- **Paths**: Contains multiple Path objects
- **States**: Paths contain sequences of States, goals are StateBase keys

## Design Rationale

### Why Dictionary of Paths?
- Natural mapping: goal → path
- Flexible access: can look up by goal
- Handles partial solutions: not all goals may be present
- Type-appropriate for multi-goal problems

### Why ALL Goals for Validity?
- Strict success criterion
- Clear semantics: valid = complete success
- Partial success still accessible via paths dictionary
- Matches typical OMSPP requirements

### Why Per-Goal Statistics?
- Enables performance analysis per goal
- Identifies difficult vs easy goals
- Supports debugging and optimization
- Provides fine-grained insights
