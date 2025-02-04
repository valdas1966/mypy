from f_graph.path.solution import SolutionPath, StatsPath
from f_graph.path.one_to_one.solution import SolutionOneToOne
from f_graph.path.node import Node


class SolutionOneToMany(SolutionPath):
    """
    ========================================================================
     Solution of One-To-Many Path-Problem.
    ========================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 sols: dict[Node, SolutionOneToOne]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._paths: dict[Node, list[Node]] = dict()
        self._stats: dict[Node, StatsPath] = dict()
        for goal, sol in sols.items():
            self._paths[goal] = sol.path
            self._stats[goal] = sol.stats
        SolutionPath.__init__(self, is_valid=is_valid, stats=self._stats)

    @property
    def paths(self) -> dict[Node, list[Node]]:
        """
        ========================================================================
         Return the Optimal-Paths from Start to Goals.
        ========================================================================
        """
        return self._paths
