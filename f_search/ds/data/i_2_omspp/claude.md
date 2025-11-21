# i_2_omspp - OMSPP Algorithm Data Structure

## Purpose
Defines `DataOMSPP`, the data container for One-to-Many Shortest Path Problem (OMSPP) algorithms.

## Class: DataOMSPP

### Overview
`DataOMSPP` is currently a simple pass-through class that extends `DataSearch` without adding additional attributes. It exists for type safety and future multi-goal optimizations.

```python
class DataOMSPP(DataSearch):
    """
    Data for One-to-Many Shortest-Path-Problem.
    """
    pass
```

### Why a Separate Class?

Even though it doesn't add functionality currently, `DataOMSPP` provides:

1. **Type Safety**
   - OMSPP algorithms declare `cls_data = DataOMSPP`
   - Type system distinguishes OMSPP from SPP data
   - Prevents type confusion in multi-goal context

2. **Semantic Clarity**
   - Explicit intent: data for multi-goal problems
   - Self-documenting algorithm requirements
   - Clear distinction from single-goal SPP

3. **Future Extensibility**
   - Room for multi-goal-specific optimizations
   - Can add shared state across goals
   - No API changes when features added

### Inherited Attributes

From `DataSearch`:
- `generated: Generated` - Priority queue of open states
- `explored: set[StateBase]` - Set of closed states
- `best: StateBase` - Currently best state
- `g: dict[StateBase, int]` - Actual costs from start
- `h: dict[StateBase, int]` - Heuristic estimates to goals
- `cost: dict[StateBase, Cost]` - Combined cost objects
- `parent: dict[StateBase, StateBase]` - Parent pointers for paths

### Current Usage: KxAStar

The KxAStar algorithm (K × A*) currently doesn't use shared data:

```python
class KxAStar(AlgoOMSPP):
    cls_data = DataOMSPP

    def run(self) -> SolutionOMSPP:
        sub_solutions = {}
        sub_problems = self._problem.to_spps()

        # Runs separate A* for each goal
        for sub_problem in sub_problems:
            astar = AStar(problem=sub_problem)  # Separate data per goal
            sub_solutions[sub_problem.goal] = astar.run()

        return self._create_solution(is_valid=True,
                                     sub_solutions=sub_solutions)
```

**Note:** Each sub-problem gets its own `DataSPP` instance. The `DataOMSPP` instance in KxAStar isn't currently utilized during the search.

### Future Extensions for Multi-Goal Algorithms

More sophisticated OMSPP algorithms could leverage shared data:

1. **Shared Explored Set**
   ```python
   self.shared_explored: set[StateBase]  # Common across all goals
   # Benefit: Don't re-explore states for different goals
   ```

2. **Multi-Goal Heuristics**
   ```python
   self.h_per_goal: dict[StateBase, dict[StateBase, int]]
   # h[state][goal] = heuristic to specific goal
   ```

3. **Goal Tracking**
   ```python
   self.goals: set[StateBase]           # All target goals
   self.goals_reached: set[StateBase]   # Goals found so far
   self.goals_remaining: set[StateBase] # Goals not yet found
   ```

4. **Shared Path Data**
   ```python
   self.paths_to_goals: dict[StateBase, Path]  # Path to each goal found
   ```

5. **Frontier Management**
   ```python
   self.goal_frontiers: dict[StateBase, Generated]
   # Separate frontier per goal for parallel exploration
   ```

### Potential OMSPP Algorithm: Unified Search

A more sophisticated algorithm could use shared data:

```python
class UnifiedOMSPP(AlgoOMSPP):
    cls_data = DataOMSPP

    def run(self) -> SolutionOMSPP:
        data = self._data
        data.goals = set(self._problem.goals)
        data.goals_reached = set()

        # Initialize
        data.g[start] = 0
        data.h[start] = min(dist(start, g) for g in data.goals)
        data.generated.push(start, Cost(g=0, h=data.h[start]))

        # Unified search
        while data.generated and len(data.goals_reached) < len(data.goals):
            data.best = data.generated.pop()

            # Check if goal
            if data.best in data.goals and data.best not in data.goals_reached:
                data.goals_reached.add(data.best)
                # Store path, continue searching for other goals

            data.explored.add(data.best)
            # ... explore successors with multi-goal heuristic

        # Build solution from shared data
        return self._create_solution_from_shared_data()
```

### Design Rationale

#### Why Not Add These Features Now?
- YAGNI (You Ain't Gonna Need It): Don't add complexity until needed
- Current KxAStar works with base DataSearch functionality
- Future algorithms can extend when requirements are clear
- Keeps base implementation simple

#### Why Keep the Class Then?
- Type system benefits exist immediately
- API stability: adding features later won't break interfaces
- Clear signal: "this is for OMSPP algorithms"
- Minimal cost: empty class is essentially free

### Comparison: OMSPP vs SPP Data

| Aspect | DataSPP | DataOMSPP |
|--------|---------|-----------|
| **Goals** | Single goal | Multiple goals |
| **Heuristic** | Distance to one goal | Min/combined distance to goals |
| **Termination** | One goal reached | All goals reached (or best effort) |
| **Path Output** | Single path | Multiple paths (one per goal) |
| **StateBase Sharing** | N/A | Potential for shared explored |
| **Complexity** | Simpler | More complex potential |

### Related Components

- **DataSearch** (ds/data/i_0_base): Base class providing all attributes
- **AlgoOMSPP** (algos/i_2_omspp/i_0_base): Base algorithm using this data
- **KxAStar** (algos/i_2_omspp/i_1_kx_astar): Current implementation (doesn't use shared data)
- **StatsOMSPP** (stats/i_2_omspp): Aggregates stats from multiple goals

### Future Research Directions

Potential OMSPP algorithms that would benefit from shared data:

1. **Best-First Multi-Goal**: Expand toward nearest unvisited goal
2. **Parallel Frontiers**: Maintain separate frontiers per goal
3. **Shared Exploration**: Don't re-explore states for different goals
4. **Adaptive Heuristics**: Adjust h-values based on goals found
5. **Bidirectional Multi-Goal**: Search backward from goals, forward from start

## Type System Integration

### Class-Level Declaration
```python
class AlgoOMSPP:
    cls_stats = StatsOMSPP
    cls_data = DataOMSPP  # Declares OMSPP data type
```

### Prevents Type Confusion
```python
# This is type-safe:
class KxAStar(AlgoOMSPP):
    cls_data = DataOMSPP  # ✓ Correct type for OMSPP

# This would be a type error:
class KxAStar(AlgoOMSPP):
    cls_data = DataSPP  # ✗ Wrong: SPP data for OMSPP algorithm
```
