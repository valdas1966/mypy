# HasStart - Mixin for Single Start StateBase

## Main Class
`HasStart`

## Purpose
Provides a single start state property to problem classes. This mixin adds the concept of an initial configuration to problems that need one.

## Core Functionality

### Constructor (`__init__`)
**Parameters:**
- **start**: `StateBase` - The initial state of the problem

**Storage:**
- `_start`: Private attribute storing the start state

**Usage:**
```python
HasStart.__init__(self, start=start_state)
```

### Property Access

#### `start` property → `StateBase`
Returns the start state of the problem.

**Read-only**: No setter provided (immutable after construction)

**Usage:**
```python
initial_state = problem.start
```

## Design Pattern

### Minimal Mixin
Provides exactly one feature:
- Storage of start state
- Read-only access via property
- Nothing more

### Immutability
Once set in constructor, start state cannot be changed:
- No setter method
- Private storage prevents direct modification
- Ensures problem consistency during algorithm execution

### Property Pattern
Uses Python `@property` decorator:
- Clean attribute-style access: `problem.start`
- Hides implementation details
- Future-proof (can add logic without API change)

## Usage in Problems

### SPP (One-to-One)
```python
class ProblemSPP(ProblemSearch, HasStart, HasGoal):
    def __init__(self, grid, start, goal):
        ProblemSearch.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)  # Add start
        HasGoal.__init__(self, goal=goal)
```

### OMSPP (One-to-Many)
```python
class ProblemOMSPP(ProblemSearch, HasStart, HasGoals):
    def __init__(self, grid, start, goals):
        ProblemSearch.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)  # Add start
        HasGoals.__init__(self, goals=goals)
```

## Usage in Algorithms

Algorithms access the start state through this mixin:

```python
# In AlgoSearch._run_pre()
start = self._problem.start
self._generated.push(start, cost_start)

# In algorithm initialization
initial_state = problem.start
g[initial_state] = 0
h[initial_state] = heuristic(initial_state)
```

## Semantics

### What is "Start"?
- **Initial configuration**: Where the search begins
- **Source**: The origin point for pathfinding
- **Root**: Root of the search tree
- **Given**: Known at problem definition time

### Assumptions
- Start state is valid (not an obstacle, within bounds)
- Start state is distinct from goal(s) (typically)
- Only one start state (for this mixin)

## Mixin Independence

HasStart is completely independent:
- **No dependencies**: Doesn't require other mixins
- **No conflicts**: Doesn't overlap with HasGoal/HasGoals
- **Composable**: Can be combined with any other mixins

## Type Safety

When a problem class includes HasStart:
- `problem.start` is guaranteed to exist
- Type checker knows `start` returns `StateBase`
- Compile-time verification of property access

## Comparison with HasStarts (Hypothetical)

If we needed multiple start states:

| Aspect | HasStart (current) | HasStarts (hypothetical) |
|--------|-------------------|-------------------------|
| **Quantity** | Single start | Multiple starts |
| **Type** | StateBase | set[StateBase] or list[StateBase] |
| **Property** | start | starts |
| **Use case** | SPP, OMSPP | Multi-source problems |

## Example Usage

```python
from f_search.ds import StateBase
from f_search.problems.mixins import HasStart

# Create start state
start_state = StateBase(key=(0, 0))


# Use in problem
# (typically as part of multiple inheritance)
class MyProblem(HasStart):
    def __init__(self, start):
        HasStart.__init__(self, start=start)


problem = MyProblem(start=start_state)
print(problem.start)  # StateBase(key=(0, 0))
```

## Relationship to Other Components

- **StateBase**: HasStart stores a StateBase object
- **Problems**: Mixed into ProblemSPP, ProblemOMSPP
- **Algorithms**: Access via `problem.start`

## Design Rationale

### Why a Mixin?
- **Reusability**: Used by multiple problem types
- **Composability**: Combines with other features
- **Single Responsibility**: Only manages start state
- **Simplicity**: Minimal, focused interface

### Why Immutable?
- **Consistency**: Problem doesn't change during solving
- **Safety**: Prevents accidental modification
- **Simplicity**: No need for update logic
