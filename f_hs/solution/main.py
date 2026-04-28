from collections.abc import Mapping
from typing import Generic, TypeVar

from f_cs.solution import SolutionAlgo
from f_hs.state.i_0_base.main import StateBase

State = TypeVar('State', bound=StateBase)


class SolutionSPP(SolutionAlgo):
    """
    ========================================================================
     Solution for Shortest-Path-Problem.
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


class SolutionOMSPP(SolutionAlgo, Mapping, Generic[State]):
    """
    ========================================================================
     Solution for the One-to-Many Shortest-Path-Problem.

     Wraps a per-goal mapping `{goal_state: SolutionSPP}`. Each
     entry is a per-goal SolutionSPP (cost may be `inf` for
     unreachable goals).

     Behaves as a `collections.abc.Mapping` over the per-goal
     dict — `.items()`, `.values()`, `.keys()`, `__getitem__`,
     `__iter__`, `__len__`, `__contains__`, `.get()` work
     transparently. `bool(sol)` returns `is_valid` (Validatable
     wins over Mapping in MRO).

     `is_valid` ⇔ at least one per-goal entry. The algorithm is
     responsible for emitting a per-goal SolutionSPP for every
     requested goal (cost=inf for unreachable). `is_all_reached`
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
        SolutionAlgo.__init__(self, is_valid=bool(per_goal))
        self._per_goal: dict[State, SolutionSPP] = dict(per_goal)

    # ── Mapping protocol ────────────────────────────────

    def __getitem__(self, key: State) -> SolutionSPP:
        return self._per_goal[key]

    def __iter__(self):
        return iter(self._per_goal)

    def __len__(self) -> int:
        return len(self._per_goal)

    # ── OMSPP-specific accessors ────────────────────────

    @property
    def per_goal(self) -> dict[State, SolutionSPP]:
        """
        ========================================================================
         The underlying `{goal: SolutionSPP}` mapping (a copy of
         the dict the algorithm produced).
        ========================================================================
        """
        return self._per_goal

    @property
    def costs(self) -> dict[State, float]:
        """
        ========================================================================
         `{goal: cost}` view — convenience for benchmark / report
         output. Costs are `float('inf')` for unreachable goals.
        ========================================================================
        """
        return {g: s.cost for g, s in self._per_goal.items()}

    @property
    def is_all_reached(self) -> bool:
        """
        ========================================================================
         True iff every goal has a finite cost (none unreachable).
        ========================================================================
        """
        return all(s.cost != float('inf')
                   for s in self._per_goal.values())
