# f_cs — Computer Science Algorithm Framework

## Purpose
Core abstractions for algorithms: Problem → Algorithm → Solution.
Provides lifecycle management, timing, and event recording.

## Package Exports
```python
from f_cs import Algo, ProblemAlgo, SolutionAlgo
```

## Architecture
```
ProblemAlgo          Algo[Problem, Solution]          SolutionAlgo
(HasName,            (ProcessIO[Problem, Solution])   (Validatable)
 Equatable)                    │                          │
    │                 ┌────────┴────────┐            ┌────┴─────┐
    │                 │ problem         │            │ is_valid │
    │                 │ elapsed         │            └──────────┘
    │                 │ recorder        │
    │                 │ name            │
    │                 │ run() → Solution│
    └─────────────────┴─────────────────┘
```

## Flow
```
1. problem = MyProblem(...)
2. algo = MyAlgo(problem, is_recording=True)
3. solution = algo.run()
4. bool(solution)             # is_valid
5. algo.elapsed               # execution time
6. algo.recorder.events       # recorded events
```

## Module Structure
```
f_cs/
├── __init__.py        Algo, ProblemAlgo, SolutionAlgo
├── algo/              Algo — base algorithm with lifecycle
├── problem/           ProblemAlgo — named, equatable problem
└── solution/          SolutionAlgo — minimal validity contract
```

## Design Decisions
- **Minimal SolutionAlgo** — only `is_valid` is universal to all
  algorithm outputs. Domain-specific data (problem, path, stats)
  belongs on subclasses. Execution metadata (elapsed, recorder)
  stays on `Algo` via `ProcessBase`.
- **Recorder on ProcessBase** — every process (including algorithms)
  has an opt-in event recorder via `is_recording` parameter.
- **Separation of concerns** — the Solution answers "what was the
  result?", the Algo answers "how did the execution go?".
