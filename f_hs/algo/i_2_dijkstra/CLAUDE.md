# Dijkstra

## Purpose
Dijkstra's Algorithm. A* with h=0 (no heuristic).
Optimal for non-negative edge costs. On unit-cost edges, the
recorded event sequence is identical to BFS (priority by g,
state tiebreak matches BFS's FIFO insertion-order expansion).

## Public API

### Constructor
```python
def __init__(self,
             problem: ProblemSPP[State],
             name: str = 'Dijkstra',
             is_recording: bool = False) -> None
```

## Priority
Inherited from AStar: `(g + h, -g, state) = (g, -g, state)`.
The State tiebreak (via HasKey / Comparable) keeps expansion
order deterministic at the frontier — required for full-sequence
recording tests.

## Event Enrichment
Dijkstra overrides `_enrich_event` to a **no-op** — AStar's
`h` and `f` fields are not recorded. Rationale (Recording
Principle, `algo/i_0_base/CLAUDE.md`):

- `h` is constant (always 0) → violates "no constants".
- `f = g` is derivable → violates "no derivable fields".

Dropping them makes Dijkstra events schema-match BFS events
exactly: `{type, state, g, parent?, duration}`.

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `graph_abc()` | `Dijkstra` | Linear A -> B -> C |
| `graph_no_path()` | `Dijkstra` | No path to goal |
| `graph_start_is_goal()` | `Dijkstra` | Start == Goal |
| `graph_diamond()` | `Dijkstra` | Diamond graph |
| `grid_3x3()` | `Dijkstra` | Open 3x3 grid |
| `grid_3x3_obstacle()` | `Dijkstra` | Grid with obstacle |
| `grid_3x3_no_path()` | `Dijkstra` | Grid with wall |
| `grid_3x3_start_is_goal()` | `Dijkstra` | Grid where start == goal |
| `grid_4x4_obstacle()` | `Dijkstra` | 4x4 grid with vertical wall, cost 7 |
| `graph_decrease()` | `Dijkstra` | Weighted graph (S→A/B→X, w(B,X)=0) — forces `decrease_g` and verifies the no-h/f schema on that event |

## Inheritance
```
AlgoSPP[State]
    └── AStar[State]
        └── Dijkstra[State]   (overrides _enrich_event → no-op)
```

## Tests
Split into three files by concern (mirrors BFS and AStar).
No `@pytest.fixture` — each test calls `Dijkstra.Factory.*`
directly, per the Factory-over-fixture rule.

| File | Scope | Count |
|------|-------|-------|
| `_tester.py` | Graph problems + lifecycle | 5 |
| `_tester_grid.py` | Grid problems | 4 |
| `_tester_recording.py` | Full event-sequence + schema (incl. `decrease_g` no-h/f) | 6 |

Run all three explicitly:
```
pytest f_hs/algo/i_2_dijkstra/_tester.py \
       f_hs/algo/i_2_dijkstra/_tester_grid.py \
       f_hs/algo/i_2_dijkstra/_tester_recording.py
```

Recording tester includes:
- `test_recording_no_h_or_f_fields` — schema check pinning the
  `_enrich_event` override (no `h`, no `f` anywhere).
- `graph_abc`, `graph_diamond`, `grid_3x3`, `grid_4x4_obstacle`
  — full-sequence assertions. The `graph_diamond` test verifies
  that Dijkstra pops C fully (unlike AStar, which finds the goal
  via B and never expands C).

## Dependencies
- `f_hs.algo.i_1_astar.AStar`
