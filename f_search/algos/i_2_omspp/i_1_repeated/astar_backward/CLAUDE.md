# AStarRepeatedBackward - Backward K x A* for OMSPP

## Purpose
Baseline backward algorithm for OMSPP. Reverses each sub-problem
(Gi→S) and runs independent A* searches. No information sharing
between sub-searches — serves as a baseline for comparing against
`AStarIncrementalBackward` (which accumulates cached/bounded
heuristics across sub-searches).

## Public API

### `__init__(self, problem: ProblemOMSPP, name: str = 'AStarRepeatedBackward', need_path: bool = False, is_analytics: bool = False) -> None`
Initialize with an OMSPP problem.

### `run(self) -> SolutionOMSPP` (inherited)
Execute the algorithm and return the solution.

## Inheritance

```
AlgoSearch
  └─ AlgoOMSPP
       └─ AStarRepeatedBackward
```

## Algorithm

1. Convert OMSPP into k forward SPPs via `to_spps()`.
2. For each sub-problem (S→Gi):
   - Reverse it to (Gi→S).
   - Run standard A* on the reversed problem.
   - Reverse the path back to get (S→Gi).
   - Wrap as a forward `SolutionSPP`.
3. Aggregate into `SolutionOMSPP`.

## Key Difference from Forward AStarRepeated

The forward `AStarRepeated` has a "by the way" optimization: if goal
Gj is explored while searching S→Gi, it extracts that solution for
free (because `g[Gj] = dist(S, Gj)`).

This does **not** apply backward: if Gj is explored while searching
Gi→S, we get `dist(Gi, Gj)`, not `dist(S, Gj)`.

## Dependencies

| Import | Purpose |
|--------|---------|
| `AStar` | Sub-search algorithm |
| `ProblemOMSPP` | Input problem |
| `ProblemSPP` | Sub-problems (reversed) |
| `SolutionSPP` | Per-goal solutions |
| `SolutionOMSPP` | Aggregated solution |
| `AlgoOMSPP` | Base class |

## Tests (`_tester.py`)

| Test | Description |
|------|-------------|
| `test_name_algo` | Solution name matches algorithm |
| `test_without_obstacles` | Stats on 4x4 grid (explored=9, discovered=18) |
| `test_with_obstacles` | Stats on 4x4 grid (explored=15, discovered=26) |
| `test_quality_h_without_obstacles` | quality_h == 1.0 |
| `test_quality_h_with_obstacles` | quality_h == (3/7 + 1.0) / 2 |
| `test_path_start_and_goal` | Paths start at S, end at Gi |
| `test_path_length` | 1000-run stress: same lengths as forward |
