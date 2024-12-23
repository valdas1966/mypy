from f_graph.path.algo import AlgoPath
from f_graph.path.multi.problem import ProblemMulti
from f_graph.path.multi.solution import SolutionMulti


class AlgoMulti(AlgoPath[ProblemMulti, SolutionMulti]):
    """
    ============================================================================
     Algorithm for Multiple-Goal Path-Problems.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemMulti,
                 name: str = 'Algo Multi') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self, problem=problem, name=name)
