# StatsSPP - Statistics for One-to-One Shortest Path Problem

## Main Class
`StatsSPP(StatsSearch)`

## Inheritance
- **Base Classes:** `StatsSearch`

## Purpose
Provides statistics for One-to-One Shortest Path Problem algorithms. Currently a pass-through class that uses all metrics from StatsSearch without additions.

## Functionality from Base Classes

### From StatsSearch
- **elapsed** - Execution time in seconds
- **generated** - States added to open queue
- **updated** - States updated with better cost
- **explored** - States fully expanded

All properties and functionality inherited directly.

## Current Implementation

```python
class StatsSPP(StatsSearch):
    pass  # Currently no additional functionality
```

The class body contains only `pass`, indicating it adds nothing beyond StatsSearch.

## Why a Separate Class?

### Type Distinction
- Provides type safety for SPP solutions
- `SolutionSPP` requires `StatsSPP` specifically
- Enables future extensions without breaking API

### Semantic Clarity
- Clear that these are SPP-specific statistics
- Distinguishes from OMSPP statistics (which add per-goal metrics)
- Makes code more readable and self-documenting

### Future Extensibility
Placeholder for potential SPP-specific metrics:
- Path quality metrics
- Heuristic accuracy
- Branching factor
- Solution optimality measures

## Usage

### Creating StatsSPP (in algorithms)
```python
stats = StatsSPP(
    elapsed=self.elapsed,
    generated=self._counters['GENERATED'],
    updated=self._counters['UPDATED'],
    explored=self._counters['EXPLORED']
)
```

### Using in Solutions
```python
solution = SolutionSPP(
    is_valid=True,
    stats=stats,  # Must be StatsSPP
    path=path
)
```

### Accessing Metrics
```python
print(f"Time: {solution.stats.elapsed}s")
print(f"Generated: {solution.stats.generated}")
print(f"Updated: {solution.stats.updated}")
print(f"Explored: {solution.stats.explored}")
```

## Comparison with StatsOMSPP

| Aspect | StatsSPP | StatsOMSPP |
|--------|-----------|-----------|
| **Base metrics** | Yes (inherited) | Yes (inherited) |
| **Per-goal metrics** | No | Yes (added) |
| **Additional data** | None | 4 dicts (per-goal) |
| **Use case** | Single goal | Multiple goals |
| **Complexity** | Simple | More complex |

## Type Safety Example

```python
# Type checker ensures correct stats type
def process_spp_solution(solution: SolutionSPP):
    stats: StatsSPP = solution.stats  # Type safe
    print(stats.explored)

# Would fail type check
def wrong_stats():
    return SolutionSPP(
        is_valid=True,
        stats=StatsOMSPP(...),  # Type error!
        path=path
    )
```

## Relationship to Other Components

- **StatsSearch**: Base class providing all current functionality
- **SolutionSPP**: Requires StatsSPP specifically
- **AlgoSPP**: Creates StatsSPP instances
- **AStar/Dijkstra**: Use StatsSPP for results

## Potential Future Extensions

Could add SPP-specific metrics:

```python
class StatsSPP(StatsSearch):
    def __init__(self, elapsed, generated, updated, explored,
                 path_length=None,
                 heuristic_accuracy=None):
        StatsSearch.__init__(self, elapsed, generated, updated, explored)
        self._path_length = path_length
        self._heuristic_accuracy = heuristic_accuracy

    @property
    def path_length(self):
        return self._path_length

    @property
    def heuristic_accuracy(self):
        return self._heuristic_accuracy
```

## Design Rationale

### Why Not Just Use StatsSearch?
- Type system benefits: Clear type signatures
- Future-proofing: Easy to add metrics later
- Semantic clarity: Explicit SPP context
- API consistency: Parallel with StatsOMSPP

### Why Currently Empty?
- No SPP-specific metrics identified yet
- Base metrics sufficient for current needs
- Can add metrics without breaking API
- Maintains clean inheritance hierarchy

## Key Properties

1. **Pass-through**: All functionality from StatsSearch
2. **Type-specific**: Required by SolutionSPP
3. **Extensible**: Ready for future additions
4. **Simple**: No additional complexity currently
