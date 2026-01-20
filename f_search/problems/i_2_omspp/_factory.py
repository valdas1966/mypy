from f_search.problems.i_2_omspp.main import ProblemOMSPP, Grid, State
from typing import Iterable


class Factory:
    """
    ============================================================================
     Factory for the ProblemOMSPP.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> ProblemOMSPP:
        """
        ========================================================================
         Return a ProblemOMSPP with a GridMap without obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        start = Factory._get_start_4x4()
        goals = Factory._get_goals_4x4()
        return ProblemOMSPP(grid=grid, start=start, goals=goals)

    @staticmethod
    def with_obstacles() -> ProblemOMSPP:
        """
        ========================================================================
         Return a ProblemOMSPP with a GridMap with obstacles.
        ========================================================================
        """
        grid = Grid.Factory.four_with_obstacles()
        start = Factory._get_start_4x4()
        goals = Factory._get_goals_4x4()
        return ProblemOMSPP(grid=grid, start=start, goals=goals)

    @staticmethod
    def all_goals(rows: int) -> ProblemOMSPP:
        """
        ========================================================================
         Return a ProblemOMSPP when all the cells are Goals.
        ========================================================================
        """
        grid = Grid(rows=rows)
        start = State(key=grid[0][0])
        goals = [State(key=cell) for cell in grid]
        return ProblemOMSPP(grid=grid, start=start, goals=goals)

    @staticmethod
    def custom(rows: int,
               pct_obstacles: int,
               k: int) -> ProblemOMSPP:
        """
        ========================================================================
         Return a ProblemOMSPP with a GridMap with obstacles.
        ========================================================================
        """
        grid = Grid.Factory.custom(rows, pct_obstacles)
        cells = grid.random.cells(size=k+1)
        start = State(key=cells[0])
        goals = [State(key=cell) for cell in cells[1:]]
        return ProblemOMSPP(grid=grid, start=start, goals=goals)
        
    @staticmethod
    def _get_start_4x4() -> State:
        """
        ========================================================================
         Return the Start StateBase for a 4x4 Grid.
        ========================================================================
        """
        grid = Grid(rows=4)
        cell_start = grid[0][0]
        return State(key=cell_start)

    @staticmethod
    def _get_goals_4x4() -> Iterable[State]:
        """
        ========================================================================
         Return the Goals for a 4x4 Grid.
        ========================================================================
        """
        grid = Grid(rows=4)
        cell_goal_a = grid[0][3]
        cell_goal_b = grid[3][3]
        goal_a = State(key=cell_goal_a)
        goal_b = State(key=cell_goal_b)
        return [goal_a, goal_b]
