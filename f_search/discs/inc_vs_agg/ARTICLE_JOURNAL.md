

# ARTICLE_JOURNAL.md - Heuristic Search for One-to-Many Shortest Path Queries

**Authors**: Roni Stern, Meir Goldenberg, Abdallah Saffidine, Ariel Felner
**Status**: Published (journal)
**File**: `Heuristic_search_for_one_to_many_shortest_path_queries (3).pdf`

---

## How to Read the Article

```python
from f_google.services.drive import Drive

drive = Drive.Factory.valdas()
response = drive.read(
    path='2026/03/Heuristic_search_for_one_to_many_shortest_path_queries (3).pdf'
)
print(response.text)        # full markdown with tables
for i, page in enumerate(response.pages):
    with open(f'/tmp/journal_page_{i}.png', 'wb') as f:
        f.write(page)        # PNG per page
```

---

## Quick Navigation (by Section)

| Section | Topic | Key Content |
|---------|-------|-------------|
| 1 | Introduction | OMSPP definition, k*A* vs kA* motivation |
| 2 | Definitions & Background | A* recap, SPP/OMSPP formal defs, notation table |
| 3 | The kA* Algorithm | Pseudocode (Algorithm 3), active goals set A, F_Phi |
| 4 | Aggregating Heuristic Values | **Core theory**: min, max, mean, projection; Theorems 1-4 |
| 4.1 | Consistent Heuristics | Theorem 1: consistency is necessary+sufficient for admissibility |
| 4.2 | Node Re-Expansion | Theorem 2: re-expansion-avoiding condition |
| 4.3 | Admissible Heuristics | Theorem 3: admissibility condition; Theorem 4: non-admissible heuristics |
| 5 | Maintaining Open | Eager vs Lazy kA*; stale F values |
| 5.1 | Lazy kA* | Lazy recomputation; responsible goals (Def 9) |
| 5.2 | General Aggregation | Isotone/antitone (Def 10); Theorem 5 (antitone => best-first) |
| 6 | Resource Analysis | **Expanded nodes, memory, runtime** comparison |
| 6.1 | Expanded Nodes | Surely expanded + surplus (Defs 11-12); Theorems 7-8 |
| 6.2 | Memory | Equations 3-5; kA* stores union of all generated |
| 6.3 | Runtime | Table 2: C_gen, C_h, C_r cost breakdown |
| 7 | Experiments | Grid pathfinding + Pancake puzzle |
| 7.1 | Grid Results | Tables 3-6: expansions and runtime |
| 7.4 | Projection Results | Projection behaves like k*A* with shared Open/Closed |
| 9 | Conclusion | Table 9: summary of all theoretical properties |

---

## Paper Summary

### Problem: OMSPP

The **One-to-Many Shortest Path Problem (OMSPP)**: given a graph G, a
start node s, and k goal nodes t1..tk, find k optimal paths from s to
each goal.

### Two Approaches

1. **k x A***: Run A* independently k times, one per goal. Simple but
   redundant -- nodes may be expanded multiple times across searches.

2. **kA***: A single best-first search toward all k goals. Maintains
   one Open list and one Closed list. Uses a **heuristic aggregation
   function Phi** to combine k heuristic values into one scalar:

   ```
   F_Phi(n) = g(n) + Phi(A, h(n))
   ```

   where A is the set of active (not yet found) goals, and h(n) is
   a k-vector of heuristic estimates to each goal.

### Per-Node Storage: k-Vector Overhead

A critical difference between kA* and k x A*:

- **k x A***: each A*_i stores **1 h-value** per node in its own Open.
  After A*_i finishes, its Open is discarded. Memory per node is
  small.

- **kA* (any Phi, including min)**: stores a **k-vector**
  h(n) = <h_t1(n), ..., h_tk(n)> for every node in Open/Closed.
  This is required because when a goal ti is found and removed from
  the active set, F must be recomputed from the stored vector
  (without re-calling the heuristic functions). The paper
  acknowledges this (Section 6.2) but assumes node representation
  cost dominates the k extra values.

- **kA* with Phi=projection**: the standard Algorithm 3 formulation
  stores the **full k-vector** like any other kA*. However,
  projection only *uses* one goal's heuristic at a time. With
  **Lazy kA* + projection**, one could theoretically store only
  1 h-value per node and compute the new goal's heuristic on demand
  when a stale node is selected -- but the paper does not discuss
  this optimization.

**Impact**: For domains with lightweight node representation (e.g.,
grid cells = just row,col), the k extra floats per node are
significant overhead. For complex state representations, less so.

### kA* Pseudocode (Algorithm 3)

1. Initialize: all goals in active set A, start s in Open
2. Loop: expand node with smallest F_Phi from Open
3. If expanded node is an active goal:
   - Store path, remove goal from A
   - Recompute F values for all nodes in Open (Eager) or defer (Lazy)
   - If A is empty, return all paths
4. Otherwise: standard A* expansion (generate successors, update g)

---

## The Two Main Aggregation Functions

### 1. Phi = min

```
F_min(n) = g(n) + min(h_t1(n), h_t2(n), ..., h_tk(n))  [over active goals]
```

**Properties**:
- **Admissible**: Yes (Theorem 1, Corollary 1) -- guarantees optimal
  paths when heuristics are consistent
- **Consistent aggregation**: Yes
- **Re-expansion-avoiding**: Yes -- never re-expands a node
  (Theorem 2)
- **Surplus avoidance**: Never expands any surplus node for k x A*
  (Theorem 7 part 1). This is **unique to min** -- no other
  admissible Phi has this guarantee.
- **Surely expanded**: Expands all surely expanded nodes of k x A*
  (Theorem 8 part 1)
- **Expanded nodes**: Same set of unique nodes as k x A*, up to tie
  breaking (Corollary 2)
- **Per-node storage**: Full k-vector h(n) = <h_t1(n),...,h_tk(n)>
  stored for every node in Open/Closed. This is k times more per
  node than k x A* (which stores only 1 h-value per node).
- **Memory (total nodes)**: Must store all generated nodes throughout
  the entire search (union of all k individual searches). Worst case:
  Mem(kA*_min) = sum of Mem(A*_i). Best case: Mem(kA*_min) =
  max(Mem(A*_i)).
- **Runtime**: Saves on C_gen (no duplicate expansions) but pays more
  on C_h (computes k heuristics per generated node until first goal
  found, k-1 until second, etc.)
- **Behavior**: Goal-driven search, guided toward nearest active goal.
  Visually, the search "reaches" toward goals (see Fig 8 left).

**When min is best**: Goals are close together (high overlap between
individual A* search spaces), heuristic is cheap to compute, and k
is not too large.

### 2. Phi = projection

```
F_proj(n) = g(n) + h_ti(n)   [where ti is the current target goal]
```

Projection uses **only one goal's heuristic at a time**. It picks a
goal, searches using only that goal's heuristic, and once that goal
is found, switches to the next goal's heuristic. Essentially: k x A*
but sharing Open and Closed between searches.

**Properties**:
- **Admissible**: Yes (Corollary 1) -- consistent aggregation
- **Consistent aggregation**: Yes
- **Re-expansion-avoiding**: Yes
- **Surplus avoidance**: No -- may expand surplus nodes that min
  avoids (Theorem 7 part 2: any admissible Phi != min can expand
  surplus nodes of k x A*)
- **Surely expanded**: Expands all surely expanded nodes (Theorem 8)
- **Expanded nodes**: May expand more nodes than min, because it does
  not benefit from multi-goal guidance. It searches toward one goal
  at a time, potentially exploring nodes irrelevant to other goals.
- **Per-node storage**: Standard kA* formulation stores the full
  k-vector (same as min). But since projection only uses 1 h-value
  at a time, Lazy kA* + projection could theoretically store just
  1 value and compute the new goal's h on demand when stale nodes
  are selected (paper does not discuss this optimization).
- **Memory (total nodes)**: Same as min (shared Open/Closed stores
  the union)
- **Runtime**: Computes only 1 heuristic per node generation (not k),
  so C_h cost is much lower than min. But may generate more nodes.
- **Behavior**: Like k x A* with shared state. Each "phase" searches
  toward one specific goal.

**When projection is best**: Heuristic is expensive to compute (e.g.,
many pivots in differential heuristics). The C_h savings from
computing only 1 heuristic (vs k) can outweigh the extra nodes.

### Min vs Projection: Comparison Table

| Aspect | min | projection |
|--------|-----|------------|
| **Optimality** | Guaranteed (consistent h) | Guaranteed (consistent h) |
| **Node expansions** | Fewer (avoids all surplus) | More (may expand surplus) |
| **Heuristic computations** | k per node (expensive) | 1 per node (cheap) |
| **Runtime (cheap h)** | Better (fewer nodes dominate) | Worse |
| **Runtime (expensive h)** | Worse (k*C_h dominates) | Better |
| **Per-node storage** | k-vector (all h values) | k-vector (standard), but only uses 1 at a time |
| **Memory (total)** | Same (union of generated) | Same (union of generated) |
| **Search character** | Multi-goal guided | Single-goal sequential |
| **Experimental result** | Usually slightly better | Usually slightly worse than min |

---

## Other Aggregation Functions (Brief)

| Phi | Consistent? | Admissible? | Notes |
|-----|-------------|-------------|-------|
| **max** | Yes | No | Not admissible with admissible-only heuristics. Consistent heuristics: admissible but may skip surely-expanded nodes. Behaves like BFS (Fig 8 right). Can expand exponentially fewer nodes than min in contrived cases (Fig 7), but never better in experiments. |
| **mean** | Yes | Yes | Admissible and consistent. In between min and max. |
| **median** | Yes | Yes | Similar to mean. |
| **sum** | No | No | Not consistent, not admissible. Cannot be safely used. Counter-example: Fig 2. |

---

## Key Terminology

### Surely Expanded Nodes (Definition 11)

A node n is **surely expanded** w.r.t. heuristic h if there exists a
path from s to n where all nodes n' on that path (except s, including
n) satisfy:

```
d(s, n') + h(n') < d(s, t)
```

Meaning: n lies on a path where every node looks strictly cheaper than
the optimal goal cost. **Any forward search algorithm MUST expand
these nodes** to guarantee optimality -- there is no way to prove
optimality without looking at them.

With consistent heuristics, simplifies to: n is surely expanded iff
`d(s, n) + h(n) < d(s, t)`.

For k x A*: a node is surely expanded if it is surely expanded for
**at least one** of the k SPPs (Definition 12).

### Surplus Nodes (Definition 11)

A node n is **surplus** if in every path from s to n there exists a
node n' != s such that:

```
d(s, n') > d(s, t)
```

Meaning: n can only be reached through nodes that are already more
expensive than the optimal solution. **No forward search algorithm
needs to expand surplus nodes** -- they can be safely skipped.

With consistent heuristics: n is surplus iff
`d(s, n) + h(n) > d(s, t)`.

For k x A*: a node is surplus if it is a surplus node for **ALL** k
SPPs (Definition 12). This is strict -- a node must be irrelevant to
every single goal.

### Active Goals (A)

The set of goals not yet expanded by kA*. Initially A = {t1,...,tk}.
When a goal ti is expanded, it is removed from A. The search halts
when A is empty.

### Stale F Value

A node in Open has a **stale** F value if it was computed w.r.t. a
set of active goals that is different from the current A (because a
goal was found and removed since the node was inserted).

### Responsible Goals (Definition 9)

A set of goals R is **responsible** for a node n if removing all
goals in R makes n's F value stale, but removing any proper subset of
R does not. Used by Lazy kA* to cheaply detect whether a node's F
value needs recomputation.

### Isotone / Antitone (Definition 10)

- **Isotone**: removing an active goal never increases Phi. Example:
  max. Implication: Lazy kA* never re-inserts a node (Observation 6).
- **Antitone**: removing an active goal never decreases Phi. Example:
  min. Implication: Lazy kA* follows best-first order w.r.t.
  up-to-date F values (Theorem 5).

---

## Eager vs Lazy kA*

| Aspect | Eager kA* | Lazy kA* |
|--------|-----------|----------|
| After goal found | Recompute F for ALL nodes in Open | Keep stale F values |
| Node selection | Always best-first (up-to-date F) | Check if selected node is stale; recompute if needed |
| Overhead | O(|Open|) recomputation k-1 times | Recomputes only for nodes actually selected |
| Expansions | Same as Lazy (up to tie-breaking) | Same as Eager (up to tie-breaking) |
| Runtime | Worse for large k (resort cost) | Better for large k |
| Recommended | -- | Yes (paper's recommendation) |

---

## Key Experimental Results

### Grid Pathfinding (polynomial domain)

- **kA*_min always expands fewer nodes** than k x A* and k-Dijkstra
- **Runtime**: kA* is faster for small k (2-8 goals). For large k
  (32+), k-Dijkstra wins because heuristic computation overhead grows
- **Close goals** (small radius): kA* dramatically better -- up to
  69x node overlap ratio for 128 goals
- **Distant goals**: advantage of kA* diminishes
- **Lazy vs Eager**: negligible difference for small k; Lazy is 2.5x
  faster for k=128

### Pancake Puzzle (exponential domain)

- kA* expands slightly fewer nodes, but **k x A* is faster** due to
  lower heuristic computation overhead
- Node overlap ratio never exceeds 2 (vs 69 for grids)
- **Recommendation**: use k x A* for exponential domains

### Impact of Heuristic Cost (Differential Heuristics)

- More pivots = more accurate heuristic but higher C_h
- k x A* always benefits from more pivots
- kA* benefits up to a point, then degrades (because it computes k
  heuristics per node)
- Sweet spot exists: for 16 goals + 8 pivots, kA* is 40x faster than
  both k-Dijkstra and k x A*

---

## Theoretical Summary (Table 9 from paper)

| Heuristics | Phi | Admissible? | Avoids surplus? | Might skip surely? | No re-expansion? |
|------------|-----|-------------|-----------------|--------------------|-----------------:|
| Consistent | Consistent + Admissible + =min | Yes | Yes | No | Yes |
| Consistent | Consistent + Admissible + !=min | Yes | No | No | ? |
| Consistent | Consistent + !Admissible + !=max | Yes | No | Yes | Yes |
| Consistent | Consistent + !Admissible + =max | Yes | No | Yes | Yes |
| Consistent | !Consistent | No | -- | -- | -- |
| Admissible | Admissible | Yes | -- | -- | -- |
| Admissible | !Admissible | No | -- | -- | -- |

---

## Codebase Mapping

| Paper Concept | Codebase Location |
|--------------|-------------------|
| kA* Aggregative | `f_search/algos/i_2_omspp/i_1_aggregative/` |
| Phi functions (min, max, mean) | `f_search/heuristics/phi/` (UPhi) |
| h-vector data structure | `f_search/ds/data/i_2_heuristics_vector/` |
| Comparison experiments | `f_search/experiments/cmp_agg_inc.py` |
| Detailed comparison | `f_search/experiments/cmp_agg_inc_detailed.py` |
