# stats - Performance Statistics for Search Algorithms

## Purpose
Contains statistics classes that track performance metrics for search algorithms. Statistics measure computational cost, efficiency, and behavior of algorithms during execution.

## Structure

- **i_0_base/** - `StatsSearch` - Base statistics for all search algorithms
- **i_1_oospp/** - `StatsOOSPP` - Statistics for One-to-One problems
- **i_1_omspp/** - `StatsOMSPP` - Statistics for One-to-Many problems (with per-goal metrics)

## Inheritance Hierarchy

```
StatsSearch (Base metrics)
  ├─ StatsOOSPP (OOSPP - currently no additions)
  └─ StatsOMSPP (OMSPP - adds per-goal metrics)
```

## Base Class: StatsSearch

Provides core performance metrics for all search algorithms:

### Standard Metrics
- **elapsed**: Execution time in seconds
- **generated**: Number of states added to open queue
- **updated**: Number of states updated with better cost
- **explored**: Number of states fully expanded

### Metric Meanings

#### elapsed
**What**: Total algorithm execution time
**Units**: Seconds (float)
**Measures**: Overall speed/efficiency
**Usage**: Compare algorithm performance

#### generated
**What**: States added to the open queue (Generated)
**Meaning**: New states discovered during search
**Counter**: Incremented when state first added to Generated
**Indicates**: Search space coverage

#### updated
**What**: States updated with better cost
**Meaning**: States re-added to Generated with improved path
**Counter**: Incremented when existing state gets better cost
**Indicates**: Path refinement, algorithm effectiveness

#### explored
**What**: States fully expanded (moved to closed list)
**Meaning**: States whose successors were generated
**Counter**: Incremented when state popped from Generated
**Indicates**: Actual search effort

## Stats Types

### StatsOOSPP (One-to-One)
**Simple statistics for single-goal problems**

**Components:** (all inherited from StatsSearch)
- elapsed
- generated
- updated
- explored

**Use Case:** AStar, Dijkstra algorithm results

**Current implementation:** `pass` (no additions to base)

### StatsOMSPP (One-to-Many)
**Extended statistics for multi-goal problems**

**Aggregate Components:** (inherited)
- elapsed - Total time across all goals
- generated - Total states generated
- updated - Total states updated
- explored - Total states explored

**Per-Goal Components:** (OMSPP-specific)
- **elapsed_per_goal**: `dict[State, float]` - Time for each goal
- **generated_per_goal**: `dict[State, int]` - Generated per goal
- **updated_per_goal**: `dict[State, int]` - Updated per goal
- **explored_per_goal**: `dict[State, int]` - Explored per goal

**Use Case:** KxAStar algorithm results

## Metric Relationships

### Key Relationships
```
explored ≤ generated
updated ≤ generated
generated = new_states + updated
```

### Why?
- **explored ≤ generated**: Can only explore what was generated
- **updated ≤ generated**: Updates are subset of generated
- States can be:
  - Generated once, never updated, never explored (discarded)
  - Generated once, explored once (efficient)
  - Generated once, updated N times, explored once (refinement)

### Typical Values
For well-performing A*:
- updated << generated (few path improvements)
- explored ≈ generated (most generated states explored)

For less efficient search:
- updated → generated (many path improvements)
- explored << generated (many states queued but not explored)

## Usage in Solutions

Statistics are embedded in solutions:

```python
# OOSPP
solution = SolutionOOSPP(
    is_valid=True,
    stats=StatsOOSPP(
        elapsed=0.042,
        generated=156,
        updated=23,
        explored=134
    ),
    path=path
)

# OMSPP
solution = SolutionOMSPP(
    is_valid=True,
    stats=StatsOMSPP(
        elapsed=0.156,
        generated=487,
        updated=72,
        explored=412,
        elapsed_per_goal={goal1: 0.048, goal2: 0.051, goal3: 0.057},
        generated_per_goal={goal1: 142, goal2: 165, goal3: 180},
        updated_per_goal={goal1: 18, goal2: 25, goal3: 29},
        explored_per_goal={goal1: 124, goal2: 144, goal3: 144}
    ),
    paths=paths
)
```

## Creating Statistics (in algorithms)

### During Algorithm Execution
```python
# Initialize counters
self._counters['GENERATED'] = 0
self._counters['UPDATED'] = 0
self._counters['EXPLORED'] = 0

# Track time
start_time = time.time()

# During search
self._counters['GENERATED'] += 1  # New state
self._counters['UPDATED'] += 1    # Updated state
self._counters['EXPLORED'] += 1   # Explored state

# End time
end_time = time.time()

# Create stats
stats = StatsOOSPP(
    elapsed=end_time - start_time,
    generated=self._counters['GENERATED'],
    updated=self._counters['UPDATED'],
    explored=self._counters['EXPLORED']
)
```

## Using Statistics (by researchers)

### Basic Analysis
```python
solution = algorithm.run()

print(f"Time: {solution.stats.elapsed:.3f}s")
print(f"Generated: {solution.stats.generated}")
print(f"Updated: {solution.stats.updated}")
print(f"Explored: {solution.stats.explored}")

# Efficiency metrics
update_ratio = solution.stats.updated / solution.stats.generated
explore_ratio = solution.stats.explored / solution.stats.generated
```

### Per-Goal Analysis (OMSPP)
```python
solution_omspp = kx_astar.run()

for goal, path in solution_omspp.paths.items():
    gen = solution_omspp.stats.generated_per_goal[goal]
    exp = solution_omspp.stats.explored_per_goal[goal]
    time = solution_omspp.stats.elapsed_per_goal[goal]
    print(f"Goal {goal}: {gen} generated, {exp} explored in {time:.3f}s")

# Identify hardest goal
hardest = max(
    solution_omspp.stats.explored_per_goal,
    key=solution_omspp.stats.explored_per_goal.get
)
print(f"Hardest goal: {hardest}")
```

### Algorithm Comparison
```python
sol_astar = AStar(problem).run()
sol_dijkstra = Dijkstra(problem).run()

print("A* vs Dijkstra:")
print(f"  Generated: {sol_astar.stats.generated} vs {sol_dijkstra.stats.generated}")
print(f"  Explored: {sol_astar.stats.explored} vs {sol_dijkstra.stats.explored}")
print(f"  Time: {sol_astar.stats.elapsed:.3f}s vs {sol_dijkstra.stats.elapsed:.3f}s")
```

## Design Philosophy

### Completeness
Track all relevant metrics:
- Time (elapsed)
- Space (generated, tracked states)
- Work (explored, actual computation)
- Efficiency (updated, path improvements)

### Immutability
Statistics are immutable after creation:
- Represents final algorithm performance
- Safe to share and analyze
- No modification methods

### Hierarchical Detail
- Base: Overall metrics
- OOSPP: Same as base (single goal)
- OMSPP: Adds per-goal breakdown

## Comparison: OOSPP vs OMSPP Stats

| Aspect | StatsOOSPP | StatsOMSPP |
|--------|-----------|-----------|
| **Base metrics** | Yes | Yes (aggregate) |
| **Per-goal metrics** | No | Yes (4 dicts) |
| **Use case** | Single goal | Multiple goals |
| **Complexity** | Simple | More detailed |

## External Dependencies

- **f_cs.stats** - StatsAlgo (generic statistics interface)
- **f_search.ds** - State (for per-goal dict keys in OMSPP)

## Extension Example

To add custom statistics:

```python
class StatsCustom(StatsSearch):
    def __init__(self, elapsed, generated, updated, explored, custom_metric):
        StatsSearch.__init__(self, elapsed, generated, updated, explored)
        self._custom_metric = custom_metric

    @property
    def custom_metric(self):
        return self._custom_metric
```

## Key Design Decisions

### Why Track Updated?
- Measures path refinement
- Indicates heuristic quality (good heuristic → few updates)
- Helps diagnose algorithm behavior

### Why Per-Goal for OMSPP?
- Understand individual goal difficulty
- Identify outliers (hard goals)
- Support fine-grained analysis
- Enable optimization opportunities

### Why Immutable?
- Statistics represent final results
- No reason to modify after creation
- Safer for analysis and sharing
