from f_graph.path.ds.graphs.graph import GraphPath as Graph, NodePath as Node
from enum import Enum, auto


class TypeHeuristic(Enum):
        """
        ============================================================================
         Enum of Heuristic-Types.
        ============================================================================
        """
        MANHATTAN = auto()
        ZERO = auto()

class Heuristic:
    """
    ============================================================================
     Func of Heuristic-Distance from a given Node to a Goal.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 goal: Node,
                 type_heuristic: TypeHeuristic = TypeHeuristic.ZERO) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._graph = graph
        self._goal = goal
        self._type_heuristic = type_heuristic

    def __call__(self, node: Node) -> int:
        """
        ========================================================================
         Return the Heuristic-Distance from a given Node to a Goal.
        ========================================================================
        """
        match self._type_heuristic:
            case TypeHeuristic.MANHATTAN:
                return self._graph.distance(node_a=node, node_b=self._goal)
            case TypeHeuristic.ZERO:
                return 0