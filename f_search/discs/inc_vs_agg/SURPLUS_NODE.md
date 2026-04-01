# Surplus Node — Definition and Context

**Source**: Definition 11 in the journal paper
"Heuristic Search for One-to-Many Shortest Path Queries"
(Stern, Goldenberg, Saffidine, Felner)

---

## Formal Definition (Single-Goal SPP)

A node **n** is a **surplus node** w.r.t. heuristic h and goal t if,
in **every** path from start s to n, there exists a node n' != s such
that:

```
d(s, n') > d(s, t)
```

where `d(s, x)` is the true shortest-path distance from s to x.

### Intuition

A surplus node **cannot be reached** without passing through at least
one node that is already **more expensive** than the optimal solution
cost. No correct forward search algorithm ever needs to expand a
surplus node to prove optimality.

### Simplified Form (Consistent Heuristics)

With consistent heuristics, the condition simplifies to:

```
n is surplus  ⟺  d(s, n) + h(n) > d(s, t)
```

This means: the best possible cost of any solution passing through n
is strictly **greater** than the known optimal cost. The node is
provably irrelevant.

---

## Extension to OMSPP (k x A*) — Definition 12

For the multi-goal case with k goals {t1, ..., tk}:

```
n is surplus for k x A*  ⟺  n is surplus for ALL k individual SPPs
```

A node is surplus only if it is irrelevant to **every single goal**.
If even one goal needs it, it is not surplus.

---

## Contrast: Surely Expanded Nodes (Definition 11)

| Property | Surely Expanded | Surplus |
|----------|----------------|---------|
| **Condition** | d(s,n) + h(n) < d(s,t) | d(s,n) + h(n) > d(s,t) |
| **Meaning** | Must be expanded by any optimal algorithm | Need not be expanded by any algorithm |
| **For k x A*** | Surely expanded for at least 1 goal | Surplus for ALL k goals |
| **Category** | Necessary work | Wasted work |

Nodes where `d(s,n) + h(n) = d(s,t)` are in neither category — they
are **borderline** nodes that may or may not be expanded depending on
tie-breaking.

---

## Why Surplus Nodes Matter for kA*

### Phi = min: No Surplus Expansion (Theorem 7, Part 1)

kA* with Phi=min **never expands any surplus node** of k x A*. This
is a unique property of min — it is the only admissible aggregation
function with this guarantee.

### Phi != min (including projection): May Expand Surplus (Theorem 7, Part 2)

Any admissible Phi other than min **can** expand surplus nodes. This
includes projection, mean, and median. The surplus nodes are wasted
work — they contribute nothing to finding any optimal path.

### Practical Impact

The number of surplus nodes expanded is a direct measure of wasted
computation. Fewer surplus expansions = more efficient search. This is
why Phi=min tends to expand fewer total nodes than other aggregation
functions in experiments.

---

## Visual Summary

```
                    f(n) = d(s,n) + h(n)

   |--- Surely Expanded ---|--- Borderline ---|--- Surplus ---|
   |  f(n) < d(s,t)        |  f(n) = d(s,t)  |  f(n) > d(s,t) |
   |  MUST expand           |  May expand      |  WASTE to expand |
```

---

## Key Takeaway

**Surplus nodes are provably irrelevant** — expanding them is pure
overhead. The strength of Phi=min is that it avoids all surplus
expansions. Other aggregation functions (projection, mean) lack this
guarantee and may waste effort on nodes that cannot contribute to any
optimal solution.
