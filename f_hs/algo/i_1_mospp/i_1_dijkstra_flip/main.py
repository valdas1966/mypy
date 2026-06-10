from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_mospp._flipped_view import _FlippedView
from f_hs.algo.i_1_mospp._recorder_shim import _OnGoalToOnStartShim
from f_hs.algo.i_1_mospp.i_0_base.main import AlgoMOSPP
from f_hs.algo.i_1_omspp.i_2_kdijkstra import KDijkstra as KDijkstraOMSPP
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionMOSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class DijkstraFlipMOSPP(Generic[State], AlgoMOSPP[State]):
    """
    ============================================================================
     k-Dijkstra for the Many-to-One Shortest Path Problem on
     non-negative-weight UNDIRECTED graphs.

     Mirror of OMSPP's `KDijkstra` via the axis-swap trick:
     build a `_FlippedView` of the MOSPP problem (the MOSPP
     goal becomes the OMSPP shared start, the MOSPP starts
     become the OMSPP goals), delegate to OMSPP `KDijkstra`,
     then re-key the per-goal solution as a per-start
     solution. Inner Dijkstra observes each MOSPP start at
     the moment it is popped (in g-order) during the single
     backward pass from the goal.

     **Correctness preconditions:**

       1. **Non-negative edge weights** (Dijkstra-family).
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
       inner   = KDijkstra(flipped, is_recording=False)
       inner._recorder = _OnGoalToOnStartShim(self._recorder)
       sol_omspp = inner.run()
       self._solutions = dict(inner.solutions)
       return SolutionMOSPP(self._solutions)
       ```

     **Recording schema** (subset of canonical MOSPP set):

       - `push`, `pop`, `decrease_g` — verbatim from the inner
         OMSPP `KDijkstra` pass (its inner `_MultiGoalDijkstra`).
       - `on_start` — translated from the inner OMSPP's
         `on_goal` events by the recorder shim. `goal_index`
         in the OMSPP payload becomes `start_index` in the
         MOSPP payload. `reason ∈ {expanded, unreachable}`.
         `already_closed` is never emitted (no per-sub-search
         restarts — single inner pass).
       - `update_frontier` — NOT emitted (no between-sub-
         search transition).

     **Counters** (mirrors the inner OMSPP `KDijkstra`):

       - `cnt_push`, `cnt_pop`, `cnt_decrease` — frontier-
         sourced.
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
                 name: str = 'DijkstraFlipMOSPP',
                 is_recording: bool = False,
                 is_timing: bool = True) -> None:
        """
        ====================================================================
         Init private Attributes. No `h` kwarg — Dijkstra
         hardcodes h≡0. The base `AlgoMOSPP` requires `h`, so
         a dummy `lambda s, g: 0` is passed internally (never
         invoked).
        ====================================================================
        """
        if len(problem.goals) != 1:
            raise ValueError(
                f'DijkstraFlipMOSPP requires exactly 1 goal '
                f'(got {len(problem.goals)})')
        AlgoMOSPP.__init__(
            self,
            problem=problem,
            h=lambda s, g: 0,
            name=name,
            is_recording=is_recording,
            is_timing=is_timing,
        )
        self._inner: KDijkstraOMSPP[State] | None = None

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def search_state(self) -> SearchStateSPP[State] | None:
        """
        ====================================================================
         The inner OMSPP `KDijkstra`'s `SearchStateSPP` (its
         own inner `_MultiGoalDijkstra`'s search bundle) after
         `run()` completes.
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
         delegate to OMSPP `KDijkstra`, re-key the per-goal
         solution as a per-start solution.
        ====================================================================
        """
        flipped = _FlippedView[State](base=self.problem)
        self._inner = KDijkstraOMSPP[State](
            problem=flipped,
            name=f'{self.name}[inner]',
            is_recording=False,
            is_timing=False,
        )
        # Route the inner's events through a shim that
        # rewrites `on_goal` → `on_start`. Push / pop /
        # decrease_g pass through unchanged.
        self._inner._recorder = _OnGoalToOnStartShim(
            self._recorder)
        self._inner.run()
        self._solutions = dict(self._inner.solutions)
        return SolutionMOSPP(self._solutions)

    def _sync_frontier_counters(self) -> None:
        """
        ====================================================================
         Mirror the inner OMSPP `KDijkstra`'s counters into
         the MOSPP scaffold.
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
         Walk the inner OMSPP `KDijkstra`'s parent dict from
         `start` back to the OMSPP origin (= the MOSPP goal),
         then reverse so the caller sees `[start, ..., goal]`
         in the MOSPP direction. Returns `[]` if `start` is
         unreachable from the MOSPP goal.
        ====================================================================
        """
        if self._inner is None:
            return []
        omspp_path = self._inner.reconstruct_path(start)
        return list(reversed(omspp_path))
