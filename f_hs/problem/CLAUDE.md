# f_hs/problem — Search Problems

## Purpose
Problem classes defining search spaces for SPP algorithms.

## Module Structure
```
problem/
├── __init__.py         ProblemSPP, ProblemGrid
├── i_0_base/           ProblemSPP — abstract SPP base
└── i_1_grid/           ProblemGrid — 2D grid domain
```

## Inheritance
```
ProblemAlgo (f_cs)
  └── ProblemSPP[State]
        └── ProblemGrid (State=StateCell)
```
