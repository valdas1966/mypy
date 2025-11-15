# HasGoals - Mixin for Multiple Goal States

## Main Class
`HasGoals`

## Purpose
Provides multiple goal states property to problem classes. This mixin adds the concept of multiple target configurations to problems (plural goals).

## Core Functionality

### Constructor (`__init__`)
**Parameters:**
- **goals**: `Iterable[State]` - Collection of goal states

**Storage:**
- `_goals`: Private attribute storing goals as `set[State]`

**Conversion:**
Goals are converted from iterable to set:
```python
self._goals: set[State] = set(goals)
```

**Usage:**
```python
HasGoals.__init__(self, goals=[goal1, goal2, goal3])
```

### Property Access

#### `goals` property → `set[State]`
Returns the set of goal states.

**Read-only**: No setter provided (immutable after construction)

**Type**: Returns `set[State]`, not list or other iterable

**Usage:**
```python
target_states = problem.goals  # set[State]
```

## Design Pattern

### Minimal Mixin
Provides exactly one feature:
- Storage of goal states as set
- Read-only access via property
- Nothing more

### Set-Based Storage
Uses `set[State]` instead of `list[State]`:
- **No duplicates**: Each goal appears once
- **No order**: Goals have no inherent ordering
- **Fast membership**: O(1) check if state is goal
- **Set semantics**: Matches mathematical definition

### Immutability
Once set in constructor, goals cannot be changed:
- No setter method
- Private storage prevents direct modification
- Ensures problem consistency during algorithm execution

## Usage in Problems

### OMSPP (One-to-Many)
```python
class ProblemOMSPP(ProblemSearch, HasStart, HasGoals):
    def __init__(self, grid, start, goals):
        ProblemSearch.__init__(self, grid=grid)
        HasStart.__init__(self, start=start)
        HasGoals.__init__(self, goals=goals)  # Add goals (plural)
```

**Note:** OOSPP uses HasGoal (singular) instead

## Usage in Algorithms

Algorithms access goal states through this mixin:

```python
# Check if current state is any goal
if current_state in self._problem.goals:
    goals_reached.add(current_state)

# Check if all goals reached
if len(goals_reached) == len(self._problem.goals):
    return solution  # All goals found

# Iterate over goals
for goal in self._problem.goals:
    # Process each goal
```

## Set Operations

### Membership Testing
```python
if state in problem.goals:
    # This state is a goal
```

### Iteration
```python
for goal in problem.goals:
    # Process each goal
```

### Size
```python
num_goals = len(problem.goals)
k = len(problem.goals)  # Common variable name
```

### Set Operations
```python
remaining_goals = problem.goals - goals_reached
all_reached = goals_reached == problem.goals
any_reached = goals_reached & problem.goals  # intersection
```

## Semantics

### What are "Goals"?
- **Target configurations**: Multiple states to reach
- **Destinations**: Multiple endpoints for pathfinding
- **Success condition**: Search succeeds when all goals reached (typically)
- **Given**: Known at problem definition time

### Assumptions
- All goal states are valid (not obstacles, within bounds)
- Goals are distinct from start (typically)
- Goals are distinct from each other (enforced by set)
- Multiple goals present (at least one)

## Mixin Independence

HasGoals is completely independent:
- **No dependencies**: Doesn't require other mixins
- **No conflicts**: Doesn't overlap with HasStart/HasGoal
- **Composable**: Can be combined with any other mixins
- **Mutually exclusive with HasGoal**: Use one or the other

## Type Safety

When a problem class includes HasGoals:
- `problem.goals` is guaranteed to exist
- Type checker knows `goals` returns `set[State]`
- Compile-time verification of property access

## Comparison with HasGoal

| Aspect | HasGoals (plural) | HasGoal (singular) |
|--------|------------------|-------------------|
| **Quantity** | Multiple goals | Single goal |
| **Type** | set[State] | State |
| **Property** | goals | goal |
| **Use case** | OMSPP | OOSPP |
| **Termination** | state in goals | state == goal |
| **Heuristic** | min/avg to goals | distance to goal |

## Example Usage

```python
from f_search.ds import State
from f_search.problems.mixins import HasGoals

# Create multiple goal states
goal_states = [
    State(key=(5, 5)),
    State(key=(10, 10)),
    State(key=(15, 5))
]

# Use in problem
class MyProblem(HasGoals):
    def __init__(self, goals):
        HasGoals.__init__(self, goals=goals)

problem = MyProblem(goals=goal_states)

# Access goals
print(len(problem.goals))  # 3
print(State(key=(5, 5)) in problem.goals)  # True

# Iterate goals
for goal in problem.goals:
    print(f"Goal: {goal}")
```

## Algorithm Integration

### Multi-Goal Termination
```python
# Track which goals reached
goals_reached = set()

# During search
if current_state in problem.goals:
    goals_reached.add(current_state)

# Check if all goals reached
if len(goals_reached) == len(problem.goals):
    return solution  # All goals found
```

### Multi-Goal Heuristic
```python
# Heuristic to nearest goal
def _heuristic(self, state: State) -> int:
    min_dist = float('inf')
    for goal in self._problem.goals:
        dist = manhattan_distance(state, goal)
        min_dist = min(min_dist, dist)
    return min_dist
```

### Problem Decomposition
```python
# Convert to multiple single-goal problems
def to_oospps(self):
    sub_problems = []
    for goal in self.goals:
        oospp = ProblemOOSPP(self.grid, self.start, goal)
        sub_problems.append(oospp)
    return sub_problems
```

## Why Set Instead of List?

### Advantages of Set
1. **No duplicates**: Automatically enforces uniqueness
2. **Fast membership**: O(1) check if state is goal
3. **Set semantics**: Natural for "collection of targets"
4. **Order-independent**: Goals have no inherent order

### Disadvantages
1. **No indexing**: Can't access goals[0]
2. **No order**: Can't iterate in specific order

**Design choice:** Advantages outweigh disadvantages for goal collection

## Design Rationale

### Why a Mixin?
- **Reusability**: Could be used by different problem types
- **Composability**: Combines with HasStart and ProblemSearch
- **Single Responsibility**: Only manages goal states
- **Simplicity**: Minimal, focused interface

### Why Separate from HasGoal?
- **Type clarity**: goals (set) vs goal (State)
- **Semantic difference**: Many targets vs one target
- **Algorithm differences**: Different termination/heuristic logic
- **API appropriateness**: Set operations for multiple goals

### Why Immutable?
- **Consistency**: Problem doesn't change during solving
- **Safety**: Prevents accidental modification
- **Simplicity**: No need for add/remove logic
