# f_hs/problem — Search Problems

## Purpose
Problem classes defining search spaces for SPP algorithms.

## Module Structure
```
problem/
├── __init__.py         ProblemSPP, ProblemGrid
├── i_0_base/           ProblemSPP — abstract SPP base
└── i_1_grid/           ProblemGrid — 2D grid domain
                        + Store (split-file save / load;
                          shared per-grid StateCell cache
                          on load)
                        + Runner (ProcessPoolExecutor; grids
                          loaded once per worker; shared
                          StateCell cache per worker)
```

## Inheritance
```
ProblemAlgo (f_cs)
  └── ProblemSPP[State]
        └── ProblemGrid (State=StateCell)
```

