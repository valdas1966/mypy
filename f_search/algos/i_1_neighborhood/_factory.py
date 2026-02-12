from f_search.algos.i_1_neighborhood.main import BFSNeighborhood
from f_search.problems import ProblemNeighborhood as Problem

class Factory:
    """
    ============================================================================
     Factory for the BFSNeighborhood.
    ============================================================================
    """

    @staticmethod
    def without_obstacles() -> BFSNeighborhood:
        """
        ========================================================================
         Return a BFSNeighborhood without obstacles.
        ========================================================================
        """
        problem = Problem.Factory.without_obstacles()
        return BFSNeighborhood(problem=problem)
