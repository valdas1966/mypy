# HasGoal - Mixin for Single Goal StateBase

## Main Class
`HasGoal`

## Purpose
Provides a single goal state property to problem classes. This mixin adds the concept of a single target configuration to problems.

## Core Functionality

### Constructor (`__init__`)
**Parameters:**
- **goal**: `StateBase` - The target state of the problem

**Storage:**
- `_goal`: Private attribute storing the goal state

**Usage:**
```python
HasGoal.__init__(self, goal=goal_state)
```

### Property Access

#### `goal` property → `StateBase`
Returns the goal state of the problem.

**Read-only**: No setter provided (immutable after construction)

**Usage:**
```python
target_state = problem.goal
```

## Design Pattern

### Minimal Mixin
Provides exactly one feature:
- Storage of goal state
- Read-only access via property
- Nothing more

### Immutability
Once set in constructor, goal state cannot be changed:
- No setter method
- Private storage prevents direct modification
- Ensures problem consistency during algorithm execution

### Property Pattern
Uses Python `@property` decorator:
- Clean attribute-style access: `problem.goal`
- Hides implementation details
- Future-proof (can add logic without API change)

## Usage in Problems

### SPP (One-to-One)
```python
class ProblemSPP(ProblemSearch, HasStart, HasGoal):
    def __init__(self, grid, start, goal):
        ProblemSearch.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)  # Add goal
```

**Note:** OMSPP uses HasGoals (plural) instead

## Usage in Algorithms

Algorithms access the goal state through this mixin:

```python
# In termination checking
def _can_terminate(self) -> bool:
    return self._best == self._problem.goal

# In heuristic calculation
def _heuristic(self, state: StateBase) -> int:
    goal = self._problem.goal
    return manhattan_distance(state, goal)
```

## Semantics

### What is "Goal"?
- **Target configuration**: Where the search aims to reach
- **Destination**: The endpoint for pathfinding
- **Success condition**: Search succeeds when goal is reached
- **Given**: Known at problem definition time

### Assumptions
- Goal state is valid (not an obstacle, within bounds)
- Goal state is distinct from start (typically)
- Only one goal state (for this mixin)

## Mixin Independence

HasGoal is completely independent:
- **No dependencies**: Doesn't require other mixins
- **No conflicts**: Doesn't overlap with HasStart/HasGoals
- **Composable**: Can be combined with any other mixins
- **Mutually exclusive with HasGoals**: Use one or the other

## Type Safety

When a problem class includes HasGoal:
- `problem.goal` is guaranteed to exist
- Type checker knows `goal` returns `StateBase`
- Compile-time verification of property access

## Comparison with HasGoals

| Aspect | HasGoal (singular) | HasGoals (plural) |
|--------|-------------------|------------------|
| **Quantity** | Single goal | Multiple goals |
| **Type** | StateBase | set[StateBase] |
| **Property** | goal | goals |
| **Use case** | SPP | OMSPP |
| **Termination** | state == goal | state in goals |

## Example Usage

```python
from f_search.ds import StateBase
from f_search.problems.mixins import HasGoal

# Create goal state
goal_state = StateBase(key=(10, 10))


# Use in problem
class MyProblem(HasGoal):
    def __init__(self, goal):
        HasGoal.__init__(self, goal=goal)


problem = MyProblem(goal=goal_state)
print(problem.goal)  # StateBase(key=(10, 10))

# Check if state is goal
if current_state == problem.goal:
    print("Goal reached!")
```

## Relationship to Other Components

- **StateBase**: HasGoal stores a StateBase object
- **Problems**: Mixed into ProblemSPP
- **Algorithms**: Access via `problem.goal` for termination/heuristic

## Algorithm Integration

### Termination Checking
```python
# SPP algorithms check single goal
if current_state == problem.goal:
    return solution  # Goal reached
```

### Heuristic Calculation
```python
# A* uses goal for heuristic
def _heuristic(self, state: StateBase) -> int:
    goal = self._problem.goal
    return abs(state.key[0] - goal.key[0]) + abs(state.key[1] - goal.key[1])
```

### Path Reconstruction
```python
# Reconstruct path from goal back to start
path_states = []
current = problem.goal
while current != problem.start:
    path_states.append(current)
    current = parent[current]
```

## Design Rationale

### Why a Mixin?
- **Reusability**: Could be used by different problem types
- **Composability**: Combines with HasStart and ProblemSearch
- **Single Responsibility**: Only manages goal state
- **Simplicity**: Minimal, focused interface

### Why Separate from HasGoals?
- **Type clarity**: goal vs goals (singular vs plural)
- **Semantic difference**: One target vs many targets
- **Algorithm differences**: Different termination/heuristic logic
- **API simplicity**: StateBase vs set[StateBase]

### Why Immutable?
- **Consistency**: Problem doesn't change during solving
- **Safety**: Prevents accidental modification
- **Simplicity**: No need for update logic
