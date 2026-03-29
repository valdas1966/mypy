# UPhi - Heuristic Aggregation Functions

## Purpose
Static utility class providing Phi aggregation functions for kA* algorithms. Each function takes a heuristic vector `h_vec` (size k, one h per goal) and a list of `active` goal indices, and returns a single aggregated heuristic value.

## Public API

### `UPhi.min(h_vec: list[int], active: list[int]) -> int`
Return the minimum h-value among active goals. Admissible and re-expansion-avoiding with consistent heuristics (Theorem 1, Corollary 1 from Stern et al.).

### `UPhi.max(h_vec: list[int], active: list[int]) -> int`
Return the maximum h-value among active goals. Consistent but NOT admissible with admissible heuristics. Re-expansion-avoiding.

### `UPhi.mean(h_vec: list[int], active: list[int]) -> int`
Return the floored mean h-value among active goals. Consistent and admissible. Re-expansion-avoiding.

### `PhiFunc = Callable[[list[int], list[int]], int]`
Type alias for Phi function signatures. Used to parameterize `AStarAggregative`.

## Inheritance (Hierarchy)
No inheritance. `UPhi` is a static utility class (no instances).

## Dependencies
Only `typing.Callable` for the `PhiFunc` type alias.

## Usage Example

```python
from f_search.heuristics.phi import UPhi, PhiFunc

h_vec = [3, 5, 7]         # distances to 3 goals
active = [0, 2]            # goals 0 and 2 still active

UPhi.min(h_vec, active)    # 3
UPhi.max(h_vec, active)    # 7
UPhi.mean(h_vec, active)   # 5

# Pass as parameter to AStarAggregative
algo = AStarAggregative(problem=problem, phi=UPhi.min)
```
