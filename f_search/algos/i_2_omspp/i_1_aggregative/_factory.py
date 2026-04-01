from f_search.algos.i_2_omspp.i_1_aggregative.main import AStarAggregative
from f_search.problems.i_2_omspp.main import ProblemOMSPP
from f_search.heuristics.phi import UPhi, PhiFunc


class Factory:
    """
    ============================================================================
     Factory for A* Aggregative Algorithm.
    ============================================================================
    """

    @staticmethod
    def without_obstacles(phi: PhiFunc = UPhi.min) -> AStarAggregative:
        """
        ========================================================================
         Create an A* Aggregative Algorithm for the given Problem.
        ========================================================================
        """
        problem = ProblemOMSPP.Factory.without_obstacles()
        return AStarAggregative(problem=problem, phi=phi)

    @staticmethod
    def with_obstacles() -> AStarAggregative:
        problem = ProblemOMSPP.Factory.with_obstacles()
        return AStarAggregative(problem=problem, phi=UPhi.min)

    @staticmethod
    def for_node_categories() -> AStarAggregative:
        problem = ProblemOMSPP.Factory.for_node_categories()
        return AStarAggregative(problem=problem, phi=UPhi.min)
