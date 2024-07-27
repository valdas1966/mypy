from f_cs.problems.graph.path.path import ProblemPath, GraphBase, NodePath
from f_cs.problems.graph.path.mixins.has_start import HasStart
from f_cs.problems.graph.path.mixins.has_goal import HasGoal
from typing import TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodePath)


class ProblemOneToOne(ProblemPath[Graph, Node], HasStart[Node], HasGoal[Node]):
    """
    ============================================================================
     Graph-Problem with single Start and single Goal.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemPath.__init__(self, graph=graph)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)
