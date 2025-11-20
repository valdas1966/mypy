# StatsSearch - Base Statistics for Search Algorithms

## Main Class
`StatsSearch(StatsAlgo)`

## Inheritance
- **Base Classes:** `StatsAlgo` (from f_cs.stats)

## Purpose
Provides foundational performance metrics for all search algorithms. Tracks the four core metrics that measure computational cost and algorithm behavior.

## Functionality from Base Classes

### From StatsAlgo
- **elapsed** property - Execution time tracking
- Generic statistics interface

## Specialized Functionality

### Constructor (`__init__`)
**Parameters:**
- **elapsed**: `int` - Total execution time in seconds
- **generated**: `int` - Number of states generated
- **updated**: `int` - Number of states updated
- **explored**: `int` - Number of states explored

**Implementation:**
```python
StatsAlgo.__init__(self, elapsed=elapsed)
self._generated = generated
self._updated = updated
self._explored = explored
```

**Initializes:**
1. Elapsed time (via StatsAlgo)
2. Search-specific metrics (generated, updated, explored)

### Core Metrics

#### `generated` property → `int`
**Meaning**: Number of states added to the open queue (Generated)

**When incremented**: When a new state is added to Generated for the first time

**Measures**: Search space coverage, states discovered

**Usage:**
```python
print(f"Generated {stats.generated} states")
```

#### `updated` property → `int`
**Meaning**: Number of states updated with better cost

**When incremented**: When an existing state in Generated gets a better path

**Measures**: Path refinement, algorithm effectiveness, heuristic quality

**Usage:**
```python
update_ratio = stats.updated / stats.generated
print(f"Update ratio: {update_ratio:.2%}")
```

#### `explored` property → `int`
**Meaning**: Number of states fully expanded (moved to closed list)

**When incremented**: When a state is popped from Generated and its successors generated

**Measures**: Actual computational work, states processed

**Usage:**
```python
print(f"Explored {stats.explored} states")
efficiency = stats.explored / stats.generated
```

## Metric Relationships

### Invariants
- `explored ≤ generated`: Can only explore generated states
- `updated ≤ generated`: Updates are subset of generated
- `generated ≥ 0, updated ≥ 0, explored ≥ 0`: All non-negative

### Typical Patterns

**Efficient A*:**
```
generated=156, updated=23, explored=134
- Most generated states are explored
- Few updates (good heuristic)
```

**Inefficient Search:**
```
generated=856, updated=312, explored=287
- Many updates (poor heuristic or complex space)
- Many generated but not explored (pruned/abandoned)
```

## Usage Context

### In Algorithms
```python
# Initialize counters
self._counters['GENERATED'] = 0
self._counters['UPDATED'] = 0
self._counters['EXPLORED'] = 0

# During search
if state not in self._generated:
    self._counters['GENERATED'] += 1
else:
    self._counters['UPDATED'] += 1

self._counters['EXPLORED'] += 1  # When expanding state

# Create stats
stats = StatsSearch(
    elapsed=self.elapsed,
    generated=self._counters['GENERATED'],
    updated=self._counters['UPDATED'],
    explored=self._counters['EXPLORED']
)
```

### In Solutions
```python
solution = SolutionSPP(
    is_valid=True,
    stats=stats,  # StatsSearch or subclass
    path=path
)
```

### By Users
```python
solution = algorithm.run()
print(f"Generated: {solution.stats.generated}")
print(f"Updated: {solution.stats.updated}")
print(f"Explored: {solution.stats.explored}")
print(f"Time: {solution.stats.elapsed}s")
```

## Design Philosophy

### Minimal Core Set
Four metrics capture essential algorithm behavior:
1. **Time**: How long?
2. **Generated**: How many states discovered?
3. **Updated**: How much refinement?
4. **Explored**: How much work?

### Immutability
Properties are read-only:
- Represents final algorithm performance
- No setters provided
- Safe to share and analyze

### Template for Extension
Base class provides common metrics; subclasses can add problem-specific ones:
- StatsSPP: Currently no additions
- StatsOMSPP: Adds per-goal metrics

## Relationship to Other Classes

- **StatsAlgo**: Base statistics interface
- **StatsSPP/OMSPP**: Specialized statistics
- **Solutions**: Contain StatsSearch instances
- **Algorithms**: Create StatsSearch instances

## Example Values

```python
# Successful A* search
StatsSearch(
    elapsed=0.042,
    generated=156,
    updated=23,
    explored=134
)

# Failed search (explored all reachable)
StatsSearch(
    elapsed=1.234,
    generated=5432,
    updated=876,
    explored=5432  # All generated were explored
)
```

## Derived Metrics

Users can compute derived metrics:

```python
# Update ratio
update_ratio = stats.updated / stats.generated

# Exploration ratio
explore_ratio = stats.explored / stats.generated

# States per second
states_per_sec = stats.explored / stats.elapsed

# Efficiency
efficiency = 1 - (stats.updated / stats.generated)  # Lower updates = more efficient
```

## Key Properties

1. **Essential metrics**: Captures core algorithm behavior
2. **Language-independent**: Applicable to any search algorithm
3. **Immutable**: Represents final performance snapshot
4. **Comparable**: Can compare across algorithms
5. **Extensible**: Subclasses can add more metrics
