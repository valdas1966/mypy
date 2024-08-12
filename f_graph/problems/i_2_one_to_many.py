from f_graph.problems.i_1_path import ProblemPath, GraphBase, NodePath
from f_graph.problems.mixins.has_start import HasStart
from f_graph.problems.mixins.has_goals import HasGoals
from typing import TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodePath)


class ProblemOneToMany(ProblemPath[Graph, Node],
                       HasStart[Node],
                       HasGoals[Node]):
    """
    ============================================================================
     Graph-Problem with single Start and multiple Goals.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goals: set[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemPath.__init__(self, graph=graph)
        HasStart.__init__(self, start=start)
        HasGoals.__init__(self, goals=goals)
