from f_graph.path.algo import AlgoPath
from f_graph.path.one_to_many.problem import ProblemOneToMany
from f_graph.path.one_to_many.solution import SolutionOneToMany


class AlgoOneToMany(AlgoPath[ProblemOneToMany, SolutionOneToMany]):
    """
    ============================================================================
     One-To-Many Path-Finding Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOneToMany,
                 name: str = 'Algo One-To-Many') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self, problem=problem, name=name)

    def run(self) -> SolutionOneToMany:
        """
        ========================================================================
         Run the One-To-Many Path-Finding Algorithm.
        ========================================================================
        """
        pass
