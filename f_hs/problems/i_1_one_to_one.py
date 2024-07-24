from f_hs.problems.i_0_graph import ProblemGraph, GraphBase
from f_hs.problems.mixins.has_start import HasStart, NodePath
from f_hs.problems.mixins.has_goal import HasGoal
from typing import Generic, TypeVar

G = TypeVar('G', bound=GraphBase)
N = TypeVar('N', bound=NodePath)


class ProblemOneToOne(ProblemGraph[G, N], HasStart[N], HasGoal[N]):
    """
    ============================================================================
     One-to-One Shortest Path Problem.
    ============================================================================
    """

    def __init__(self,
                 graph: G,
                 start: N,
                 goal: N) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemGraph.__init__(self, graph=graph)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)
