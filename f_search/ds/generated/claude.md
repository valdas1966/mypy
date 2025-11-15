# Generated - Priority Queue for Generated States

## Main Class
`Generated(Dictable[State, Cost])`

## Inheritance
- **Base Classes:** `Dictable[State, Cost]` (from f_core.mixins)
- **Type Parameters:** Maps `State` keys to `Cost` values

## Purpose
Implements a priority queue for generated states (open list) using a dictionary-based approach. Manages states that have been generated but not yet explored, ordered by their cost/priority. States are retrieved in best-first order (lowest cost first).

## Core Functionality

### Constructor (`__init__`)
Creates an empty Generated queue.

**Implementation:**
- Calls `Dictable.__init__(self)` to initialize internal dictionary
- Internal storage: `_data: dict[State, Cost]`

**Initial State:** Empty queue (no states)

### Queue Operations

#### `push(state: State, cost: Cost)` → `None`
Adds a state to the queue or updates its cost.

**Parameters:**
- **state**: The State to add/update
- **cost**: The Cost object for priority ordering

**Behavior:**
- If state not in queue: Adds new entry
- If state already in queue: Updates to new cost

**Time Complexity:** O(1) - Dictionary insertion/update

**Usage:**
```python
generated = Generated()
generated.push(state, cost)  # Add state
generated.push(state, new_cost)  # Update with better cost
```

**Note:** Caller responsible for checking if new cost is better

#### `pop()` → `State`
Removes and returns the state with lowest cost.

**Returns:** State object with minimum cost value

**Behavior:**
- Finds state with minimum cost in the queue
- Removes it from the queue
- Returns the state

**Time Complexity:** O(n) - Linear search for minimum

**Implementation:**
```python
item_lowest = min(self._data, key=self._data.get)
del self._data[item_lowest]
return item_lowest
```

**Usage:**
```python
best_state = generated.pop()  # Get and remove best state
```

**Note:** Raises exception if queue is empty

## Design Philosophy

### Dictionary-Based Implementation
Uses Python dictionary (`dict[State, Cost]`) rather than heap:

**Advantages:**
- **O(1) push**: Instant add/update operations
- **O(1) contains**: Fast membership testing
- **O(1) update**: Efficient cost updates (common in A*)
- **Simple implementation**: Easy to understand and debug
- **Direct access**: Can check/update any state directly

**Disadvantages:**
- **O(n) pop**: Must scan all entries to find minimum
- **Memory overhead**: Dictionary structure overhead

### Trade-off Justification
For search algorithms, especially A*:
- **Updates are frequent**: States often updated with better costs
- **Queue size moderate**: For grid problems, n is manageable
- **Simplicity valued**: Research framework prioritizes clarity
- **O(1) update >> O(log n) pop**: Update frequency dominates

**Alternative (Heap-based):**
- O(log n) pop, O(log n) push
- O(n) update (must find and update in heap)
- More complex implementation

**Design choice:** Dictionary approach better for this use case

## Usage in Search Algorithms

### Initialization
```python
def _run_pre(self):
    self._generated = Generated()
    # Add start state
    self._generated.push(start, cost_start)
```

### Main Search Loop
```python
while self._generated:  # While not empty
    # Get best state
    best = self._generated.pop()

    # Check termination
    if best == goal:
        return solution

    # Explore state
    for successor in successors(best):
        if successor not in explored:
            # Calculate new cost
            g_new = g[best] + step_cost
            cost_new = Cost(key=successor, g=g_new, h=h(successor))

            # Add or update
            if successor not in self._generated:
                self._generated.push(successor, cost_new)
                counters['GENERATED'] += 1
            elif cost_new < cost_old:
                self._generated.push(successor, cost_new)
                counters['UPDATED'] += 1
```

### State Update Pattern
```python
# Check if state already generated
if state in self._generated:
    # Compare costs
    old_cost = self._generated._data[state]  # Direct access
    if new_cost < old_cost:
        # Update with better cost
        self._generated.push(state, new_cost)
```

## Dictionary Interface (via Dictable)

From `Dictable` mixin, the class inherits:
- `__contains__`: Membership testing (`state in generated`)
- `__len__`: Queue size (`len(generated)`)
- `__bool__`: Empty check (`if generated:`)
- Direct access to `_data` dictionary

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|------------|-------|
| **push** | O(1) | Dictionary insert/update |
| **pop** | O(n) | Linear search for minimum |
| **contains** | O(1) | Dictionary lookup |
| **update** | O(1) | Same as push |
| **size** | O(1) | Dictionary length |

### Expected Performance
For grid pathfinding with n states in queue:
- **A* typical case**: n = O(solution_depth × branching_factor)
- **Grid 2D**: branching_factor ≈ 4 (up, down, left, right)
- **Moderate grids**: n < 10,000 → O(n) pop acceptable

## Comparison with Heap Implementation

| Aspect | Dictionary (Current) | Binary Heap |
|--------|---------------------|-------------|
| **push** | O(1) | O(log n) |
| **pop** | O(n) | O(log n) |
| **update** | O(1) | O(n) or O(log n)* |
| **Implementation** | Simple | Complex |
| **A* suitability** | Good (frequent updates) | Fair (infrequent updates) |

*Heap update: O(n) to find, O(log n) to fix; or O(log n) with index tracking

## Relationship to Other Classes

- **State**: Keys in the queue (what we're storing)
- **Cost**: Values in the queue (how we order states)
- **AlgoSearch**: Uses Generated as `_generated` open list
- **AStar/Dijkstra**: Pop states, push successors, update costs

## Key Invariants

1. **No duplicates**: Each state appears at most once
2. **Best-first**: pop() always returns minimum cost state
3. **Consistency**: Cost for each state reflects current best path
4. **Non-empty pop**: pop() should only be called when queue not empty

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## Common Patterns

### Check Before Pop
```python
if generated:  # Not empty
    state = generated.pop()
```

### Conditional Update
```python
if state not in generated:
    generated.push(state, cost)
else:
    old_cost = generated._data[state]
    if cost < old_cost:
        generated.push(state, cost)
```

### Queue Size Monitoring
```python
max_queue_size = 0
while generated:
    max_queue_size = max(max_queue_size, len(generated))
    state = generated.pop()
    # ... process state
```

### Empty Check
```python
while generated:  # While queue not empty
    # Process states
```

## Example Usage

```python
# Create queue
generated = Generated()

# Add start state
start_cost = Cost(key=start, g=0, h=10)
generated.push(start, start_cost)

# Main loop
while generated:
    # Get best state
    current = generated.pop()

    # Generate successors
    for neighbor in neighbors(current):
        g_new = g[current] + 1
        h_new = heuristic(neighbor)
        cost_new = Cost(key=neighbor, g=g_new, h=h_new)

        # Add or update
        if neighbor not in explored:
            if neighbor not in generated:
                generated.push(neighbor, cost_new)
            else:
                if cost_new < generated._data[neighbor]:
                    generated.push(neighbor, cost_new)
```

## Future Optimizations

Potential improvements for larger problems:
1. **Heap-based implementation**: O(log n) pop
2. **Fibonacci heap**: O(1) amortized update
3. **Bucket queue**: For integer costs
4. **Lazy deletion**: Mark deleted, skip when popped

**Current design rationale:** Simplicity and O(1) updates more valuable for research framework and typical problem sizes.
