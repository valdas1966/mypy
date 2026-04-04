from f_search.problems import ProblemSearch
from f_search.problems.i_2_omspp.main import ProblemOMSPP
from f_search.problems.i_1_spp.main import ProblemSPP
from f_search.problems.mixins import HasStarts, HasGoals
from f_search.ds.state import StateCell as State
from f_ds.grids import GridMap as Grid


class ProblemMMSPP(ProblemSearch, HasStarts, HasGoals):
    """
    ============================================================================
     Many-to-Many Shortest-Path-Problem on a Grid.
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __init__(self,
                 grid: Grid,
                 starts: list[State],
                 goals: list[State],
                 name: str = 'ProblemMMSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemSearch.__init__(self, grid=grid, name=name)
        HasStarts.__init__(self, starts=starts)
        HasGoals.__init__(self, goals=goals)

    @property
    def h_starts(self) -> float:
        """
        ========================================================================
         Return avg pairwise Manhattan distance between Starts.
        ========================================================================
        """
        starts = self.starts
        n = len(starts)
        if n < 2:
            return 0.0
        total = sum(starts[i].distance(starts[j])
                    for i in range(n) for j in range(i + 1, n))
        return total / (n * (n - 1) / 2)

    @property
    def norm_h_starts(self) -> float:
        """
        ========================================================================
         Return normalized h_starts [0,1] relative to max Manhattan dist.
        ========================================================================
        """
        return self.grid.norm_distance(distance=self.h_starts)

    @property
    def h_goals(self) -> float:
        """
        ========================================================================
         Return avg pairwise Manhattan distance between Goals.
        ========================================================================
        """
        goals = self.goals
        n = len(goals)
        if n < 2:
            return 0.0
        total = sum(goals[i].distance(goals[j])
                    for i in range(n) for j in range(i + 1, n))
        return total / (n * (n - 1) / 2)

    @property
    def norm_h_goals(self) -> float:
        """
        ========================================================================
         Return normalized h_goals [0,1] relative to max Manhattan dist.
        ========================================================================
        """
        return self.grid.norm_distance(distance=self.h_goals)

    @property
    def h_cross(self) -> float:
        """
        ========================================================================
         Return avg Manhattan distance from each Start to each Goal.
        ========================================================================
        """
        starts = self.starts
        goals = self.goals
        total = sum(s.distance(g) for s in starts for g in goals)
        return total / (len(starts) * len(goals))

    @property
    def norm_h_cross(self) -> float:
        """
        ========================================================================
         Return normalized h_cross [0,1] relative to max Manhattan dist.
        ========================================================================
        """
        return self.grid.norm_distance(distance=self.h_cross)

    def to_analytics(self) -> dict:
        """
        ========================================================================
         Return a dict of analytic values for reporting.
        ========================================================================
        """
        d = ProblemSearch.to_analytics(self)
        d['h_starts'] = self.h_starts
        d['norm_h_starts'] = self.norm_h_starts
        d['h_goals'] = self.h_goals
        d['norm_h_goals'] = self.norm_h_goals
        d['h_cross'] = self.h_cross
        d['norm_h_cross'] = self.norm_h_cross
        return d

    def to_omspps(self) -> list[ProblemOMSPP]:
        """
        ========================================================================
         Convert to a list of OMSPP sub-problems (one per Start).
        ========================================================================
        """
        return [ProblemOMSPP(grid=self.grid,
                             start=start,
                             goals=self.goals)
                for start in self.starts]

    def to_mospps(self) -> list[ProblemOMSPP]:
        """
        ========================================================================
         Convert to a list of reverse OMSPP sub-problems (one per Goal).
         Each OMSPP searches from a Goal to all Starts (undirected grid).
        ========================================================================
        """
        return [ProblemOMSPP(grid=self.grid,
                             start=goal,
                             goals=self.starts)
                for goal in self.goals]

    def to_spps(self) -> list[ProblemSPP]:
        """
        ========================================================================
         Convert to a list of SPP sub-problems (one per Start-Goal pair).
        ========================================================================
        """
        return [ProblemSPP(grid=self.grid,
                           start=start,
                           goal=goal)
                for start in self.starts
                for goal in self.goals]
