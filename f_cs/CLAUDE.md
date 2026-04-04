# f_cs — Computer Science Algorithm Framework

## Purpose
Core abstractions for algorithms: Problem → Algorithm → Solution.
Provides lifecycle management, timing, and event recording.
No statistics classes — counters belong in domain-specific Recorders.

## Package Exports
```python
from f_cs import Algo, ProblemAlgo, SolutionAlgo
```

## Architecture
```
ProblemAlgo          Algo[Problem, Solution]          SolutionAlgo[Problem]
(HasName,            (ProcessIO[Problem, Solution])   (Validatable)
 Equatable)                    │                             │
    │                 ┌────────┴────────┐              ┌─────┴──────┐
    │                 │ problem         │              │ name_algo  │
    │                 │ elapsed         │              │ problem    │
    │                 │ recorder        │              │ elapsed    │
    │                 │ name            │              │ recorder   │
    │                 │ run() → Solution│              │ is_valid   │
    └─────────────────┴─────────────────┘              └────────────┘
```

## Flow
```
1. problem = MyProblem(...)
2. algo = MyAlgo(problem, is_recording=True)
3. solution = algo.run()
4. solution.elapsed           # execution time
5. solution.recorder.events   # recorded events
6. bool(solution)             # is_valid
```

## Module Structure
```
f_cs/
├── __init__.py        Algo, ProblemAlgo, SolutionAlgo
├── algo/              Algo — base algorithm with lifecycle
├── problem/           ProblemAlgo — named, equatable problem
└── solution/          SolutionAlgo — result with elapsed + recorder
```

## Design Decisions
- **No StatsAlgo** — `elapsed` is a direct property on SolutionAlgo.
  Counters are tracked by Recorder, not a separate Stats class.
- **Recorder on ProcessBase** — every process (including algorithms)
  has an opt-in event recorder via `is_recording` parameter.
- **elapsed flows naturally** — ProcessBase tracks it, algorithm
  passes `self.elapsed` when constructing the Solution.
