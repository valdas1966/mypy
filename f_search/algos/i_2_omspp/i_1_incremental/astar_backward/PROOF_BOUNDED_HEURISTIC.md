# Formal Proof: Bounded Heuristic from Explored States

## Setting

A backward incremental search solves OMSPP by running k sub-searches on
the reverse graph G_R = (V, E_R, w), each from a different goal t_i
toward the shared original start s.

After sub-search i completes (A* from t_i to s with consistent heuristic
h), define for every explored state X:

    b_i(X) = g_i* - g_i(X)

where:
- g_i* = dist_{G_R}(t_i, s) — optimal cost found by A*
- g_i(X) = dist_{G_R}(t_i, X) — optimal distance from t_i to X
  (guaranteed by A* with consistent heuristic)

We use b_i(X) as a heuristic estimate of dist_{G_R}(X, s) in future
sub-searches j > i.

---

## Lemma 1: Admissibility

**Claim.** For every explored state X: b(X) <= dist(X, s).

**Proof.** By triangle inequality on shortest-path distances:

    dist(t_i, s) <= dist(t_i, X) + dist(X, s)

Substituting:

    g* <= g(X) + dist(X, s)

Rearranging:

    dist(X, s) >= g* - g(X) = b(X)                                    ∎

**Required conditions:**
- Non-negative edge weights (for well-defined shortest paths).
- g(X) = dist(t_i, X), i.e., g-values are optimal.
  Guaranteed by A* with consistent heuristic (no reopening needed).
  Also holds with admissible heuristic if reopening is enabled.

**NOT required:** unit costs, grid structure, specific heuristic form,
any dimensionality or connectivity constraint.

---

## Lemma 2: Dominance over Base Heuristic

**Claim.** For every explored state X: b(X) >= h(X).

**Proof.** A* with consistent heuristic expands states in non-decreasing
f-order. The goal s is expanded with f(s) = g*. Therefore, every
previously explored state satisfies:

    f(X) <= g*
    g(X) + h(X) <= g*
    h(X) <= g* - g(X) = b(X)                                          ∎

**Required conditions:**
- **Consistent** heuristic (not just admissible). Consistency guarantees
  f-values are non-decreasing along any optimal path, which ensures
  f(X) <= g* for all explored states.
- With merely admissible h, a state can be explored with f(X) > g*
  (expanded early with non-optimal g, then not reopened). The dominance
  guarantee breaks.

**NOT required:** unit costs, grid structure, specific heuristic form.

**Consequence:** Using b(X) directly (without max(b(X), h(X))) is safe —
it already dominates the base heuristic for all explored states.

---

## Lemma 3: Exactness on Optimal-Path States

**Claim.** If X lies on an optimal path from t_i to s, then
b(X) = dist(X, s).

**Proof.** Optimal substructure of shortest paths:

    dist(t_i, s) = dist(t_i, X) + dist(X, s)
    g* = g(X) + dist(X, s)
    dist(X, s) = g* - g(X) = b(X)                                     ∎

**Required conditions:**
- Non-negative edge weights (for optimal substructure to hold).

**NOT required:** consistency, unit costs, grid structure.

---

## Lemma 4: Consistency within Bounded Region

**Claim.** For any two adjacent explored states X, Y:
b(X) - b(Y) <= w(X, Y).

**Proof.** By triangle inequality on optimal distances from t_i:

    g(Y) <= g(X) + w(X, Y)

Therefore:

    b(X) - b(Y) = (g* - g(X)) - (g* - g(Y))
                 = g(Y) - g(X)
                 <= w(X, Y)                                            ∎

**Required conditions:**
- g-values are optimal shortest-path distances (guaranteed by
  consistent heuristic).

**NOT required:** unit costs, grid structure.

**Note on boundary consistency.** At the boundary between bounded and
unbounded states, the combined heuristic ĥ(X) = b(X) for bounded X,
ĥ(Y) = h(Y) for unbounded Y, is NOT necessarily consistent:

    ĥ(X) - ĥ(Y) = b(X) - h(Y) can exceed w(X, Y)

This happens because b(X) >= h(X) (Lemma 2) while h(Y) can be much
smaller than b(X). However, this inconsistency is in the "safe direction"
for A* without reopening: bounded states have INFLATED h, hence HIGH f,
hence are explored LATE. Their unbounded neighbors (with lower f) are
explored first, ensuring optimal g-values propagate to bounded states
before those states are expanded. This direction of inconsistency does
not cause suboptimality in A* without reopening.

---

## Lemma 5: Safe Accumulation across Sub-Searches

**Claim.** When multiple sub-searches contribute bounds for the same
state X, keeping max_i b_i(X) preserves admissibility and maximizes
informativeness.

**Proof.** Each b_i(X) <= dist(X, s) by Lemma 1. Therefore:

    max_i b_i(X) <= dist(X, s)

Admissibility preserved. The max yields the tightest admissible bound. ∎

**Required conditions:** same as Lemma 1 (non-negative weights, optimal
g-values).

---

## Conditions Summary

### Required

| Condition                   | Used in          | Why                        |
|-----------------------------|------------------|----------------------------|
| Non-negative edge weights   | Lemmas 1, 3, 4   | Triangle inequality,       |
|                             |                  | optimal substructure       |
| Consistent heuristic        | Lemma 2          | Guarantees f(X) <= g*      |
|                             |                  | for all explored states    |
| Optimal g-values            | All lemmas       | b(X) = g* - g(X) requires |
|                             |                  | g(X) = dist(t_i, X)       |
| Shared goal across searches | Lemma 1          | b(X) estimates dist(X, s), |
|                             |                  | valid only if goal is same |

### NOT Required

| Condition               | Why not needed                              |
|-------------------------|---------------------------------------------|
| Unit edge costs         | All proofs use general w(X, Y) >= 0         |
| Grid structure          | All proofs use abstract graph properties     |
| Manhattan distance      | Any consistent heuristic works (Lemma 2     |
|                         | only needs f(X) <= g* for explored states)  |
| 2D or any dimensionality| No geometric argument used                  |
| 4-neighbor connectivity | No connectivity assumption used             |

### Minimal Abstract Requirements

The proof works on **any directed weighted graph G = (V, E, w) with
w: E -> R_{>=0}**, using **any consistent heuristic h**, where **A*
guarantees optimal g-values** for explored states, and **all sub-searches
share the same goal**.

This means the bounded heuristic mechanism is valid for:
- Weighted road networks (non-uniform edge costs)
- 3D grids, hexagonal grids, triangular grids
- Arbitrary graph topologies (social networks, communication graphs)
- Any consistent heuristic (Euclidean, octile, landmark-based, etc.)

---

## Comparison: Explored Bounds vs. Neighbor Propagation

The paper (Algorithm 5) propagates bounds to neighbors of path states
using the triangle inequality: ĥ(N) = |h*(P) - w(P, N)|.

On **unit-cost graphs with consistent heuristics**, this propagation
never beats the base heuristic. The proof (by induction on depth d):

For state N_d at graph distance d from path state P, propagated bound
= h*(P) - d. For each intermediate state N_j:
- If N_j was generated by A*: h(N_j) >= g* - g(N_j) >= h*(P) - j
  (since g(N_j) <= g(P) + j and f(N_j) >= g* for unexplored states).
- If N_j was not generated: by consistency, h(N_j) >= h(N_{j-1}) - 1.

Both cases yield h(N_d) >= h*(P) - d = propagated bound.

On **non-unit-cost graphs**, this proof BREAKS: consistency gives
h(N) >= h(neighbor) - w(edge), but the propagated bound decays by
w(edge) too, so they stay matched. However, if g(N_j) < g(P) + sum of
weights (possible with variable costs and alternate routes), the
generated-state argument may yield h(N_j) > propagated bound, making
propagation even less useful.

The explored-bounds approach is therefore a **hermetic replacement** for
neighbor propagation on unit-cost graphs. On non-unit-cost graphs, the
explored bounds are valid (all lemmas hold) but the hermetic replacement
claim would need separate verification per domain.
