from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_mospp._flipped_view import _FlippedView
from f_hs.algo.i_1_mospp._recorder_shim import _OnGoalToOnStartShim
from f_hs.algo.i_1_mospp.i_0_base.main import AlgoMOSPP
from f_hs.algo.i_1_omspp.i_1_kbfs import KBFS as KBFSOMSPP
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionMOSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class BFSFlipMOSPP(Generic[State], AlgoMOSPP[State]):
    """
    ============================================================================
     k-BFS for the Many-to-One Shortest Path Problem on
     uniform-weight UNDIRECTED graphs.

     Mirror of OMSPP's `KBFS` via the axis-swap trick: build a
     `_FlippedView` of the MOSPP problem (the MOSPP goal
     becomes the OMSPP shared start, the MOSPP starts become
     the OMSPP goals), delegate to OMSPP `KBFS`, then re-key
     the per-goal solution as a per-start solution. Inner BFS
     observes each MOSPP start at the moment it is popped
     during the single backward pass from the goal.

     **Correctness preconditions:**

       1. **Uniform edge weights** (BFS depth = optimal cost).
          For non-uniform non-negative weights use
          `DijkstraFlipMOSPP`.
       2. **Undirected graph** (or symmetric weights and
          symmetric `successors`). The flipped view does NOT
          reverse the adjacency — it relabels which list is
          "starts" vs "goals." On an undirected graph
          `dist(goal, start_i) == dist(start_i, goal)` and the
          delegated computation is correct. On a directed
          graph it silently computes the wrong quantity. No
          runtime check (`ProblemSPP` does not expose
          directionality).
       3. **Exactly one goal** — `ValueError` at construction
          if `len(problem.goals) != 1`.

     **Algorithm shape (delegation):**

       ```
       flipped = _FlippedView(base=self.problem)
       inner   = KBFS(flipped, is_recording=False)
       inner._recorder = _OnGoalToOnStartShim(self._recorder)
       sol_omspp = inner.run()
       self._solutions = dict(inner.solutions)
       return SolutionMOSPP(self._solutions)
       ```

     **Recording schema** (subset of canonical MOSPP set):

       - `push`, `pop` — verbatim from the inner OMSPP `KBFS`
         pass (the inner `_MultiGoalBFS`).
       - `on_start` — translated from the inner OMSPP's
         `on_goal` events by the recorder shim. `goal_index`
         in the OMSPP payload becomes `start_index` in the
         MOSPP payload. `reason ∈ {expanded, unreachable}`.
         `already_closed` is never emitted (no per-sub-search
         restarts — single inner pass).
       - `update_frontier` — NOT emitted (no between-sub-
         search transition).
       - `decrease_g` — NOT emitted (FIFO has no `decrease`
         op on the inner BFS frontier).

     **Counters** (mirrors the inner OMSPP `KBFS`):

       - `cnt_push`, `cnt_pop` — frontier-sourced.
       - `cnt_decrease` — 0 (FIFO has no decrease op;
         synthesized at the algo level).
       - `cnt_expanded`, `cnt_generated` — search-semantic.
       - `mem_open`, `mem_closed` — NODE COUNTS via
         `AlgoMOSPP._sync_memory_snapshot`: `len(frontier)` +
         `len(closed)` read once at completion. Exact peak
         coincident memory (the search is accumulative, so
         `|OPEN| + |CLOSED|` is monotone). Apples-to-apples with
         every other MOSPP algo.
       - `cnt_h_*` — ABSENT from the scaffold (no heuristic).

     **Within/between elapsed split:**

       Phase stays `PHASE_SEARCH` throughout —
       `elapsed_update == 0.0` by construction.

     **Path reconstruction:**

       Walks the inner's parent-pointer dict from `start` back
       to the (OMSPP-direction) origin (the MOSPP goal), then
       reverses so the caller sees `[start, ..., goal]` in
       MOSPP direction.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSPP[State],
                 name: str = 'BFSFlipMOSPP',
                 is_recording: bool = False,
                 is_timing: bool = True) -> None:
        """
        ====================================================================
         Init private Attributes. No `h` kwarg — BFS has no
         heuristic. The base `AlgoMOSPP` requires `h`, so a
         dummy `lambda s, g: 0` is passed internally (never
         invoked).
        ====================================================================
        """
        if len(problem.goals) != 1:
            raise ValueError(
                f'BFSFlipMOSPP requires exactly 1 goal '
                f'(got {len(problem.goals)})')
        AlgoMOSPP.__init__(
            self,
            problem=problem,
            h=lambda s, g: 0,
            name=name,
            is_recording=is_recording,
            is_timing=is_timing,
        )
        self._inner: KBFSOMSPP[State] | None = None

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def search_state(self) -> SearchStateSPP[State] | None:
        """
        ====================================================================
         The inner OMSPP `KBFS`'s `SearchStateSPP` (its own
         inner `_MultiGoalBFS`'s search bundle) after `run()`
         completes. Available for post-hoc inspection.
        ====================================================================
        """
        return self._inner.search_state if self._inner else None

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionMOSPP:
        """
        ====================================================================
         Build a flipped (OMSPP) view of the MOSPP problem,
         delegate to OMSPP `KBFS`, re-key the per-goal
         solution as a per-start solution.
        ====================================================================
        """
        flipped = _FlippedView[State](base=self.problem)
        self._inner = KBFSOMSPP[State](
            problem=flipped,
            name=f'{self.name}[inner]',
            is_recording=False,
            is_timing=False,
        )
        # Route the inner's events through a shim that
        # rewrites `on_goal` → `on_start`. Push / pop pass
        # through unchanged.
        self._inner._recorder = _OnGoalToOnStartShim(
            self._recorder)
        self._inner.run()
        # Re-key as MOSPP per-start solution. The OMSPP inner
        # already keys by State (= MOSPP starts after the
        # flip), so it's a direct copy.
        self._solutions = dict(self._inner.solutions)
        return SolutionMOSPP(self._solutions)

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         Mirror the inner OMSPP `KBFS`'s counters into the
         MOSPP scaffold. Single inner pass — no aggregation
         across sub-searches.
        ====================================================================
        """
        if self._inner is None:
            return
        ic = self._inner.counters
        self._counters.assign('cnt_push', ic['cnt_push'])
        self._counters.assign('cnt_pop', ic['cnt_pop'])
        self._counters.assign('cnt_decrease', ic['cnt_decrease'])
        self._counters.assign('cnt_expanded', ic['cnt_expanded'])
        self._counters.assign(
            'cnt_generated', ic['cnt_generated'])

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self, start: State) -> list[State]:
        """
        ====================================================================
         Walk the inner OMSPP `KBFS`'s parent dict from `start`
         back to the OMSPP origin (= the MOSPP goal), then
         reverse so the caller sees `[start, ..., goal]` in
         the MOSPP direction. Returns `[]` if `start` is
         unreachable from the MOSPP goal (which, on an
         undirected graph, is equivalent to the goal being
         unreachable from `start`).
        ====================================================================
        """
        if self._inner is None:
            return []
        omspp_path = self._inner.reconstruct_path(start)
        return list(reversed(omspp_path))
