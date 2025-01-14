from f_graph.path.solution import SolutionPath, Node
from f_graph.path.single.solution import SolutionSingle
from f_ds.mixins.collectionable import Collectionable
from f_core.mixins.validatable import Validatable


class SolutionMulti(SolutionPath, Collectionable, Validatable):
    """
    ============================================================================
     Solution of Path-Algorithm with Multiple-Goals.
    ============================================================================
    """

    def __init__(self, solutions: dict[Node, SolutionSingle]) -> None:
        """
        ========================================================================
         Init Attributes.
        ========================================================================
        """
        SolutionPath.__init__(self)
        Collectionable.__init__(self)
        Validatable.__init__(self, is_valid=all(solutions))
        self._solutions = solutions

    @property
    def paths(self) -> dict[Node, list[Node]]:
        """
        ========================================================================
         Return the paths of the solutions.
        ========================================================================
        """
        return {goal: sol.path for goal, sol in self._solutions.items()}

    @property
    def elapsed(self) -> int:
        """
        ========================================================================
         Return the elapsed time of the search.
        ========================================================================
        """
        return sum(solution.elapsed for solution in self._solutions)

    @property
    def generated(self) -> int:
        """
        ========================================================================
         Return the number of generated nodes during the search.
        ========================================================================
        """
        return sum(len(solution.state.generated) for solution
                   in self._solutions.values())

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the number of explored nodes during the search.
        ========================================================================
        """
        return sum(len(solution.state.explored) for solution
                   in self._solutions.values())

    def to_iterable(self) -> tuple[Node, SolutionSingle]:
        """
        ========================================================================
         Return the solution as a tuple of (Node, SolutionSingle).
        ========================================================================
        """
        return tuple(self._solutions.items())

    def __getitem__(self, item: Node) -> SolutionSingle:
        """
        ========================================================================
         Return the single-solution for a given goal.
        ========================================================================
        """
        return self._solutions[item]

