
from path_finding.base import ProblemPathFinding, GraphBase as Graph, NodePatas Node
from path_finding.mixins.has_start import HasStart
from path_finding.mixins.has_goal import HasGoal

class OneToOne(ProblemPathFinding, HasStart, HasGoal):
    """
    ============================================================================
     One-to-One Path-Finding Problem (one Start and one Goal).
    ============================================================================
    """

    def __init__(self,
                 graph: Graph[Node],
                 start: Node,
                 goal: Node) -> None:
        ProblemPathFinding.__init__(self, graph=graph)
        HasStart.__init__(self, start=start)
        HasGoal.__init__(self, goal=goal)
