from f_core.abstracts.dictable import Dictable
from f_graph.path.solution import SolutionPath
from f_graph.path.node import NodePath as Node
from typing import Generic, TypeVar

Solution = TypeVar('Solution', bound=SolutionPath)


class SolutionsPath(Generic[Solution], Dictable[Node, Solution]):
    """
    ========================================================================
     Solutions of Path-Problems.
    ========================================================================
    """

    def __init__(self, sols: dict[Node, Solution]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Dictable.__init__(self, sols)
        self._elapsed: int = sum(sol.stats.elapsed for sol in sols.values())
        self._generated: int = sum(sol.stats.generated for sol in sols.values())
        self._explored: int = sum(sol.stats.explored for sol in sols.values())

    @property
    def elapsed(self) -> int:
        """
        ========================================================================
         Return the overall elapsed time of all solutions.
        ========================================================================
        """
        return self._elapsed

    @property
    def generated(self) -> int:
        """
        ========================================================================
         Return the overall number of generated nodes of all solutions.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the overall number of explored nodes of all solutions.
        ========================================================================
        """
        return self._explored

    def __bool__(self) -> bool:
        """
        ========================================================================
         Return True if all solutions are valid.
        ========================================================================
        """
        return all(self.values())
