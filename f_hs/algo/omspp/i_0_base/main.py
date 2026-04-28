from f_core.recorder.main import Recorder
from f_cs.algo import Algo
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionOMSPP, SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AlgoOMSPP(Generic[State],
                Algo[ProblemSPP[State], SolutionOMSPP]):
    """
    ============================================================================
     Abstract base for One-to-Many Shortest Path Problem
     algorithms (KAStarInc, KAStarAgg, future KDijkstra).

     Inherits the standard f_cs Algo lifecycle:

         run()  →  _run_pre  →  _run  →  _run_post

     `elapsed` (wall-clock) and `recorder` are auto-managed by
     ProcessBase / Algo. Subclasses override `_run()` to execute
     the algorithm body and return a `SolutionOMSPP`.

     Provides a unified 8-counter scaffold so cross-algorithm
     benchmarks (KAStarAgg vs KAStarInc) can produce a uniform
     metric table. Counters are reset to 0 in `_run_pre()`
     before every `run()`. Each subclass increments whichever
     subset it supports (others stay at 0; document with
     reason in the subclass CLAUDE.md).

     The 8 counters:
       cnt_h_search    — h(state, goal) calls in normal flow.
       cnt_h_update    — h(state, goal) calls in refresh flow
                         (post-goal F refresh / inter-sub-search
                         priority refresh).
       cnt_phi_search  — `_compute_F` calls in normal flow
                         (Φ-aggregation algorithms only).
       cnt_phi_update  — `_compute_F` calls in refresh flow
                         (Φ-aggregation algorithms only).
       cnt_push        — frontier.push calls.
       cnt_pop         — frontier.pop calls.
       cnt_pop_stale   — subset of cnt_pop: stale-F re-insertions
                         (lazy-mode algorithms only).
       cnt_decrease    — frontier.decrease calls.
    ============================================================================
    """

    # Factory
    Factory: type = None

    _COUNTER_NAMES: tuple[str, ...] = (
        'cnt_h_search', 'cnt_h_update',
        'cnt_phi_search', 'cnt_phi_update',
        'cnt_push', 'cnt_pop', 'cnt_pop_stale', 'cnt_decrease',
    )

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: Callable[[State, State], int],
                 name: str = 'AlgoOMSPP',
                 is_recording: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algo.__init__(self, problem=problem, name=name,
                      is_recording=is_recording)
        self._h: Callable[[State, State], int] = h
        self._solutions: dict[State, SolutionSPP] = {}
        self._reset_counters()

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def solutions(self) -> dict[State, SolutionSPP]:
        """
        ====================================================================
         Per-goal `{goal: SolutionSPP}` populated by `_run()`.
         Same dict that the returned `SolutionOMSPP` wraps.
        ====================================================================
        """
        return self._solutions

    @property
    def counters(self) -> dict[str, int]:
        """
        ====================================================================
         Per-run operation counters. Reset to 0 in `_run_pre()`,
         so `algo.counters` after `run()` reflects the most
         recent run only.
        ====================================================================
        """
        return {n: getattr(self, f'_{n}')
                for n in self._COUNTER_NAMES}

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run_pre(self) -> None:
        """
        ====================================================================
         Reset wall-clock + per-run mutable state (counters,
         solutions dict). Called automatically by Algo.run()
         before _run().
        ====================================================================
        """
        super()._run_pre()
        self._reset_counters()
        self._solutions = {}

    def _run(self) -> SolutionOMSPP:
        """
        ====================================================================
         Subclass override point. Execute the algorithm and
         return a `SolutionOMSPP` wrapping `self._solutions`.
        ====================================================================
        """
        raise NotImplementedError

    # ──────────────────────────────────────────────────
    #  Internal
    # ──────────────────────────────────────────────────

    def _reset_counters(self) -> None:
        """
        ====================================================================
         Zero all 8 counters. Called from _run_pre() and from
         subclass __init__.
        ====================================================================
        """
        for n in self._COUNTER_NAMES:
            setattr(self, f'_{n}', 0)
