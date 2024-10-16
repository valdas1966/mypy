from f_graph.nodes.i_1_path import NodePath
from typing import TypeVar, Generic

Node = TypeVar('Node', bound=NodePath)


class Cache(Generic[Node]):
    """
    ============================================================================
     Cache for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 paths_optimal: dict[Node, list[Node]] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._paths_optimal = paths_optimal if paths_optimal else dict()

    def path_optimal(self, node: Node) -> list[Node] | None:
        """
        ========================================================================
         Return an Optimal Path from a Node to Goal (None on not exists).
        ========================================================================
        """
        return self._paths_optimal.get(node, None)

    def distance_to_goal(self, node: Node) -> int | None:
        """
        ========================================================================
         Return an accurate distance from a Node to a Goal.
        ========================================================================
        """
        return len(self._paths_optimal.get(node, []))
