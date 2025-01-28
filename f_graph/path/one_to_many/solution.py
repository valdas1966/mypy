from f_graph.path.solution import SolutionPath, StatsPath
from f_graph.path.node import Node


class SolutionOneToMany(SolutionPath):
    """
    ========================================================================
     Solution of One-To-Many Path-Problem.
    ========================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 stats: StatsPath,
                 paths: list[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionPath.__init__(self, is_valid=is_valid, stats=stats)
        self._paths = paths

    @property
    def paths(self) -> list[Node]:
        """
        ========================================================================
         Return the Optimal-Paths from Start to Goals.
        ========================================================================
        """
        return self._paths
