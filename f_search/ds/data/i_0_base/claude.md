# i_0_base - Base Algorithm Data Structure

## Purpose
Defines `DataSearch`, the base data container class that holds all working state for search algorithms during execution.

## Class: DataSearch

### Overview
`DataSearch` encapsulates all mutable state that search algorithms need to track their progress. This includes the open list (generated), closed list (explored), cost mappings, and parent pointers for path reconstruction.

### Attributes

#### generated: Generated
- **Type**: Priority queue of states waiting to be explored
- **Purpose**: Open list - states discovered but not yet expanded
- **Operations**:
  - `push(state, cost)` - Add/update state with priority
  - `pop()` - Remove and return lowest f-value state
  - `state in generated` - Check membership
- **Implementation**: Dictionary-based priority queue (O(1) push, O(n) pop)

#### explored: set[StateBase]
- **Type**: Set of fully explored states
- **Purpose**: Closed list - states already expanded
- **Operations**:
  - `add(state)` - Mark state as explored
  - `state in explored` - Check if already explored
- **Why set?**: Fast O(1) membership checking

#### best: StateBase | None
- **Type**: Current best state (or None initially)
- **Purpose**: Tracks the most recently popped state from generated
- **Usage**:
  - Used as parent when generating successors
  - Checked in termination condition
  - Provides context for current exploration

#### g: dict[StateBase, int]
- **Type**: Mapping from states to actual costs
- **Purpose**: Tracks g-value (actual cost from start to state)
- **Values**:
  - Start state: `g[start] = 0`
  - Other states: `g[state] = g[parent] + edge_cost`
- **Updates**: When better path to state is found

#### h: dict[StateBase, int]
- **Type**: Mapping from states to heuristic estimates
- **Purpose**: Tracks h-value (estimated cost from state to goal)
- **Values**: Computed by `_heuristic(state)` method
- **Properties**:
  - Should be admissible (never overestimate)
  - Manhattan distance for grid pathfinding

#### cost: dict[StateBase, Cost]
- **Type**: Mapping from states to Cost objects
- **Purpose**: Stores combined cost for priority queue
- **Structure**: `Cost(key=state, g=g_value, h=h_value)`
- **f-value**: Computed as `g + h` inside Cost object
- **Why separate?**: Cost objects handle comparison for priority queue

#### parent: dict[StateBase, StateBase]
- **Type**: Mapping from states to their parent states
- **Purpose**: Enables path reconstruction from goal back to start
- **Updates**: Set when state is first generated or updated with better path
- **Usage**: After goal found, follow parents backward to reconstruct path

### Initialization

```python
def __init__(self) -> None:
    self.generated = Generated()
    self.explored = set()
    self.best = None
    self.g = dict()
    self.h = dict()
    self.cost = dict()
    self.parent = dict()
```

All structures start empty, ready to be populated during algorithm execution.

### Typical Algorithm Flow

1. **Initialization**:
   ```python
   data.g[start] = 0
   data.h[start] = heuristic(start)
   data.cost[start] = Cost(g=0, h=data.h[start])
   data.generated.push(start, data.cost[start])
   data.parent[start] = None
   ```

2. **Main Loop**:
   ```python
   while data.generated:
       data.best = data.generated.pop()
       if is_goal(data.best):
           return success
       data.explored.add(data.best)
       # ... explore successors
   ```

3. **Successor Generation**:
   ```python
   for succ in successors(data.best):
       if succ in data.explored:
           continue

       g_new = data.g[data.best] + 1

       if succ not in data.generated:
           # New state
           data.parent[succ] = data.best
           data.g[succ] = g_new
           data.h[succ] = heuristic(succ)
           data.cost[succ] = Cost(g=g_new, h=data.h[succ])
           data.generated.push(succ, data.cost[succ])
       elif g_new < data.g[succ]:
           # Better path found
           data.parent[succ] = data.best
           data.g[succ] = g_new
           data.cost[succ] = Cost(g=g_new, h=data.h[succ])
           data.generated.push(succ, data.cost[succ])
   ```

4. **Path Reconstruction**:
   ```python
   path = []
   state = data.best  # Goal state
   while state is not None:
       path.append(state)
       state = data.parent.get(state)
   path.reverse()
   ```

### Memory Complexity

- **Best case**: O(d) where d = solution depth (straight path to goal)
- **Worst case**: O(b^d) where b = branching factor (explore entire space)
- **Typical**: Depends on heuristic quality and branching factor
- **Dominated by**: g, h, cost, parent dictionaries (4 dicts × states)

### Design Rationale

#### Why Dictionaries Instead of StateBase Attributes?
- States are immutable and shared across algorithms
- Need to track different costs/parents for same state in different runs
- Allows multiple algorithms to work on same problem simultaneously
- Cleaner separation of state identity vs. algorithm-specific data

#### Why Separate g, h, cost?
- Could store everything in cost object, but:
- Frequent access to g-values for comparison
- Heuristic computation happens once, referenced multiple times
- Explicit separation makes algorithm logic clearer
- Small memory overhead for significant code clarity

#### Why best Attribute?
- Could re-compute from context, but:
- Used frequently (every successor generation)
- Explicit storage makes code more readable
- Minimal memory cost (single reference)
- Provides clear "current focus" for algorithm

### Integration Points

- **AlgoSearch**: Creates and manages DataSearch instance
- **Generated**: Priority queue implementation (ds/generated)
- **StateBase**: Search state representation (ds/state)
- **Cost**: Cost object with f-value (ds/cost)

### Testing Considerations

DataSearch is easily testable in isolation:

```python
def test_data_initialization():
    data = DataSearch()
    assert len(data.generated) == 0
    assert len(data.explored) == 0
    assert data.best is None
    assert len(data.g) == 0
```

```python
def test_data_population():
    data = DataSearch()
    state = StateBase(key=Cell(x=0, y=0))

    data.g[state] = 0
    data.h[state] = 10
    data.cost[state] = Cost(g=0, h=10)
    data.generated.push(state, data.cost[state])

    assert state in data.generated
    assert data.g[state] == 0
    assert data.h[state] == 10
```

## Related Components

- **Generated** (ds/generated): Priority queue for open list
- **StateBase** (ds/state): Immutable state representation
- **Cost** (ds/cost): Cost object with f-value comparison
- **AlgoSearch** (algos/i_0_base): Algorithm that uses this data
