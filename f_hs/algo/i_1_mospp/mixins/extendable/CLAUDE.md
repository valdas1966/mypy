# ExtendableMOSPP — MOSPP start-sequence extension mixin

## Purpose

Capability mixin that adds `extend(new_starts)` to MOSPP
orchestrators whose `_run()` body is a per-start sub-search
loop. Sibling of `ExtendableOMSPP`; same orchestration
shape with axis-specific naming.

**True ABC** (bases: `Generic[State], ABC`) — the two hooks
`_handle_start` and `_repush_last_reached_start` are
`@abstractmethod`, so a composing class that omits either fails
at CONSTRUCTION (not at first call).

## Public API

### `extend(new_starts: list[State]) -> SolutionMOSPP`

Resume the orchestrator with additional starts appended to
the sequence already solved by `run()` (and any prior
`extend()`s). Returns a `SolutionMOSPP` over the FULL set
of starts seen so far.

Post-batch, `extend()` mirrors `AlgoMOSPP._run_post`:
`_flush_phase_timer` → accumulate `_elapsed` →
`_sync_frontier_counters` → `_sync_memory_snapshot` →
`finalize_mem_total`. The trailing `finalize_mem_total`
keeps `mem_total = Σ mem_*` consistent after an extend
(without it, `mem_total` would stay stale at its
last-`run()` value).

### `run_nested(problems, h, ...) -> ExtendableMOSPP`
*(classmethod)*

Convenience: solve a prefix-extending list of MOSPP
problems via one call.

### `is_extendable(algo) -> bool`

Free function — `isinstance(algo, ExtendableMOSPP)`.

## Subclass contract

A subclass MUST:

1. Inherit `AlgoMOSPP` AND `ExtendableMOSPP`.
2. Implement `_handle_start(start, idx)` (**`@abstractmethod`**):
   the per-start sub-search body.
3. Implement `_repush_last_reached_start()`
   (**`@abstractmethod`**): push or no-op per the algo's
   frontier-sharing semantics.

Both hooks are `@abstractmethod`, so a composing class that
omits either cannot be instantiated (fails at construction).
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
| `AStarIncMOSPP` | yes | per-start sub-search loop; the carried goal-anchored cache / bounds survive an extend for free (`extend()` does not call `_run()`, so its `_cache` / `_bounds` reset is bypassed) |

## Dependencies

- `f_hs.algo.i_1_mospp.i_0_base.main.PHASE_SEARCH`
- `f_hs.solution.main.SolutionMOSPP`
- `f_hs.state.i_0_base.main.StateBase`

Composes with `AlgoMOSPP` at runtime (reads `_elapsed`,
`_is_timing`, `_phase`, `_t_phase_start`, `_solutions`;
calls `_flush_phase_timer`, `_sync_frontier_counters`,
`_sync_memory_snapshot`).
