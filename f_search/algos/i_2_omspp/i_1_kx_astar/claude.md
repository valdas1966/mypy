# KxAStar - K Times A* Algorithm for OMSPP

## Main Class
`KxAStar(AlgoOMSPP)`

## Inheritance
- **Base Classes:** `AlgoOMSPP[ProblemOMSPP, SolutionOMSPP]`
- **Inherits From:**
  - `AlgoOMSPP`: OMSPP-specific algorithm base
  - `AlgoSearch`: Core search data structures
  - `Algo`: Generic algorithm framework

## Purpose
Implements a naive approach to solving One-to-Many Shortest Path Problems by decomposing them into multiple One-to-One problems and running A* independently for each goal. The name "K×A*" reflects that it runs A* algorithm K times, where K is the number of goals.

## Functionality from Base Classes
From `AlgoOMSPP` and `AlgoSearch`:
- Algorithm lifecycle management
- Type safety for multi-goal problems
- Statistics tracking infrastructure

## Specialized Functionality

### Algorithm Strategy
**Decompose → Solve → Aggregate**

The algorithm follows a three-phase approach:
1. **Decomposition**: Convert OMSPP into k independent SPP sub-problems
2. **Independent Solving**: Execute A* for each sub-problem separately
3. **Aggregation**: Combine all results into a single OMSPP solution

### Core Algorithm Flow

#### 1. Initialization (`_run_pre()`)
Prepares data structures for multi-goal solving:
- Calls parent initialization
- Creates `_sub_problems`: List to store k SPP problems
- Creates `_sub_solutions`: Dictionary mapping goals to their solutions
- Initializes aggregate counters: GENERATED, UPDATED, EXPLORED (all to 0)

#### 2. Main Execution (`run()`)
Orchestrates the three-phase process:
```
1. _run_pre() - Initialize
2. _create_sub_problems() - Decompose into k SPP
3. _solve_sub_problems() - Run A* for each
4. _create_solution() - Aggregate results
```

#### 3. Sub-Problem Creation (`_create_sub_problems()`)
Converts the OMSPP into k SPP problems:
- Extracts start, grid, and goals from the OMSPP problem
- For each goal in goals:
  - Creates `ProblemSPP(grid, start, goal)`
  - Adds to `_sub_problems` list
- Result: k independent single-goal problems

#### 4. Sub-Problem Solving (`_solve_sub_problems()`)
Executes A* independently for each goal:
- For each sub-problem in `_sub_problems`:
  - Creates `AStar(problem=sub_problem, verbose=False)`
  - Runs algorithm: `solution = astar.run()`
  - Stores solution indexed by goal: `_sub_solutions[goal] = solution`
  - If solution valid: aggregates counters (GENERATED, UPDATED, EXPLORED)
- Result: Dictionary of goal → solution mappings

#### 5. Statistics Calculation (`_calc_stats()`)
Computes both aggregate and per-goal metrics:
- **Aggregate stats**: Totals across all sub-problems
  - `elapsed`: Total execution time
  - `generated`: Sum of all generated states
  - `updated`: Sum of all updated states
  - `explored`: Sum of all explored states
- **Per-goal stats**: Individual metrics for each goal
  - `elapsed_per_goal[goal]`: Time for this goal's A* run
  - `generated_per_goal[goal]`: States generated for this goal
  - `updated_per_goal[goal]`: States updated for this goal
  - `explored_per_goal[goal]`: States explored for this goal
- Returns `StatsOMSPP` with all metrics

#### 6. Solution Creation (`_create_solution()`)
Aggregates all sub-solutions into final result:
- Calls `_run_post()` to finalize statistics
- Extracts paths from all valid sub-solutions
- Determines overall validity:
  - Valid only if ALL sub-problems have valid solutions
  - Invalid if any goal unreachable
- Returns `SolutionOMSPP(is_valid, stats, paths)`

### Data Structures

#### `_sub_problems: list[ProblemSPP]`
List of k SPP problems, one per goal.

#### `_sub_solutions: dict[State, SolutionSPP]`
Maps each goal state to its A* solution.

#### Aggregate Counters
Tracks totals across all A* runs:
- `GENERATED`: Total states generated
- `UPDATED`: Total states updated
- `EXPLORED`: Total states explored

## Algorithm Characteristics

### Advantages
1. **Simplicity**: Straightforward decomposition approach
2. **Correctness**: Each path is optimal (A* guarantees)
3. **Modularity**: Reuses existing A* implementation
4. **Independence**: Sub-problems can be parallelized
5. **Baseline**: Good benchmark for sophisticated algorithms

### Disadvantages
1. **Redundancy**: Explores overlapping regions k times
2. **Inefficiency**: No information sharing between runs
3. **Scalability**: Linear cost growth with number of goals
4. **Waste**: Duplicate work in shared search spaces
5. **Suboptimal**: Overall computational cost not minimized

## Performance Analysis

### Time Complexity
- **Best case**: O(k × A*_best) where goals are far apart
- **Average case**: O(k × A*_avg)
- **Worst case**: O(k × A*_worst) where goals overlap significantly

### Space Complexity
- O(k × V) where V is number of vertices (states)
- Each A* run uses O(V) space independently

### Redundancy Factor
- **High overlap**: Waste approaching (k-1) × shared_work
- **Low overlap**: Waste minimal, approach is reasonable

## Optimality

**Path Optimality**: Yes (each path is optimal via A*)
**Computational Optimality**: No (redundant work not minimized)

## Use Cases

**When to Use:**
- Quick baseline implementation
- Small number of goals (k ≤ 5)
- Goals are far apart (minimal overlap)
- Prototyping and benchmarking

**When to Avoid:**
- Large number of goals (k > 10)
- Goals are clustered (high overlap)
- Performance critical applications
- Need computational efficiency

## Comparison with Potential Alternatives

| Algorithm | Strategy | Redundancy | Complexity | Status |
|-----------|----------|------------|------------|---------|
| **KxAStar** | k independent A* | High | O(k × A*) | Implemented |
| Multi-goal A* | Single search tree | Low | O(A*) | Future work |
| Incremental A* | Builds on previous | Medium | O(k × A*/k) | Future work |

## Example Execution

Given: Start S, Goals {G1, G2, G3}

**Phase 1: Decompose**
- Sub-problem 1: S → G1
- Sub-problem 2: S → G2
- Sub-problem 3: S → G3

**Phase 2: Solve**
- Run A*(S → G1) → path₁, stats₁
- Run A*(S → G2) → path₂, stats₂
- Run A*(S → G3) → path₃, stats₃

**Phase 3: Aggregate**
- paths = {G1: path₁, G2: path₂, G3: path₃}
- stats = aggregate(stats₁, stats₂, stats₃) + per-goal tracking
- is_valid = all solutions valid
- Return SolutionOMSPP(is_valid, stats, paths)

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## Future Improvements

Potential optimizations:
1. **Parallelization**: Run A* instances concurrently
2. **Early termination**: Stop if any goal unreachable
3. **State caching**: Share explored states across runs
4. **Heuristic adaptation**: Use multi-goal aware heuristics
5. **Incremental solving**: Build each solution on previous ones
