from f_graph.nodes.i_1_path import NodePath
from typing import TypeVar, Protocol

Node = TypeVar('Node', bound=NodePath)


class ProtocolData(Protocol[Node]):
    """
    ============================================================================
     Protocol of Data objects in the Path-Finding Algorithms.
    ============================================================================
    """

    def mark_generated(self, node: Node) -> None:
        """
        ========================================================================
         Mark a Node as Generated.
        ========================================================================
        """

    def mark_explored(self, node: Node) -> None:
        """
        ========================================================================
         Mark a Node as Explored.
        ========================================================================
        """

    def is_generated(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node is already Generated.
        ========================================================================
        """

    def is_explored(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node is already Explored.
        ========================================================================
        """
        ...

    def is_active_goal(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node is an Active-Goal.
        ========================================================================
        """

    def remove_active_goal(self, goal: Node) -> None:
        """
        ========================================================================
         Remove a Goal from the Active-Goals set.
        ========================================================================
        """

    def has_generated(self) -> bool:
        """
        ========================================================================
         Return True if there has more Nodes in the Generated list.
        ========================================================================
        """

    def has_active_goals(self) -> bool:
        """
        ========================================================================
         Return True if there has more Goals in the Active-Goals set.
        ========================================================================
        """