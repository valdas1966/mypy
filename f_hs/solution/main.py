from typing import Generic, TypeVar

from f_cs.solution import SolutionAlgo
from f_hs.solution.per_key import SolutionPerKey
from f_hs.state.i_0_base.main import StateBase

State = TypeVar('State', bound=StateBase)


class SolutionSPP(SolutionAlgo):
    """
    ========================================================================
     Solution for the Shortest-Path-Problem (single start →
     single goal). Holds the optimal path cost.

     `is_valid` ⇔ `cost < inf`. Path reconstruction is on the
     Algo (`algo.reconstruct_path()`), not on the Solution.
    ========================================================================
    """

    def __init__(self, cost: float) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionAlgo.__init__(self, is_valid=cost < float('inf'))
        self._cost = cost

    @property
    def cost(self) -> float:
        """
        ========================================================================
         Return the Path Cost.
        ========================================================================
        """
        return self._cost


class SolutionOMSPP(SolutionPerKey[State, SolutionSPP], Generic[State]):
    """
    ========================================================================
     Solution for the One-to-Many Shortest-Path-Problem
     (single start → k goals).

     Wraps `dict[goal_state, SolutionSPP]`. Each entry is a
     per-goal SolutionSPP (cost may be `inf` for unreachable
     goals). Behaves as a `Mapping` — see `SolutionPerKey`.

     `is_valid` ⇔ at least one per-goal entry. The algorithm
     emits a per-goal SolutionSPP for every requested goal
     (cost=inf for unreachable). `is_all_reached` (inherited)
     is the stronger predicate (every cost finite).
    ========================================================================
    """

    def __init__(self,
                 per_goal: dict[State, SolutionSPP]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(per_key=per_goal)

    @property
    def per_goal(self) -> dict[State, SolutionSPP]:
        """
        ========================================================================
         The underlying `{goal: SolutionSPP}` mapping (the dict
         the algorithm produced, copied once at construction).
        ========================================================================
        """
        return self._per_key

    @property
    def costs(self) -> dict[State, float]:
        """
        ========================================================================
         `{goal: cost}` view — convenience for benchmark / report
         output. Costs are `float('inf')` for unreachable goals.
        ========================================================================
        """
        return {g: s.cost for g, s in self._per_key.items()}


class SolutionMOSPP(SolutionPerKey[State, SolutionSPP], Generic[State]):
    """
    ========================================================================
     Solution for the Many-to-One Shortest-Path-Problem
     (k starts → single goal).

     Wraps `dict[start_state, SolutionSPP]`. Each entry is a
     per-start SolutionSPP (cost may be `inf` if the goal is
     unreachable from that start). Behaves as a `Mapping` —
     see `SolutionPerKey`. Symmetric to `SolutionOMSPP`,
     differing only in what the key represents.

     `is_valid` ⇔ at least one per-start entry.
     `is_all_reached` (inherited) ⇔ goal reachable from every
     start.
    ========================================================================
    """

    def __init__(self,
                 per_start: dict[State, SolutionSPP]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(per_key=per_start)

    @property
    def per_start(self) -> dict[State, SolutionSPP]:
        """
        ========================================================================
         The underlying `{start: SolutionSPP}` mapping (the dict
         the algorithm produced, copied once at construction).
        ========================================================================
        """
        return self._per_key

    @property
    def costs(self) -> dict[State, float]:
        """
        ========================================================================
         `{start: cost}` view — convenience for benchmark /
         report output. Costs are `float('inf')` for starts
         from which the goal is unreachable.
        ========================================================================
        """
        return {s: sol.cost for s, sol in self._per_key.items()}
