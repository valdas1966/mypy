from f_graph.solution import SolutionGraph
from f_graph.path.elements.node import NodePath as Node


class SolutionPath(SolutionGraph[Node]):
    """
    ============================================================================
     ABC for Solution of Path-Problem.
    ============================================================================
    """

    def __init__(self) -> None:
        SolutionGraph.__init__(self)
        self.