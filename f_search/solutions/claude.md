# solutions - Algorithm Solution Containers

## Purpose
Contains solution classes that encapsulate the results of search algorithms. Solutions package together validity status, performance statistics, and paths, providing a complete result object.

## Structure

- **i_0_base/** - `SolutionSearch` - Base solution class for all search problems
- **i_1_oospp/** - `SolutionOOSPP` - Solution for One-to-One problems (single path)
- **i_1_oospp/** - `SolutionOMSPP` - Solution for One-to-Many problems (multiple paths)

## Inheritance Hierarchy

```
SolutionSearch[Stats] (Generic base)
  ├─ SolutionOOSPP (StatsOOSPP, single Path)
  └─ SolutionOMSPP (StatsOMSPP, multiple Paths)
```

## Base Class: SolutionSearch

Provides foundational solution structure:

### Core Components
- **is_valid**: Boolean indicating if solution is valid (goal(s) reached)
- **stats**: Statistics object tracking performance metrics

### Generic Type Parameter
- `Stats` bounded to `StatsSearch`
- Allows type-safe specialization (StatsOOSPP vs StatsOMSPP)

## Solution Types

### SolutionOOSPP (One-to-One)
**Single start → Single goal**

**Components:**
- `is_valid`: True if goal was reached
- `stats`: StatsOOSPP with performance metrics
- `path`: Single Path object (sequence of states from start to goal)

**Use Case:** Results from AStar, Dijkstra algorithms

### SolutionOMSPP (One-to-Many)
**Single start → Multiple goals**

**Components:**
- `is_valid`: True if ALL goals were reached
- `stats`: StatsOMSPP with aggregate and per-goal metrics
- `paths`: Dictionary mapping each goal to its path (`dict[State, Path]`)

**Use Case:** Results from KxAStar algorithm

## Solution Validity

### When is a Solution Valid?

**OOSPP:**
- Goal state was reached
- Path exists from start to goal
- Algorithm succeeded

**OMSPP:**
- ALL goal states were reached
- Paths exist from start to each goal
- All sub-problems succeeded

### Invalid Solutions
Solutions can be invalid when:
- Goal unreachable (obstacles block path)
- Search space exhausted without finding goal
- Algorithm terminated early
- Timeout or resource limit reached

**Invalid solutions still contain:**
- `is_valid = False`
- Statistics from the search attempt
- Empty or partial paths

## Common Solution Interface

All solutions provide:
- `is_valid` property → `bool`
- `stats` property → Statistics object

Specific solutions add:
- OOSPP: `path` property → `Path`
- OMSPP: `paths` property → `dict[State, Path]`

## Relationship to Other Components

```
Algorithm
    ↓ produces
Solution
    ↓ contains
  ├─ Validity (bool)
  ├─ Statistics (performance metrics)
  └─ Path(s) (solution paths)
```

## Usage Pattern

### Creating Solutions (in algorithms)
```python
# OOSPP
solution = SolutionOOSPP(
    is_valid=True,
    stats=stats_oospp,
    path=path
)

# OMSPP
solution = SolutionOMSPP(
    is_valid=all_goals_reached,
    stats=stats_omspp,
    paths={goal1: path1, goal2: path2, goal3: path3}
)
```

### Consuming Solutions (by users)
```python
# Run algorithm
solution = algorithm.run()

# Check validity
if solution.is_valid:
    # Access path(s)
    if isinstance(solution, SolutionOOSPP):
        path = solution.path
        print(f"Path length: {len(path.to_iterable())}")

    elif isinstance(solution, SolutionOMSPP):
        for goal, path in solution.paths.items():
            print(f"Path to {goal}: {path}")

    # Access statistics
    print(f"Generated: {solution.stats.generated}")
    print(f"Explored: {solution.stats.explored}")
    print(f"Time: {solution.stats.elapsed}s")
else:
    print("No solution found")
```

## Design Philosophy

### Complete Result Package
Solutions contain everything needed:
- Success/failure status
- Performance metrics
- Actual solution paths

No need to query multiple objects.

### Immutability
Solutions are immutable after creation:
- No setters for properties
- Represents final algorithm result
- Safe to share and cache

### Type Safety
Generic type parameters ensure:
- Correct stats type for solution type
- Compile-time verification
- Clear type signatures

## Performance Metrics (via Stats)

All solutions include performance statistics:

**Common metrics:**
- `elapsed`: Total execution time
- `generated`: States added to open queue
- `updated`: States updated with better cost
- `explored`: States fully expanded

**OMSPP additional metrics:**
- `*_per_goal`: Individual metrics for each goal
- Per-goal breakdown of performance

## Comparison: OOSPP vs OMSPP Solutions

| Aspect | SolutionOOSPP | SolutionOMSPP |
|--------|--------------|--------------|
| **Path(s)** | Single Path | dict[State, Path] |
| **Stats** | StatsOOSPP | StatsOMSPP |
| **Validity** | Goal reached | All goals reached |
| **Property** | path | paths |
| **Iteration** | N/A | for goal, path in paths.items() |

## External Dependencies

- **f_cs.solution** - SolutionAlgo (generic solution interface)
- **f_search.stats** - StatsSearch, StatsOOSPP, StatsOMSPP
- **f_search.ds** - Path, State

## Extension Example

To add a new solution type (e.g., Many-to-Many):

```python
class SolutionMMSPP(SolutionSearch[StatsMMSPP]):
    def __init__(self, is_valid, stats, paths):
        SolutionSearch.__init__(self, is_valid=is_valid, stats=stats)
        self._paths = paths  # Different structure for M→M
```

## Key Design Decisions

### Why Separate Solution Types?
- **Type safety**: Different path structures (Path vs dict[State, Path])
- **Clarity**: Clear distinction between problem types
- **API appropriateness**: Single path vs multiple paths
- **Stats alignment**: Each solution type has matching stats type

### Why Include is_valid?
- **Explicit success/failure**: Don't rely on path existence
- **Partial results**: Can have invalid solution with stats
- **Error handling**: Caller can check without exceptions
- **Debugging**: Statistics useful even for failed searches
