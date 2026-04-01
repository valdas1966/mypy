# Surely Expanded Node — Definition and Context

**Source**: Definition 11 in the journal paper
"Heuristic Search for One-to-Many Shortest Path Queries"
(Stern, Goldenberg, Saffidine, Felner)

---

## Formal Definition (Single-Goal SPP)

A node **n** is **surely expanded** w.r.t. heuristic h and goal t if
there exists a path from start s to n where **all** nodes n' on that
path (except s, including n) satisfy:

```
d(s, n') + h(n') < d(s, t)
```

where `d(s, x)` is the true shortest-path distance from s to x.

### Intuition

A surely expanded node lies on a path where **every node looks strictly
cheaper** than the known optimal cost. Any correct best-first search
algorithm **must expand** these nodes to guarantee optimality — there is
no way to prove you found the best solution without looking at them.

### Simplified Form (Consistent Heuristics)

With consistent heuristics (like Manhattan distance on a grid), the
condition simplifies to:

```
n is surely expanded  ⟺  d(s, n) + h(n) < d(s, t)
```

This means: the estimated total cost through n is strictly **less** than
the true optimal cost. A* must pop this node from Open before it can
prove that d(s, t) is optimal.

---

## Extension to OMSPP (k x A*) — Definition 12

For the multi-goal case with k goals {t1, ..., tk}:

```
n is surely expanded for k x A*  ⟺  n is surely expanded for
                                      AT LEAST ONE of the k SPPs
```

A node is surely expanded if **any** single goal needs it. Even if k-1
goals could skip it, the one remaining goal forces its expansion.

---

## Contrast: Surplus Nodes (Definition 11)

| Property | Surely Expanded | Surplus |
|----------|----------------|---------|
| **Condition** | d(s,n) + h(n) < d(s,t) | d(s,n) + h(n) > d(s,t) |
| **Meaning** | Must be expanded by any optimal algo | Need not be expanded |
| **For k x A*** | Surely expanded for at least 1 goal | Surplus for ALL k goals |
| **Category** | Necessary work | Wasted work |

Nodes where `d(s,n) + h(n) = d(s,t)` are **borderline** — they may or
may not be expanded depending on tie-breaking.

---

## Concrete Example: SPP with Obstacles

Using `ProblemSPP.Factory.with_obstacles()`:
4x4 grid, obstacles at (0,2) and (1,2), S=(0,0), T=(0,3).

```
 S(3)  .(3)   #   T(7)       h = Manhattan to (0,3)
 .(5)  .(5)   #   .(7)       d(s,t) = 7
 .(7)  .(7)  .(7) .(7)       f(n) = d(s,n) + h(n)
 .(9)  .(9)  .(9) .(9)
```

f-values per cell (parentheses above):

| f-value | Cells | Classification |
|---------|-------|---------------|
| 3 | (0,0), (0,1) | **Surely Expanded** — f < 7 |
| 5 | (1,0), (1,1) | **Surely Expanded** — f < 7 |
| 7 | (0,3), (1,3), (2,0)-(2,3) | **Borderline** — f = 7 |
| 9 | (3,0)-(3,3) | **Surplus** — f > 7 |

**4 surely expanded nodes**: A* MUST expand (0,0), (0,1), (1,0), (1,1)
before it can prove d(s,t) = 7 is optimal. Each has f < 7 so A* pops
them before any node with f >= 7.

---

## Concrete Example: OMSPP with Obstacles

Using `ProblemOMSPP.Factory.with_obstacles()`:
Same grid, S=(0,0), goals T1=(0,3) and T2=(3,3).

### Per-Goal Analysis

**Goal T1 = (0,3)**, d(s, t1) = 7:
- Surely expanded: (0,0), (0,1), (1,0), (1,1) — f1 < 7
- Surplus: (3,0), (3,1), (3,2), (3,3) — f1 = 9 > 7

**Goal T2 = (3,3)**, d(s, t2) = 6:
- Surely expanded: none — all cells have f2 >= 6
- Surplus: (0,3) f2=13, (1,3) f2=8 — both f2 > 6

### k x A* Combined (Definition 12)

| Classification | Rule | Result |
|----------------|------|--------|
| **Surely expanded** | SE for at least 1 goal | (0,0), (0,1), (1,0), (1,1) — from T1 |
| **Surplus** | Surplus for ALL goals | **None** — no cell is surplus for both T1 and T2 |

**Key insight**: Adding goal T2 eliminates all surplus nodes. The bottom
row (3,0)-(3,3) was surplus for T1 but is borderline for T2 (f2=6).
The cells (0,3) and (1,3) were surplus for T2 but are borderline for
T1 (f1=7). No cell is wasted for both goals simultaneously.

---

## Why Surely Expanded Nodes Matter

### Lower Bound on Work

The set of surely expanded nodes defines the **minimum work** any
optimal algorithm must do. No algorithm — no matter how clever — can
find the optimal solution without expanding these nodes. They form an
irreducible core of necessary computation.

### Measuring Algorithm Efficiency

An algorithm's efficiency can be measured by how close its total
expansions are to the surely-expanded count:

```
efficiency ≈ |surely expanded| / |total expanded|
```

- Ratio = 1.0: perfect (only expanded necessary nodes + borderline)
- Ratio << 1.0: algorithm wastes effort on surplus nodes

### Phi = min: Optimal Efficiency (Theorem 7)

kA* with Phi=min never expands surplus nodes (Theorem 7, Part 1). Its
total expansions are: surely expanded + some borderline nodes. This is
the best achievable by any admissible aggregation function.

### Phi != min: May Waste Work (Theorem 7, Part 2)

Other admissible aggregation functions (projection, mean, median) can
expand surplus nodes — pushing the total expansion count above the
minimum. The gap between their count and the surely-expanded count
includes wasted surplus expansions.

---

## Visual Summary

```
                    f(n) = d(s,n) + h(n)

   |--- Surely Expanded ---|--- Borderline ---|--- Surplus ---|
   |  f(n) < d(s,t)        |  f(n) = d(s,t)  |  f(n) > d(s,t) |
   |  MUST expand           |  May expand      |  WASTE to expand|
   |  (necessary work)      |  (tie-breaking)  |  (overhead)     |
```

---

## Key Takeaway

**Surely expanded nodes are the irreducible core of search work** —
every optimal algorithm must expand them. They provide a theoretical
lower bound on node expansions. The closer an algorithm's expansion
count is to this lower bound, the more efficient it is. Phi=min
achieves the tightest bound by avoiding all surplus expansions.
