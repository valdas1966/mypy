# StatsOMSPP - Statistics for One-to-Many Shortest Path Problem

## Main Class
`StatsOMSPP(StatsSearch)`

## Inheritance
- **Base Classes:** `StatsSearch`

## Purpose
Provides extended statistics for One-to-Many Shortest Path Problem algorithms. Adds per-goal metrics on top of aggregate metrics from StatsSearch, enabling fine-grained performance analysis for multi-goal problems.

## Functionality from Base Classes

### From StatsSearch (Aggregate Metrics)
- **elapsed** - Total execution time across all goals
- **generated** - Total states generated across all sub-problems
- **updated** - Total states updated
- **explored** - Total states explored

## Specialized Functionality

### Constructor (`__init__`)
**Parameters:**

**Base metrics** (aggregate):
- **elapsed**: `int` - Total time
- **generated**: `int` - Total generated
- **updated**: `int` - Total updated
- **explored**: `int` - Total explored

**Per-goal metrics**:
- **elapsed_per_goal**: `dict[StateBase, float]` - Time for each goal
- **generated_per_goal**: `dict[StateBase, int]` - Generated for each goal
- **updated_per_goal**: `dict[StateBase, int]` - Updated for each goal
- **explored_per_goal**: `dict[StateBase, int]` - Explored for each goal

**Implementation:**
```python
StatsSearch.__init__(self, elapsed, updated, generated, explored)
self._generated_per_goal = generated_per_goal
self._updated_per_goal = updated_per_goal
self._explored_per_goal = explored_per_goal
self._elapsed_per_goal = elapsed_per_goal
```

### Per-Goal Metrics

#### `generated_per_goal` property → `dict[StateBase, int]`
**Meaning**: States generated for each goal's sub-problem

**Structure**: Maps goal state to its generated count

**Usage:**
```python
for goal, count in stats.generated_per_goal.items():
    print(f"Goal {goal}: {count} generated")
```

#### `explored_per_goal` property → `dict[StateBase, int]`
**Meaning**: States explored for each goal's sub-problem

**Structure**: Maps goal state to its explored count

**Usage:**
```python
hardest_goal = max(stats.explored_per_goal, key=stats.explored_per_goal.get)
print(f"Hardest goal: {hardest_goal}")
```

#### `elapsed_per_goal` property → `dict[StateBase, float]`
**Meaning**: Execution time for each goal's sub-problem

**Structure**: Maps goal state to its time in seconds

**Usage:**
```python
for goal, time in stats.elapsed_per_goal.items():
    print(f"Goal {goal}: {time:.3f}s")
```

#### `updated_per_goal` property → `dict[StateBase, int]`
**Note:** Property exists but has no docstring in the code

**Meaning**: States updated for each goal's sub-problem

**Structure**: Maps goal state to its updated count

## Two-Level Statistics

### Aggregate Level (from StatsSearch)
Overall performance across all goals:
```python
total_time = stats.elapsed
total_generated = stats.generated
total_explored = stats.explored
```

### Per-Goal Level (OMSPP-specific)
Individual performance for each goal:
```python
for goal in stats.explored_per_goal.keys():
    time = stats.elapsed_per_goal[goal]
    generated = stats.generated_per_goal[goal]
    explored = stats.explored_per_goal[goal]
```

## Usage Context

### Creating StatsOMSPP (in KxAStar)
```python
# Aggregate from sub-solutions
stats = StatsOMSPP(
    elapsed=self.elapsed,
    generated=self._counters['GENERATED'],
    updated=self._counters['UPDATED'],
    explored=self._counters['EXPLORED'],
    elapsed_per_goal={goal1: 0.048, goal2: 0.051, goal3: 0.057},
    generated_per_goal={goal1: 142, goal2: 165, goal3: 180},
    updated_per_goal={goal1: 18, goal2: 25, goal3: 29},
    explored_per_goal={goal1: 124, goal2: 144, goal3: 144}
)
```

### Using in Solutions
```python
solution = SolutionOMSPP(
    is_valid=True,
    stats=stats,  # Must be StatsOMSPP
    paths=paths
)
```

### Analyzing Results
```python
solution = kx_astar.run()

# Aggregate analysis
print(f"Total time: {solution.stats.elapsed}s")
print(f"Total explored: {solution.stats.explored}")

# Per-goal analysis
for goal in solution.paths.keys():
    gen = solution.stats.generated_per_goal[goal]
    exp = solution.stats.explored_per_goal[goal]
    time = solution.stats.elapsed_per_goal[goal]
    print(f"{goal}: {gen} generated, {exp} explored in {time:.3f}s")

# Find extremes
easiest = min(solution.stats.explored_per_goal, key=solution.stats.explored_per_goal.get)
hardest = max(solution.stats.explored_per_goal, key=solution.stats.explored_per_goal.get)

print(f"Easiest goal: {easiest} ({solution.stats.explored_per_goal[easiest]} explored)")
print(f"Hardest goal: {hardest} ({solution.stats.explored_per_goal[hardest]} explored)")
```

## Per-Goal Analysis Use Cases

### Identify Difficult Goals
```python
# Goals ranked by difficulty (explored count)
sorted_goals = sorted(
    stats.explored_per_goal,
    key=stats.explored_per_goal.get,
    reverse=True
)
print("Goals by difficulty:")
for goal in sorted_goals:
    print(f"  {goal}: {stats.explored_per_goal[goal]} explored")
```

### Detect Outliers
```python
import statistics

explored_values = list(stats.explored_per_goal.values())
mean_explored = statistics.mean(explored_values)
stdev_explored = statistics.stdev(explored_values)

for goal, explored in stats.explored_per_goal.items():
    if explored > mean_explored + 2 * stdev_explored:
        print(f"Outlier: {goal} ({explored} explored, mean={mean_explored:.0f})")
```

### Compare Goal Performance
```python
for goal in stats.explored_per_goal.keys():
    ratio = stats.updated_per_goal[goal] / stats.generated_per_goal[goal]
    print(f"{goal}: update ratio = {ratio:.2%}")
```

## Metric Consistency

### Aggregate = Sum of Per-Goal
In KxAStar (naive decomposition):
```python
assert stats.generated == sum(stats.generated_per_goal.values())
assert stats.explored == sum(stats.explored_per_goal.values())
assert stats.updated == sum(stats.updated_per_goal.values())
assert stats.elapsed ≈ sum(stats.elapsed_per_goal.values())  # Approximately
```

**Note:** For more sophisticated algorithms (e.g., unified multi-goal A*), aggregate metrics may not equal sum of per-goal metrics due to shared computation.

## Comparison with StatsSPP

| Aspect | StatsOMSPP | StatsSPP |
|--------|-----------|-----------|
| **Base metrics** | Yes (aggregate) | Yes |
| **Per-goal metrics** | Yes (4 dicts) | No |
| **Additional data** | 4 dictionaries | None |
| **Use case** | Multiple goals | Single goal |
| **Complexity** | Higher | Lower |
| **Analysis depth** | Fine-grained | Basic |

## Example Values

```python
StatsOMSPP(
    # Aggregate metrics
    elapsed=0.156,
    generated=487,
    updated=72,
    explored=412,

    # Per-goal metrics
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
    updated_per_goal={
        StateBase((5,5)): 18,
        StateBase((10,10)): 25,
        StateBase((15,5)): 29
    },
    explored_per_goal={
        StateBase((5,5)): 124,
        StateBase((10,10)): 144,
        StateBase((15,5)): 144
    }
)
```

## Relationship to Other Components

- **StatsSearch**: Base class providing aggregate metrics
- **SolutionOMSPP**: Requires StatsOMSPP specifically
- **AlgoOMSPP**: Creates StatsOMSPP instances
- **KxAStar**: Aggregates per-goal stats from multiple A* runs
- **StateBase**: Used as dictionary keys for per-goal metrics

## Design Rationale

### Why Per-Goal Metrics?
- **Understand variance**: Some goals harder than others
- **Identify patterns**: Clustered vs isolated goals
- **Debug algorithms**: Detect problematic goals
- **Optimize**: Target improvements to difficult goals
- **Research**: Analyze multi-goal algorithm behavior

### Why Four Dictionaries?
- **Complete picture**: All metrics available per-goal
- **Consistency**: Parallel structure to aggregate metrics
- **Flexibility**: Can analyze any metric by goal
- **Granularity**: Maximum analysis capability

## Key Properties

1. **Two-level tracking**: Aggregate + per-goal
2. **Complete coverage**: All base metrics available per-goal
3. **Analysis-ready**: Supports fine-grained performance analysis
4. **KxAStar-specific**: Designed for decomposition-based solving
5. **Extensible**: Can add more per-goal metrics
