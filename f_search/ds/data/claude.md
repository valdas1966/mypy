# ds/data - Algorithm Data Structures

## Purpose
Contains data structure classes that hold the working state for search algorithms during execution. These classes encapsulate all mutable state needed by algorithms to track exploration progress.

## Structure

- **i_0_base/** - `DataSearch` - Base data container for all search algorithms
- **i_1_spp/** - `DataSPP` - Data container for SPP algorithms (currently extends base)
- **i_2_omspp/** - `DataOMSPP` - Data container for OMSPP algorithms (currently extends base)

## Design Philosophy

### Separation of Concerns
- **Algorithm classes** contain the logic (methods)
- **Data classes** contain the state (attributes)
- This separation enables:
  - Easier testing and debugging
  - State inspection during execution
  - Potential state serialization/checkpointing
  - Clear distinction between algorithm logic and working memory

### Why Not Direct Attributes?
Instead of algorithms having `self._generated`, `self._g`, etc., we group them in `self._data`:

**Benefits:**
- **Cohesion**: All search state in one logical unit
- **Reusability**: Can pass data between algorithm runs (warm-starting)
- **Testability**: Can inspect/mock/initialize state independently
- **Memory management**: Easy to clear all state at once
- **Serialization**: Single object to save/load for checkpointing

**Tradeoff:**
- Slightly more verbose: `self._data.g[state]` vs `self._g[state]`

## Base Class: DataSearch

The foundation for all algorithm data containers.

### Attributes

```python
generated: Generated           # Priority queue of states to explore
explored: set[State]          # Set of fully explored states
best: State                   # Currently best state (last popped from generated)
g: dict[State, int]          # Actual cost from start to each state
h: dict[State, int]          # Heuristic estimate from state to goal
cost: dict[State, Cost]      # Combined cost objects (f = g + h)
parent: dict[State, State]   # Parent pointers for path reconstruction
```

### Lifecycle

1. **Initialization**: `DataSearch()` creates empty data structures
2. **Population**: Algorithm fills structures during search
3. **Query**: Algorithm reads from structures to make decisions
4. **Cleanup**: Data discarded after solution is created

### Usage Pattern

```python
class SomeAlgo(AlgoSearch):
    def run(self):
        data = self._data

        # Add start state
        data.g[start] = 0
        data.h[start] = self._heuristic(start)
        data.cost[start] = Cost(g=0, h=data.h[start])
        data.generated.push(start, data.cost[start])

        # Main loop
        while data.generated:
            data.best = data.generated.pop()
            data.explored.add(data.best)
            # ... explore successors
```

## Derived Classes

### DataSPP (i_1_spp)
**One-to-One Shortest Path Problem Data**

Currently a simple pass-through of `DataSearch` (no additional attributes). Exists for:
- Type safety (algorithms work with `DataSPP` specifically)
- Future extensibility (can add SPP-specific state if needed)
- Clear semantic distinction

### DataOMSPP (i_2_omspp)
**One-to-Many Shortest Path Problem Data**

Currently a simple pass-through of `DataSearch`. The KxAStar algorithm doesn't use shared data across sub-problems, so this is mostly for type consistency.

**Future possibilities:**
- Shared explored set across goals
- Cached heuristics for multiple goals
- Global state for more sophisticated OMSPP algorithms

## Key Design Decisions

### Why Mutable Public Attributes?
The data classes use public attributes (not properties) because:
- Algorithms need fast, direct access to mutate state
- These are internal data structures, not public API
- No business logic or validation needed on access
- Simplicity and performance over encapsulation

### Why Not Properties/Getters?
Adding `@property` decorators would:
- Add overhead without benefit (no logic to encapsulate)
- Make syntax more verbose for no gain
- Complicate mutation (need setters)

### Why Not Dataclasses?
We don't use `@dataclass` because:
- Need custom initialization logic
- Explicit attribute initialization is clearer
- More control over type annotations
- No need for auto-generated `__init__`, `__repr__`, etc.

## Integration with Algorithms

### Class-Level Specification
Algorithms declare their data type using class attributes:

```python
class AlgoSearch:
    cls_data = DataSearch

class AlgoSPP(AlgoSearch):
    cls_data = DataSPP
```

### Initialization
Base algorithm class creates data instance:

```python
# In AlgoSearch.__init__:
self._data = data if data else self.cls_data()
```

### Aliasing Pattern
For convenience, algorithms often alias data at method level:

```python
def _explore(self):
    data = self._data  # Short alias

    data.explored.add(data.best)
    for succ in self._problem.successors(data.best):
        if succ not in data.explored:
            # ... generate state
```

## Related Components

- **Generated** (ds/generated): Priority queue for open list
- **State** (ds/state): Search state representation
- **Cost** (ds/cost): Cost object with f-value comparison
- **AlgoSearch** (algos/i_0_base): Base algorithm that uses data
- **Stats** (stats/): Metrics tracked separately from working data

## State vs Data vs Stats

Understanding the distinction:

| Component | Purpose | Lifetime | Mutability |
|-----------|---------|----------|------------|
| **State** | Represents a search configuration | Created per state, immutable | Immutable |
| **Data** | Working memory during search | Created per algorithm run | Highly mutable |
| **Stats** | Performance metrics | Created with solution | Mutable during run, frozen after |

## Performance Considerations

### Memory
- Dominated by dictionary overhead (g, h, cost, parent maps)
- Typical memory: O(states_generated)
- Can be significant for large search spaces

### Access Patterns
- Frequent reads: `data.best`, `data.g[state]`
- Frequent writes: `data.generated.push()`, `data.explored.add()`
- Direct attribute access minimizes overhead

## Future Extensions

Potential enhancements to data classes:

1. **Checkpointing**: Add `save()` / `load()` methods
2. **Statistics**: Track memory usage, max queue size
3. **Debugging**: Add `snapshot()` for state inspection
4. **Warm-starting**: Initialize from previous run's data
5. **Shared state**: For OMSPP, share explored across goals
6. **Memory optimization**: Use more compact representations
