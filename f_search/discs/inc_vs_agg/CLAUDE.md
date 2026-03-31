# inc_vs_agg - Incremental vs Aggregative kA* Discussion

## Purpose
Working directory for comparing two kA* algorithm variants for
OMSPP (One-to-Many Shortest Path Problem), as described in two
related research papers stored on Google Drive.

---

## Source Papers (Google Drive)

Both files are located at Drive path `2026/03`:

| # | Filename | Status | Algorithm |
|---|----------|--------|-----------|
| 1 | `SoCS_2026_paper_5875.pdf` | SoCS candidate | kA* Incremental |
| 2 | `Heuristic_search_for_one_to_many_shortest_path_queries (3).pdf` | Published (journal) | kA* Aggregative |

### How to Read the Papers

```python
from f_google.services.drive import Drive

drive = Drive.Factory.valdas()

# List all PDFs at 2026/03
files = drive.files(path='2026/03')
pdfs = [f for f in files if f.lower().endswith('.pdf')]
# -> ['SoCS_2026_paper_5875.pdf',
#     'Heuristic_search_for_one_to_many_shortest_path_queries (3).pdf']

# Read a paper into memory (returns markdown text + page images)
response = drive.read(path='2026/03/SoCS_2026_paper_5875.pdf')
print(response.text)        # markdown with tables
for i, page in enumerate(response.pages):
    with open(f'/tmp/socs_page_{i}.png', 'wb') as f:
        f.write(page)

response = drive.read(
    path='2026/03/Heuristic_search_for_one_to_many_shortest_path_queries (3).pdf'
)
print(response.text)
```

**Drive path semantics**: `path=None` is the Drive root ("My Drive").
Paths are relative from root, so `2026/03` not `mydrive/2026/03`.

**`drive.read()` returns** a `_ReadResponse` with:
- `.text` — markdown-formatted content (includes tables)
- `.pages` — list of PNG bytes (one per rendered page)

---

## Paper 1: Published Journal Paper (Aggregative kA*)

**File**: `Heuristic_search_for_one_to_many_shortest_path_queries (3).pdf`
**Authors**: Stern et al.
**Status**: Published in journal

### What It Introduces
The **kA* algorithm with aggregative heuristic** for OMSPP.

**Core idea**: Run a single A* search toward all k goals simultaneously.
Each state stores a heuristic vector `h_vec` of size k (one h-value per
goal). An aggregation function **Phi** combines these into a single
scalar:

```
F(n) = g(n) + Phi(h_vec(n), active_goals)
```

**Aggregation functions (Phi)**:
- `min` — admissible, avoids re-expansion (Theorem 1, Corollary 1)
- `max` — consistent but not admissible
- `mean` — consistent and admissible

When a goal is found, it is removed from the active set and F-values of
all frontier states are eagerly recomputed from stored vectors (no
distance recomputation needed).

**Key contribution**: The **Projection** aggregation function — a
specific Phi that projects the multi-goal heuristic space in a way
that guides search efficiently toward all remaining goals.

### Codebase Implementation
- `f_search/algos/i_2_omspp/i_1_aggregative/` — `AStarAggregative`
- `f_search/heuristics/phi/` — `UPhi` (min, max, mean)
- `f_search/ds/data/i_2_heuristics_vector/` — `DataHeuristicsVector`

---

## Paper 2: SoCS Candidate (Incremental kA*)

**File**: `SoCS_2026_paper_5875.pdf`
**Status**: Candidate for SoCS 2026 publication

### What It Introduces
The **kA* Incremental algorithm** for OMSPP.

**Core idea**: Solve k sub-problems sequentially, accumulating heuristic
knowledge from each solved sub-problem to accelerate subsequent ones.

After solving each sub-problem (backward from goal Gi toward start S):
- **Cached** (exact): distances to Gi for states on the optimal path
- **Bounded** (lower bounds): distances for explored non-path states

Future sub-searches use these cached/bounded values as improved
heuristics instead of the default Manhattan distance.

### Codebase Implementation
- `f_search/algos/i_2_omspp/i_1_incremental/` — incremental variants
  - `astar/` — `AStarIncremental` (forward sequential)
  - `astar_backward/` — `AStarIncrementalBackward` (backward, with
    bounds)
  - `bfs/` — `BFSIncremental`
  - `dijkstra/` — `DijkstraIncremental`

---

## Connection Between the Two Papers

The incremental kA* algorithm (SoCS paper) is **closely related** to
the **Projection** aggregation function from the published journal
paper.

### Shared Principle
Both approaches exploit heuristic information gathered while searching
for some goals to improve the search for remaining goals. The
difference is in *how* they structure the search:

| Aspect | Aggregative (Journal) | Incremental (SoCS) |
|--------|----------------------|-------------------|
| **Search structure** | Single unified search | k sequential sub-searches |
| **Heuristic storage** | Vector per state (size k) | Cached/bounded dicts accumulated |
| **Goal removal** | Remove from active set, re-aggregate | Sub-problem completed, move to next |
| **F recomputation** | Eager (recompute all frontier) | Implicit (better h for next search) |
| **Key mechanism** | Phi aggregation function | Heuristic learning across runs |

### Why They Are "Very Similar"
The Projection function in the aggregative approach and the incremental
approach both effectively:
1. Use information from previously found goals
2. Tighten heuristic estimates for remaining goals
3. Reduce the search space for subsequent goal searches

The incremental approach can be viewed as a **sequential unfolding** of
the aggregative Projection — instead of maintaining all goals in one
search and projecting, it solves goals one at a time and carries
forward exact/bounded distances as enhanced heuristics.

---

## Discussion Topics

Key comparison axes for analyzing the two algorithms:

1. **Expansion count**: Which approach explores fewer states total?
2. **Memory usage**: Vector storage (agg) vs accumulated dicts (inc)
3. **Goal ordering sensitivity**: Does the order of goals matter more
   for incremental?
4. **Scalability with k**: How do they scale as number of goals grows?
5. **Grid topology effects**: Obstacles, corridors, open spaces
6. **Theoretical guarantees**: Admissibility, optimality, completeness
7. **Practical runtime**: Wall-clock time differences
8. **Hybrid approaches**: Can elements of both be combined?

### Existing Experimental Infrastructure
- `f_search/experiments/cmp_agg_inc.py` — comparison script
- `f_search/experiments/cmp_agg_inc_detailed.py` — detailed analysis
- `f_search/discs/inc_vs_agg/expansion/` — expansion analysis
