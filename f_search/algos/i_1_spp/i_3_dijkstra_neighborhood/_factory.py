from f_search.algos.i_1_spp.i_3_dijkstra_neighborhood.main import DijkstraNeighborhood
from f_search.ds.states import StateCell as State
from f_search.problems import ProblemSPP
from f_ds.grids import GridMap as Grid


class Factory:
    """
    ============================================================================
     Factory for DijkstraNeighborhood.
    ============================================================================
    """
    
    @staticmethod
    def grid_4x4_with_obstacles() -> DijkstraNeighborhood:
        """
        ========================================================================
         Return a DijkstraNeighborhood for a 4x4 grid with obstacles and k=2.
        ========================================================================
        """
        grid = Grid.Factory.four_with_obstacles()
        state = State(grid[0][0])
        problem = ProblemSPP.Factory.fictive_goal(grid=grid, start=state)
        dijkstra = DijkstraNeighborhood(problem=problem, steps=2)
        return dijkstra

    @staticmethod
    def grid_4x4_without_obstacles() -> DijkstraNeighborhood:
        """
        ========================================================================
         Return a DijkstraNeighborhood for a 4x4 grid with obstacles and k=2.
        ========================================================================
        """
        grid = Grid.Factory.four_without_obstacles()
        state = State(grid[0][0])
        problem = ProblemSPP.Factory.fictive_goal(grid=grid, start=state)
        dijkstra = DijkstraNeighborhood(problem=problem, steps=2)
        return dijkstra
