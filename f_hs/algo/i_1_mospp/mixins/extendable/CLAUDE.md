# ExtendableMOSPP — MOSPP start-sequence extension mixin

## Purpose

Capability mixin that adds `extend(new_starts)` to MOSPP
orchestrators whose `_run()` body is a per-start sub-search
loop. Sibling of `ExtendableOMSPP`; same orchestration
shape with axis-specific naming.

## Public API

### `extend(new_starts: list[State]) -> SolutionMOSPP`

Resume the orchestrator with additional starts appended to
the sequence already solved by `run()` (and any prior
`extend()`s). Returns a `SolutionMOSPP` over the FULL set
of starts seen so far.

### `run_nested(problems, h, ...) -> ExtendableMOSPP`
*(classmethod)*

Convenience: solve a prefix-extending list of MOSPP
problems via one call.

### `is_extendable(algo) -> bool`

Free function — `isinstance(algo, ExtendableMOSPP)`.

## Subclass contract

A subclass MUST:

1. Inherit `AlgoMOSPP` AND `ExtendableMOSPP`.
2. Implement `_handle_start(start, idx)`: the per-start
   sub-search body.
3. Implement `_repush_last_reached_start()`: push or no-op
   per the algo's frontier-sharing semantics.
4. Initialize `self._all_starts: list[State] = []`,
   `self._last_reached_start: State | None = None`,
   `self._last_algo: object | None = None` in `__init__`.
5. Set `self._all_starts = list(self.problem.starts)` at
   the top of `_run`; reset bookkeeping to None.
6. Inside `_handle_start`, update bookkeeping on
   successful expansion; clear on fast-path / unreachable.

## Composition table

| algo | composes today | rationale |
|---|---|---|
| `AStarRepMOSPP` | yes | per-start sub-search loop |

## Dependencies

- `f_hs.algo.i_1_mospp.i_0_base.main.PHASE_SEARCH`
- `f_hs.solution.main.SolutionMOSPP`
- `f_hs.state.i_0_base.main.StateBase`

Composes with `AlgoMOSPP` at runtime (reads `_elapsed`,
`_is_timing`, `_phase`, `_t_phase_start`, `_solutions`;
calls `_flush_phase_timer`, `_sync_frontier_counters`,
`_sync_memory_snapshot`).
