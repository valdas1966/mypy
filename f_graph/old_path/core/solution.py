from f_graph._base.solution import SolutionGraph
from f_graph.old_path.core.stats import StatsPath
from typing import Generic, TypeVar

Stats = TypeVar('Stats', bound=StatsPath)


class SolutionPath(Generic[Stats], SolutionGraph[Stats]):
    """
    ============================================================================
     ABC for Solution of Path-Problem.
    ============================================================================
    """

    def __init__(self, is_valid: bool, stats: Stats) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionGraph.__init__(self, is_valid=is_valid, stats=stats)
    