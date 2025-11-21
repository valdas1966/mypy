# Cost - StateBase Cost and Priority Representation

## Main Class
`Cost[Key](Generic[Key], Comparable)`

## Inheritance
- **Base Classes:** `Generic[Key]`, `Comparable` (from f_core.mixins)
- **Generic Parameter:** `Key` - the type of identifier for the associated state

## Purpose
Represents the cost and priority of a state in the search space. Used primarily for ordering states in the priority queue (Generated) to determine which state to explore next. Encapsulates both actual cost (g), heuristic estimate (h), and additional priority factors.

## Core Functionality

### Constructor (`__init__`)
Creates a Cost object with the following parameters:

**Parameters:**
- **key**: Identifier for the associated state (typically a cell/coordinate)
- **g**: Actual path cost from start to this state (g-value)
- **h**: Heuristic estimate from this state to goal (h-value)
- **is_cached**: Boolean flag indicating if this is a cached cost (default: False)
- **is_bounded**: Boolean flag indicating if this cost is bounded (default: False)

**Storage:**
All parameters stored as private attributes: `_key`, `_g`, `_h`, `_is_cached`, `_is_bounded`

### Comparison Method (`key_comparison`)
Returns a tuple used for comparing and ordering costs.

**Return Type:** `tuple[int, int, int, int, Key]`

**Comparison Tuple:**
```python
(f-value, priority_cached, priority_bounded, h-value, key)
```

**Components:**
1. **f-value** = `g + h` - Total estimated cost (primary sorting key)
2. **priority_cached** = `int(not is_cached)` - Non-cached (1) before cached (0)
3. **priority_bounded** = `int(not is_bounded)` - Non-bounded (1) before bounded (0)
4. **h-value** = `h` - Heuristic value (tie-breaker)
5. **key** = StateBase identifier (final tie-breaker)

**Ordering Logic:**
- States with lower f-values explored first (best-first search)
- Among equal f-values: non-cached preferred over cached
- Among equal cache status: non-bounded preferred over bounded
- Among equal bound status: lower h-values preferred
- Among equal h-values: key order determines final ordering

## Design Philosophy

### f-value Priority
The primary ordering criterion `f = g + h` implements best-first search:
- **g**: Actual cost from start (known, exact)
- **h**: Estimated cost to goal (heuristic, approximate)
- **f**: Total estimated cost through this state

This enables informed search algorithms like A* to prioritize promising paths.

### Cache and Bound Flags
These flags support advanced search features:

**is_cached:**
- Indicates if this cost was computed from cached information
- Non-cached costs preferred (more up-to-date)
- Useful for incremental or dynamic search

**is_bounded:**
- Indicates if this cost has bounds/constraints
- Non-bounded costs preferred (more general)
- Useful for constrained pathfinding

### Tie-Breaking Strategy
The multi-level tie-breaking ensures deterministic behavior:
1. Prefer lower total cost (f)
2. Prefer fresh over cached
3. Prefer general over bounded
4. Prefer closer to goal (h)
5. Use state identity (key)

## Usage in Search Algorithms

### A* Algorithm
```python
# Create cost for start state
cost_start = Cost(key=start, g=0, h=heuristic(start))

# Create cost for successor
g_new = g_current + step_cost
h_new = heuristic(successor)
cost_successor = Cost(key=successor, g=g_new, h=h_new)

# Compare costs (via key_comparison)
if cost_successor < cost_current:
    # Update state in priority queue
```

### Dijkstra Algorithm
```python
# Dijkstra uses h=0, so f=g
cost = Cost(key=state, g=path_cost, h=0)
```

### Priority Queue
```python
# Generated queue uses Cost for ordering
generated.push(state, cost)
best_state = generated.pop()  # Returns state with minimum cost
```

## Comparison Behavior

Costs are compared using the `key_comparison()` tuple via the `Comparable` mixin:
```python
cost1 < cost2  # True if cost1.key_comparison() < cost2.key_comparison()
```

**Example:**
```
cost1 = Cost(key=A, g=10, h=5)  → (15, 1, 1, 5, A)
cost2 = Cost(key=B, g=12, h=3)  → (15, 1, 1, 3, B)

cost1 vs cost2: (15, 1, 1, 5, A) > (15, 1, 1, 3, B)
→ cost2 < cost1 (B has lower h-value)
```

## Relationship to Other Classes

- **StateBase**: Cost references a StateBase via its key
- **Generated**: Uses Cost to order States in priority queue
- **AlgoSearch**: Creates and updates Cost objects during search
- **Heuristic functions**: Provide h-values for Cost creation

## Properties

### Immutability
Once created, Cost objects are effectively immutable:
- No public methods to modify g, h, key, or flags
- Updates require creating a new Cost object
- Ensures consistency in priority queue

### Type Safety
Generic `Key` parameter ensures:
- Type consistency with StateBase keys
- Compile-time type checking
- Flexible key types (cells, coordinates, indices, etc.)

## Performance

- **Creation**: O(1) - Simple attribute assignment
- **Comparison**: O(1) - Tuple comparison (assuming key comparison is O(1))
- **Memory**: Minimal - 3 ints + 2 bools + 1 key reference

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## Advanced Features

### Cached Costs
The `is_cached` flag supports scenarios where:
- Costs are precomputed and stored
- Incremental search reuses previous computations
- Dynamic environments update cached values

**Priority**: Fresh computations preferred over cached

### Bounded Costs
The `is_bounded` flag supports scenarios where:
- Costs have constraints or limits
- Search space has regions with different properties
- Constrained pathfinding with resource limits

**Priority**: General costs preferred over bounded

## Common Use Cases

1. **Standard A***: `Cost(key, g, h, False, False)`
2. **Dijkstra**: `Cost(key, g, 0, False, False)`
3. **Cached state**: `Cost(key, g, h, True, False)`
4. **Bounded search**: `Cost(key, g, h, False, True)`

## Example Values

```
StateBase at (5, 3) with g=10, h=7:
Cost = (key=(5,3), g=10, h=7, is_cached=False, is_bounded=False)
key_comparison = (17, 1, 1, 7, (5,3))

StateBase at (6, 4) with g=12, h=5:
Cost = (key=(6,4), g=12, h=5, is_cached=False, is_bounded=False)
key_comparison = (17, 1, 1, 5, (6,4))

→ Second state preferred (same f=17, but lower h=5)
```
