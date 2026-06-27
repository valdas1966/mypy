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
| `graph_decrease()` | `BFS` | Weighted graph (S→A/B→X, w(B,X)=0) — FIFO re-encounters X but cannot relax (no decrease op); pops X with g=2, no `decrease_g` |
| `grid_3x3()` | `BFS` | Open 3x3 grid |
| `grid_3x3_obstacle()` | `BFS` | Grid with obstacle |
| `grid_3x3_no_path()` | `BFS` | Grid with wall |
| `grid_3x3_start_is_goal()` | `BFS` | Grid where start == goal |
| `grid_4x4_obstacle()` | `BFS` | 4x4 grid with vertical wall, cost 7 |

## Counters

**Inherited from `AlgoSPP`.** `FrontierFIFO` owns only the
2-counter scaffold (`cnt_push`, `cnt_pop`) — FIFO has **no**
`decrease` op and therefore **no** `cnt_decrease` counter.
`bfs.counters` still surfaces `cnt_decrease` because the
algo-level scaffold declares it for every algo; the
`AlgoSPP.counters` property **guards** the read
(`fc['cnt_decrease'] if 'cnt_decrease' in fc else 0`) and
**synthesizes a structural `0`** for FIFO-backed BFS, keeping
the cross-algo comparison grid rectangular. The old framing
("`cnt_decrease=0` because `decrease` is a no-op on FIFO") is
obsolete — there is no decrease op and no counter on FIFO; the
0 is fabricated at the algo level.

## Frontier Relaxation

BFS does **not** relax frontier nodes. When a node already on
the FIFO is re-encountered via a different parent, `AlgoSPP`'s
`_relax_frontier_child` no-op default fires (FIFO cannot
decrease a key — it has no `decrease` op), so BFS keeps the
first-seen `g` / `parent`. On the synthetic weighted
`graph_decrease` fixture BFS therefore pops X with `g=2` (the
first FIFO path), does **not** adopt the cheaper `w(B,X)=0`
path, and emits **no** `decrease_g` event. BFS is non-optimal
on weighted graphs regardless — this is the honest FIFO
behavior.

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
| `_tester_recording.py` | Full event-stream pins (one per scenario; each is a single `actual == expected` assertion). Scenarios: canonical `grid_4x4_obstacle`, graph_abc, graph_decrease (weighted; FIFO re-encounter, no relax — no `decrease_g`), grid_3x3 | 4 |

Run all three explicitly:
```
pytest f_hs/algo/i_1_bfs/_tester.py \
       f_hs/algo/i_1_bfs/_tester_grid.py \
       f_hs/algo/i_1_bfs/_tester_recording.py
```

## Dependencies
- `f_hs.algo.i_0_base.AlgoSPP`
- `f_hs.frontier.i_1_fifo.FrontierFIFO`
