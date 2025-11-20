# i_1_spp - SPP Algorithm Data Structure

## Purpose
Defines `DataSPP`, the data container for One-to-One Shortest Path Problem (SPP) algorithms.

## Class: DataSPP

### Overview
`DataSPP` is currently a simple pass-through class that extends `DataSearch` without adding additional attributes. It exists primarily for type safety and future extensibility.

```python
class DataSPP(DataSearch):
    """
    Data for One-to-One Shortest-Path-Problem.
    """
    pass
```

### Why a Separate Class?

Even though it doesn't add functionality currently, `DataSPP` provides:

1. **Type Safety**
   - SPP algorithms declare `cls_data = DataSPP`
   - Type system ensures SPP algorithms work with SPP data
   - Prevents mixing SPP and OMSPP data accidentally

2. **Semantic Clarity**
   - Makes code intention explicit
   - Clear distinction between generic search and SPP-specific
   - Self-documenting code

3. **Future Extensibility**
   - Can add SPP-specific attributes without breaking base class
   - Examples: single-goal-specific optimizations, specialized caching

4. **API Stability**
   - If we add SPP-specific features later, no API changes needed
   - Algorithms already depend on the right type

### Inherited Attributes

From `DataSearch`:
- `generated: Generated` - Priority queue of open states
- `explored: set[State]` - Set of closed states
- `best: State` - Currently best state
- `g: dict[State, int]` - Actual costs from start
- `h: dict[State, int]` - Heuristic estimates to goal
- `cost: dict[State, Cost]` - Combined cost objects
- `parent: dict[State, State]` - Parent pointers for paths

### Usage in SPP Algorithms

```python
class AStar(AlgoSPP):
    cls_data = DataSPP  # Type specification

    def run(self) -> SolutionSPP:
        data = self._data  # Type: DataSPP

        # Initialize with start
        data.g[start] = 0
        data.h[start] = self._heuristic(start)
        data.cost[start] = Cost(g=0, h=data.h[start])
        data.generated.push(start, data.cost[start])

        # Main search loop
        while data.generated:
            data.best = data.generated.pop()

            if data.best == self._problem.goal:
                return self._create_solution(is_valid=True)

            data.explored.add(data.best)
            # ... explore successors
```

### Potential Future Extensions

SPP-specific attributes that could be added:

1. **Goal-Specific Optimizations**
   ```python
   self.goal_state: State  # Cache goal for fast comparison
   self.min_h_seen: int    # Track minimum h-value seen
   ```

2. **Bidirectional Search Support**
   ```python
   self.forward_data: DataSearch  # Forward search from start
   self.backward_data: DataSearch # Backward search from goal
   self.meeting_point: State      # Where searches meet
   ```

3. **Pathfinding Caching**
   ```python
   self.distance_cache: dict[tuple[State, State], int]
   ```

4. **Memory Optimization**
   ```python
   self.pruned_count: int  # Track pruned states for analysis
   ```

### Design Pattern: Placeholder Classes

This is a common design pattern where:
- Base class provides core functionality
- Derived classes exist for type differentiation
- Functionality added incrementally as needed
- Alternative to complex conditionals in base class

**Benefits:**
- Clean type hierarchy
- No if-then logic based on problem type
- Easy to specialize later
- Clear separation of concerns

**Tradeoff:**
- Slightly more classes
- May seem over-engineered if never specialized
- Worth it for type safety and clarity

### Related Components

- **DataSearch** (ds/data/i_0_base): Base class with all attributes
- **AlgoSPP** (algos/i_1_spp/i_0_base): Base algorithm using this data
- **AStar** (algos/i_1_spp/i_1_astar): Concrete algorithm using this data
- **Dijkstra** (algos/i_1_spp/i_2_dijkstra): Another algorithm using this data

### Comparison with DataOMSPP

| Aspect | DataSPP | DataOMSPP |
|--------|---------|-----------|
| **Problem Type** | Single goal | Multiple goals |
| **Base Class** | DataSearch | DataSearch |
| **Current Extensions** | None | None |
| **Future Possibilities** | Goal caching | Shared explored set |
| **Algorithm Examples** | AStar, Dijkstra | KxAStar |

## Type System Integration

### Class-Level Declaration
```python
class AlgoSPP:
    cls_stats = StatsSPP
    cls_data = DataSPP  # Declares data type
```

### Runtime Instantiation
```python
# In AlgoSearch.__init__:
self._data = data if data else self.cls_data()
# Creates DataSPP() for SPP algorithms
```

### Type Checking
Static type checkers can verify:
- SPP algorithms work with DataSPP
- No mixing of SPP and OMSPP data
- Correct attribute access patterns
