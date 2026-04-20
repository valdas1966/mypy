# BFS

## Purpose
Breadth-First Search. Optimal for unit-cost edges.
Composes a `FrontierFIFO` and inherits everything else from
`AlgoSPP` — no overrides needed beyond the constructor.

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             name: str = 'BFS',
             is_recording: bool = False,
             search_state: SearchStateSPP[State] | None = None
             ) -> None
```
`search_state` — optional pre-built bundle; see
`algo/i_0_base/CLAUDE.md`.
Injects `FrontierFIFO[State]()` into `AlgoSPP`. No frontier
hooks to override — `_priority` defaults to `None` (ignored
by FIFO), `_frontier.{push,pop,...}` are used directly.

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc()` | `BFS` | Linear A -> B -> C |
| `graph_no_path()` | `BFS` | No path to goal |
| `graph_start_is_goal()` | `BFS` | Start == Goal |
| `graph_diamond()` | `BFS` | Diamond graph |
| `graph_decrease()` | `BFS` | Weighted graph (S→A/B→X, w(B,X)=0) — forces `decrease_g` |
| `grid_3x3()` | `BFS` | Open 3x3 grid |
| `grid_3x3_obstacle()` | `BFS` | Grid with obstacle |
| `grid_3x3_no_path()` | `BFS` | Grid with wall |
| `grid_3x3_start_is_goal()` | `BFS` | Grid where start == goal |
| `grid_4x4_obstacle()` | `BFS` | 4x4 grid with vertical wall, cost 7 |

## Inheritance
```
AlgoSPP[State]
    └── BFS[State]
```

## Tests
Split into three files by concern. No `@pytest.fixture` — each
test calls `BFS.Factory.*` directly (per the Factory-over-fixture
rule).

| File | Scope | Count |
|------|-------|-------|
| `_tester.py` | Graph problems + lifecycle | 5 |
| `_tester_grid.py` | Grid problems | 4 |
| `_tester_recording.py` | Full event-sequence assertion (incl. `decrease_g`) | 4 |

Run all three explicitly:
```
pytest f_hs/algo/i_1_bfs/_tester.py \
       f_hs/algo/i_1_bfs/_tester_grid.py \
       f_hs/algo/i_1_bfs/_tester_recording.py
```

## Dependencies
- `f_hs.algo.i_0_base.AlgoSPP`
- `f_hs.frontier.i_1_fifo.FrontierFIFO`
